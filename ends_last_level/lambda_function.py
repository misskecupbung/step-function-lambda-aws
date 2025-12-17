"""Lambda function to record game completion when user finishes the last level."""

import logging
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TABLE_NAME = "CompletedGame"
dynamodb_client = boto3.client("dynamodb")


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Record game completion in DynamoDB.

    Args:
        event: Input event containing user_id and total_score.
        context: Lambda context object.

    Returns:
        The original event for downstream processing.

    Raises:
        ValueError: If required fields are missing.
        ClientError: If DynamoDB operation fails.
    """
    logger.info("Processing game completion event: %s", event)

    user_id = event.get("user_id")
    total_score = event.get("total_score")

    if not user_id:
        raise ValueError("user_id is required")
    if total_score is None:
        raise ValueError("total_score is required")

    try:
        dynamodb_client.put_item(
            TableName=TABLE_NAME,
            Item={
                "user_id": {"S": user_id},
                "completed": {"BOOL": True},
                "timestamp": {"S": str(time.time())},
                "total_score": {"N": str(total_score)},
            },
        )
        logger.info("Successfully recorded game completion for user: %s", user_id)
    except ClientError as e:
        logger.error("Failed to record game completion: %s", e)
        raise

    return event
