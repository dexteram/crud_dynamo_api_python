import json
import  boto3

#start the lambda function to query the request
def lambda_handler(event, context):
    #validates the type of method that enters through the event
    if ("POST" in event.values()):
        #delete the word request so that the event can be used by the function
        del event["HttpMethod"]
        #call the function
        create = create_book(event)
        #return the book created
        return create
        
        
    #validates the type of method that enters through the event    
    elif("GET" in event.values()):
        #delete the word request so that the event can be used by the function
        del event["HttpMethod"]
        #call the funcion
        get = get_book(event)
        #returns the queried id
        return get
        
    #validates the type of method that enters through the event   
    elif("GET_ALL" in event.values()):
        #delete the word request so that the event can be used by the function
        del event["HttpMethod"]
        #call the function
        get_all_books = get_books(event)
        #return all books are in table book in dynamodb
        return get_all_books
        
    #validates the type of method that enters through the event     
    elif("DELETE" in event.values()):
        #delete the word request so that the event can be used by the function
        del event["HttpMethod"]
        delete = delete_book(event)
        #return the book was deleted
        return  delete
        
    #validates the type of method that enters through the event       
    elif("PUT" in event.values()):
        #delete the word request so that the event can be used by the function
        del event["HttpMethod"]
        #call the function
        update = update_book(event)
        # return the value updated
        return update
    else:
        # return this message in case the json request is incorrect
        return "invalid Request"
    

#FUNCTION CREATE_BOOK
def create_book(event):
    """
    Create item from DynamoDB
    """
    try:
        #call the database
        dynamodb = boto3.resource('dynamodb')
        #calll the table created in dynamodb
        table = dynamodb.Table('BOOKS')
        #insert values in the table
        table.put_item(Item=event)
        #message when entering values in the table
        return {
            'statusCode': 200,
            'body': json.dumps(event)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }
        

#GET_BOOK
def get_book(event):
    """
    Get item from DynamoDB
    """
    try:
        #call the database
        dynamodb = boto3.resource('dynamodb')
        #calll the table created in dynamodb
        table = dynamodb.Table('BOOKS')
        #value searched in the table
        response = table.get_item(
            Key={
                'id': event['id']
                }
        )
        #return the value searched
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        #return error
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }
        
        
# #GET_ALL BOOKS
def get_books(event):
    """
    Get all item from DynamoDB
    """
    try:
        #call the database
        dynamodb = boto3.resource('dynamodb')
        #calll the table created in dynamodb
        table = dynamodb.Table('BOOKS')
        #query in table
        response = table.scan()
        #return all the values in the table
        return response
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }
            

#UPDATE_BOOK
def update_book(event):
    """
    Update item from DynamoDB
    """
    try:
        #call the database
        dynamodb = boto3.resource('dynamodb')
        #calll the table created in dynamodb
        table = dynamodb.Table('BOOKS')
        #values to update in the table
        table.update_item(
            Key={
                'id': event['id']
            },
            #values from the table books
            UpdateExpression="set #title = :title, #author = :author, #editorial = :editorial",
            ExpressionAttributeValues={
                ':title': event['title'],
                ':author': event['author'],
                ':editorial': event['editorial']
            },
            ExpressionAttributeNames={
                '#title': 'title',
                '#author': 'author',
                '#editorial': 'editorial'
            },
            ReturnValues="UPDATED_NEW"
        )
        return event
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }

#FUNCION DELETE BOOK
def delete_book(event):
    """
    Delete item from DynamoDB
    """
    try:
        #call the database
        dynamodb = boto3.resource('dynamodb')
        #calll the table created in dynamodb
        table = dynamodb.Table('BOOKS')
        #values to delete in table
        response = table.delete_item(
            Key={
                'id': event['id']
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(e)
        }
