import datetime

raw_data = [
    {
        "name": "Hayes Inc",
        "billingAddress": {
            "line1": "789 Maple Street",
            "city": "San Francisco",
            "zip": "94103",
            "country": "US"
        },
        "currency": "USD",
        "contracts": [
            {
                "startDate": "2023-09-22",
                "endDate": "2024-09-22",
                "products": [
                    {
                        "name": "Implementation Fee",
                        "quantity": 1,
                        "price": 5000.00
                    },
                    {
                        "name": "Monthly Subscription",
                        "quantity": 12,
                        "price": 500.00
                    }
                ]
            }
        ],
    },
    {
        "name": "Smith & Co Ltd",
        "billingAddress": {
            "line1": "456 Oak Avenue",
            "city": "London",
            "zip": "EC1A 1BB",
            "country": "UK"
        },
        "currency": "GBP",
        "contracts": [
            {
                "startDate": "2023-06-01",
                "endDate": "2024-06-01",
                "products": [
                    {
                        "name": "Consultation Fee",
                        "quantity": 1,
                        "price": 4000.00
                    },
                    {
                        "name": "Annual Service Subscription",
                        "quantity": 12,
                        "price": 300.00
                    }
                ]
            }
        ]
    },
    {
        "name": "Dupont SA",
        "billingAddress": {
            "line1": "123 Rue de Rivoli",
            "city": "Paris",
            "zip": "75001",
            "country": "FR"
        },
        "currency": "EUR",
        "contracts": [
            {
                "startDate": "2023-11-15",
                "endDate": "2024-11-15",
                "products": [
                    {
                        "name": "Setup Fee",
                        "quantity": 1,
                        "price": 4500.00
                    },
                    {
                        "name": "Monthly Support Subscription",
                        "quantity": 12,
                        "price": 400.00
                    }
                ]
            }
        ]
    }

]


class customersProcessor:

    def run(self, customers = []):
        c = 1
        all_customers = []
        eucountries = ["AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI",
                       "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU",
                       "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE"]
        for i in customers:
            activeContracts = [x for x in i["contracts"] if datetime.datetime.strptime(x["startDate"], "%Y-%m-%d") <= datetime.datetime.now() and datetime.datetime.strptime(x["endDate"], "%Y-%m-%d") >= datetime.datetime.now()]
            if len(activeContracts) > 0:
                has_active_contract = True
            else:
                has_active_contract = False
            all_contracts = []
            if i["currency"] == "USD":
                exchangerate = "0.77"
            elif i["currency"] == "EUR":
                exchangerate = "0.84"
            else:
                exchangerate = 1
            for y in i["contracts"]:
                total_contract_value = 0
                for z in y["products"]:
                    total_contract_value = total_contract_value + z["quantity"] * z["price"]

                contract = {
                    "startDate": y["startDate"],
                    "endDate": y["endDate"],
                    "contract_length_days": (datetime.datetime.strptime(y["endDate"], "%Y-%m-%d") - datetime.datetime.strptime(y["startDate"], "%Y-%m-%d")).days,
                    "total_contract_value_local": total_contract_value,
                    "total_contract_value_gbp": total_contract_value * float(exchangerate)
                }
                all_contracts.append(contract)
            customer = {
                "id": c,
                "name": i["name"],
                "billing_address": {
                    "line1": i["billingAddress"]["line1"],
                    "city": i["billingAddress"]["city"],
                    "zip": i["billingAddress"]["zip"],
                    "country": i["billingAddress"]["country"]
                },
                "currency": i["currency"],
                "is_eu_country": i["billingAddress"]["country"] in eucountries,
                "has_active_contract": has_active_contract,
                "contracts": all_contracts
            }
            all_customers.append(customer)
            c = c + 1
        return all_customers


processor = customersProcessor()
output = processor.run(raw_data)

expected_output = [
    {
        "id": 1,
        "name": "Hayes Inc",
        "billing_address": {
            "line1": "789 Maple Street",
            "city": "San Francisco",
            "zip": "94103",
            "country": "US"
        },
        "currency": "USD",
        "is_eu_country": False,
        "has_active_contract": True,
        "contracts": [
            {
                "startDate": "2023-09-22",
                "endDate": "2024-09-22",
                "contract_length_days": 366,
                "total_contract_value_local": 11000.0,
                "total_contract_value_gbp": 8470.0
            }
        ]
    },
    {
        "id": 2,
        "name": "Smith & Co Ltd",
        "billing_address": {
            "line1": "456 Oak Avenue",
            "city": "London",
            "zip": "EC1A 1BB",
            "country": "UK"
        },
        "currency": "GBP",
        "is_eu_country": False,
        "has_active_contract": False,
        "contracts": [
            {
                "startDate": "2023-06-01",
                "endDate": "2024-06-01",
                "contract_length_days": 366,
                "total_contract_value_local": 7600.0,
                "total_contract_value_gbp": 7600.0
            }
        ]
    },
    {
        "id": 3,
        "name": "Dupont SA",
        "billing_address": {
            "line1": "123 Rue de Rivoli",
            "city": "Paris",
            "zip": "75001",
            "country": "FR"
        },
        "currency": "EUR",
        "is_eu_country": True,
        "has_active_contract": True,
        "contracts": [
            {
                "startDate": "2023-11-15",
                "endDate": "2024-11-15",
                "contract_length_days": 366,
                "total_contract_value_local": 9300.0,
                "total_contract_value_gbp": 7812.0
            }
        ]
    }
]