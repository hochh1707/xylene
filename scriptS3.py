import boto3

def s3():
    # s3_resource = boto3.resource('s3',
    #     aws_access_key_id='AKIA5FW42GJNL3SWB46P',
    #     aws_secret_access_key='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')
    #     response = s3_resource.Bucket('wuut').upload_file(Filename=f,Key=z,ExtraArgs={'ContentType': 'application/pdf'})

    # create bucket
    # s3_resource.create_bucket(Bucket='wuut',CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    # s3_resource.create_bucket(Bucket='documents',CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
    
    # upload to wuut
    # response = s3_resource.Bucket('wuut').upload_file(Filename='./static/documents/doc100091.pdf',Key='doc100091.pdf',ExtraArgs={'ContentType': 'application/pdf'})
    # response = s3_resource.Bucket('wuut').upload_file(Filename='./static/documents/doc100091.pdf',Key='doc100091.pdf')

    #upload all to documents
    # zzz = os.listdir('./static/documents/')
    # for z in zzz:
    #     f = "./static/documents/" + z
    #     response = s3_resource.Bucket('wuut').upload_file(Filename=f,Key=z,ExtraArgs={'ContentType': 'application/pdf'})
    
    # print all the file names in wuut
    for b in s3_resource.Bucket('wuut').objects.all():
        print(b.key)

    return "wuut"
