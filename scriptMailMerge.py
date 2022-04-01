from classMailMerge import classMailMerge
from classEnterStuff import classEnterStuff
from classS3stuff import classS3stuff
from dbStuff import classDbStuff
from flask import Flask, render_template, request, session

def mailMerge1(request,ckl):
    # mail merge 1 allows the user to view all the documents available to mail to, and allows user to filter them.
    # ft = list of possible trustee sale dates for user to choose from
    
    # initialize variables
    obMm = classMailMerge()
    obEs = classEnterStuff()
    filterCounties = {}
    ft = obEs.firstTuesdays()

    ## set default filters
    # by default, all counties are selected
    for i in obEs.counties(): filterCounties[i] = 1
    filterTsd = obEs.nextSaleDate()
    filterEquity = "all"
    filterReturnedMail = "exclude"
    sortField = "equity"

    if request.method=="POST":
        # update filters based on user input
        filterTsd = request.form['tsd']
        for c in obEs.counties():
            if c in request.form.keys():
               filterCounties[c] = 1
            else:
                filterCounties[c] = 0
        filterEquity = request.form['equity']
        filterReturnedMail = request.form['filter_returned_mail']
        sortField = request.form['sort_field']

    listForMerge = obMm.getListForMerge(session['working_user'])
    if listForMerge != None: 
        dataForMerge = obMm.getDataForMerge(listForMerge,session['working_user'],filterTsd,filterCounties,filterEquity,filterReturnedMail,sortField)    
    else:
        dataForMerge = []
    return render_template('mailmerge1.html',dfm=dataForMerge,ckl=ckl,tsd=filterTsd,
        ft=ft,ccc=filterCounties,equity=filterEquity,filterReturnedMail=filterReturnedMail,sortField=sortField)

def mailMerge2(request,ckl):
    obMm = classMailMerge()
    obS3 = classS3stuff()
    listToMail = request.form
    obS3.xferDocs(listToMail)
    obMm.mailMerge(ckl,listToMail)
    return render_template('mailmerge2.html',ltm=listToMail,ckl=ckl)
