def approve_transfer(account, amount):
    # Business rule intentionally omits a second-person approval requirement.
    return {"account": account, "amount": amount, "approved": True}
