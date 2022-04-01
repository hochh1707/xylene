from dbStuff import classDbStuff
from flask import Flask, render_template, request, session

def dashboard(ckl):
    dbStuff = classDbStuff()
    dashboardData = {}
    dashboardData['count_total_docs'] = dbStuff.getCountDocuments()
    dashboardData['count_incomplete_docs' + '_' + ckl[1]] = dbStuff.getCountIncompleteDocuments(ckl[1])
    dashboardData['count_incomplete_docs_all'] = dbStuff.getCountIncompleteDocuments("all")
    return render_template('dashboard.html',dashboardData=dashboardData,ckl=ckl)
