import boto3
import json
import os
from datetime import datetime

# Ask user for access key, secret key and region
accessKey = input("Enter your access key: ")
secretKey = input("Enter your secret key: ")
region = input("Enter your region: ")
tag = input("Enter the tag for this access key: ")

# Connect to s3 using provided credentials
try:
    s3 = boto3.client('s3', aws_access_key_id=accessKey,
                      aws_secret_access_key=secretKey,
                      region_name=region)
    print("Connection Successful!")
except:
    print("Connection Failed!")
    exit()

# Create credentials json
def save_credentials():
    credentials = {
        'accessKey': accessKey,
        'secretKey': secretKey,
        'region': region,
        'tag': tag,
        'timestamp': datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    }

    # Authenticate credentials using boto3
    try:
        s3 = boto3.client('s3', aws_access_key_id=accessKey,
                          aws_secret_access_key=secretKey,
                          region_name=region)
        print("Credentials authenticated!")
    except:
        print("Credentials authentication failed!")
        exit()

    # Open credentials.json and check for duplicate access keys
    with open('credentials.json', 'r+') as outfile:
        # Check if file is empty
        if os.stat("credentials.json").st_size == 0:
            # Create JSON data if file is empty
            data = [{
                'accessKey': accessKey,
                'secretKey': secretKey,
                'region': region,
                'tag': tag,
                'timestamp': datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            }]
            json.dump(data, outfile)
        else:
            # Load JSON data if file is not empty
            data = json.load(outfile)
            # Append credentials to json and save
            data.append({
                'accessKey': accessKey,
                'secretKey': secretKey,
                'region': region,
                'tag': tag,
                'timestamp': datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            })
            outfile.seek(0)
            outfile.write(json.dumps(data, indent=4))
            outfile.truncate()

# Call save_credentials function to save credentials
save_credentials()

# Output success message
print("AWS credentials successfully saved to credentials.json")