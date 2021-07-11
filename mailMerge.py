import os
from os import path
import glob
from fpdf import FPDF
from pdfrw import PdfReader, PdfWriter, PageMerge, pdfwriter
from dbStuff import classDbStuff

class mailMerge(object):

    def getDataForMerge(self,workingUser,tsd):
        obDb = classDbStuff()
        ddd = obDb.getListCompleteDocuments(workingUser)
        if ddd == None: return None
        fff = []
        for d in ddd:
            aaa = {}
            aaa['docnum'] = d[0]
            eee = obDb.getDataSingleDoc(d[0])
            for e in eee:
                if e['field_name'] == "trustee_sale_date": aaa['trustee_sale_date'] = e['data']
                if e['field_name'] == "owner_name": aaa['owner_name'] = e['data']
                if e['field_name'] == "property_address": aaa['property_address'] = e['data']
                if e['field_name'] == "owner_mailing1": aaa['owner_mailing1'] = e['data']
                if e['field_name'] == "owner_mailing2": aaa['owner_mailing2'] = e['data']
            fff.append(aaa)
            if tsd != "all":
                for i,f in enumerate(fff):
                    if f['trustee_sale_date'] != tsd:
                        fff.pop(i)
        return fff

    def mailMerge(self,ckl,listToMail):
        ml = ""
        self.deleteOldLetters()
        for i,j in enumerate(listToMail):
            dfl = self.getDataForLetter(j,ckl)
            ml = ml + str(i+1) + " of " + str(len(listToMail)) + ": " + dfl['ooo'] + "\n        " + dfl['mmm'].replace("\n","\n        ") + "\n\n"
            self.generateLetter(dfl)
            self.combinePDF(dfl['lfn'],dfl['docnum'])
        self.generateMailingList(ml)
        self.combineAllPDFs()

    def deleteOldLetters(self):
        fff = glob.glob("static/pdf_output/*")
        for f in fff:
            os.remove(f)

    def getDataForLetter(self,i,ckl):
        docnum = i.split("_m")[0]
        mailing = i.split("_m")[1]
        lfn = "letter_" + i + ".pdf"
        obDb = classDbStuff()
        ddd = obDb.getDataSingleDoc(docnum)
        docData = {}
        for d in ddd:
            docData[d['field_name']] = d['data']
        ooo = docData['owner_name']
        mmm = docData["owner_mailing" + mailing]
        ppp = "Re. " + docData['property_address']
        ggg = docData['greeting']
        if mmm == docData['property_address']: ppp = ""
        ppp = ppp.split("\r\n")[0]
        ttt = self.getTextForLetter(ooo,mmm,ppp,ggg,ckl)
        dfl = {
            'docnum': docnum,
            'mailing': mailing,
            'ooo': ooo,
            'mmm': mmm,
            'ppp': ppp,
            'ggg': ggg,
            'ttt': ttt,
            'lfn': lfn
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

    def generateLetter(self,dfl):
        pdf = FPDF(orientation="P", unit="mm", format="letter")
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        pdf.set_y(25)
        pdf.set_top_margin(25)
        pdf.set_left_margin(25)
        pdf.multi_cell(160, 5, txt=dfl['ttt'],  border=0, ln=1, align="L")
        pdf.output("static/pdf_output/" + dfl['lfn'])

    def combinePDF(self,lfn,docnum):
        wr = PdfWriter()
        rd1 = PdfReader("static/pdf_output/" + lfn)
        rd2 = PdfReader("static/documents/doc" + str(docnum) + ".pdf")
        rd2pages = self.get4(docnum,rd2.pages)
        wr.addpages(rd1.pages)
        wr.addpage(rd2pages)
        wr.write("static/pdf_output/" + lfn)

    def generateMailingList(self,ml):
        pdf = FPDF(orientation="P", unit="mm", format="letter")
        pdf.add_page()
        pdf.set_font("Courier", size=12)
        pdf.set_y(25)
        pdf.set_top_margin(25)
        pdf.set_left_margin(25)
        pdf.multi_cell(160, 5, txt=ml,  border=0, ln=1, align="L")
        pdf.output("static/pdf_output/000_ml.pdf")

    def combineAllPDFs(self):
        wrc = PdfWriter()
        fff = sorted(glob.glob("static/pdf_output/*"))
        for f in fff:
            wrc.addpages(PdfReader(f).pages)
        wrc.write("static/pdf_output/combined.pdf")

    def get4(self,docnum,srcpages):
        wr = PdfWriter()
        scale = 0.5
        srcpages = PageMerge() + srcpages
        x_increment, y_increment = (scale * i for i in srcpages.xobj_box[2:])
        for i, page in enumerate(srcpages):
            page.scale(scale)
            page.x = x_increment if i & 1 else 0
            page.y = 0 if i & 2 else y_increment
        srcpages = srcpages.render()
        return srcpages
    
