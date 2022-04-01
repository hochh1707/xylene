from dbStuff import classDbStuff
from classS3stuff import classS3stuff
from classEnterStuff import classEnterStuff
from flask import Flask, render_template, request, session
import boto3

def newFiles(ckl):
    obEs = classEnterStuff()
    dbStuff = classDbStuff()
    obS3 = classS3stuff()
    newFiles = []
    message = ""
    # figure out the next document number to use
    ldn = dbStuff.getLastDocumentNumber()
    if ldn == None:
        return render_template('error.html',ckl=ckl)
    else:
        ndn = int(ldn) + 1
    # if user just uploaded new files, save them as doc100001.pdf, doc100002.pdf, etc.
    # then create new database records
    if request.method == "POST":
        fff = request.files.getlist("file")
        for f in fff:
            if f.filename == "": continue
            nf = "doc" + str(ndn) + ".pdf"
            f.save("static/documents/newfile.pdf")
            response = obS3.connect.Bucket('wuut').upload_file(Filename='static/documents/newfile.pdf',Key=nf,ExtraArgs={'ContentType': 'application/pdf'})
            newFiles.append(nf)
            dbStuff.createBlankDocumentRecord(ckl[1],ndn,obEs.dataFields())
            ndn = ndn + 1
    message = "There were " + str(len(newFiles)) + " new files imported"
    return render_template('new_files.html',message=message,newFiles=newFiles,ckl=ckl)
