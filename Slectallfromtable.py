import boto3
import string
from boto3.dynamodb.conditions import Key, Attr

class NumberCleaner:
    # allow only digits, +, -
    def __init__(self, keep=string.digits+"+"+"-"):
        self.comp = dict((ord(c),c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)

def lambda_handler(event, context):
    phoneNumber = ""
    lastname ="unknown"
    firstname ="unknown"
    businessphone =""
    mobilephone =""
    email ="unknown"
    company ="unknown"
    department ="unknown"
    vipflag ="false"
   
    try:
        rawPhoneNumber = event["Details"]["ContactData"]["CustomerEndpoint"]["Address"]
        
        nc = NumberCleaner()
        phoneNumber = rawPhoneNumber.translate(nc)
    except KeyError as ke:
        print("Error: invalid event format (phonenumber missing)")
   
    print("Phone: ",phoneNumber)
    if phoneNumber != "":
 
        dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
        table = dynamodb.Table('connect-user-data')
 
        #try:
            # Mit GSI
            # response = table.query(IndexName='business-phone-index',KeyConditionExpression=Key('business-phone').eq(business-phone))
            
            # Ohne GSI
            response = table.query(KeyConditionExpression=Key('business-phone').eq(ENTERED_VALUE))

            lastname = "{}".format(response['Items'][0]['lastname'])
            firstname = "{}".format(response['Items'][0]['lastname'])
            businessphone = "{}".format(response['Items'][0]['business-phone'])
            mobilephone = "{}".format(response['Items'][0]['mobile-phone'])
            email = "{}".format(response['Items'][0]['email'])
            company = "{}".format(response['Items'][0]['company'])
            department = "{}".format(response['Items'][0]['department'])
            vipflag = "{}".format(response['Items'][0]['vip-flag'])
                    
            print("lookup phone number {}: {}".format(phoneNumber, lastname))
        #except Exception as e:
        #    print("Error looking up phone number {}".format(phoneNumber))
 
 
        resultMap = {"lastname": lastname, "firstname": firstname,"business-phone": businessphone,"mobile-phone": mobilephone,"email": email,"company": company,"department": department,"vip-flag": vipflag}
    return resultMap  