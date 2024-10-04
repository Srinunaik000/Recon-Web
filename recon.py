from flask import Flask, render_template, request, session
import subprocess
import whois
import dns.resolver
import random
import socket

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

# Function definitions

def whois_lookup(domain):
    """Perform a WHOIS lookup on the given domain."""
    try:
        w = whois.whois(domain)
        if isinstance(w, dict):
            whois_info = "\n".join(f"{key}: {value}" for key, value in w.items())
        else:
            whois_info = str(w)
        return whois_info
    except Exception as e:
        return f"WHOIS lookup failed: {e}"

def subdomain_enumeration(domain):
    """Perform subdomain enumeration on the given domain."""
    try:
        result = subprocess.run(['subfinder', '-d', domain, '-o', '/dev/stdout'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Subdomain enumeration failed: {e}"

def dns_record_gathering(domain):
    """Gather DNS records for the given domain."""
    record_types = ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'NS', 'SOA']
    dns_records = {rtype: [] for rtype in record_types}
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records = [str(rdata) for rdata in answers]
            dns_records[record_type] = records
        except dns.resolver.NoAnswer:
            dns_records[record_type] = ['No records found']
        except dns.resolver.NXDOMAIN:
            dns_records[record_type] = ['Domain does not exist.']
        except Exception as e:
            dns_records[record_type] = [f"Error fetching {record_type} records: {e}"]
    return dns_records

def nmap_scan(target):
    """Run Nmap scan on the given target."""
    try:
        result = subprocess.run(['nmap', target], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Nmap scan failed: {e}"

def reverse_dns_lookup(ip_address):
    """Perform a reverse DNS lookup on the given IP address."""
    try:
        host_name, _, _ = socket.gethostbyaddr(ip_address)
        return host_name
    except socket.herror:
        return "Host could not be resolved."
    except socket.gaierror:
        return "Invalid IP address format."
    except Exception as e:
        return f"Reverse DNS lookup failed: {e}"

# Flask routes

@app.route('/')
def index():
    """Render the main index page with tabs for different tools."""
    return render_template('index.html')

@app.route('/whois', methods=['GET', 'POST'])
def whois_lookup_page():
    print(f"Received {request.method} request")  # Debugging line
    if request.method == 'POST':
        domain = request.form['domain']
        whois_result = whois_lookup(domain)
        session['whois_domain'] = domain
        session['whois_result'] = whois_result
        return render_template('whois.html', domain=domain, whois_result=whois_result)
    else:
        domain = session.get('whois_domain', '')
        whois_result = session.get('whois_result', '')
        return render_template('whois.html', domain=domain, whois_result=whois_result)

@app.route('/subdomains', methods=['GET', 'POST'])
def subdomain_enumeration_page():
    """Handle subdomain enumeration functionality."""
    if request.method == 'POST':
        domain = request.form['domain']
        subdomains_result = subdomain_enumeration(domain)
        session['subdomains_domain'] = domain
        session['subdomains_result'] = subdomains_result
        return render_template('subdomains.html', domain=domain, subdomains_result=subdomains_result)
    domain = session.get('subdomains_domain', '')
    subdomains_result = session.get('subdomains_result', '')
    return render_template('subdomains.html', domain=domain, subdomains_result=subdomains_result)

@app.route('/dns', methods=['GET', 'POST'])
def dns_records_page():
    """Handle DNS record gathering functionality."""
    if request.method == 'POST':
        domain = request.form['domain']
        dns_records_result = dns_record_gathering(domain)
        session['dns_domain'] = domain
        session['dns_result'] = dns_records_result
        return render_template('dns.html', domain=domain, dns_records_result=dns_records_result)
    domain = session.get('dns_domain', '')
    dns_records_result = session.get('dns_result', '')
    return render_template('dns.html', domain=domain, dns_records_result=dns_records_result)

@app.route('/nmap', methods=['GET', 'POST'])
def nmap_scan_page():
    """Handle Nmap scanning functionality."""
    if request.method == 'POST':
        target = request.form.get('target', '')
        if not target:
            return "Target is required", 400
        nmap_result = nmap_scan(target)
        session['nmap_target'] = target
        session['nmap_result'] = nmap_result
        return render_template('nmap.html', target=target, nmap_result=nmap_result)
    target = session.get('nmap_target', '')
    nmap_result = session.get('nmap_result', '')
    return render_template('nmap.html', target=target, nmap_result=nmap_result)

@app.route('/reverse_dns', methods=['GET', 'POST'])
def reverse_dns_page():
    """Handle reverse DNS lookup functionality."""
    reverse_dns_result = None
    ip_address = None
    if request.method == 'POST':
        ip_address = request.form.get('ip_address')
        if ip_address:
            reverse_dns_result = reverse_dns_lookup(ip_address)
    return render_template('reverse_dns.html', reverse_dns_result=reverse_dns_result, ip_address=ip_address)

if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port, debug=True)
