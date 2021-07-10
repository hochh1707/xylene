from mailMerge import mailMerge
from classResponses import classResponses
from enterStuff import enterStuff
from dbStuff import classDbStuff
from flask import Flask, render_template, request, session
import os
import time
from os import listdir
import random
import bcrypt

application = Flask(__name__)
application.secret_key = "blah"
dbStuff = classDbStuff()
obEs = enterStuff()

def defaultSettings(userName):
    session['working_user'] = userName

def checkLogin():
    if 'user_name' in session and time.time() - session['login_time'] < 24*60*60:
        status = 1
        userName = session['user_name']
        accessLevel = session['access_level']
    elif 'user_name' in session:
        status = 0
        userName = "<Login expired>"
        accessLevel = 0
    else:
        status = 0
        userName = "<Not logged in>"
        accessLevel = 0
    return [status,userName,accessLevel]

@application.route('/')
def home():
    ckl = checkLogin()
    color = "%06x" % random.randint(0, 0xFFFFFF)
    return render_template('base.html',color=color,ckl=ckl)

@application.route('/settings', methods=["POST","GET"])
def settings():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    ckl = checkLogin()
    if request.method == "POST":
        session['working_user'] = request.form['working_user']
    return render_template('settings.html',color=color,ckl=ckl,workingUser=session['working_user'])

@application.route('/login')
def login():
    ckl = checkLogin()
    if ckl[0] == 1:
        message = "User: " + session['user_name'] + " is already logged in!"
    else:
        message = "Log in and get to work!"
    return render_template('login1.html',message=message,status=ckl[0])

@application.route('/login2', methods=['POST'])
def login2():
    ckl = checkLogin()
    message = "Whoops! That didn't work!"
    if ckl[0] == 0 and request.form['username'] == "david":
            ppp = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt())
            if bcrypt.checkpw(b"yyy444bbb",ppp) == True:
                defaultSettings(request.form['username'])
                session['user_name'] = request.form['username']
                session['access_level'] = 2
                session['login_time'] = time.time()
                message = "User: " + request.form['username'] + " is logged in!"
    elif ckl[0] == 0 and request.form['username'] == "jeremy":
            ppp = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt())
            if bcrypt.checkpw(b"qw713hh",ppp) == True:
                defaultSettings(request.form['username'])
                session['user_name'] = request.form['username']
                session['access_level'] = 1
                session['login_time'] = time.time()
                message = "User: " + request.form['username'] + " is logged in!"
    return render_template('login2.html',message=message)

@application.route('/logout')
def logout():
    ckl = checkLogin()
    if ckl[0] == 1:
        message = "User: " + session['user_name'] + " is logged out."
        session.pop('user_name')
    else:
        message = "You were never logged in!"
    return render_template('logout.html',message=message)

@application.route('/dashboard')
def dashboard():
    ckl = checkLogin()
    dashboardData = {}
    if ckl[0] == 1:
        dashboardData['count_total_docs'] = dbStuff.getCountDocuments()
        dashboardData['count_incomplete_docs'] = dbStuff.getCountIncompleteDocuments()
    return render_template('dashboard.html',dashboardData=dashboardData,ckl=ckl)

@application.route('/new_files', methods=["POST","GET"])
def new_files():
    newFiles = []
    resultImport = ""
    ckl = checkLogin()
    if ckl[0] == 1:
        if request.method == "POST":
            fff = request.files.getlist("file")
            for f in fff:
                f.save("static/documents/" + f.filename)
        bbb = os.listdir("./static/documents")
        for b in bbb:
            if b[0:3] != "doc":
                lastDocNum = int(dbStuff.getLastDocumentNumber()) + 1
                dbStuff.createBlankDocumentRecord(ckl[1],lastDocNum,obEs.dataFields())
                newFile = "doc" + str(lastDocNum) + ".pdf"
                newFiles.append(newFile)
                os.rename("./static/documents/" + b,"./static/documents/" + newFile)
                newFile = ""
        if len(newFiles) == 0:
            resultImport = "No new files detected"
        else:
            resultImport = "There were " + str(len(newFiles)) + " new files imported: "
    return render_template('new_files.html',resultImport=resultImport,newFiles=newFiles,ckl=ckl)

