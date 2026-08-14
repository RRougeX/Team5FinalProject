from getpass import getpass
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError, NoRegionError
from tools.folderPathLogic import load_config, load_config_and_get_section, save_config

def enterNewKeys():
    # Try to load in config before we add new things to prevent overwriting.
    config = load_config()

    config["AWS"] = {
        "access_key_id": input("AWS access key: ").strip(),
        "secret_access_key": getpass("AWS secret key: ").strip(),
        "region": input("AWS region: ").strip()
    }

    save_config(config=config)

    print("Keys saved✅")

def is_AWS_config_credentials_valid() -> bool:
    # Pull keys from config
    # Call boto3 and see if keys are valid
    # return true if valid, false if not.
    """
    Validates AWS credentials and verifies if the specified region is reachable.
    - Note: code form googles AI. A lot of changes made since it was not the best though.
    """
    try:
        aws = load_config_and_get_section(section = "AWS")

        aws_access_key_id = aws.get("access_key_id")
        aws_secret_access_key = aws.get("secret_access_key")
        region_name = aws.get("region")

        # 1. Create a session with explicit keys and region
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        
        # 2. Verify credentials globally via STS
        sts_client = session.client('sts')
        identity = sts_client.get_caller_identity()
        print(f"✅ Credentials: VALID (User: {identity['Arn']})")
        
        # 3. Verify region validity by making a regional call (EC2 is ideal for this)
        ec2_client = session.client('ec2')
        # describe_regions is lightweight and tests regional endpoint connectivity
        ec2_client.describe_regions(RegionNames=[region_name])
        print(f"✅ Region: VALID '{region_name}': .")
        return True

    except EndpointConnectionError:
        print(f"❌ Region: INVALID '{region_name}'. Could not resolve endpoint. Check spelling (e.g., 'us-east-1').")
        return False
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code in ['InvalidClientTokenId', 'SignatureDoesNotMatch', 'AuthFailure']:
            print(f"❌ Credentials: INVALID AWS keys. Error: {error_code}")
        elif error_code == 'UnauthorizedOperation':
            # This means credentials and region are valid, but IAM lacks EC2 describe permissions
            print(f"✅ Region: VALID '{region_name}', but your IAM user lacks 'ec2:DescribeRegions' permissions.")
            return True
        else:
            print(f"❌ AWS Error occurred: {e}")
        return False
    except NoRegionError:
        print("❌ Region: None provided. Please specify a valid region string.")
        return False
    except NoCredentialsError:
        print("Error: No AWS credentials could be found in your environment.")
        return False