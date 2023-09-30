<h1 align="center">CS2 Address Scan By Pattern </h1>
<p align="center">
    <a href="https://github.com/McDaived/CS2-Address-Scan-By-Pattern">
        <img src="https://github.com/McDaived/CS2-Address-Scan-By-Pattern/assets/18085492/db304b03-11cd-47d0-9efa-b3cdfc923152" alt="Logo" width="500" height="100">
    </a>
<h4 align="center">This script searches for addresses in the game within specific dll by signatures pattern, through it, you can find out the new offsets for the pattern you are looking for, you can also see the addresses that change constantly through this script.</h4>

```py
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

```

## ![](https://github.com/McDaived/NoRecoil-CS2/assets/18085492/7eab67ab-4b44-40ee-b050-53e48a856fc5)How it work : 

1. Install pymem library &rarr; `` pip install pymem ``

   

2. Put ur pattern for search about address,

 **Replace this example with  your code**
```py
pattern = rb'x48x8Bx0D....x48x8Bx01x48xFFx60x30'
```

**And make sure ur pattern format like this**

![](https://github.com/McDaived/CS2-Address-Scan-By-Pattern/assets/18085492/a45f29f1-5f21-4afc-8f52-bf42e308c3bc)

3. Change size of mov for pattern in code

```py
    # +3 (size of mov)
    address = match.start() + 3
```
**To know what is the size of mov , i will provide a simplified explanation**

![](https://github.com/McDaived/CS2-Address-Scan-By-Pattern/assets/18085492/ec4dd1bf-255a-4e91-bde0-4637a80f4272)

**Sometimes when you come across signatures they'll also come with an offset, when you scan for a pattern the address that is returned is the address of the very first bytes in the pattern but sometimes that first byte is not the data you're looking .**


![](https://github.com/McDaived/CS2-Address-Scan-By-Pattern/assets/18085492/7b43c8e6-b65c-4f63-918d-10d6a028cc8e)


4. Run it &rarr; `` python PatternAddress.py ``

   


## ![](https://github.com/McDaived/CS2-Address-Scan-By-Pattern/assets/18085492/21f45901-364e-41d7-9799-c72301ce3336)IF you want to know more about signatures pattern or scanpattern follow this Method : 

**Im using SigMaker in IDA Pro to ScanPattern it very helpful, i will explain a little about it.**

1. Download SigMaker From Here &rarr; [SigMaker IDA Pro](https://github.com/ajkhoury/SigMaker-x64/releases/tag/1.0.7)

2. Drag sigmaker into the plugins folder in your Ida Pro directory:

   Go to **IDA Pro folder** &rarr; **Plugins** &rarr; put **sigmaker dll** in folder.

3. Open IDA Pro go to &rarr; **options** &rarr; **General** &rarr; change number of **opcode bytes** to a higher number like ``16``.

   ``After you do this you will notice that in the text view next to each assembly instruction you willl be able to see all the bytes that represent that instruction these are the bytes we are going to be scanning for.``

**But unfortunately it's not that simple you can't just scan for these exact bytes because variables changed while your program is running if you had to scan for these exact bytes it would fail because when the program is running, functions and variables have different values and addresses to combat this problem signatures include something called wildcards in the place of functions and variables you'll find question marks because those bytes can be any value when the program is running it doesn't matter.**


``you can see this in action by selecting a few bytes near the data you want to find and then pressing (Ctrl+Alt+s) which is the sigmaker shortcut once Sigmaker is open select (create ida pattern from selection) and look at the pattern that is generated in output.``

![](https://github.com/McDaived/CS2-Address-Scan-By-Pattern/assets/18085492/1e322d51-47a2-4fef-a5df-7a18dbc0d8bb)

**that's all.**
