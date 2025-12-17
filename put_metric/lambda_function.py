"""Lambda function to publish game metrics to CloudWatch."""

import logging
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

METRIC_NAME = "CompleteLevel"
NAMESPACE = "GameMetrics"
cw_client = boto3.client("cloudwatch")


def lambda_handler(event: list[dict[str, Any]], context: Any) -> dict[str, Any]:
    """Publish time_played metric to CloudWatch.

    This function receives output from parallel Step Function branches.

    Args:
        event: List of results from parallel branches.
        context: Lambda context object.

    Returns:
        Success status and metric details.

    Raises:
        ClientError: If CloudWatch operation fails.
    """
    logger.info("Processing metrics for event: %s", event)

    source_event = event[0] if event else {}
    time_played = source_event.get("time_played", 0)

    if not isinstance(time_played, (int, float)):
        logger.warning("Invalid time_played value: %s, defaulting to 0", time_played)
        time_played = 0

    try:
        cw_client.put_metric_data(
            Namespace=NAMESPACE,
            MetricData=[
                {
                    "MetricName": METRIC_NAME,
                    "Value": time_played,
                    "Unit": "Seconds",
                }
            ],
        )
        logger.info("Successfully published metric: %s = %s seconds", METRIC_NAME, time_played)
    except ClientError as e:
        logger.error("Failed to publish metric: %s", e)
        raise

    return {"success": True, "metric": METRIC_NAME, "value": time_played}
