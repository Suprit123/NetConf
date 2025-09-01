from ncclient import manager  # Import the NETCONF client library
from getpass import getpass  # Securely get password input from user

# ----------------------
# Step 1: Define device connection details
# ----------------------

device_ip = "172.16.166.133"  # IP address of the NETCONF-enabled device
netconf_port = 830  # Standard NETCONF port (default is 830)

# Create a dictionary with device credentials and connection parameters
device_credentials = {
    "host": device_ip,
    "port": netconf_port,
    "username": "admin",
    "password": getpass("Enter your password: "),
    "hostkey_verify": False,
}

# ----------------------
# Step 2: Establish NETCONF connection
# ----------------------

# Use ncclient's manager to establish a NETCONF session with the device
with manager.connect(**device_credentials) as netconf_session:
    print("✅ NETCONF connection established!")

    # ----------------------
    # Step 3: Define interface configuration payload in XML/YANG format
    # ----------------------

    interface_config_payload = """
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>GigabitEthernet3</name>  <!-- Interface name to be configured -->
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:ethernetCsmacd     <!-- Ethernet interface type -->
                </type>
                <enabled>true</enabled>        <!-- Admin status: true = up -->
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>192.168.3.3</ip>   <!-- IP address to assign -->
                        <netmask>255.255.255.0</netmask> <!-- Subnet mask -->
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """

    # ----------------------
    # Step 4: Send configuration to device
    # ----------------------

    response = netconf_session.edit_config(
        target="running",  # Apply to the running configuration
        config=interface_config_payload,  # Pass the XML payload
    )

    # ----------------------
    # Step 5: Display response from the device
    # ----------------------

    print("✅ Interface configuration applied. Device response:")
    print(response)
