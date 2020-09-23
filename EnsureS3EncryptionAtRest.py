import boto3
import botocore


#Determines if the bucket is encrypted by default
def needs_encryption(bucket_name):
    try:
        s3_client.get_bucket_encryption(Bucket=bucket_name)
        return False
    except botocore.exceptions.ClientError:
        return True


#Adds default encryption at rest to bucket
def encrypt_bucket(bucket_name):
    s3_client.put_bucket_encryption(
    Bucket=bucket_name,
    ServerSideEncryptionConfiguration={
        'Rules': [
            {
                'ApplyServerSideEncryptionByDefault': {
                    'SSEAlgorithm': 'AES256'
                }
            }
        ]
    }
)


s3_client = boto3.client('s3')
buckets = s3_client.list_buckets()['Buckets']
for bucket in buckets:
    if needs_encryption(bucket['Name']):
        print("Bucket", bucket['Name'], ("not encrypted by default"))
        encrypt_bucket(bucket['Name'])