# AWS Step Functions with Lambda

A serverless workflow for tracking game level completions using AWS Step Functions and Lambda.

## Architecture

```
                    ┌─────────────────────────────┐
                    │    ProcessLevelCompletion   │
                    │        (Parallel State)     │
                    └─────────────┬───────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                                       │
              ▼                                       ▼
    ┌─────────────────┐                    ┌─────────────────┐
    │ GenerateReport  │                    │  CheckLevelType │
    │   (Lambda)      │                    │    (Choice)     │
    └─────────────────┘                    └────────┬────────┘
              │                                     │
              │                     ┌───────────────┴───────────────┐
              │                     │                               │
              │                     ▼                               ▼
              │           ┌─────────────────┐             ┌─────────────────┐
              │           │ HandleLastLevel │             │HandleSimpleLevel│
              │           │   (Lambda)      │             │   (Lambda)      │
              │           └─────────────────┘             └─────────────────┘
              │                     │                               │
              └─────────────────────┼───────────────────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │  PublishMetrics │
                          │    (Lambda)     │
                          └─────────────────┘
```

## Lambda Functions

| Function | Description |
|----------|-------------|
| `generate_report` | Generates a level completion report and uploads to S3 |
| `ends_last_level` | Records game completion in DynamoDB when user finishes the final level |
| `ends_simple_level` | Updates level progress in DynamoDB for non-final levels |
| `put_metric` | Publishes game metrics (time played) to CloudWatch |

## AWS Resources Required

- **DynamoDB Tables**:
  - `CompletedGame` - Stores completed game records
  - `CompletedLevel` - Stores level progress
- **S3 Bucket**: For storing generated reports
- **CloudWatch**: For game metrics

## Deployment

1. Replace `ACCOUNT_ID` in `step_function.json` with your AWS account ID
2. Set the `REPORT_BUCKET` environment variable for the `generate_report` Lambda
3. Deploy each Lambda function from its respective folder
4. Create the Step Function using the `step_function.json` definition

## Test Event

```json
{
    "user_id": "12345678901234567890",
    "level": "latest",
    "score": 10,
    "max_score": 100,
    "time_played": 9885983982,
    "total_score": 10000
}
```

## Workflow Behavior

- When `level` is `"latest"`: Uses `ends_last_level` to mark the game as completed
- For any other level: Uses `ends_simple_level` to update progress
- Both paths run in parallel with report generation
- Metrics are published after all parallel branches complete