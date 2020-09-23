import boto3 
import botocore

#Checks if a bucket has any public permissions
def bucket_public(bucket_name):
    try:
        blocks = s3_client.get_public_access_block(Bucket=bucket_name)['PublicAccessBlockConfiguration']
    except botocore.exceptions.ClientError:
        return True
    blockPublicAcls = blocks['BlockPublicAcls']
    ignorePublicAcls = blocks['IgnorePublicAcls']
    blockPublicPolicy = blocks['BlockPublicPolicy']
    restrictPublicBuckets = blocks['RestrictPublicBuckets']
    return not (blockPublicAcls and ignorePublicAcls and blockPublicPolicy and restrictPublicBuckets)


#Blocks public access to s3 bucket
def remove_public_access(bucket_name):
    s3_client.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    })


s3_client = boto3.client('s3')
buckets = s3_client.list_buckets()['Buckets']
for bucket in buckets:
    if bucket_public(bucket['Name']):
        print("Bucket '", bucket['Name'], "' allows public access")
        remove_public_access(bucket['Name'])