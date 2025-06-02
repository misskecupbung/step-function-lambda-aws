import boto3
bucket_name = "BUCKET_NAME"
s3_client = boto3.client("s3")
def lambda_handler(event, context):
    level = event.get("level")
    user_id = event.get("user_id")
    score = event.get("score")
    max_score = event.get("max_score")
    report = "Completed Level: %s\nMy Score: %s\%s\n" % (level, score, max_score)
    s3_client.put_object(
        ACL="public-read",
        Bucket=bucket_name,
        Key="%s_report_%s.txt" % (user_id, level),
        Body=report,
    )
    return event
