from ncclient import manager
from getpass import getpass

# ----------------------------
# Device Connection Parameters
# ----------------------------

# IP address and NETCONF port of the target network device
device_ip = "172.16.166.133"
netconf_port = 830  # Default NETCONF port

# Dictionary holding device credentials and connection settings
device_credentials = {
    "host": device_ip,
    "port": netconf_port,
    "username": "admin",
    "password": getpass("Enter your password: "),  # Prompt for password at runtime
    "hostkey_verify": False,  # Disable host key verification (use with caution!)
}

# ----------------------------
# Establish NETCONF Session
# ----------------------------

# Use a context manager to open and close the NETCONF session cleanly
with manager.connect(**device_credentials) as netconf_session:
    print("✅ NETCONF connection established!")

    # ----------------------------
    # Get Number of Interfaces to Configure
    # ----------------------------
    number_of_interfaces = int(
        input("Enter the number of interfaces which you would like to configure: ")
    )

    # ----------------------------
    # Loop Through Each Interface
    # ----------------------------
    for _ in range(number_of_interfaces):

        # Ask user for interface type
        interface_choice = int(
            input(
                "Please select the type of interface: \n"
                "1. Physical Interface\n"
                "2. Loopback Interface\n"
                "Enter choice (1 or 2): "
            )
        )

        # Map user's choice to YANG interface type
        if interface_choice == 1:
            interface_type = "ethernetCsmacd"
        elif interface_choice == 2:
            interface_type = "softwareLoopback"
        else:
            print("❌ Invalid choice. Skipping this interface...\n")
            continue  # Skip to next iteration if invalid

        # Get interface details from user
        interface_name = input(
            "Enter the name of the interface (e.g., GigabitEthernet1): "
        )
        interface_ip = input("Enter the IP address to assign: ")
        interface_netmask = input("Enter the subnet mask: ")

        # ----------------------------
        # Build XML Payload (YANG model)
        # ----------------------------
        xml_payload = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{interface_name}</name>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                        ianaift:{interface_type}
                    </type>
                    <enabled>true</enabled>
                    <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                        <address>
                            <ip>{interface_ip}</ip>
                            <netmask>{interface_netmask}</netmask>
                        </address>
                    </ipv4>
                </interface>
            </interfaces>
        </config>
        """

        # ----------------------------
        # Push Configuration to Device
        # ----------------------------
        print(f"\n🔧 Configuring interface {interface_name}...")

        # Send configuration to the NETCONF server (device)
        response = netconf_session.edit_config(
            target="running",  # Apply changes to the running config
            config=xml_payload,  # The XML payload to send
        )

        # Print success message and interface summary
        print("✅ Configuration applied successfully.\n")
        print(
            f"Interface: {interface_name}, IP: {interface_ip}, "
            f"Mask: {interface_netmask}, Type: {interface_type}"
        )
