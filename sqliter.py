import sqlite3
import re
from random import randint,choice
class SQLighter:


    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        with self.connection:
            # Создаём нужные таблицы на случай их отсутствия
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'users' ('id' varchar, 'balance' varchar, 'refbalance' varchar, 'refered' varchar)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'sale' ('promo' varchar, 'sale' varchar, 'amount' varchar)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'pay' ('id' varchar, 'id_pay' varchar)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'buttons' ('id' varchar, 'if_need' varchar, 'text' varchar)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'pay' ('id' varchar, 'cid' varchar)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'cat' ('id' varchar, 'name' varchar)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'podcat' ('id' varchar, 'name' varchar,'parent' varchar)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'products' ('id' varchar, 'name' varchar,'parent' varchar,'price' varchar,'description' varchar,'amount' varchar)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'log_chat' ('id' varchar)")
            self.cursor.execute("SELECT * FROM log_chat")
            if self.cursor.fetchone() == None:
                self.cursor.execute("INSERT INTO log_chat (id) VALUES ('0')")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'bot' ('date_down' varchar, 'date_live' varchar, 'money_make' varchar, 'sold' varchar, 'refproc' varchar)")
            self.cursor.execute("SELECT * FROM bot")
            if self.cursor.fetchone() == None:
                self.cursor.execute("INSERT INTO bot ('date_down','date_live','money_make','sold','refproc') VALUES ('1','0','0','0','0')")

            self.cursor.execute("SELECT * FROM buttons WHERE id = '1'")
            if self.cursor.fetchone() == None:
                self.cursor.execute("INSERT INTO buttons (id,if_need,text ) VALUES ('1','False','0')")
            self.cursor.execute("SELECT * FROM buttons WHERE id = '2'")
            if self.cursor.fetchone() == None:
                self.cursor.execute("INSERT INTO buttons (id,if_need,text ) VALUES ('2','False','0')")
    def change_button(self,name,text,id):
        with self.connection:
            self.cursor.execute(f"UPDATE buttons SET if_need = '{name}' WHERE id = '{id}'")
            self.cursor.execute(f"UPDATE buttons SET text = '{text}' WHERE id = '{id}'")
    def get_button_name(self,name):
        with self.connection:
            self.cursor.execute(f"SELECT text FROM buttons WHERE if_need = '{name}'")
            row = self.cursor.fetchone()
            if not row:
                return "0"
            else:
                return row
    def change_ref_proc(self,ref):
        with self.connection:
            self.cursor.execute(f"UPDATE bot SET refproc = '{ref}' ")
    def get_users_id(self):
        with self.connection:
            self.cursor.execute("SELECT id FROM users")
            return self.cursor.fetchall()
    def get_len_users(self):
        with self.connection:
            self.cursor.execute("SELECT id FROM users")
            sas = self.cursor.fetchall()
            length = len(sas)
            return length
    def get_log_chat(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM log_chat")
            return self.cursor.fetchone()[0]
    def add_log(self,cid):
        with self.connection:
            self.cursor.execute(f"UPDATE log_chat SET id = '{cid}' ")
    def reg_user(self,user_id,ref_id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
            if self.cursor.fetchone() == None:
                self.cursor.execute(f"INSERT INTO users ('id','balance','refbalance','refered') VALUES ('{user_id}','0','0','{ref_id}')")

    def minus_day(self,amount):
        with self.connection:
            self.cursor.execute("SELECT * FROM bot")
            row = self.cursor.fetchone()
            new_time = int(row[0]) - int(amount)
            new_live = int(row[1]) + int(amount)
            
     
            self.cursor.execute(f"UPDATE bot SET date_down = '{new_time}'")
            self.cursor.execute(f"UPDATE bot SET date_live = '{new_live}'")
    def plus_balance(self,user_id,amount):
        with self.connection:
            self.cursor.execute(f"SELECT balance FROM users WHERE id = '{user_id}'")
            new_balance = int(self.cursor.fetchone()[0]) + int(amount)
            self.cursor.execute(f"UPDATE users SET balance = '{new_balance}' WHERE id = '{user_id}'")

            self.cursor.execute(f"SELECT money_make FROM bot")
            new_money_make = int(self.cursor.fetchone()[0]) + int(amount)
    def minus_balance(self,user_id,amount):
        with self.connection:
            self.cursor.execute(f"SELECT balance FROM users WHERE id = '{user_id}'")
            new_balance = int(self.cursor.fetchone()[0]) - int(amount)
            self.cursor.execute(f"UPDATE users SET balance = '{new_balance}' WHERE id = '{user_id}'")
    def plus_day(self,amount):
        with self.connection:
            self.cursor.execute("SELECT * FROM bot")
            row = self.cursor.fetchone()
            new_time = int(row[0]) + int(amount)
            self.cursor.execute(f"UPDATE bot SET date_down = '{new_time}'")
    def get_bot(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM bot")
            return self.cursor.fetchone()
    def get_ebal(self,user_id):
        with self.connection:
            self.cursor.execute(f"SELECT balance FROM users WHERE id = '{user_id}'")
            return self.cursor.fetchone()
    def get_buttons(self,id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM buttons WHERE id = '{id}'")
            arr = self.cursor.fetchone()
            if arr == None:
                return "0"
            else:
                if arr[1] == "False":
                    return "0"
                else:
                    return arr[1]
    def add_cat(self,catname):
        with self.connection:
            ran_cat_id = randint(0,999999)
            self.cursor.execute(f"INSERT INTO cat ('id','name') VALUES ('{ran_cat_id}','{catname}') ")
    def del_cat(self,catname):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM cat WHERE name = '{catname}'")
            idcat = self.cursor.fetchone()
            self.cursor.execute(f"DELETE FROM cat WHERE name = '{catname}'")
            self.cursor.execute(f"SELECT id FROM podcat WHERE name = '{idcat[0]}'")
            idpodcat = self.cursor.fetchone()
            self.cursor.execute(f"DELETE FROM podcat WHERE parent = '{idcat[0]}'")
            self.cursor.execute(f"DELETE FROM products WHERE parent = '{idpodcat[0]}'")
    def del_podcat(self,podcatname):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM podcat WHERE name = '{podcatname}'")
            idpodcat = self.cursor.fetchone()
            self.cursor.execute(f"DELETE FROM podcat WHERE id = '{idpodcat[0]}'")
            self.cursor.execute(f"DELETE FROM products WHERE parent = '{idpodcat[0]}'")
    def del_tovar(self,tovid):
        with self.connection:
            self.cursor.execute(f"DELETE FROM products WHERE id = '{tovid[0]}'")
    def add_podcat(self,catname,podcatname):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM cat WHERE name = '{catname}'")
            catid = self.cursor.fetchone()
            if catid != None:
                ran_podcat_id = randint(0,999999)
                self.cursor.execute(f"INSERT INTO podcat ('id','name','parent') VALUES ('{ran_podcat_id}','{podcatname}','{catid[0]}') ")
    def add_prod(self,podcatname,tovarname,price,desc):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM podcat WHERE name = '{podcatname}'")
            podcatid = self.cursor.fetchone()
            if podcatid:
                ran_prod_id = randint(0,999999)
                self.cursor.execute(f"INSERT INTO products ('id','name','parent','price','description') VALUES ('{ran_prod_id}','{tovarname}','{podcatid[0]}','{price}','{desc}')")
                self.cursor.execute(f"CREATE TABLE IF NOT EXISTS '{ran_prod_id}' ('data' varchar)")
                return ran_prod_id
    def get_parent(self,text):
         with self.connection:
            self.cursor.execute("SELECT name FROM cat")
            return self.cursor.fetchall()
    def get_cat(self):
        with self.connection:
            self.cursor.execute("SELECT name FROM cat")
            return self.cursor.fetchall()
    def get_podcat_by_parent(self,parentname,need):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM cat WHERE name = '{parentname}'")
            local = self.cursor.fetchone()
            if local:
                self.cursor.execute(f"SELECT name FROM podcat WHERE parent = '{local[0]}'")
                if need:
                    return self.cursor.fetchall()
                else:
                    return True
            else:
                return False
    def get_prod_by_parent(self,name,need):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM podcat WHERE name = '{name}'")
            podcatid = self.cursor.fetchone()
            if podcatid:
                if need:
                    self.cursor.execute(f"SELECT name FROM products WHERE parent = '{podcatid[0]}'")
                    return self.cursor.fetchall()
                else:
                    return True
            else:
                return False
    def get_prod_advanced(self,name,need):
        with self.connection:          
            self.cursor.execute(f"SELECT id FROM products WHERE name = '{name}'")
            tovarid = self.cursor.fetchone()
            if tovarid:
                if need:
                    self.cursor.execute(f"SELECT description FROM products WHERE id = '{tovarid[0]}'")
                    local1 = self.cursor.fetchone()
                    self.cursor.execute(f"SELECT price FROM products WHERE id = '{tovarid[0]}'")
                    local2 = self.cursor.fetchone()
                    self.cursor.execute(f"SELECT * FROM '{tovarid[0]}'")
                    local3 = self.cursor.fetchall()
                    local3 = len(local3)
                    listik = (local1[0],local2[0],local3,tovarid[0])
                    return listik
                else:
                    return True
            else:
                return False
    def get_prod_advanced_by_id(self,name,need):
        with self.connection:
            tovarid = (name,"blabla")
            if tovarid:
                if need:
                    self.cursor.execute(f"SELECT description FROM products WHERE id = '{tovarid[0]}'")
                    local1 = self.cursor.fetchone()
                    self.cursor.execute(f"SELECT price FROM products WHERE id = '{tovarid[0]}'")
                    local2 = self.cursor.fetchone()
                    self.cursor.execute(f"SELECT * FROM '{tovarid[0]}'")
                    local3 = self.cursor.fetchall()
                    local3 = len(local3)
                    listik = (local1[0],local2[0],local3,tovarid[0])
                    return listik
                else:
                    return True
            else:
                return False
    def add_prod_real(self,prodid,datayoba):
        with self.connection:
            self.cursor.execute(f"INSERT INTO '{prodid[0]}' ('data') VALUES ('{datayoba}') ")
    def get_prod_real_1(self,prodid):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM '{prodid}'")
            data = self.cursor.fetchall()
            if len(data)>0:
                data = choice(data)
            else:
                return "AMOUNT"
    def get_prod_real(self,prodid):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM '{prodid}'")
            data = self.cursor.fetchall()
            if len(data)>0: 
                self.cursor.execute(f"DELETE FROM '{prodid}' WHERE data = '{data[0][0]}'")
                return data
            else:
                return "AMOUNT"
    def get_prod(self):
        with self.connection:
            self.cursor.execute("SELECT name FROM products")
            return self.cursor.fetchall()
    def get_prodid_by_name(self,name):
        with self.connection:
            self.cursor.execute(f"SELECT id FROM products WHERE name = '{name}'")
            return self.cursor.fetchone()
    def get_prodname_by_id(self,tovid):
        with self.connection:
            self.cursor.execute("SELECT name FROM products WHERE id = '{tovid}'")
            return self.cursor.fetchone()
    def get_price_byid(self,tovid):
         with self.connection:
            self.cursor.execute(f"SELECT price FROM products WHERE id = '{tovid}'")
            return self.cursor.fetchone()