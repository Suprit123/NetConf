# Importing required libraries
from ncclient import manager
from getpass import getpass

ip = "172.16.166.133"

# Creating a dictionary to hold device credentials.
device_credentials = {
    "host": ip,
    "port": 830,
    "username": "admin",
    "password": getpass("enter your password: "),
    "hostkey_verify": False,
}

# Establishing NETCONF connection using the provided device credentials.
with manager.connect(**device_credentials) as netconf:
    print("Connection established successfully...!")

    # Asking the user how many interfaces they want to configure.
    user_input = int(input("Enter the number of interfaces you wish to configure: "))

    # Looping through the number of interfaces specified by the user.
    for interface in range(user_input):
        print(f"Configuring interface {interface} of {user_input}: ")

        # Asking the user to select the type of interface.
        user_choice = int(
            input(
                """Please select the type of interface you want to configure: 
                                1. Physical Interface
                                2. Loopback Interface
                                Please make a choice(1/2): """
            )
        )

        # Determining the interface type based on user selection.
        if user_choice == 1:
            int_type = "ethernetCSmacd"
            print("You have selected Physical Interface (eg Gig1): ")

        elif user_choice == 2:
            int_type = "softwareLoopback"
            print("You have selected Loopback interface (eg Loopback1): ")

        else:
            print("Invalid input detected. Please select from option 1 or 2: ")

        # Getting interface-specific details from the user.
        int_name = input("Enter the name of interface: ")
        int_ip = input("Enter the IP for your interface: ")
        int_mask = input("Enter the subnet mask for the IP: ")

        # Creating the NETCONF payload for the interface configuration.
        int_payload = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{int_name}</name>  <!-- Interface name to be configured -->
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    ianaift:{int_type}     <!-- Ethernet interface type -->
                </type>
                <enabled>true</enabled>        <!-- Admin status: true = up -->
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{int_ip}</ip>   <!-- IP address to assign -->
                        <netmask>{int_mask}</netmask> <!-- Subnet mask -->
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>
    """

        # Sending the NETCONF configuration to the device using edit_config operation.
        int_config = netconf.edit_config(int_payload, target="running")
        print(f"Interface {int_name} configured: ")
        print(int_config)
