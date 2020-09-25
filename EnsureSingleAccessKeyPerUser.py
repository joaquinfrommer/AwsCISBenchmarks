import boto3


#Compares times last used. Returns True if time0 was last used. Returns True if dates are equal.
def compare_times(time0, time1):
    if time0 == time1: 
        return True
    if time0 == 0:
        return False
    if time1 == 0:
        return True
    for z, o in time0, time1:
        if z > o:
            return True
        if z < o:
            return False
    return True #Here as a default case, code should never reach this point


#Disables the access key not used most recently.
def disable_key(keys, username, client):
    #Covers null last used date
    if 'LastUsedDate' in client.get_access_key_last_used(AccessKeyId=keys[0]['AccessKeyId'])['AccessKeyLastUsed']:
        time0 = client.get_access_key_last_used(AccessKeyId=keys[0]['AccessKeyId'])['AccessKeyLastUsed']['LastUsedDate']
    else:
        time0 = 0
    if 'LastUsedDate' in client.get_access_key_last_used(AccessKeyId=keys[1]['AccessKeyId'])['AccessKeyLastUsed']:
        time1 = client.get_access_key_last_used(AccessKeyId=keys[1]['AccessKeyId'])['AccessKeyLastUsed']['LastUsedDate']
    else:
        time1 = 0
    #Compares last used dates and disables keys
    if compare_times(time0, time1):
        client.update_access_key(AccessKeyId=keys[1]['AccessKeyId'], UserName=username, Status='Inactive')
    else:
        client.update_access_key(AccessKeyId=keys[0]['AccessKeyId'], UserName=username, Status='Inactive')


#Determines if multiple access keys are active for a single user
def multiple_active_keys(user_keys, name, client):
    if len(user_keys) < 2:
        return False
    count = 0
    for key in user_keys:
        if key['Status'] == 'Active':
            count += 1
    if count > 1:
        print("User '" + name + "' has", count, "access keys active")
        return True
    return False


#Starting sequence
def start():
    iam = boto3.client('iam')
    users = iam.list_users()['Users']

    for user in users:
        user_keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
        if multiple_active_keys(user_keys, user["UserName"], iam):
            disable_key(user_keys, user["UserName"], iam)


if __name__ == "__main__":
    start()