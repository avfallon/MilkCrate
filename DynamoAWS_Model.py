import boto3

dynamodb = boto3.resource("dynamodb")

table = dynamodb.create_table(
    TableName="newTable",
    KeySchema=[{
        'AttributeName': 'username',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': "recipe_name"
    }

    ]
    KeyType=
)


