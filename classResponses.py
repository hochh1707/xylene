import os
from os import path
import glob
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter, PageMerge, pdfwriter
from dbStuff import classDbStuff
from classMailMerge import classMailMerge

class classResponses(object):

    def getDocListForView(self,workingUser,filter):
        obDb = classDbStuff()
        ddd = obDb.getListForView(workingUser,filter)
        if ddd == None: return None
        return ddd

    def getDataForView(self,listCompleteDocs,workingUser,filterTsd,filterCounties,filterEquity,filterReturnedMail,filterResponses,sortField):
        # tsd = trustee sale date. It's either all or the first tuesday of a particular month.
        obDb = classDbStuff()
        obM = classMailMerge()
        listDataForMerge = []
        # Convert the mysql results to the dictionary format we need
        for doc in listCompleteDocs:
            dictDataForLetter = {}
            dictDataForLetter['docnum'] = doc[0]
            dictDataForLetter['returned_mail'] = []
            dictDataForLetter['responses'] = []
            listDataSingleDoc = obDb.getDataSingleDoc(doc[0])
            for i in listDataSingleDoc:
                dictDataForLetter['docnum'] = i['docnum']
                if i['field_name'] == "trustee_sale_date": dictDataForLetter['trustee_sale_date'] = i['data']
                if i['field_name'] == "county": dictDataForLetter['county'] = i['data']
                if i['field_name'] == "owner_name": dictDataForLetter['owner_name'] = i['data']
                if i['field_name'] == "property_address": dictDataForLetter['property_address'] = i['data']
                if i['field_name'] == "cad_link": dictDataForLetter['cad_link'] = i['data']
                if i['field_name'] == "deed_of_trust_year": dictDataForLetter['deed_of_trust_year'] = i['data']
                if i['field_name'] == "original_loan_amount": dictDataForLetter['original_loan_amount'] = i['data']
                if i['field_name'] == "market_value": dictDataForLetter['market_value'] = i['data']
                if i['field_name'] == "owner_mailing1": dictDataForLetter['owner_mailing1'] = i['data']
                if i['field_name'] == "owner_mailing2": dictDataForLetter['owner_mailing2'] = i['data']
                if i['field_name'] == "returned_mail": dictDataForLetter['returned_mail'].append(i['data'])
                if i['field_name'] == "status": dictDataForLetter['status'] = i['data']
                if i['field_name'] == "status" and i['data'] == "complete": dictDataForLetter['updated'] = i['updated']
                if i['field_name'] == "returned_mail": dictDataForLetter['returned_mail'].append(i['data'])
                if i['field_name'] == "response": dictDataForLetter['responses'].append(i['data'])
            dictDataForLetter['est_equity'] = obM.computeEquity(dictDataForLetter['deed_of_trust_year'],dictDataForLetter['original_loan_amount'],dictDataForLetter['market_value'])
            listDataForMerge.append(dictDataForLetter)

        # Remove records that don't match the user selected sale date, counties, equity, or returned mail
        for i in range(len(listDataForMerge)-1,-1,-1):
            yyy = listDataForMerge[i]
            if listDataForMerge[i]['status'] != "complete":
                listDataForMerge.pop(i)
            elif filterTsd != "all" and listDataForMerge[i]['trustee_sale_date'] != filterTsd:
                listDataForMerge.pop(i)
            elif filterCounties[listDataForMerge[i]['county']] == 0:
                listDataForMerge.pop(i)
            elif filterEquity == "over100" and int(listDataForMerge[i]['est_equity']) < 99999:
                listDataForMerge.pop(i)
            elif filterEquity == "under100" and int(listDataForMerge[i]['est_equity']) > 100000:
                listDataForMerge.pop(i)
            elif filterReturnedMail == "exclude":
                if "returned_mail" in listDataForMerge[i].keys():
                    if "owner_mailing1" in listDataForMerge[i]['returned_mail']:
                        listDataForMerge.pop(i)
                    if "owner_mailing2" in listDataForMerge[i]['returned_mail']:
                        listDataForMerge.pop(i)
            elif filterReturnedMail == "only":
                if len(listDataForMerge[i]['returned_mail']) == 0: listDataForMerge.pop(i)
            elif filterResponses == "exclude":
                if len(listDataForMerge[i]['responses']) > 0: listDataForMerge.pop(i)
            elif filterResponses == "only":
                if len(listDataForMerge[i]['responses']) == 0: listDataForMerge.pop(i)

        listDataForMerge = obM.sortMergeData(listDataForMerge,sortField)
        
        return listDataForMerge

    def getDataForSingleView(self,workingUser,docnum):
        obDb = classDbStuff()
        fff = []
        aaa = {
            "trustee_sale_date": "",
            "owner_name": "",
            "property_address": "",
            "owner_mailing1": "",
            "owner_mailing2": "",
            "status": "",
            "returned_mail": []
        }
        aaa['docnum'] = docnum
        eee = obDb.getDataSingleDoc(docnum)
        for e in eee:
            if e['field_name'] == "trustee_sale_date": aaa['trustee_sale_date'] = e['data']
            if e['field_name'] == "owner_name": aaa['owner_name'] = e['data']
            if e['field_name'] == "property_address": aaa['property_address'] = e['data']
            if e['field_name'] == "owner_mailing1": aaa['owner_mailing1'] = e['data']
            if e['field_name'] == "owner_mailing2": aaa['owner_mailing2'] = e['data']
            if e['field_name'] == "status": aaa['status'] = e['data']
            if e['field_name'] == "returned_mail": aaa['returned_mail'].append(e['data'])
        fff.append(aaa)
        for i,f in enumerate(fff):
            if f['status'] != "complete": fff.pop(i)
        return fff