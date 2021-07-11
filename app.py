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

app = Flask(__name__)
app.secret_key = "blah"
try:
    dbStuff = classDbStuff()
except Exception as e:
    dbStuff = 0
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

@app.route('/')
def home():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    ckl = checkLogin()
    if dbStuff == 0: return render_template('error.html',ckl=ckl)
    return render_template('base.html',color=color,ckl=ckl)

@app.route('/settings', methods=["POST","GET"])
def settings():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    ckl = checkLogin()
    if request.method == "POST":
        session['working_user'] = request.form['working_user']
    return render_template('settings.html',color=color,ckl=ckl,workingUser=session['working_user'])

@app.route('/login')
def login():
    ckl = checkLogin()
    if ckl[0] == 1:
        message = "User: " + session['user_name'] + " is already logged in!"
    else:
        message = "Log in and get to work!"
    return render_template('login1.html',message=message,status=ckl[0])

@app.route('/login2', methods=['POST'])
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

@app.route('/logout')
def logout():
    ckl = checkLogin()
    if ckl[0] == 1:
        message = "User: " + session['user_name'] + " is logged out."
        session.pop('user_name')
    else:
        message = "You were never logged in!"
    return render_template('logout.html',message=message)

@app.route('/dashboard')
def dashboard():
    ckl = checkLogin()
    dashboardData = {}
    if ckl[0] == 1:
        dashboardData['count_total_docs'] = dbStuff.getCountDocuments()
        dashboardData['count_incomplete_docs' + '_' + ckl[1]] = dbStuff.getCountIncompleteDocuments(ckl[1])
        dashboardData['count_incomplete_docs_all'] = dbStuff.getCountIncompleteDocuments("all")
    return render_template('dashboard.html',dashboardData=dashboardData,ckl=ckl)

@app.route('/new_files', methods=["POST","GET"])
def new_files():
    newFiles = []
    message = ""
    ckl = checkLogin()
    if ckl[0] == 1:
        # figure out the next document number to use
        ldn = dbStuff.getLastDocumentNumber()
        if ldn == None:
            return render_template('error.html',ckl=ckl)
        else:
            ndn = int(ldn) + 1
        # if user just uploaded new files, save them as doc100001.pdf, doc100002.pdf, etc.
        # then create new database records
        if request.method == "POST":
            fff = request.files.getlist("file")
            for f in fff:
                if f.filename == "": continue
                nf = "doc" + str(ndn) + ".pdf"
                f.save("static/documents/" + nf)
                newFiles.append(nf)
                dbStuff.createBlankDocumentRecord(ckl[1],ndn,obEs.dataFields())
                ndn = ndn + 1
        message = "There were " + str(len(newFiles)) + " new files imported"
    return render_template('new_files.html',message=message,newFiles=newFiles,ckl=ckl)

@app.route('/enter_stuff')
def enter_stuff():
    configs = {}
    message = "Looks like you are done entering data!"
    ckl = checkLogin()
    if ckl[0] == 1:
        rd = obEs.pickRandomDoc(session['working_user'])
        if rd != None:
            configs['docnum'] = rd[0]
            configs['username_created'] = rd[1]
            configs['data_field'] = obEs.getNextFieldToEnter(rd[0])
            configs['doc_data'] = obEs.getDataForDoc(rd[0])
            configs['file_to_show'] = "doc" + rd[0] + ".pdf"
            configs['input_type'] = obEs.dataFields()[configs['data_field']]['input_type']
            configs['max_length'] = obEs.dataFields()[configs['data_field']]['max_length']
            if configs['input_type'] == "radio":
                configs['data_choices'] = obEs.dataFields()[configs['data_field']]['data_choices']
    return render_template('enter_stuff.html', configs=configs, ckl=ckl, message=message)

@app.route('/submit', methods=['POST'])
def submit():
    params = {}
    ckl = checkLogin()
    if ckl[0] == 1:
        params['data_field'] = request.form.get('data_field')
        params['docnum'] = request.form.get('docnum')
        params['data'] = request.form.get('data')
        dbStuff.updateDocument(params,ckl[1])
    return render_template('submit.html',params=params,ckl=ckl)

@app.route('/mark_unknown/<docnum>/<dataField>')
def markUnknown(docnum,dataField):
    params = {}
    ckl = checkLogin()
    if ckl[0] == 1:
        params['data_field'] = dataField
        params['docnum'] = docnum
        params['data'] = "unk"
        dbStuff.updateDocument(params,ckl[1])
    return render_template('submit.html',params=params,ckl=ckl)

@app.route('/create_letter')
def letter():
    ckl = checkLogin()
    return render_template('letter.html',ckl=ckl)

@app.route('/mail_merge1', methods=["GET","POST"])
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
        if dfm == None: return render_template('error.html',ckl=ckl)
    return render_template('mailmerge1.html',dfm=dfm,ckl=ckl,tsd=tsd,ft=ft)

@app.route('/mail_merge2',methods=['POST'])
def mail_merge2():
    ckl = checkLogin()
    if ckl[0] == 1:
        ltm = request.form
        print(ltm)
        obMm = mailMerge()
        obMm.mailMerge(ckl,ltm)
    return render_template('mailmerge2.html',ltm=ltm,ckl=ckl)

@app.route('/responses', methods=["GET","POST"])
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
        if dfm == None: return render_template('error.html',ckl=ckl)
    return render_template('responses.html',dfm=dfm,ckl=ckl,tsd=tsd,ft=ft,filter=filter)

@app.route('/enter_response/<docnum>', methods=["GET"])
def enter_response(docnum):
    dfm = []
    rrr = []
    ckl = checkLogin()
    if ckl[0] == 1:
        rrr = dbStuff.getResponses(docnum)
        obR = classResponses()
        dfm = obR.getDataForSingleView(session['working_user'],docnum)
    return render_template('enter_response.html',dfm=dfm,ckl=ckl,rrr=rrr)

@app.route('/submit_response', methods=["POST"])
def submit_response():
    message = "Not logged in!"
    ckl = checkLogin()
    if ckl[0] == 1:
        dbStuff.enterResponse(ckl[1],request.form['docnum'],request.form['response'])
        message = request.form['response']
    return render_template('submit_response.html',ckl=ckl,docnum=request.form['docnum'],message=message)

@app.route('/submit_return/<ooo>', methods=["GET"])
def enter_return(ooo):
    ckl = checkLogin()
    if ckl[0] == 1:
        docnum = ooo.split("m")[0]
        mailing = "owner_mailing" + str(ooo.split("m")[1])
        dbStuff.enterReturn(ckl[1],docnum,mailing)
    return render_template('submit_return.html',ckl=ckl,docnum=docnum,mailing=mailing)

@app.route('/sysadmin')
def sysadmin():
    ckl = checkLogin()
    return render_template('sysadmin.html',ckl=ckl)

@app.route('/dbtable/<operation>')
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
    app.run()
