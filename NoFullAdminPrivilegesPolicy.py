import boto3


#Checks for policy compliance. 
def check_policy(plcy):
    #get the Arn and default version number for policy
    arn = plcy["Arn"]
    vid = plcy["DefaultVersionId"]
    #get policy action, resource, and effect permissions
    full_policy = iam.get_policy_version(PolicyArn=arn, VersionId=vid)
    permissions = full_policy['PolicyVersion']['Document']['Statement'][0]
    #checks if the permissions do not give full admin access
    action_permission = permissions['Action'].split(':')[1]
    not_compliant = permissions['Effect'] == 'Allow' and action_permission == '*' and permissions['Resource'] == '*' 
    return not_compliant


#Deletes all non-compliant policies.
def delete_policy(plcy):
    iam.delete_policy(PolicyArn=plcy["Arn"])


#Returns a list of non-compliant policies.
def check_policies(policies):
    for policy in policies:
        if check_policy(policy):
            print(policy["Arn"])
            #delete_policy(policy["Arn"])


iam = boto3.client('iam')
policy_list = iam.list_policies(Scope='Local')['Policies']
print("Policy Arns which have full admin privileges and are not compliant:")
check_policies(policy_list)