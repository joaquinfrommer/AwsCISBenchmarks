import boto3

vpc = boto3.client('ec2')
vpc_resource = boto3.resource('ec2')


#Deletes inbound and outbound rules for default security group
def delete_rules(description, secgroup):
    for rule in description["IpPermissions"]:
        secgroup.revoke_ingress(GroupName=description['GroupName'], IpPermissions=[rule])
    for rule in description['IpPermissionsEgress']:
        secgroup.revoke_egress(IpPermissions=[rule])
    print("Rules deleted!")


#Ensures default security groups restrcit all trafic. 
def check_default_rules(group_description, security_group):
    if len(group_description['IpPermissions']) == 0 and group_description['IpPermissionsEgress'] == 0:
        return
    print("Default security group with id '" + group_description['GroupId'] + "' does not restrict all traffic")
    #delete_rules(group_description, security_group)
    return 


#Checks groups for default groups and assesses their rules.
def check_groups(groups):
    for group in groups:
        if group['GroupName'] == "default":
            security_group = vpc_resource.SecurityGroup(group['GroupId'])
            check_default_rules(group, security_group)


security_groups_description = vpc.describe_security_groups()
security_groups = security_groups_description['SecurityGroups']
check_groups(security_groups)