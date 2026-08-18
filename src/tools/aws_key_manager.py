from getpass import getpass
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError, NoRegionError
from tools.folder_path_logic import load_config, load_config_and_get_section, save_config, get_default_config_file

# Added aws_section for testing.
def enter_new_keys(config_path: str = "", aws_section = {}):
    """
    When called, prompts the user to input their AWS keys which are then saved to the default config.
    Note: this method would need a better implementation if this project ever had to be continued, but it will work for this.
    """
    if config_path == "":
        config_path = get_default_config_file()

    # Try to load in config before we add new things to prevent overwriting.
    config = load_config(config_path)

    # for each input
        # Do we have a previous config of the data?
        # Load in previous data
        # If use puts in "" leave it the same, else change it.

    access_key_id_info = ""
    secret_access_key_info = ""
    region_info = ""

    access_key_id_display = ""
    secret_access_key_display = ""
    region_display = ""

    if "AWS" in config:
        aws = config["AWS"]
        access_key_id_info = aws.get("access_key_id")
        if access_key_id_info == None:
            access_key_id_info = ""
        else:
            access_key_id_display = f" [****{access_key_id_info[-4:]}]"

        secret_access_key_info = aws.get("secret_access_key")
        if secret_access_key_info == None:
            secret_access_key_info = ""
        else:
            secret_access_key_display = f" [****{secret_access_key_info[-4:]}]"

        region_info = aws.get("region")
        if region_info == None:
            region_info = ""
        else:
            region_display = f" [{region_info}]"

    access_key_id = ""
    secret_access_key = ""
    region = ""
    # aws_section is used for making testing easier.
    if aws_section == {}:
        access_key_id = getpass(f"AWS access key{access_key_id_display}: ", echo_char="*").strip()
        secret_access_key = getpass(f"AWS secret key{secret_access_key_display}: ", echo_char="*").strip()
        region = input(f"AWS region{region_display}: ").strip()
    else:
        access_key_id = aws_section["access_key_id"]
        secret_access_key = aws_section["secret_access_key"]
        region = aws_section["region"]

    if access_key_id == "":
        access_key_id = access_key_id_info

    if secret_access_key == "":
        secret_access_key = secret_access_key_info

    if region == "":
        region = region_info
        
        

    
    config["AWS"] = {
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
        "region": region
    }

    # Our config_path was not being passed in. Problem solved.
    save_config(config=config, config_path=config_path)

    print("Keys saved✅")

def is_AWS_config_credentials_valid(config_path = "", creds = {}) -> bool:
    # Pull keys from config
    # Call boto3 and see if keys are valid
    # return true if valid, false if not.
    """
    Validates AWS credentials and verifies if the specified region is reachable.
    - Note: code form googles AI. A lot of changes made since it was not the best though.
    """
    try:
        aws_access_key_id = ""
        aws_secret_access_key = ""
        region_name = ""
        
        if creds == {}:
            if config_path == "":
                config_path = get_default_config_file()

            aws = load_config_and_get_section(config_path=config_path,section = "AWS")
            aws_access_key_id = aws.get("access_key_id")
            aws_secret_access_key = aws.get("secret_access_key")
            region_name = aws.get("region")
        else:
            aws_access_key_id = creds.get("access_key_id")
            aws_secret_access_key = creds.get("secret_access_key")
            region_name = creds.get("region")

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