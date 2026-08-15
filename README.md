ADS-B Flight Tracking Station: Complete Setup Guide

This is a step-by-step guide to building a 24/7 commercial-grade flight tracking feeder setup designed for high network stability, remote headless access, and custom hardware thermal monitoring.

=========================================
PHASE 1: HARDWARE DEPLOYMENT
=========================================

Step 1: Gather the Core Hardware
You will need a Raspberry Pi 4, a Nooelec NESDR SMArt v5 Software-Defined Radio, a 12V Cuzor UPS, and an MCP9808 High-Accuracy I2C Temperature Sensor Breakout Module.

Step 2: Connect the SDR Safely
Plug the Nooelec SDR strictly into one of the black USB 2.0 ports. Do not use the blue USB 3.0 ports on the Pi 4, as they emit electromagnetic interference that creates a jamming bubble and kills 2.4GHz Wi-Fi signals.

Step 3: Position for Signal Integrity
Place the Raspberry Pi at least 12 to 18 inches away from the Cuzor UPS. The dense lithium-ion cells in the UPS act as a physical shield against wireless signals.

Step 4: Weatherproof the Antenna
If you are placing the bundled magnetic whip antenna outdoors, you must protect it from rain to prevent frequency detuning and permanent coaxial wicking. Wrap the cable entry point tightly with self-amalgamating silicone tape or house the antenna inside a sealed PVC pipe radome.

=========================================
PHASE 2: OS FLASHING & INITIAL SETUP
=========================================

Step 5: Flash Raspberry Pi OS
Download and open the Raspberry Pi Imager on your main computer. Select "Raspberry Pi OS (Bookworm, 64-bit)" as the operating system and choose your SD card as the storage target.

Step 6: Configure Headless Settings
Before flashing, click the gear icon (Edit Settings) in the Imager. Set your hostname (e.g., pi24-bookworm), create your user/password, enter your Wi-Fi SSID and password, and enable SSH (using password authentication). Write the image, insert the SD card into the Pi, and power it on.

Step 7: Set a Static IP
Log into your Pi via SSH. Find your active Wi-Fi connection name by running:
nmcli connection show

Modify the connection to use a manual static IP (replace the IP addresses with your specific network details):
sudo nmcli connection modify "xyz" ipv4.addresses 0.0.0.0 ipv4.gateway 0.0.0.0 ipv4.dns "1.1.1.1,8.8.8.8" ipv4.method manual

Apply the changes:
sudo nmcli connection up "xyz"

=========================================
PHASE 3: SOFTWARE DEPLOYMENT
=========================================

Step 8: Install Tailscale (Remote Access)
Install Tailscale to enable secure, remote headless SSH access without opening router ports:
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

Step 9: Install Flightradar24 Feeder
Execute the automated Flightradar24 installation script (this also installs the dump1090 decoder):
sudo bash -c "$(wget -O - https://repo-feed.flightradar24.com/install_fr24_rpi.sh)"
(Follow the on-screen prompts to enter your sharing key and coordinate details).

Step 10: Install FlightAware (PiAware)
To dual-feed data to FlightAware, install the PiAware repository and software:
wget https://flightaware.com/adsb/piaware/files/packages/pool/piaware/f/flightaware-apt-repository/flightaware-apt-repository_1.2_all.deb
sudo dpkg -i flightaware-apt-repository_1.2_all.deb
sudo apt update
sudo apt install piaware dump1090-fa -y
sudo piaware-config allow-auto-updates yes
sudo piaware-config allow-manual-updates yes

Step 11: Install System Optimisation Tools
To reduce SD card wear and visualise your tracking data, install these community packages (look up their respective GitHub installation scripts):
* log2ram: Moves system logs to RAM.
* graphs1090: Generates system and radio performance graphs.
* tar1090: Provides a high-resolution web interface for viewing tracked aircraft locally.

=========================================
PHASE 4: NETWORK STABILITY & MAINTENANCE
=========================================

Step 12: Apply the IPv4 Routing Fix
Tailscale's IPv6 routing can break the Pi's ability to resolve Flightradar24 ingestion servers. Open the routing file:
sudo nano /etc/gai.conf

Scroll to the very bottom and add this active rule:
precedence ::ffff:0:0/96  100

Save, exit, and restart the feeder service:
sudo systemctl restart fr24feed

Step 13: Set up Hardware Telemetry (temps.py)
Ensure your custom Python I2C script (temps.py) is loaded on the system to monitor the thermal performance of the radio and Pi CPU. This script interfaces with the MCP9808 module and is configured to run exactly three polling loops per execution.

Step 14: Schedule Weekly Automated Reboot
To ensure long-term software stability, schedule a weekly automated reboot to clear temporary memory and reset USB port handshakes. Open the cron editor:
sudo crontab -e

Add this rule to reboot every Sunday at 08:00 AM IST (02:30 UTC):
30 2 * * 0 /sbin/shutdown -r now

Save and exit. 
Your 24/7 commercial-grade ADS-B station is now fully deployed.
