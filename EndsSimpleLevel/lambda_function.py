import time
import boto3
dynamodb_client = boto3.client("dynamodb")
table_name = "CompletedLevel"
def lambda_handler(event, context):
    user_id = event.get("user_id")
    level = event.get("level")
    update_params = {
        "TableName": table_name,
        "Key": {"user_id": {"S": user_id}},
        "AttributeUpdates": {
            "last_level": {"Value": {"S": level}, "Action": "PUT"},
            "timestamp": {"Value": {"S": str(time.time())}, "Action": "PUT"},
        },
    }
    dynamodb_client.update_item(**update_params)
    return event
