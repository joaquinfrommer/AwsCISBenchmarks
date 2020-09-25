import boto3 
import botocore

#Checks if a bucket has any public permissions
def bucket_public(bucket_name, client):
    try:
        blocks = client.get_public_access_block(Bucket=bucket_name)['PublicAccessBlockConfiguration']
    except botocore.exceptions.ClientError:
        return True
    blockPublicAcls = blocks['BlockPublicAcls']
    ignorePublicAcls = blocks['IgnorePublicAcls']
    blockPublicPolicy = blocks['BlockPublicPolicy']
    restrictPublicBuckets = blocks['RestrictPublicBuckets']
    return not (blockPublicAcls and ignorePublicAcls and blockPublicPolicy and restrictPublicBuckets)


#Blocks public access to s3 bucket
def remove_public_access(bucket_name, client):
    client.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    })


#Starting sequence
def start():
    s3_client = boto3.client('s3')
    buckets = s3_client.list_buckets()['Buckets']
    for bucket in buckets:
        if bucket_public(bucket['Name'], s3_client):
            print("Bucket '", bucket['Name'], "' allows public access")
            remove_public_access(bucket['Name'], s3_client)


if __name__ == "__main__":
    start()