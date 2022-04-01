import boto3
import os

class classS3stuff(object):
    def __init__(self):
        self.connect = self.s3Connect()

    def s3Connect(self):
        s3_resource = boto3.resource('s3',
            aws_access_key_id='AKIA5FW42GJNL3SWB46P',
            aws_secret_access_key='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')
        return s3_resource
    
    def xferDocs(self,listToMail):
        for i in listToMail:
            if i[-2:] == "m1" and os.path.exists('./static/documents/doc' + i[0:6] + '.pdf') == False:
                try:
                    self.connect.Bucket('wuut').download_file(Filename='./static/documents/doc' + i[0:6] + '.pdf',Key='doc' + i[0:6] + '.pdf')
                except Exception as e:
                    print(e)
