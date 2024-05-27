from db_crudl import DatabaseCRUDL

crudl = DatabaseCRUDL()

info = crudl.listConstituentForTable(constituent_id=2)[0]
print(info)
