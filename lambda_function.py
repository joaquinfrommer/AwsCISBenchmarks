import json
import EnsureAllVpcsEnableFlowLogs
import EnsureKeyRotation
import EnsureNoRootAcessKey
import EnsureS3BucketsBlockPublicAccess
import EnsureS3EncryptionAtRest
import EnsureSingleAccessKeyPerUser
import NoFullAdminPrivilegesPolicy
import NoRDPPortsExposed
import NoRemotePortAclIngress
import SSHPortNotExposedToInternet
import VpcDefaultSecuritGroupsRestrictAllTrafic


def lambda_handler(event, context):
    # TODO implement
    EnsureSingleAccessKeyPerUser.start()
    EnsureS3EncryptionAtRest.start()
    EnsureS3BucketsBlockPublicAccess.start()
    EnsureNoRootAcessKey.start()
    EnsureKeyRotation.start()
    EnsureAllVpcsEnableFlowLogs.start()
    NoFullAdminPrivilegesPolicy.start()
    NoRDPPortsExposed.start()
    NoRemotePortAclIngress.start()
    SSHPortNotExposedToInternet.start()
    VpcDefaultSecuritGroupsRestrictAllTrafic.start()
    return {
        'statusCode': 200,
        'body': json.dumps('Done!')
    }