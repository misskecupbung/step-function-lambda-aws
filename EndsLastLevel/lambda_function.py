import boto3
import time
table_name = "CompletedGame"
dynamodb_client = boto3.client("dynamodb")
def lambda_handler(event, context):
    user_id = event.get("user_id")
    total_score = event.get("total_score")
    put_params = {
        "TableName": table_name,
        "Item": {
            "user_id": {"S": user_id},
            "completed": {"BOOL": True},
            "timestamp": {"S": str(time.time())},
            "total_score": {"N": str(total_score)},
        },
    }
    dynamodb_client.put_item(**put_params)
    return event
