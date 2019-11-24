import json
import boto3

def lambda_handler(event, context):

    # Define clients
    client_transcribe = boto3.client('transcribe')
    # client_s3 = boto3.client('s3')
    
    # Get the bucket name as object
    INCOME_BUCKET = event['Records'][0]['s3']['bucket']['name']

    # Get the name of the uploaded file
    FILE = event['Records'][0]['s3']['object']['key']

    # Define further variables
    REGION = "eu-west-1"
    OUTPUT_BUCKET = "trc-mw-transcribe-output"
    FILE_URI = str("https://s3-" + REGION + ".amazonaws.com/" + INCOME_BUCKET + "/" + FILE)
    JOB_NAME = "transcription_job_" + FILE
    LABELS = 123

    response = client_transcribe.start_transcription_job(
                                                            TranscriptionJobName = JOB_NAME,
                                                            LanguageCode = 'de-DE',
                                                            MediaFormat = 'mp3',
                                                            Media={
                                                                'MediaFileUri': FILE_URI
                                                            },
                                                            OutputBucketName= OUTPUT_BUCKET,
                                                            Settings={
                                                                        'ShowSpeakerLabels': True,
                                                                        'MaxSpeakerLabels': LABELS,
                                                                    }
                                                        )
    response = {
                'TranscriptionJobName': JOB_NAME,
                'URI': FILE_URI   
                }
    
    return response