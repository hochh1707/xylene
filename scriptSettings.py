from flask import render_template,session

def userSettings(request,color,ckl):
    if request.method == "POST":
        session['working_user'] = request.form['working_user']
    return render_template('settings.html',color=color,ckl=ckl,workingUser=session['working_user'])
