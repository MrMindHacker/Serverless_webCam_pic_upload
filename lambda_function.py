import json
import boto3
import base64
import email
import random
from datetime import datetime as dt

def lambda_handler(event, context):
    error = 0
    
    if event['httpMethod'] == 'PUT':
        try:
            AWS_BUCKET_NAME = 'compicbucket'
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(AWS_BUCKET_NAME)
            # bd =  email.message_from_bytes(event['body'])
            # msg = email.parser.BytesParser().parsebytes(bd)
            # bd = event['body']
            # body = base64.b64decode(event['body'])
            # body_dec = base64.b64decode(body['image'])
            # bd = body
            post_data = base64.b64decode(event['body'])
            headers, data = post_data.decode('utf-8').split('\r\n', 1)
            path = 'img_' + str(dt.now()) + str(random.randint(0,100))+ '.jpg'
            
            bucket.put_object(
            Key=path,
            Body=data,
            )
            # # print({
            #     part.get_param('name', header='content-disposition'): part.get_payload(decode=True)
            #     for part in msg.get_payload()
            # })
            # requests.
        except Exception as e:
            error = 'b: ' + str(e)
            
        if error == 0:
            body_r = json.dumps({
                'upload': 'successfull',
                "bucket": AWS_BUCKET_NAME,
                "path": 'https://compicbucket.s3.amazonaws.com/'+path,
                # "post_data": post_data
            })
        else:
            body_r = json.dumps(str(error))
    else:
        body_r = json.dumps("Server Responds To Only POST Method!")
    return {
        # # 'headers':json.dumps('Access-Control-Allow-Origin')
        'statusCode': 200,
        'body': body_r,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
            }
    }

