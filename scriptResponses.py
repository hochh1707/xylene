from classEnterStuff import classEnterStuff
from classMailMerge import classMailMerge
from classResponses import classResponses
from dbStuff import classDbStuff
from flask import Flask, render_template, request, session

def responses(ckl,request):
    # initialize variables
    obR = classResponses()
    obMm = classMailMerge()
    obEs = classEnterStuff()
    ft = obEs.firstTuesdays()
    filterCounties = {}
    dfm = ""

    ## set default filters
    # by default, all counties are selected
    for i in obEs.counties(): filterCounties[i] = 1
    filterTsd = obEs.nextSaleDate()
    filterEquity = "all"
    filterReturnedMail = "include"
    filterText = ""
    filterResponses = "include"
    sortField = "equity"

    # update filters with user selections
    if request.method=="POST":
        filterText = request.form['filter_text']
        filterTsd = request.form['tsd']
        for c in obEs.counties():
            if c in request.form.keys():
               filterCounties[c] = 1
            else:
                filterCounties[c] = 0
        filterEquity = request.form['equity']
        filterReturnedMail = request.form['filter_returned_mail']
        filterResponses = request.form['filter_responses']
        sortField = request.form['sort_field']

    listForView = obR.getDocListForView(session['working_user'],filterText)
    if listForView == None: return render_template('error.html',ckl=ckl)
    dfm = obR.getDataForView(listForView,session['working_user'],filterTsd,filterCounties,filterEquity,filterReturnedMail,filterResponses,sortField)
    return render_template('responses1.html',dfm=dfm,ckl=ckl,tsd=filterTsd,
        ft=ft,ccc=filterCounties,equity=filterEquity,filterReturnedMail=filterReturnedMail,filterResponses=filterResponses,sortField=sortField,filterText=filterText)

def enterResponse(ckl,docnum):
    obR = classResponses()
    dbStuff = classDbStuff()
    dfm = []
    rrr = []
    rrr = dbStuff.getResponses(docnum)
    dfm = obR.getDataForSingleView(session['working_user'],docnum)
    return render_template('enter_response.html',dfm=dfm,ckl=ckl,rrr=rrr)

def submitResponse(ckl,response):
    dbStuff = classDbStuff()
    dbStuff.enterResponse(ckl[1],request.form['docnum'],request.form['response'])
    message = request.form['response']
    return render_template('submit_response.html',ckl=ckl,docnum=request.form['docnum'],message=message)

def enterReturn(ckl,ooo):
    dbStuff = classDbStuff()
    docnum = ooo.split("m")[0]
    mailing = "owner_mailing" + str(ooo.split("m")[1])
    dbStuff.enterReturn(ckl[1],docnum,mailing)
    return render_template('submit_return.html',ckl=ckl,docnum=docnum,mailing=mailing)
