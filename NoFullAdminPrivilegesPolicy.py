import boto3


#Checks for policy compliance. 
def check_policy(plcy, client):
    #get the Arn and default version number for policy
    arn = plcy["Arn"]
    vid = plcy["DefaultVersionId"]
    #get policy action, resource, and effect permissions
    full_policy = client.get_policy_version(PolicyArn=arn, VersionId=vid)
    permissions = full_policy['PolicyVersion']['Document']['Statement'][0]
    #checks if the permissions do not give full admin access
    action_permission = permissions['Action'].split(':')[1]
    not_compliant = permissions['Effect'] == 'Allow' and action_permission == '*' and permissions['Resource'] == '*' 
    return not_compliant


#Deletes all non-compliant policies.
def delete_policy(plcy, client):
    client.delete_policy(PolicyArn=plcy["Arn"])


#Returns a list of non-compliant policies.
def check_policies(policies, client):
    for policy in policies:
        if check_policy(policy, client):
            print(policy["Arn"])
            #delete_policy(policy["Arn"], client)


#Starting sequence
def start():
    iam = boto3.client('iam')
    policy_list = iam.list_policies(Scope='Local')['Policies']
    print("Policy Arns which have full admin privileges and are not compliant:")
    check_policies(policy_list, iam)


if __name__ == "__main__":
    start()