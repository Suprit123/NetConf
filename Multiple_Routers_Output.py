from ncclient import manager  # NETCONF client library
from xml.dom.minidom import parseString  # For pretty-printing XML
from getpass import getpass  # Secure password input

# Secure password input from user
password = getpass("Enter your password: ")

# List of router IPs to connect to
router_ip_list = ["172.16.166.133", "172.16.166.137"]

# Loop through each router IP
for router_ip in router_ip_list:
    print(f"\n Attempting connection to router: {router_ip}")

    router_params = {
        "host": router_ip,
        "port": 830,
        "username": "admin",
        "password": password,
        "hostkey_verify": False,
    }

    try:
        # Establish NETCONF session
        with manager.connect(**router_params) as netconf:
            print(f"✅ Connected to router: {router_ip}")

            # Get the running config
            running_config = netconf.get_config(source="running")

            # Prettify the XML
            formatted_config = parseString(running_config.xml).toprettyxml()

            # Unique filename per router
            file_name = f"/Users/apple/Desktop/GitHub/NetConf/Running_Config_{router_ip.replace('.', '_')}.xml"

            # Save to file
            with open(file_name, "w") as config_file:
                config_file.write(formatted_config)

            print(f" Configuration from {router_ip} saved to: {file_name}")

    except Exception as e:
        # Catch all errors (connection/auth issues etc.)
        print(f"❌ Failed to connect to {router_ip}. Reason: {str(e)}")

print("\n Script completed. All reachable router configurations have been processed.")
