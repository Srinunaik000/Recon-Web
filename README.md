# Recon-Web
### Recon Tool Website
This is a web-based recon tool built using Flask, designed to perform WHOIS lookups, subdomain enumeration, DNS record gathering, Nmap scans, and reverse DNS lookups.

### Features
- WHOIS Lookup: Performs a WHOIS lookup for a given domain.
- Subdomain Enumeration: Enumerates subdomains for a given domain using Subfinder.
- DNS Record Gathering: Gathers DNS records (A, AAAA, MX, CNAME, TXT, NS, SOA) for a domain.
- Nmap Scan: Runs an Nmap scan for the given target.
- Reverse DNS Lookup: Performs a reverse DNS lookup for a given IP address.

### Prerequisites
Before running this project, ensure you have the following installed:

## Python Packages
- Flask: A lightweight web framework for Python.
- python-whois: A library to perform WHOIS lookups.
- dnspython: A library for DNS queries in Python.

### To install the required Python packages, run:

- pip install -r requirements.txt

- Nmap, Subfinder need to be already installed on your system required

- sudo apt-get install nmap

- go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

### Usage
- Add Executable Permissions to python file and the execute
chmod +x recon.py

python3 recon.py

- it start's a server on your loopback address http://127.0.0.1:5000 you can visit this address to access web Recon Interface
