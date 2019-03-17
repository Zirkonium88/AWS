import json

def lambda_handler(event, context):
    string = "Hello from Lambda!"
    congrats = "This is your serverless pushed AWS Lambda"
    execution = "AWS Lambda executed sucessfull"

    responses = {
        "Part 1": json.dumps(string),
        "Part 2": json.dumps(congrats),
        "Part 3": json.dumps(execution)
    }

    return responses
