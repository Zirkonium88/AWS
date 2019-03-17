import json
import botocore
import boto3
import os
from contextlib import closing

def lambda_handler(event, context):
    
    # Initialise AWS services
    rekognition_client = boto3.client('rekognition')
    s3_client = boto3.client('s3')
    polly_client = boto3.client('polly')
    
    # Get the uploaded file
    key_sourceFile = 'CompareFaces/source.jpg' # This picture needs to show at least one face. Otherwise, an InvalidParameterException error is shown.
    key_targetFile = 'CompareFaces/target.jpg'
    BUCKET_NAME = 'SAMPLE_BUCKET'
    
    response = rekognition_client.compare_faces(
                                    SimilarityThreshold=80,
                                    SourceImage={
                                        'S3Object': {
                                            'Bucket': BUCKET_NAME,
                                            'Name': key_sourceFile,
                                        },
                                    },
                                    TargetImage={
                                        'S3Object': {
                                            'Bucket': BUCKET_NAME,
                                            'Name': key_targetFile,
                                        },
                                    },
                                )
    faceMatch = response['FaceMatches']

    # Are there matches?
    if len(str(faceMatch)) < 10:       
        string = 'Hello, we have never met before. Who are you? If you would like to use this accommodation, please register at example.com and with the help of our fantastic app. See you later.'
        matches = "No matching faces"
        sim = 0
    else:
        sim = response['FaceMatches'][0]['Similarity']
        if sim > 70:
            string = 'Hello YOUR_NAME_HERE, good to see you again! Welcome to your reservated accomodation! Please Step in and enjoy the beauty of this flat!'
            matches = "I found matching faces"
        else:
            string = 'Hello, we have never met before. Who are you? If you would like to use this accommodation, please register at example.com and with the help of our fantastic app. See you later.'
            matches = "No matching faces"
    
    # Save the audio stream returned by Amazon Polly on Lambda's temp
    # directory. If there are multiple text blocks, the audio stream
    # will be combined into a single file. 
    textBlocks = []
    while (len(string) > 1100):
        begin = 0
        end = string.find(".", 1000)
        if (end == -1):
            end = string.find(" ", 1000)
            textBlock = string[begin:end]
            string = string[end:]
            textBlocks.append(textBlock)
    textBlocks.append(string)

    for textBlock in textBlocks:
            response = polly_client.synthesize_speech(
                OutputFormat='mp3',
                Text=textBlock,
                VoiceId='Joanna')
    
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    output = os.path.join("/tmp/response")

                    with open(output, "wb") as file:
                        file.write(stream.read())
    
    # Upload the mp3 file
    s3_client.upload_file('/tmp/response',BUCKET_NAME,'CompareFaces/response.mp3')
    
    # Save response
    response = {
        "matches": matches,
        "faceMatch": json.dumps(sim),
        "string": json.dumps(string)
    }
    
    # Return response
    return response

