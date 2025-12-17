"""Lambda function to update level progress for non-final levels."""

import logging
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = "CompletedLevel"
dynamodb_client = boto3.client("dynamodb")


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Update level progress in DynamoDB.

    Args:
        event: Input event containing user_id and level.
        context: Lambda context object.

    Returns:
        The original event for downstream processing.

    Raises:
        ValueError: If required fields are missing.
        ClientError: If DynamoDB operation fails.
    """
    logger.info("Processing level completion event: %s", event)

    user_id = event.get("user_id")
    level = event.get("level")

    if not user_id:
        raise ValueError("user_id is required")
    if not level:
        raise ValueError("level is required")

    try:
        dynamodb_client.update_item(
            TableName=TABLE_NAME,
            Key={"user_id": {"S": user_id}},
            UpdateExpression="SET last_level = :level, #ts = :timestamp",
            ExpressionAttributeNames={"#ts": "timestamp"},
            ExpressionAttributeValues={
                ":level": {"S": level},
                ":timestamp": {"S": str(time.time())},
            },
        )
        logger.info("Successfully updated level progress for user: %s", user_id)
    except ClientError as e:
        logger.error("Failed to update level progress: %s", e)
        raise

    return event
