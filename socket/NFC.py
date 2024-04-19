import usb.core
import usb.util
import socket
import Klient
# USB vendor and product IDs for the ACR122U NFC reader
VENDOR_ID = 0x072f
PRODUCT_ID = 0x2200
RASPBERRY_PI_IP = '10.200.130.75'
RASPBERRY_PI_PORT = 12351

def read_nfc():
    # Find the NFC reader device
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    if device is None:
        raise ValueError("ACR122U NFC reader not found!")

    try:
        # Detach the kernel driver from the NFC reader
        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)

        # Claim the NFC reader interface
        usb.util.claim_interface(device, 0)

        # Start reading NFC tags
        print("Waiting for NFC tag...")
        while True:
            # Attempt to read data from the NFC reader
            try:
                data = device.read(0x81, 16)
                if data:
                    Klient.run_client(data)
                    # Connect to Raspberry Pi
                    """with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((RASPBERRY_PI_IP, RASPBERRY_PI_PORT))
                        s.sendall(data)
                        """
                    print("Tag detected and sent to Raspberry Pi:", data)
            except usb.core.USBError as e:
                if e.errno == 60:  # Operation timed out
                    continue  # Retry reading

    except KeyboardInterrupt:
        print("Program terminated by user.")

    finally:
        # Release the interface and reattach the kernel driver
        usb.util.release_interface(device, 0)
        usb.util.dispose_resources(device)

if __name__ == "__main__":
    read_nfc()