import os
import sys
import requests
from os import path
import glob
import datetime
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter, PageMerge, pdfwriter
from dbStuff import classDbStuff

class classMailMerge(object):

    def getListForMerge(self,workingUser):
        obDb = classDbStuff()
        listCompleteDocs = obDb.getListCompleteDocuments(workingUser)
        if listCompleteDocs == None: return None
        return listCompleteDocs

    def getDataForMerge(self,listCompleteDocs,workingUser,filterTsd,filterCounties,filterEquity,filterReturnedMail,sortField):
        # tsd = trustee sale date. It's either all or the first tuesday of a particular month.
        obDb = classDbStuff()
        listDataForMerge = []
        # Convert the mysql results to the dictionary format we need
        for doc in listCompleteDocs:
            dictDataForLetter = {}
            dictDataForLetter['docnum'] = doc[0]
            dictDataForLetter['returned_mail'] = []
            listDataSingleDoc = obDb.getDataSingleDoc(doc[0])
            for i in listDataSingleDoc:
                dictDataForLetter['docnum'] = i['docnum']
                if i['field_name'] == "trustee_sale_date": dictDataForLetter['trustee_sale_date'] = i['data']
                if i['field_name'] == "county": dictDataForLetter['county'] = i['data']
                if i['field_name'] == "owner_name": dictDataForLetter['owner_name'] = i['data']
                if i['field_name'] == "property_address": dictDataForLetter['property_address'] = i['data']
                if i['field_name'] == "deed_of_trust_year": dictDataForLetter['deed_of_trust_year'] = i['data']
                if i['field_name'] == "original_loan_amount": dictDataForLetter['original_loan_amount'] = i['data']
                if i['field_name'] == "market_value": dictDataForLetter['market_value'] = i['data']
                if i['field_name'] == "owner_mailing1": dictDataForLetter['owner_mailing1'] = i['data']
                if i['field_name'] == "owner_mailing2": dictDataForLetter['owner_mailing2'] = i['data']
                if i['field_name'] == "returned_mail": dictDataForLetter['returned_mail'].append(i['data'])
                if i['field_name'] == "status": dictDataForLetter['status'] = i['data']
                if i['field_name'] == "status" and i['data'] == "complete": dictDataForLetter['updated'] = i['updated']
            dictDataForLetter['est_equity'] = self.computeEquity(dictDataForLetter['deed_of_trust_year'],dictDataForLetter['original_loan_amount'],dictDataForLetter['market_value'])
            listDataForMerge.append(dictDataForLetter)

        # Remove records that don't match the user selected sale date, counties, equity, or returned mail
        for i in range(len(listDataForMerge)-1,-1,-1):
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
                        listDataForMerge[i]['owner_mailing1'] = "unk"
                    if "owner_mailing2" in listDataForMerge[i]['returned_mail']:
                        listDataForMerge[i]['owner_mailing2'] = "unk"
        
        listDataForMerge = self.sortMergeData(listDataForMerge,sortField)
        
        return listDataForMerge

    def sortMergeData(self,listDataForMerge,sortField):
        swap = 1
        countLoops = 0
        countSwaps = 0
        while swap == 1:
            swap = 0
            for i,j in enumerate(listDataForMerge):
                if i == len(listDataForMerge) - 1: continue
                if sortField == "equity":
                    v1 = int(listDataForMerge[i]['est_equity'])
                    v2 = int(listDataForMerge[i+1]['est_equity'])
                elif sortField == "updated":
                    v1 = listDataForMerge[i]['updated']
                    v2 = listDataForMerge[i+1]['updated']
                if v2 > v1:
                    listDataForMerge[i], listDataForMerge[i+1] = listDataForMerge[i+1], listDataForMerge[i]
                    swap = 1
                    countSwaps = countSwaps + 1
            countLoops = countLoops + 1
        return listDataForMerge

    def computeEquity(self,dotYear,origLoan,mktValue):
        equity = 0
        years = 0
        if dotYear.isnumeric():
            years = datetime.date.today().year - int(dotYear)
        if origLoan.isnumeric() and mktValue.isnumeric():
            equity = int(mktValue) - (1-0.02*years)*int(origLoan)
            equity = str(round(equity))
        if int(equity) < 0: equity = 0
        return equity

    def mailMerge(self,ckl,listToMail):
        self.deleteOldLetters()
        # generate list
        ml = self.generateMailingList(listToMail,ckl)
        self.generateMailingListPDF(ml)
        # generate letters
        lenListToMail = len(listToMail)
        for i,j in enumerate(listToMail):
            dfl = self.getDataForLetter(i,j,len(listToMail),ckl)
            self.generateLetterPDF(dfl)
            self.combinePDF(dfl['lfn'],dfl['docnum'])
        self.combineAllPDFs()

    def generateMailingList(self,listToMail,ckl):
        ml = ""
        for i,j in enumerate(listToMail):
            dfl = self.getDataForLetter(i,j,len(listToMail),ckl)
            ml = ml + str(i+1) 
            ml = ml + " of " + str(len(listToMail)) + ": " 
            ml = ml + "Est. Equity: " + dfl['equity']
            ml = ml + "\n         "
            ml = ml + "DOT year: " + dfl['dotyr'] + ", Orig: " + dfl['orig'] + ", Value: " + dfl['value']
            ml = ml + "\n         "
            ml = ml + "Completed date: " + dfl['completed']
            ml = ml + "\n         "
            ml = ml + dfl['ooo'] 
            ml = ml + "\n         "
            ml = ml + dfl['mmm'].replace("\n","\n         ") 
            ml = ml + "\n\n"
        return ml

    def deleteOldLetters(self):
        fff = glob.glob("static/pdf_output/*")
        for f in fff:
            os.remove(f)

    def getDataForLetter(self,i,j,lenListToMail,ckl):
        # lfn = letter file name
        docnum = j.split("_m")[0]
        mailingAddrId = j.split("_m")[1]
        while len(str(i)) < len(str(lenListToMail)): i = str(0) + str(i)
        lfn = str(i) + "_letter_" + j + ".pdf"
        obDb = classDbStuff()
        listDataSingleDoc = obDb.getDataSingleDoc(docnum)
        docData = {}
        # for loop organizes the mysql results into an easy to use dictionary
        for d in listDataSingleDoc:
            docData[d['field_name']] = d['data']
            if d['field_name'] == "status": docData['completed'] = d['updated']
        # now make a new dict that formats the data to put into the letter
        if docData["owner_mailing" + mailingAddrId] == docData['property_address']: 
            regarding = ""
        else:
            regarding = "Re. " + docData['property_address']
            regarding = regarding.split("\n")[0]
        textOfLetter = self.getTextForLetter(docData['owner_name'],docData["owner_mailing" + mailingAddrId],regarding,docData['greeting'],ckl)
        dfl = {
            'docnum': docnum,
            'ooo': docData['owner_name'],
            'mmm': docData["owner_mailing" + mailingAddrId],
            'ppp': regarding,
            'ggg': docData['greeting'],
            'ttt': textOfLetter,
            'lfn': lfn,
            'completed': docData['completed'],
            'equity': str(self.computeEquity(docData['deed_of_trust_year'],docData['original_loan_amount'],docData['market_value'])),
            'dotyr': docData['deed_of_trust_year'],
            'orig': docData['original_loan_amount'],
            'value': docData['market_value']
        }
        return dfl

    def getTextForLetter(self,ooo,mmm,ppp,ggg,ckl):
        fff = open("static/letters/" + ckl[1] + ".txt","r")
        rrr = fff.read()
        rrr = rrr.replace("<owner_name>",ooo)
        rrr = rrr.replace("<owner_mailing>",mmm)
        rrr = rrr.replace("<property_address>",ppp)
        rrr = rrr.replace("<greeting>",ggg)
        return rrr

    def generateLetterPDF(self,dfl):
        pdf = FPDF(orientation="P", unit="mm", format="letter")
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.set_y(25)
        pdf.set_top_margin(25)
        pdf.set_left_margin(25)
        pdf.multi_cell(160, 5, txt=dfl['ttt'], border=0, align="L")
        # pdf.multi_cell(160, 5, txt=dfl['ttt'],  border=0, ln=1, align="L")
        pdf.output("static/pdf_output/" + dfl['lfn'])

    def combinePDF(self,lfn,docnum):
        wr = PdfWriter()
        letterPDF = PdfReader("static/pdf_output/" + lfn)
        documentPDF = PdfReader("static/documents/doc" + str(docnum) + ".pdf")
        docPDFpages = self.reformatDocumentPDF(docnum,documentPDF.pages)
        wr.addpages(letterPDF.pages)
        wr.addpage(docPDFpages)
        wr.write("static/pdf_output/" + lfn)

    def generateMailingListPDF(self,ml):
        pdf = FPDF(orientation="P", unit="mm", format="letter")
        pdf.add_page()
        pdf.set_font("Courier", size=12)
        pdf.set_y(25)
        pdf.set_top_margin(25)
        pdf.set_left_margin(25)
        pdf.multi_cell(160, 5, txt=ml,  border=0, align="L")
        # pdf.multi_cell(160, 5, txt=ml,  border=0, ln=1, align="L")
        pdf.output("static/pdf_output/000_ml.pdf")

    def combineAllPDFs(self):
        wrc = PdfWriter()
        fff = sorted(glob.glob("static/pdf_output/*"))
        for f in fff:
            wrc.addpages(PdfReader(f).pages)
        wrc.write("static/pdf_output/combined.pdf")

    def reformatDocumentPDF(self,docnum,sourcePages):
        countPages = len(sourcePages)
        if(countPages) == 2:
            sourcePages[0].Rotate = 90
            sourcePages[1].Rotate = 90
        sourcePages = PageMerge() + sourcePages
        # countPages = sum(1 for i in sourcePages)
        if countPages == 1:
            for i, page in enumerate(sourcePages):
                page.scale(792/page.h)
        elif countPages == 2:
            for i, page in reversed(list(enumerate(sourcePages))):
                scale = 6.5/8.5 * 792/page.w
                page.scale(scale)
                if i == 0:
                    page.x = 0
                    page.y = page.h
                if i == 1:
                    page.x = 0
                    page.y = 0
        elif countPages > 2:
            for i, page in reversed(list(enumerate(sourcePages))):
                scale = 0.5*792/page.h
                h1 = page.h * scale
                w1 = page.w * scale
                page.scale(scale)
                # page.x = x_increment if i & 1 else 0
                # page.y = 0 if i & 2 else y_increment
                if i == 0:
                    page.x = 0
                    page.y = h1
                if i == 1:
                    page.x = w1
                    page.y = h1
                if i == 2: 
                    page.x = 0
                    page.y = 0
                if i == 3: 
                    page.x = w1
                    page.y = 0
                if i>3:
                    sourcePages.pop(i)
        sourcePages = sourcePages.render()
        return sourcePages
    
