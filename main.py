import nfc
import sys


def on_connect(tag):
    # Extract the tag data
    tag_data = str(tag)

    # Write the tag data to stdout
    sys.stdout.write(tag_data)
    sys.stdout.flush()  # Ensure the data is immediately written to stdout


# Replace 'usb:001:004' with the correct device path for your USB NFC reader
clf = nfc.ContactlessFrontend('usb:001:004')
clf.connect(rdwr={'on-connect': on_connect})
