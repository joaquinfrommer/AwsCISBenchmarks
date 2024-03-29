import boto3

PORTS = [22, 3389]


#Removes an entry for the acl
def remove_acl_rule(aclid, rulenum, client):
    client.delete_network_acl_entry(NetworkAclId=aclid, RuleNumber=rulenum, Egress=False)


#Checks to see if the security rule allows ingress from listed ports. 
def check_ports_open(from_port, to_port):
    for port in PORTS:
        if from_port <= port and to_port >= port:
            return True
    return False


#Checks the rule to ensure no ingress traffic is allowed to remote ports
def check_acl_rule(rule):
    protocals = ["-1", "udp", "tcp"]
    from_port = rule['PortRange']['From'] if 'PortRange' in rule else 0
    to_port = rule['PortRange']['To'] if 'PortRange' in rule else 65535
    ip_range = rule['CidrBlock']
    protocal = rule['Protocol']
    non_compliant = check_ports_open(from_port, to_port) and ip_range == '0.0.0.0/0' and protocal in protocals
    return non_compliant


def check_acl_rules(rules, acl_id, client):
    for entry in rules:
        if not entry['Egress'] and entry['RuleAction'] == 'allow':
            if check_acl_rule(entry):
                print("Acl", acl_id, "rule #" + str(entry['RuleNumber']), "is not compliant")
                remove_acl_rule(acl_id, entry['RuleNumber'], client)


#Starting sequence
def start():
    ec2_client = boto3.client('ec2')
    acls = ec2_client.describe_network_acls()['NetworkAcls']
    for acl in acls:
        check_acl_rules(acl['Entries'], acl['NetworkAclId'], ec2_client)


if __name__ == "__main__":
    start()