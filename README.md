# WHISPER - Fast Pair Vulnerability Research Too

## SECURITY DISCLAIMER AND LEGAL WARNING

**THIS SOFTWARE IS FOR AUTHORIZED SECURITY RESEARCH AND ETHICAL TESTING ONLY**

## OVERVIEW

WHISPER (Wireless Hardware Inspection & Security Protocol Exploitation Research) is a security assessment tool for analyzing CVE-2025-36911 vulnerabilities in Google's Fast Pair protocol implementation. The tool provides:

- Real-time Bluetooth device scanning and enumeration
- Fast Pair device detection and vulnerability assessment
- Hands-Free Profile (HFP) connection testing
- Audio capture capabilities for authorized testing
- Professional reporting and logging

## INSTALLATION GUIDE

### Step 1: Clone the Repository

```bash
git clone https://github.com/ekomsSavior/whisper.git
cd whisper
```

### Step 2: Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-pip bluetooth bluez libbluetooth-dev
```

```bash
pip3 install bleak dbus-python --break-system-packages
#if you dont want to run break system packages do a VENV...
```

### Step 4:Attach Bluetooth adapter then Configure Bluetooth Stack

```bash
# Stop existing Bluetooth service
sudo systemctl stop bluetooth

# Enable and restart Bluetooth service
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

# Check Bluetooth status
sudo systemctl status bluetooth
hciconfig -a

# Ensure Bluetooth is discoverable
sudo hciconfig hci0 piscan
```

## HOW TO USE WHISPER

### Running the Tool

```bash
# Always run with root privileges (required for Bluetooth)
sudo python3 whisper.py
```

### Available Modes

<img width="1366" height="768" alt="Screenshot_2026-01-20_09_06_43" src="https://github.com/user-attachments/assets/8273a0b1-8902-4f5d-8508-b673e9af2adb" />

#### 1. Real Scan for Fast Pair Devices
Scans for devices using Google's Fast Pair protocol. Duration options:
- Quick scan (10 seconds)
- Standard scan (30 seconds) 
- Deep scan (60 seconds)
- Custom duration

#### 2. Continuous Bluetooth Scan
Displays all Bluetooth devices in real-time, highlighting Fast Pair devices with vulnerability ratings.

#### 3. Target Specific Device
Allows targeting a specific device by MAC address for detailed analysis.

#### 4. View Discovered Devices
Shows detailed information about previously discovered devices.

#### 5. Real Exploit Specific Device
Attempts exploitation of CVE-2025-36911 on a selected device (requires confirmation).

#### 6. Real Exploit All Devices
Attempts exploitation on all discovered devices (requires explicit confirmation).

#### 7. Test HFP Connection
Tests Hands-Free Profile connectivity for audio access capabilities.

#### 8. Capture Audio
Attempts audio capture from HFP-connected devices (requires established connection).

#### 9. View Scan History
Displays previously saved scan results from the results directory.

#### 10. Clear Device List
Clears the current device list from memory.

### Workflow Example

```bash
# 1. Start the tool
sudo python3 whisper.py

# 2. Accept responsibility
Type: I ACCEPT RESPONSIBILITY

# 3. Start with a quick scan
Select option: 1
Select scan type: 1 (10-second scan)

# 4. Review discovered devices
Found X Fast Pair device(s)
View device details and vulnerability ratings

# 5. Target specific device for testing
Select option: 5
Choose device number
Confirm with: EXPLOIT

# 6. Review results and save reports
```

## RESULTS AND LOGGING

WHISPER automatically saves all results to organized directories:

- `whisper_results/scans/` - Device scan results in JSON format
- `whisper_results/exploits/` - Exploitation attempt results
- `whisper_results/audio/` - Captured audio files (if applicable)

Each file is timestamped for easy tracking and includes detailed information about the operation performed.


### Testing Bluetooth Functionality

```bash
# Check if Bluetooth is working
bluetoothctl
# In bluetoothctl:
list
scan on
# Wait for devices to appear, then:
scan off
exit
```

## ETHICAL USE GUIDELINES

1. **Only test devices you own** - Never test devices without explicit permission
2. **Stay within legal boundaries** - Understand and comply with local laws
3. **Use in controlled environments** - Avoid testing in public spaces
4. **Document your work** - Keep detailed records of all testing activities
5. **Report vulnerabilities responsibly** - Follow responsible disclosure practices
6. **Respect privacy** - Do not capture or store personal audio without consent

![image0(1)](https://github.com/user-attachments/assets/04697899-cb60-46cf-a355-5f07473d34eb)
