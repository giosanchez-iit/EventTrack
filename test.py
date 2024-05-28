from db_crudl import DatabaseCRUDL

crudl = DatabaseCRUDL()

items = crudl.executeQueryWithReturn("select comm_name from committee order by comm_name")
items = list({item[0] for item in items})
items = crudl.executeQueryWithReturn("select comm_name from committee order by comm_name")
sel = crudl.executeQueryWithReturn("select comm_name from committee order by comm_name limit 1 offset 4")
print(items[4], sel)
print(items)
