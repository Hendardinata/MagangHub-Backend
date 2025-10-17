import re
from bson import ObjectId

def serialize_customer(customer):
    return {
        "_id": str(customer["_id"]),
        "name": customer.get("name"),
        "email": customer.get("email"),
        "account_number": customer.get("account_number"),
        "balance": float(customer.get("balance", 0.0)),
    }

# validasi input
def validate_customer_data(data, is_update=False):
    errors = {}

    # Create
    required_fields = ["name", "email", "account_number"]

    if not is_update:
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                errors[field] = f"{field} is required."

    # Validasi name
    if "name" in data:
        if not isinstance(data["name"], str):
            errors["name"] = "Name must be a string."
        elif len(data["name"].strip()) < 3:
            errors["name"] = "Name must be at least 3 characters."

    # Validasi email
    if "email" in data:
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, data["email"]):
            errors["email"] = "Invalid email format."

    # Validasi nomor rekening
    if "account_number" in data:
        acc = str(data["account_number"])
        if not acc.isdigit():
            errors["account_number"] = "Account number must be numeric."
        elif len(acc) < 6:
            errors["account_number"] = "Account number must be at least 6 digits."

    # Validasi saldo
    if "balance" in data:
        try:
            data["balance"] = float(data["balance"])
            if data["balance"] < 0:
                errors["balance"] = "Balance cannot be negative."
        except ValueError:
            errors["balance"] = "Balance must be a number."

    # Return hasil validasi
    if errors:
        return False, errors

    if "name" in data: data["name"] = data["name"].strip()
    if "email" in data: data["email"] = data["email"].strip()

    return True, data
