from flask import Flask, render_template, request, session
import time
import bcrypt

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

def login1(ckl):
    if ckl[0] == 1:
        message = "User: " + session['user_name'] + " is already logged in!"
    else:
        message = "Log in and get to work!"
    return render_template('login1.html',message=message,status=ckl[0])

def login2(ckl):
    message = "Whoops! That didn't work!"
    if ckl[0] == 0 and request.form['username'] == "david":
            ppp = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt())
            if bcrypt.checkpw(b"yyy444bbb",ppp) == True:
                session['working_user'] = request.form['username']
                session['user_name'] = request.form['username']
                session['access_level'] = 2
                session['login_time'] = time.time()
                message = "User: " + request.form['username'] + " is logged in!"
    elif ckl[0] == 0 and request.form['username'] == "jeremy":
            ppp = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt())
            if bcrypt.checkpw(b"qw713hh",ppp) == True:
                session['working_user'] = request.form['username']
                session['user_name'] = request.form['username']
                session['access_level'] = 1
                session['login_time'] = time.time()
                message = "User: " + request.form['username'] + " is logged in!"
    return render_template('login2.html',message=message)

def logout(ckl):
    if ckl[0] == 1:
        message = "User: " + session['user_name'] + " is logged out."
        session.pop('user_name')
    else:
        message = "You were never logged in!"
    return render_template('logout.html',message=message)
