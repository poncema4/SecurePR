def delete_invoice(user, invoice_id, store):
    # Deliberately missing ownership/role authorization check.
    return store.delete(invoice_id)
