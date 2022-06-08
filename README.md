# crud_dynamo_api_python

1) just donwload the lambda_function.py in your file in lambda function, then do the deploy
2) create one on one the event to test all the events

previously you must have created the database, the security role, create the api gateway

this is the events for test in lambda function

{
  "HttpMethod": "DELETE",
  "id": "101"
}


{
  "HttpMethod": "GET",
  "id": "102",
  "title": "",
  "author": "",
  "editorial": ""
}


{
  "HttpMethod": "POST",
  "id": "102",
  "title": "Book of the life",
  "author": "Dita Dago",
  "editorial": "Marketing Blocks"
}


{
  "HttpMethod": "PUT",
  "id": "888",
  "title": "Viaje al centro de la tierra",
  "author": "Julio Verne",
  "editorial": "Basr-slow-PR"
}
