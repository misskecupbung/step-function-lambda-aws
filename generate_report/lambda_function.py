"""Lambda function to generate and store level completion reports in S3."""

import logging
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BUCKET_NAME = os.environ.get("REPORT_BUCKET", "BUCKET_NAME")
s3_client = boto3.client("s3")


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Generate and upload a level completion report to S3.

    Args:
        event: Input event containing level, user_id, score, and max_score.
        context: Lambda context object.

    Returns:
        The original event for downstream processing.

    Raises:
        ValueError: If required fields are missing.
        ClientError: If S3 operation fails.
    """
    logger.info("Generating report for event: %s", event)

    level = event.get("level")
    user_id = event.get("user_id")
    score = event.get("score")
    max_score = event.get("max_score")

    if not all([level, user_id, score is not None, max_score is not None]):
        raise ValueError("level, user_id, score, and max_score are required")

    report = f"""Level Completion Report
=======================
Level: {level}
Score: {score}/{max_score}
Percentage: {(score / max_score * 100):.1f}%
"""

    object_key = f"{user_id}_report_{level}.txt"

    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=object_key,
            Body=report,
            ContentType="text/plain",
        )
        logger.info("Successfully uploaded report to s3://%s/%s", BUCKET_NAME, object_key)
    except ClientError as e:
        logger.error("Failed to upload report: %s", e)
        raise

    return event
