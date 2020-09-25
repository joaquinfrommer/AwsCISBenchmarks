import boto3

SSHPORT = 22
vpc = boto3.client('ec2')
vpc_resource = boto3.resource('ec2')


#Deletes the non-compliant rule in security group. 
def delete_rule(secgroup, group_name, ip_permissions):
    secgroup.revoke_ingress(GroupName=group_name, IpPermissions=[ip_permissions])

#Gets the ingress ip ranges. Returns 'none' if no range is found.
def get_ip_range(rule):
    ip_ranges = rule['IpRanges']
    if len(ip_ranges):
        return ip_ranges[0]['CidrIp']
    return "none" 


#Gets the start port number of the port range.
def get_from_port(rule):
    if 'FromPort' in rule:
        return rule['FromPort'] 
    return 1


#Gets the end port number of the port range.
def get_to_port(rule):
    if 'ToPort' in rule:
        return rule['ToPort'] 
    return 65535


#Checks to see if the security rule allows ingress from listed ports. 
def check_ports_open(from_port, to_port):
    if from_port <= SSHPORT and to_port >= SSHPORT:
        return True
    return False


#Checks the rule permisssions to see if the group is compliant. 
def check_inbound_permissions(rule):
    protocals = ["-1", "udp", "tcp"]
    ip_range = get_ip_range(rule)
    from_port = get_from_port(rule)
    to_port = get_to_port(rule)
    protocal = rule['IpProtocol']
    non_compliant = check_ports_open(from_port, to_port) and ip_range == '0.0.0.0/0' and protocal in protocals
    return non_compliant


#Checks to see if all rules in a group are compliant
def check_group_rules(secgroup, group_name, rules):
    non_compliant = False
    for rule in rules: 
        if check_inbound_permissions(rule):
            delete_rule(secgroup, group_name, rule)
            non_compliant = True
    return non_compliant


#Checks groups to see if they allow SSH from anywhere. Prints non-compliant group names and deletes them.
def check_groups(groups):
    for group in groups:
        security_group = vpc_resource.SecurityGroup(group['GroupId'])
        if check_group_rules(security_group, group['GroupName'], group['IpPermissions']):
            print(group['GroupName'])


#Starting sequence
def start():
    security_groups_description = vpc.describe_security_groups()
    security_groups = security_groups_description['SecurityGroups']
    print("Non-compliant security groups with ports exposed:")
    check_groups(security_groups)


if __name__ == "__main__":
    start()