from dbStuff import classDbStuff
from flask import Flask, render_template, request, session
import random
from scriptMailMerge import *
from scriptLogin import *
from scriptSettings import *
from scriptDashboard import *
from scriptNewFiles import *
from scriptEnterStuff import *
from scriptResponses import *
from scriptSysadmin import *
from scriptS3 import *

app = Flask(__name__)
app.secret_key = "blah"
try:
    dbStuff = classDbStuff()
except Exception as e:
    print(e)
    dbStuff = 0

@app.route('/')
def home():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    ckl = checkLogin()
    if dbStuff == 0: return render_template('error.html',ckl=ckl)
    return render_template('base.html',color=color,ckl=ckl)

@app.route('/user_settings', methods=["POST","GET"])
def settings():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return userSettings(request,color,ckl)

@app.route('/login1')
def login1page():
    ckl = checkLogin()
    return login1(ckl)

@app.route('/login2', methods=['POST'])
def login2page():
    ckl = checkLogin()
    return login2(ckl)

@app.route('/logout')
def logoutPage():
    ckl = checkLogin()
    return logout(ckl)

@app.route('/dashboard')
def dashboardPage():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return dashboard(ckl)

@app.route('/new_files', methods=["POST","GET"])
def newFilesPage():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return newFiles(ckl)

@app.route('/enter_stuff')
def enterStuffPage():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return enterStuff(ckl)

@app.route('/submit', methods=['POST'])
def submitPage():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return submit(ckl)

@app.route('/copy_old', methods=['POST'])
def copyOldPage():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    yyy = copyOld(ckl,request.form['old_docnum'],request.form['new_docnum'])
    return enterStuff(ckl)

@app.route('/mark/<docnum>/<dataField>/<value>')
def markUnknownPage(docnum,dataField,value):
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return markUnknown(ckl,docnum,dataField,value)

@app.route('/create_letter')
def letter():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return render_template('letter.html',ckl=ckl)

@app.route('/mail_merge1', methods=["GET","POST"])
def mail_merge1():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return mailMerge1(request,ckl)

@app.route('/mail_merge2',methods=['POST'])
def mail_merge2():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return mailMerge2(request,ckl)

@app.route('/responses', methods=["GET","POST"])
def responsesPage():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return responses(ckl,request)

@app.route('/enter_response/<docnum>', methods=["GET"])
def enter_response(docnum):
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return enterResponse(ckl,docnum)

@app.route('/submit_response', methods=["POST"])
def submit_response():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return submitResponse(ckl,request)

@app.route('/submit_return/<ooo>', methods=["GET"])
def enter_return(ooo):
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return enterReturn(ckl,ooo)

@app.route('/sysadmin')
def sysadmin():
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return render_template('sysadmin.html',ckl=ckl)

@app.route('/dbtable/<operation>')
def dbTablePage(operation):
    result = ""
    ckl = checkLogin()
    if ckl[0] != 1: return render_template('login1.html',message="You're not logged in!",status=ckl[0])
    return dbTable(ckl,operation)

@app.route('/s3test')
def s3Page():
    return s3()

if __name__ == "__main__":
    app.run()
