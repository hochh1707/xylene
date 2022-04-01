from dbStuff import classDbStuff
from classEnterStuff import classEnterStuff
from flask import Flask, render_template, request, session

def enterStuff(ckl):
    obEs = classEnterStuff()
    configs = {}
    message = "Looks like you are done entering data!"
    rd = obEs.pickWorkingDoc(session['working_user'])
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

def submit(ckl):
    dbStuff = classDbStuff()
    params = {}
    if ckl[0] == 1:
        params['data_field'] = request.form.get('data_field')
        params['docnum'] = request.form.get('docnum')
        params['data'] = request.form.get('data')
        dbStuff.updateDocument(params,ckl[1])
    return render_template('submit.html',params=params,ckl=ckl)

def copyOld(ckl,oldDocnum,newDocnum):
    obDb = classDbStuff()
    listDataOldDoc = obDb.getDataSingleDoc(oldDocnum)
    for i in listDataOldDoc:
        if i['field_name'] == "trustee_sale_date": continue
        if i['field_name'] == "status": continue
        params = {}
        params['data'] = i['data']
        params['docnum'] = newDocnum
        params['data_field'] = i['field_name']
        obDb.updateDocument(params,ckl[1])
    return "hhh"

def markUnknown(ckl,docnum,dataField,value):
    dbStuff = classDbStuff()
    params = {}
    if ckl[0] == 1:
        params['docnum'] = docnum
        params['data_field'] = dataField
        params['data'] = value
        dbStuff.updateDocument(params,ckl[1])
    return render_template('submit.html',params=params,ckl=ckl)

