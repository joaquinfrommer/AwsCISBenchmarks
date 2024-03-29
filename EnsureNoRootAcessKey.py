import boto3

#Start sequence
def start():
    iam = boto3.resource('iam')
    account_summary = iam.AccountSummary().summary_map
    if account_summary['AccountAccessKeysPresent']:
        print("Root access key present, please delete!")
    else:
        print("No root access key detected!")


if __name__ == "__main__":
    start()
