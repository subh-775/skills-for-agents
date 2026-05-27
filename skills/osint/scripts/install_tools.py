#!/usr/bin/env python3
"""
OSINT Tools Installer — checks and installs OSINT tools
Usage: python install_tools.py [--check] [--install] [--tool NAME]
"""

import subprocess
import sys
import json
import shutil
from pathlib import Path

TOOLS = {
    "sherlock": {
        "name": "Sherlock",
        "description": "Username enumeration across 400+ sites",
        "install": "pip install sherlock-project",
        "check_cmd": "sherlock --version",
        "category": "username",
        "github": "https://github.com/sherlock-project/sherlock"
    },
    "holehe": {
        "name": "Holehe",
        "description": "Email to platform check (120+ sites)",
        "install": "pip install holehe",
        "check_cmd": "holehe --help",
        "category": "email",
        "github": "https://github.com/megadose/holehe"
    },
    "maigret": {
        "name": "Maigret",
        "description": "Extended username search (3000+ sites)",
        "install": "pip install maigret",
        "check_cmd": "maigret --version",
        "category": "username",
        "github": "https://github.com/soxoj/maigret"
    },
    "theHarvester": {
        "name": "theHarvester",
        "description": "Emails, subdomains from public sources",
        "install": "pip install theHarvester",
        "check_cmd": "theHarvester --help",
        "category": "domain",
        "github": "https://github.com/laramies/theHarvester"
    },
    "h8mail": {
        "name": "h8mail",
        "description": "Email breach checker",
        "install": "pip install h8mail",
        "check_cmd": "h8mail --help",
        "category": "email",
        "github": "https://github.com/khast3x/h8mail"
    },
    "photon": {
        "name": "Photon",
        "description": "Fast web crawler for OSINT",
        "install": "pip install photon-crawler",
        "check_cmd": "photon --help",
        "category": "web",
        "github": "https://github.com/s0md3v/Photon"
    },
    "instaloader": {
        "name": "Instaloader",
        "description": "Instagram profile/post scraper",
        "install": "pip install instaloader",
        "check_cmd": "instaloader --help",
        "category": "social",
        "github": "https://github.com/instaloader/instaloader"
    },
    "subfinder": {
        "name": "Subfinder",
        "description": "Passive subdomain enumeration",
        "install": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "check_cmd": "subfinder -version",
        "category": "domain",
        "github": "https://github.com/projectdiscovery/subfinder"
    },
    "phoneinfoga": {
        "name": "PhoneInfoga",
        "description": "Phone number OSINT scanner",
        "install": "Download from https://github.com/sundowndev/phoneinfoga/releases",
        "check_cmd": "phoneinfoga version",
        "category": "phone",
        "github": "https://github.com/sundowndev/phoneinfoga"
    },
    "nmap": {
        "name": "nmap",
        "description": "Network port scanner",
        "install": "apt install nmap / brew install nmap",
        "check_cmd": "nmap --version",
        "category": "network",
        "github": "https://nmap.org"
    },
    "exiftool": {
        "name": "ExifTool",
        "description": "Metadata extraction from files",
        "install": "apt install exiftool / brew install exiftool",
        "check_cmd": "exiftool -ver",
        "category": "metadata",
        "github": "https://exiftool.org"
    },
    "whois": {
        "name": "whois",
        "description": "Domain registration lookup",
        "install": "apt install whois / brew install whois",
        "check_cmd": "whois --version",
        "category": "domain",
        "github": None
    },
    "dig": {
        "name": "dig",
        "description": "DNS lookup tool",
        "install": "apt install dnsutils / brew install bind",
        "check_cmd": "dig -v",
        "category": "domain",
        "github": None
    },
    "jq": {
        "name": "jq",
        "description": "JSON processor",
        "install": "apt install jq / brew install jq",
        "check_cmd": "jq --version",
        "category": "utility",
        "github": "https://github.com/jqlang/jq"
    },
    "curl": {
        "name": "curl",
        "description": "HTTP client",
        "install": "apt install curl / brew install curl",
        "check_cmd": "curl --version",
        "category": "utility",
        "github": "https://curl.se"
    }
}

API_KEYS = {
    "HIBP_API_KEY": "Have I Been Pwned API key (https://haveibeenpwned.com/API/Key)",
    "SHODAN_API_KEY": "Shodan API key (https://account.shodan.io)",
    "IPINFO_TOKEN": "ipinfo.io token (https://ipinfo.io/signup)",
    "NUMVERIFY_API_KEY": "NumVerify API key (https://numverify.com)",
    "GOOGLE_API_KEY": "Google Custom Search API key",
    "GOOGLE_CSE_ID": "Google Custom Search Engine ID",
    "ABUSEIPDB_KEY": "AbuseIPDB API key (https://abuseipdb.com/account/api)",
    "INTELX_API_KEY": "IntelX API key (https://intelx.io)",
    "VT_API_KEY": "VirusTotal API key (https://www.virustotal.com/gui/my-apikey)"
}

def check_tool(name, tool_info):
    """Check if a tool is installed."""
    cmd = tool_info["check_cmd"].split()
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def install_tool(name, tool_info):
    """Install a tool."""
    install_cmd = tool_info["install"]
    if install_cmd.startswith("pip"):
        result = subprocess.run(install_cmd.split(), capture_output=True, timeout=120)
        return result.returncode == 0
    elif install_cmd.startswith("go "):
        result = subprocess.run(install_cmd.split(), capture_output=True, timeout=120)
        return result.returncode == 0
    else:
        print(f"  Manual install required: {install_cmd}")
        return False

def check_api_keys():
    """Check which API keys are set."""
    print("\n=== API Keys ===")
    for key, desc in API_KEYS.items():
        status = "SET" if key in __import__('os').environ else "MISSING"
        symbol = "✓" if status == "SET" else "✗"
        print(f"  {symbol} {key}: {status}")
        if status == "MISSING":
            print(f"    → {desc}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="OSINT Tools Installer")
    parser.add_argument("--check", action="store_true", help="Check which tools are installed")
    parser.add_argument("--install", action="store_true", help="Install missing tools")
    parser.add_argument("--tool", help="Check/install specific tool")
    parser.add_argument("--api-keys", action="store_true", help="Check API key status")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if args.api_keys:
        check_api_keys()
        return
    
    results = {}
    
    for name, info in TOOLS.items():
        if args.tool and name != args.tool:
            continue
        
        installed = check_tool(name, info)
        results[name] = {
            "name": info["name"],
            "installed": installed,
            "description": info["description"],
            "category": info["category"],
            "github": info["github"],
            "install_cmd": info["install"]
        }
        
        if args.json:
            continue
        
        symbol = "✓" if installed else "✗"
        print(f"  {symbol} {info['name']}: {'installed' if installed else 'NOT installed'}")
        
        if not installed and args.install:
            print(f"    Installing {info['name']}...")
            if install_tool(name, info):
                print(f"    ✓ {info['name']} installed")
                results[name]["installed"] = True
            else:
                print(f"    ✗ {info['name']} install failed")
    
    if args.json:
        print(json.dumps(results, indent=2))
    
    if args.check:
        installed = sum(1 for r in results.values() if r["installed"])
        total = len(results)
        print(f"\n{installed}/{total} tools installed")
        
        missing = [r["name"] for r in results.values() if not r["installed"]]
        if missing:
            print(f"Missing: {', '.join(missing)}")
            print(f"\nRun: python {__file__} --install")

if __name__ == "__main__":
    main()
