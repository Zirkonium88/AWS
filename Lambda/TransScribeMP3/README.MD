# Get text from speech

This [example](https://github.com/Zirkonium88/AWS/blob/master/Lambda/TransScribeMP3/handler.py) shows how to use Amazon Transscribe to retreive text from MP3-files. Be are of the following things. First, this is not a real- or near-real time process. Second, MP3-files can not be longer than 4 hours. Interestingly, 
`start_transcription_job()` does not need a s3-client-object. So, only `client_transcribe = boto3.client('transcribe')`
is needed.

```python
import json
import boto3

def lambda_handler(event, context):

    # Define clients
    client_transcribe = boto3.client('transcribe')

    # Get the bucket name as object
    INCOME_BUCKET = event['Records'][0]['s3']['bucket']['name']

    # Get the name of the uploaded file
    FILE = event['Records'][0]['s3']['object']['key']

    # Define further variables
    REGION = "eu-west-1"
    OUTPUT_BUCKET = "SAMPLE_OUTPUTBUCKET"
    FILE_URI = str("https://s3-" + REGION + ".amazonaws.com/" + INCOME_BUCKET + "/" + FILE)
    JOB_NAME = "transcription_job_" + FILE
    LABELS = 123

    response = client_transcribe.start_transcription_job(
                                                            TranscriptionJobName = JOB_NAME,
                                                            LanguageCode = 'de-DE', # Change the langugae accordingly
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
```
