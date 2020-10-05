import boto3
import argparse


#Starting sequence. 
#Gets password policy and updates it if the password reuse prevention currently does not match the input number.
def start(num_passwords):
    iam_client = boto3.client('iam')
    current_policy = iam_client.get_account_password_policy()['PasswordPolicy']
    if current_policy['PasswordReusePrevention'] != num_passwords:
        iam_client.update_account_password_policy(
            #TODO: Figure out what to do for default values.
            MinimumPasswordLength=current_policy['MinimumPasswordLength'] if 'MinimumPasswordLength' in current_policy else None,
            RequireSymbols=current_policy['RequireSymbols'] if 'RequireSymbols' in current_policy else None,
            RequireNumbers=current_policy['RequireNumbers'] if 'RequireNumbers' in current_policy else None,
            RequireUppercaseCharacters=current_policy['RequireUppercaseCharacters'] if 'RequireUppercaseCharacters' in current_policy else None,
            RequireLowercaseCharacters=current_policy['RequireLowercaseCharacters'] if 'RequireLowercaseCharacters' in current_policy else None,
            AllowUsersToChangePassword=current_policy['AllowUsersToChangePassword'] if 'AllowUsersToChangePassword' in current_policy else None,
            MaxPasswordAge=current_policy['MaxPasswordAge'] if 'MaxPasswordAge' in current_policy else None,
            PasswordReusePrevention=num_passwords,
            HardExpiry=current_policy['HardExpiry'] if 'HardExpiry' in current_policy else None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("num_pwords", type=int)
    args = parser.parse_args()
    num_pwords = args.num_pwords
    start(num_pwords)