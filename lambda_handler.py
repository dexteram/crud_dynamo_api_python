#import libraries
import boto3
import json
from requests import request
from custom_encoder import CustomEncoder
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#CONSTANTS1
dynamodbTableName = 'BOOKS'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

#CONSTANTS2
getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
healthPath = '/health'
bookPath = '/book'
bookPath = '/books/{id}'

# Lambda handler main function
def lambda_handler(event, context):
    logger.info(event)
    
    path = event['path']
    httpMethod = event['httpMethod']
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == bookPath:
        response = getBook(event['queryStringParameters']['id'])
    elif httpMethod == getMethod and path == bookPath:
        response = getBooks()
    elif httpMethod == postMethod and path == bookPath:
        response = postBook(json.loads(event['body']))
    elif httpMethod == patchMethod and path == bookPath:
        requestBody = json.loads(event['body'])
        response = patchBook(requestBody['id'],requestBody['updateKey'] ,requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == bookPath:
        requestBody = json.loads(event['body'])
        response = deleteBook(requestBody['id'])
    else:
        response = buildResponse(404, 'Not Found')
    return response


#GET ITEM
def getBook(id):
    try:
        response = table.get_item(
            Key={
                'id': id
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'message':'Id Not Found' % id})
    except:
        logger.exception('An error has occurred, the book you are entering could have been create¡¡¡')


#GET ALL ITEMS
def getBooks(id):
    try:
        response = table.scan()
        result = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])
            body = {
                'book': result
            }
            return buildResponse(200, body)
    except:
       logger.exception('an error has been presented, the book you are consulting was not found¡¡¡')


#SAVE ITEM
def postBook(requestBody):
    try:
        table.put_item(
            Item=requestBody
        )
        body = {
            'Operation': 'SAVE',
            'Message': 'The book has been saved successfully',
            'Item': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('An error has occurred, an error has occurred, the book could not be saved¡¡¡')


#UPDATE ITEM
def patchBook(id, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                'id': id
            },
            UpdateExpression="set %s = :value" % updateKey,
            ExpressionAttributeNames={
                ':value': updateKey
            },
            ExpressionAttributeValues={
                ':val': updateValue
            },
            ReturnValues="UPDATED_NEW"
        )
        body = {
            'Operation': 'UPDATE_NEW',
            'Message': 'The book has been updated successfully',
            'UpdatesAttrbutes': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('An error has occurred, the book you are updating could not be updated¡¡¡')


#DELETE ITEM
def deleteBook(id):
    try:
        response = table.delete_item(
            Key={
                'id': id
            },
            ReturnValues="ALL_OLD"
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'The book has been deleted successfully',
            'DeletedItem': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('An error has occurred, the book you are deleting could not be deleted¡¡¡')


#BUILD RESPONSE
def buildResponse(statusCode, body=None):
    responses = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        responses['body'] = json.dumps(body, cls=CustomEncoder)
    return responses