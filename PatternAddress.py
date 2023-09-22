import pymem
import time
import re


pm = pymem.Pymem('cs2.exe')
client = pymem.process.module_from_name(pm.process_handle, 'client.dll')

clientModule = pm.read_bytes(client.lpBaseOfDll, client.SizeOfImage)

# Search the specified pattern in the DLL
pattern = rb'\x48\x8B\x0D....\x48\x8B\x01\x48\xFF\x60\x30'
match = re.search(pattern, clientModule)

if match:
    # +3 (size of mov)
    address = match.start() + 3
    
    
    # Address with hex & decimal
    print(f"Address found: 0x{address:X}\nAddress found: {int(address):d}")
    print("Waiting for new value to be found...")
    time.sleep(10)

    # Check the current value if changed
    new_value = 2 if pm.read_uchar(address) == 1 else 1
    
    # Check if the value was changed and print a message 
    if pm.read_uchar(address) == new_value:
        print(f"Value at address 0x{address:X} changed to {new_value}")
    else:
        print("Value did not change. Ending search.")
else:
    print("Pattern not found in client module")

pm.close_process()
