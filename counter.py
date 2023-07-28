from model import *
from get_doc import *
import threading

class Counter:
    def __init__(self, file):
        self.file = file
        self.db = Model(self.file)

    def count(self, table, colonne):
        """sert à compter des éléménts genre visiteurs, nombre de click, etc..."""
        self.lock = threading.Lock()
        with self.lock:
            try:
                elements = self.db.get_elements_from_colonne(table, colonne)
                nb = int(elements[-1])
                nb2 = str(nb+1)
            except:
                nb2 = "1"
            self.db.add_item_begin_colonne(table,colonne,nb2)
                
    def read(self, table, colonne):
        """sert à lire les comptes"""
        with self.lock:
            elements = self.db.get_elements_from_colonne(table, colonne)
            if len(elements) == 0:
                return 0
            return elements[-1]

    def get_db(self):
        """get db tool for use later"""
        return self.db

if __name__ == "__main__":
    counter = Counter("db/database.db")
    counter.count("data", "count_visitor")
    print(counter.read("data", "count_visitor"))
