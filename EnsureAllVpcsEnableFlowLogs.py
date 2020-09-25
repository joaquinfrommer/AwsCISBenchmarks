import boto3


#Creates a flow log for the vpc
def create_vpc_flow_logs(ids):
    print("Creating flow logs...")
    vpc_client.create_flow_logs(
        ResourceIds=ids, 
        ResourceType='VPC', 
        TrafficType='REJECT', 
        LogDestinationType='cloud-watch-logs',
        LogDestination='', #TODO: Set up a log destination
        DeliverLogsPermissionArn='') #TODO: Create roll for delivering logs
        #works


vpc_client = boto3.client('ec2')
flow_logs = vpc_client.describe_flow_logs()['FlowLogs']
vpcs = vpc_client.describe_vpcs()['Vpcs']
vpc_ids = [vpc['VpcId'] for vpc in vpcs]
flow_log_ids = [log['ResourceId'] for log in flow_logs] #Ids of resources with flow logs attached

vpcs_with_no_flow_logs = []
for id in vpc_ids:
    if id not in  flow_log_ids:
        print("VPC with id '" + id + "' does not have flow log")
        vpcs_with_no_flow_logs.append(id)
create_vpc_flow_logs(vpcs_with_no_flow_logs)
        


