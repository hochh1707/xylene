from dbStuff import classDbStuff
from flask import Flask, render_template, request, session

def dbTable(ckl,operation):
    dbStuff = classDbStuff()
    if ckl[0] == 1 and ckl[2] == 2:
        if operation == "backup":
            dbStuff.backup()
        elif operation == "restore":
            dbStuff.restore()
        elif operation == "drop":
            dbStuff.dropTable()
        elif operation == "make_table":
            result = dbStuff.makeTable()
    return render_template('make_table.html',operation=operation,result=result,ckl=ckl)