@application.route('/enter_stuff')
def enter_stuff():
    configs = {}
    message = "Looks like you are done entering data!"
    ckl = checkLogin()
    if ckl[0] == 1:
        docnum = obEs.pickRandomDoc(session['working_user'])
        if docnum != None:
            configs['docnum'] = docnum
            configs['data_field'] = obEs.getNextFieldToEnter(docnum)
            configs['doc_data'] = obEs.getDataForDoc(docnum)
            configs['file_to_show'] = "doc" + docnum + ".pdf"
            configs['input_type'] = obEs.dataFields()[configs['data_field']]['input_type']
            configs['max_length'] = obEs.dataFields()[configs['data_field']]['max_length']
            if configs['input_type'] == "radio":
                configs['data_choices'] = obEs.dataFields()[configs['data_field']]['data_choices']
    return render_template('enter_stuff.html', configs=configs, ckl=ckl, message=message)

@application.route('/submit', methods=['POST'])
def submit():
    params = {}
    ckl = checkLogin()
    if ckl[0] == 1:
        params['data_field'] = request.form.get('data_field')
        params['docnum'] = request.form.get('docnum')
        params['data'] = request.form.get('data')
        dbStuff.updateDocument(params,ckl[1])
    return render_template('submit.html',params=params,ckl=ckl)

@application.route('/mark_unknown/<docnum>/<dataField>')
def markUnknown(docnum,dataField):
    params = {}
    ckl = checkLogin()
    if ckl[0] == 1:
        params['data_field'] = dataField
        params['docnum'] = docnum
        params['data'] = "unk"
        dbStuff.updateDocument(params,ckl[1])
    return render_template('submit.html',params=params,ckl=ckl)

@application.route('/create_letter')
def letter():
    ckl = checkLogin()
    return render_template('letter.html',ckl=ckl)

@application.route('/mail_merge1', methods=["GET","POST"])
def mail_merge1():
    ft = obEs.firstTuesdays()
    dfm = ""
    tsd = "all"
    ckl = checkLogin()
    if request.method=="POST":
        tsd = request.form['tsd']
    if ckl[0] == 1:
        obMm = mailMerge()
        dfm = obMm.getDataForMerge(session['working_user'],tsd)
    return render_template('mailmerge1.html',dfm=dfm,ckl=ckl,tsd=tsd,ft=ft)

@application.route('/mail_merge2',methods=['POST'])
def mail_merge2():
    ckl = checkLogin()
    if ckl[0] == 1:
        ltm = request.form
        print(ltm)
        obMm = mailMerge()
        obMm.mailMerge(ckl,ltm)
    return render_template('mailmerge2.html',ltm=ltm,ckl=ckl)

@application.route('/responses', methods=["GET","POST"])
def responses():
    ft = obEs.firstTuesdays()
    dfm = ""
    filter = ""
    tsd = "all"
    ckl = checkLogin()
    if request.method=="POST":
        filter = request.form['filter']
        tsd = request.form['tsd']
    if ckl[0] == 1:
        obR = classResponses()
        dfm = obR.getDataForView(session['working_user'],tsd,filter)
    return render_template('responses.html',dfm=dfm,ckl=ckl,tsd=tsd,ft=ft,filter=filter)

@application.route('/enter_response/<docnum>', methods=["GET"])
def enter_response(docnum):
    dfm = []
    rrr = []
    ckl = checkLogin()
    if ckl[0] == 1:
        rrr = dbStuff.getResponses(docnum)
        obR = classResponses()
        dfm = obR.getDataForSingleView(session['working_user'],docnum)
    return render_template('enter_response.html',dfm=dfm,ckl=ckl,rrr=rrr)

@application.route('/submit_response', methods=["POST"])
def submit_response():
    message = "Not logged in!"
    ckl = checkLogin()
    if ckl[0] == 1:
        dbStuff.enterResponse(ckl[1],request.form['docnum'],request.form['response'])
        message = request.form['response']
    return render_template('submit_response.html',ckl=ckl,docnum=request.form['docnum'],message=message)

@application.route('/submit_return/<ooo>', methods=["GET"])
def enter_return(ooo):
    ckl = checkLogin()
    if ckl[0] == 1:
        docnum = ooo.split("m")[0]
        mailing = "owner_mailing" + str(ooo.split("m")[1])
        dbStuff.enterReturn(ckl[1],docnum,mailing)
    return render_template('submit_return.html',ckl=ckl,docnum=docnum,mailing=mailing)

@application.route('/sysadmin')
def sysadmin():
    ckl = checkLogin()
    return render_template('sysadmin.html',ckl=ckl)

@application.route('/dbtable/<operation>')
def dbtable(operation):
    result = ""
    ckl = checkLogin()
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

if __name__ == "__main__":
    application.run()
