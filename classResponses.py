import os
from os import path
import glob
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter, PageMerge, pdfwriter
from dbStuff import classDbStuff

class classResponses(object):

    def getDataForView(self,workingUser,tsd,filter):
        obDb = classDbStuff()
        ddd = obDb.getListForView(workingUser,filter)
        if len(ddd) == 0: return None
        fff = []
        for d in ddd:
            aaa = {
                "trustee_sale_date": "",
                "owner_name": "",
                "property_address": "",
                "owner_mailing1": "",
                "owner_mailing2": "",
                "status": "",
                "return_mail": {"owner_mailing1": [],
                                "owner_mailing2": []
                                }
            }
            aaa['docnum'] = d[0]
            eee = obDb.getDataSingleDoc(d[0])
            for e in eee:
                if e['field_name'] == "trustee_sale_date": aaa['trustee_sale_date'] = e['data']
                if e['field_name'] == "owner_name": aaa['owner_name'] = e['data']
                if e['field_name'] == "property_address": aaa['property_address'] = e['data']
                if e['field_name'] == "owner_mailing1": aaa['owner_mailing1'] = e['data']
                if e['field_name'] == "owner_mailing2": aaa['owner_mailing2'] = e['data']
                if e['field_name'] == "status": aaa['status'] = e['data']
                if e['field_name'] == "return_mail" and e['data'] == "owner_mailing1":
                    aaa['return_mail']['owner_mailing1'].append(e['updated'])
            fff.append(aaa)
            for i,f in enumerate(fff):
                if f['trustee_sale_date'] != tsd and tsd != "all": fff.pop(i)
                if f['status'] != "complete": fff.pop(i)
        return fff

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
            "return_mail": {"owner_mailing1": [],
                            "owner_mailing2": []
                            }
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
            if e['field_name'] == "return_mail" and e['data'] == "owner_mailing1":
                aaa['return_mail']['owner_mailing1'].append(e['updated'])
        fff.append(aaa)
        for i,f in enumerate(fff):
            if f['status'] != "complete": fff.pop(i)
        return fff