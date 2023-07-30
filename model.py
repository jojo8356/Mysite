from pysqlcipher3 import dbapi2 as sqlite
from utils import *
from tabulate import tabulate
import os
from get_doc import *
from tools import *

class Model:
    def __init__(self, file):
        self.file, self.password = file, password
        self.verif_file()
        self.conn = sqlite.connect(self.file, check_same_thread=False) # type: ignore
        self.conn.execute(f"PRAGMA key='{self.password}'")
        self.cursor = self.conn.cursor()

    def init_var(self):
        """initialise les variables"""
        try:
            os.remove(self.file)
        except:
            pass
        self.conn = sqlite.connect(self.file, check_same_thread=False) # type: ignore
        self.conn.execute(f"PRAGMA key='{self.password}'")
        self.cursor = self.conn.cursor()

    def verif_file(self):
        if not os.path.isfile(self.file):
            self.conn = sqlite.connect(self.file, check_same_thread=False) # type: ignore

    def exec_sql(self, sql):
        """éxécute le sql"""
        self.conn.execute(f"PRAGMA key='{self.password}'")
        if sql.strip().startswith(("SELECT", "PRAGMA", "EXPLAIN")):
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        else:
            self.conn.execute(sql)
            self.conn.commit()

    def get_password(self):
        """récupère le mdp"""
        return self.password

    def get_conn(self):
        """récupère la connexion (conn)"""
        return self.conn

    def get_cursor(self):
        """get le cursor"""
        return self.cursor

    def get_file(self):
        """get le nom du file"""
        return self.file

    def verif_table(self, table):
        """vérifie si la table exist"""
        tables = self.get_tables_names()
        return table in tables

    def verif_colonne(self, table, colonne):
        """vérifie si la colonne exist"""
        colonnes = self.get_colonnes_name_from_table(table)
        return colonne in colonnes

    def verif_item(self, table, colonne, item):
        """vérifie si l'item existe"""
        items = self.get_elements_from_colonne(table,colonne)
        return item in items

    def create_colonne(self, table, colonne):
        """create a column in a table"""
        if self.verif_colonne(table,colonne):
            return
        if self.verif_table(table):
            self.exec_sql(f"ALTER TABLE {table} ADD COLUMN {colonne}")
            print(f"Colonne {colonne} ajoutée à la table {table} existante.")
        else:
            self.exec_sql(f"CREATE TABLE {table} ({colonne})")
            print(f"Table {table} et colonne {colonne} créées.")

    def add(self, table, colonne, item):
        """ajoute un élément dans la base de données"""
        self.create_colonne(table,colonne)
        self.exec_sql(f"INSERT INTO {table} ({colonne}) VALUES ('{item}');")
        print(f"L'item {item} a été ajouté dans la colonne {colonne} qui est dans la table {table}")

    def display_table(self, table_name):
        """affiche une table sous un table(eau) LOL"""
        columns = self.exec_sql(f"PRAGMA table_info({table_name})")
        rows = self.exec_sql(f"SELECT * FROM {table_name}")
        headers = [column[1] for column in columns]
        table = tabulate(rows, headers=headers, tablefmt="fancy_grid")
        print(f"Table: {table_name}")
        print(table)
        print()

    def get_tables_names(self):
        """get names of tables in db"""
        tables = self.exec_sql("SELECT name FROM sqlite_master WHERE type='table';")
        return [table[0] for table in tables]

    def print_db(self):
        """print all db"""
        print()
        liste = self.get_tables_names()
        for x in liste:
            self.display_table(x)

    def get_elements_from_colonne(self, table, colonne):
        """get elements from colonnes"""
        self.create_colonne(table,colonne)
        elements = self.exec_sql(f"SELECT {colonne} FROM {table}")
        elements = [x[0] for x in elements]
        return elements
    
    def get_colonnes_name_from_table(self, table):
        """get colonnes names from table"""
        colonnes = self.exec_sql(f"PRAGMA table_info({table});")
        colonnes = [x[1] for x in colonnes]
        return colonnes

    def update_element(self, table, colonne, old_element, nw_element):
        """MAJ d'un element"""
        if not self.verif_item(table, colonne, old_element):
            raise ValueError("Le premier élément (celui de départ) n'existe pas")
        dictio = self.get_db_in_dictio()
        index = dictio[table][colonne].index(old_element)
        dictio[table][colonne][index] = nw_element
        self.re_push_dictio_elements_in_db(dictio)

    def del_table(self, table):
        """del table"""
        dictio = self.get_db_in_dictio()
        del dictio[table]
        self.re_push_dictio_elements_in_db(dictio)

    def del_colonne(self, table, colonne):
        """del une colonne dans une table"""
        dictio = self.get_db_in_dictio()
        del dictio[table][colonne]       
        self.re_push_dictio_elements_in_db(dictio)

    def del_item(self, table, colonne, item):
        """del item"""
        dictio = self.get_db_in_dictio()
        index = dictio[table][colonne].index(item)
        if dictio[table][colonne][index] != "":
            dictio[table][colonne][index] = ""
            self.re_push_dictio_elements_in_db(dictio)
        else:
            print("l'élément "+item+" à déja été supprimer ou n'est pas remplis")

    def get_db_in_dictio(self):
        """get db in dictionnary"""
        dictio = {}
        tables = self.get_tables_names()
        for x in tables:
                dictio[x] = self.get_colonnes_name_from_table(x)
        for table_name, column_names in dictio.items():
                for x in range(len(column_names)):
                    elements = self.get_elements_from_colonne(table_name, column_names[x])
                    dictio[table_name][x] = {column_names[x]: elements}
        dictio = format_dictio(dictio)
        return dictio

    def add_multiple_element(self, table, colonne_et_element):
        """add multiple element in db"""
        colonnes = colonne_et_element[0]
        elements = colonne_et_element[1:]
        colonnes_sql = format_data_for_sql(colonnes)
        for x in colonnes:
            self.create_colonne(table, x)
        for x in elements:
            liste = format_data_for_sql(x)
            self.exec_sql(f"INSERT INTO {table} {colonnes_sql} VALUES {liste}")        

    def re_push_dictio_elements_in_db(self, dictio):
        """re push the dictionnary (db) in db"""
        if not self.check_data_existance_in_db():
            self.init_var()
        else:
            self.init_var()
            for table, data in dictio.items():
                keys = list(data.keys())
                values = list(data.values())

                result = [keys] + list(zip(*values))
                result = eval(str(result).replace("(","[").replace(",)","]").replace(")","]"))
                for x in range(len(result)):
                    my_list = result[x]
                    for i in range(len(my_list)):
                        if my_list[i] is None:
                            my_list[i] = ""
                self.add_multiple_element(table,result)

    def check_data_existance_in_db(self):
        dictio = self.get_db_in_dictio()
        return len(list(dictio.keys())) != 0

    def add_item_begin_colonne(self,table,colonne,item):
        self.create_colonne(table,colonne)
        try: 
            items = self.get_elements_from_colonne(table,colonne)
            if len(items) == 0:
                return self.add(table,colonne,item)
            self.update_element(table,colonne,items[0],item)
        except:
            return self.add(table,colonne,item)
