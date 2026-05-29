from struct import unpack
import sys
import os.path
import traceback

def strip(demo_path, out_path):
    with open(demo_path, "rb") as f:
        data = bytearray(f.read()) # Read demo into a bytearray
        
    ind = 1072 # end of header
    
    stripped = 0
    
    while ind < len(data):

        packet_type = data[ind]
        ind += 1
        if packet_type == 7:
            tick, = unpack("<I", data[ind:ind+3] + b"\0")
            ind += 3
        else:
            tick, = unpack("<I", data[ind:ind+4])
            ind += 4

        match packet_type:
            case 1 | 2: # Signon and Message
                ind += 84
                length, = unpack("<I", data[ind:ind+4])
                ind += 4 + length
                pass
            case 3: # Synctick
                pass
            case 4:
                length, = unpack("<I", data[ind:ind+4]) # read tick and length of command
                ind += 4
                command = data[ind:ind+length] # get command bytes
                print(f"{tick}: {bytes(command)}")

                ind -= 1 + 4 + 4
                del data[ind:ind+4*2+length+1]
                stripped += 1
                
            case 5: # UserCmd
                ind += 4
                length, = unpack("<I", data[ind:ind+4])
                ind += 4 + length
            case 6: # DataTable
                length, = unpack("<I", data[ind:ind+4])
                ind += 4 + length
            case 7: # Stop
                pass
            case 8: # StringTable
                length, = unpack("<I", data[ind:ind+4])
                ind += 4 + length
    
    with open(out_path, "wb") as out:
        out.write(data)
    return stripped

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print(f"Usage: {sys.argv[0]} <demo file>")
            sys.exit()
            
        demo = sys.argv[1]
        name, ext = os.path.splitext(demo)
        out_path = f"{name}_stripped{ext}"
        stripped = strip(demo, out_path)
        
        print(f"{stripped} commands removed")
        print(f"Saved to {out_path}")
    except Exception:
        traceback.print_exc()
    input("Press Enter to exit")
