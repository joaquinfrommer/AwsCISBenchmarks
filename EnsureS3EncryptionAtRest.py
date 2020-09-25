import boto3
import botocore


#Determines if the bucket is encrypted by default
def needs_encryption(bucket_name, client):
    try:
        client.get_bucket_encryption(Bucket=bucket_name)
        return False
    except botocore.exceptions.ClientError:
        return True


#Adds default encryption at rest to bucket
def encrypt_bucket(bucket_name, client):
    client.put_bucket_encryption(
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


#Starting sequence
def start():
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()['Buckets']
    for bucket in buckets:
        if needs_encryption(bucket['Name'], s3_client):
            print("Bucket", bucket['Name'], ("not encrypted by default"))
            encrypt_bucket(bucket['Name'], s3_client)


if __name__ == "__main__":
    start()