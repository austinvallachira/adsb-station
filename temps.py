import smbus
import time

# Get I2C bus for the MCP9808
bus = smbus.SMBus(1)
address = 0x18

def read_sdr_temp():
    """Reads the temperature from the MCP9808 I2C sensor"""
    try:
        # Read 2 bytes of data from the temperature register (0x05)
        data = bus.read_i2c_block_data(address, 0x05, 2)
        
        # Convert the data to 13-bits
        temp_raw = (data[0] & 0x0F) * 256 + data[1]
        
        # Check for negative temperatures (Sign bit)
        if data[0] & 0x10:
            return 256 - (temp_raw / 16.0)
        else:
            return temp_raw / 16.0
    except Exception:
        return None # In case the sensor wire gets bumped

def read_cpu_temp():
    """Reads the internal CPU temperature of the Raspberry Pi"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_raw = f.read()
        # The Pi outputs temp in millidegrees Celsius, so divide by 1000
        return float(temp_raw) / 1000.0
    except Exception:
        return None

print("Reading temperatures 3 times...")
print("-" * 45)

# Loop exactly 3 times instead of running forever
for i in range(3):
    sdr_temp = read_sdr_temp()
    cpu_temp = read_cpu_temp()
    
    # Format the strings to handle any reading errors gracefully
    sdr_str = f"{sdr_temp:>5.2f} °C" if sdr_temp is not None else "Error  "
    cpu_str = f"{cpu_temp:>5.2f} °C" if cpu_temp is not None else "Error  "
    
    # Print side-by-side with your requested names
    print(f"RTL SDR: {sdr_str}   |   CPU: {cpu_str}")
    
    # Wait 2 seconds before checking again (skip waiting after the last read)
    if i < 2:
        time.sleep(2)

print("-" * 45)
