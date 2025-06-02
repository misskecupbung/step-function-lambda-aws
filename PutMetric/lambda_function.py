import boto3
import json
cw_client = boto3.client("cloudwatch")
metric_name = "CompleteLevel"
def lambda_handler(event, context):
    source_event = {}
    if len(event) > 0:
        source_event = event[0]
    time_played = source_event.get("time_played", False)
    cw_client.put_metric_data(
        Namespace="FLOW",
        MetricData=[
            {"MetricName": metric_name, "Value": time_played, "Unit": "Seconds"}
        ],
    )
    return True
