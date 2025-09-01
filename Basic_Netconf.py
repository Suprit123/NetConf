# To enable the NETCONF connection
from ncclient import manager

# For securely entering the password without showing it.
from getpass import getpass

# For parsing XML data and pretty-printing.
from xml.dom.minidom import parseString

# Define connection paramaters for the router.
router_connection_params = {
    "host": "172.16.166.133",
    # NETCONF default port is 830
    "port": 830,
    "username": "admin",
    "password": getpass("Enter Password: "),
    # Disables host key verification(useful for initial connections & SSL verification)
    "hostkey_verify": False,
}

# Eastablish a NETCONF connection to the router using the defined paramaters
# Using the 'manager.connect' method from the ncclient's manager module
netconfig_clinet = manager.connect(**router_connection_params)
print("Connection established ...")

# Request the running configuration from the router using NETCONF get_config operation
running_config = netconfig_clinet.get_config(source="running")
# Convert the raw running configuration into human-readable format by pretty-printing the XML
# Parsing the XML and fromatting it for readability.
formatted_running_config = parseString(running_config.xml).toprettyxml()
print(formatted_running_config)

# Open the file in write mode(this will create the file if it does not exist or overwrite it if it does.)
with open(r"/Users/apple/Desktop/GitHub/NetConf/output.xml", "w") as my_file:

    # Write the formatted configuration data into the file.
    my_file.write(formatted_running_config)
print("Configuration exported succesfully..!")
