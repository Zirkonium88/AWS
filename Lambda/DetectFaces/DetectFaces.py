# Load libraries
import boto3
import json
import os

BUCKET_NAME = 'SAMPLE_BUCKET'
KEY = 'source.jpg' # A picture to be analysed
FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox","Confidence")
REGION = 'eu-west-1'
attributes=['ALL']

def lambda_handler(event, context):
	
	# Initialise AWS services
	s3_client = boto3.client('s3')
	rekognition = boto3.client("rekognition")
	response = rekognition.detect_faces(
	    Image={
			"S3Object": {
				"Bucket": BUCKET_NAME,
				"Name": KEY,
			}
		},
	    Attributes=attributes,
	)
	# Store response
	gain = response['FaceDetails']
	print(response.get('AgeRange'))
	type(response)
	
	for face in gain:
		faces = "Face ({Confidence}%)".format(**face)
		# Get emotions
		emotions = []
		for emotion in face['Emotions']:
			emotions.append(''.join("  {Type} : ({Confidence}%)".format(**emotion)))
			# Get quality
			qualities = []
			for quality, value in face['Quality'].items():
				qualities.append(''.join("  {quality} : ({value})".format(quality=quality, value=value)))
			# Get facial features
			features = []
			for feature, data in face.items():
				if feature not in FEATURES_BLACKLIST:
					features.append(''.join("{feature} : {data}".format(feature=feature, data=data)))
	# Save results
	responses = {
        "face": json.dumps(faces),
        "emotions": json.dumps(emotions)
		}
	# Write a temporary file to Lambdas /tmp storage
	os.chdir('/tmp')
	with open('data.json', 'w') as fp:
		json.dump(responses, fp)
		
	# Upload data.json to s3
	s3_client.upload_file('/tmp/data.json',BUCKET_NAME,'DetectFaces/data.json')
	
	# Return results
	return responses

