import boto3

kms = boto3.client('kms')
keyIds = [key['KeyId'] for key in kms.list_keys()['Keys']] #Gets key IDs
for key in keyIds:
    if not kms.get_key_rotation_status(KeyId=key)['KeyRotationEnabled']:
        print("Key with id '" + key + "' does not have rotaion enabled.")
        try:
            kms.enable_key_rotation(KeyId=key) #Enables rotation if not enabled already
            print("Rotation enabled for key: " + key)
        #Catches exceptions if the key can't be rotated
        except (kms.exceptions.KMSInvalidStateException, kms.exceptions.UnsupportedOperationException): 
            print("Key '" + key + "' can't be rotated")