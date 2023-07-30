from model import *

table = "data"
colonne = "test"
elmt1 = "1"
elmt2 = "2"
file = "test.db"
db = Model(file)
db.print_db()
db.add(table,colonne,"1")
db.add("alpha","A","B")
db.print_db()
db.add_item_begin_colonne("alpha","A","test")
print("_________________________________________")
db.print_db()
