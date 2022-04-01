import mysql.connector
import time
import datetime
import json
import os

class classDbStuff(object):
    def __init__(self):
        db = 2
        if db == 1:
            self.mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "aaabbbccc",
                    database = "xylene",
                    auth_plugin = "mysql_native_password",
                    autocommit = True
                    )
        elif db == 2:
            self.mydb = mysql.connector.connect(
                    host = "qao3ibsa7hhgecbv.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
                    user = "xgyxs1vptj3sxubk",
                    password = "baiytm82d2jzcz6m",
                    database = "fpsep8uzl8l7ece5",
                    autocommit = True
                    )

    def makeTable(self):
        mycursor = self.mydb.cursor(dictionary=True)
        q1 = ("CREATE TABLE documents" 
              " ("
              "pk INT AUTO_INCREMENT PRIMARY KEY,"
              " username_created VARCHAR(64),"
              " username_updated VARCHAR(64),"
              " updated VARCHAR(64),"
              " docnum VARCHAR(10),"
              " field_name VARCHAR(255),"
              " data VARCHAR(255)"
              ")"
              )
        try:
            mycursor.execute(q1)
        except Exception as e:
            return e
        return "Success"
    
    def backup(self):
        os.system("mysqldump -h localhost -u root -p xylene > xylene.sql")

    def restore(self):
        os.system("mysql -h localhost -u root -p xylene < xylene.sql")

    def dropTable(self):
        mycursor = self.mydb.cursor()
        q1 = "DROP TABLE documents"
        try:
            mycursor.execute(q1)
            mycursor.close()
        except Exception as e:
            print(e)

    def getLastDocumentNumber(self):
        mycursor = self.mydb.cursor()
        q1 = "SELECT max(docnum) from documents"
        try:
            mycursor.execute(q1)
            x = mycursor.fetchone()[0]
            if x == None: x = 100000
            mycursor.close()
            return x
        except Exception as e:
            print(e)
        return None

    def createBlankDocumentRecord(self,userName,docnum,fields):
        for f in fields:
            mycursor = self.mydb.cursor()
            q1 = ("INSERT INTO documents (username_created,username_updated,updated,docnum,field_name,data) VALUES('"
                  + userName + "','" + userName + "',NOW(),'" + str(docnum) + "','" + f + "','" + fields[f]['default'] + "')"
                 )
            try:
                mycursor.execute(q1)
                mycursor.close()
            except Exception as e:
                print(e)

    def getListIncompleteDocuments(self,workingUser):
        mycursor = self.mydb.cursor()
        q1 = "SELECT docnum, username_created FROM documents WHERE field_name = 'status' AND data = 'incomplete'"
        if workingUser == "all":
            q1 = q1 + " ORDER BY docnum ASC"
        else:
            q1 = q1 + " AND username_created = '" + workingUser + "' ORDER BY docnum ASC"
        try:
            mycursor.execute(q1)
            x = list(mycursor.fetchall())
            mycursor.close()
            return x
        except Exception as e:
            print(e)
        return None

    def getListCompleteDocuments(self,workingUser):
        mycursor = self.mydb.cursor()
        q1 = ("SELECT docnum FROM documents WHERE"
             + " field_name = 'status'"
             + " AND data = 'complete'"
            )
        if workingUser != "all":
            q1 = q1 + " AND username_created = '" + workingUser + "'"
        try:
            mycursor.execute(q1)
            x = list(mycursor.fetchall())
            mycursor.close()
            return x
        except Exception as e:
            print(e)
        return None

    def getListForView(self,workingUser,filter):
        mycursor = self.mydb.cursor()
        if filter == "": filter="%"
        q1 = ("SELECT DISTINCT(docnum) FROM documents WHERE"
             + " data like '%" + filter + "%'"
            )
        if workingUser != "all":
            q1 = q1 + " AND username_created = '" + workingUser + "'"
        try:
            mycursor.execute(q1)
            x = list(mycursor.fetchall())
            mycursor.close()
            return x
        except Exception as e:
            print(e)
        return None

    def updateDocument(self,params,userName):
        mycursor = self.mydb.cursor()
        q1 = ("UPDATE documents SET"
              + " data = '" + params['data'] + "',"
              + " username_updated = '" + userName + "',"
              + " updated = NOW()"
              + " WHERE docnum = '" + params['docnum'] + "'"
              + " AND field_name = '" + params['data_field'] + "'"
             )
        try:
            mycursor.execute(q1)
        except Exception as e:
            print(e)

    def getDataSingleDoc(self,docnum):
        mycursor = self.mydb.cursor(dictionary=True)
        q1 = "SELECT * FROM documents WHERE docnum = " + str(docnum)
        try:
            mycursor.execute(q1)
            x = mycursor.fetchall()
        except Exception as e:
            print(e)
        return x

    def getResponses(self,docnum):
        mycursor = self.mydb.cursor(dictionary=True)
        q1 = "SELECT * FROM documents WHERE docnum = '" + str(docnum) + "' AND field_name = 'response'"
        try:
            mycursor.execute(q1)
            x = mycursor.fetchall()
        except Exception as e:
            print(e)
        return x

    def getCountDocuments(self):
        mycursor = self.mydb.cursor()
        q1 = "SELECT COUNT(DISTINCT(docnum)) FROM documents"
        try:
            mycursor.execute(q1)
            x = mycursor.fetchone()[0]
        except Exception as e:
            print(e)
        return x

    def getCountIncompleteDocuments(self,workingUser):
        mycursor = self.mydb.cursor()
        q1 = "SELECT count(docnum) FROM documents WHERE field_name = 'status' AND data = 'incomplete'"
        if workingUser != "all":
            q1 = q1 + " AND username_created = '" + workingUser + "'"
        try:
            mycursor.execute(q1)
            x = mycursor.fetchone()[0]
        except Exception as e:
            print(e)
        return x

    def checkIfBlank(self,docnum,field):
        # picks the next data field that has not been filled in yet
        mycursor = self.mydb.cursor(dictionary=True)
        q1 = "SELECT data FROM documents WHERE docnum = " + str(docnum) + " AND field_name = '" + field + "'"
        try:
            mycursor.execute(q1)
            x = mycursor.fetchone()
        except Exception as e:
            print(e)
        if x == None:
            return False
        elif x['data'] == "blank" or None:
            return True
        return False

    def enterResponse(self,userName,docnum,response):
        mycursor = self.mydb.cursor()
        q1 = ("INSERT INTO documents (username_created,username_updated,updated,docnum,field_name,data) VALUES('"
                + userName + "','" + userName + "',NOW(),'" + str(docnum) + "','response','" + response + "')"
                )
        try:
            mycursor.execute(q1)
            mycursor.close()
        except Exception as e:
            print(e)

    def enterReturn(self,userName,docnum,mailing):
        mycursor = self.mydb.cursor()
        q1 = ("INSERT INTO documents (username_created,username_updated,updated,docnum,field_name,data) VALUES('"
                + userName + "','" + userName + "',NOW(),'" + str(docnum) + "','returned_mail','" + str(mailing) + "')"
                )
        try:
            mycursor.execute(q1)
            mycursor.close()
        except Exception as e:
            print(e)