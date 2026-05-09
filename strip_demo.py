from struct import unpack
import sys
import os.path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <demo file>")
        exit(0)
        
    demo = sys.argv[1]
    
    with open(demo, "rb") as f:
        data = bytearray(f.read()) # Read demo into a bytearray
        
    ticks, = unpack("<I" , data[1060:1064]) # get total tick count
    
    ind = data.find(b"\x04", 1065) # 4 is the packet type id for ConsoleCmd
    
    while ind != -1:
        tick, length = unpack("<II", data[ind+1:ind+1+4*2]) # read tick and length of command
        
        if tick <= ticks and length < 256: # limit length, cuz the \x04 could be random data
            command = data[ind+1+4*2:ind+4*2+length] # get command bytes
            if command.isascii() and len(command) > 0 and command.decode().isprintable(): # checks to discard random data
                print(f"{tick}: '{command.decode()}'")
                data[ind+1+4*2:ind+4*2+length] = b" " * (length - 1) # overwrite command with spaces
        
        ind = data.find(b"\x04", ind+1) # find next potential packet
    
    name, ext = os.path.splitext(demo)
    
    with open(f"{name}_stripped{ext}", "wb") as out:
        out.write(data)