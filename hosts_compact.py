"""
hosts_compact
Reduces the amount of entries in a hosts file by assigning up to 9 hosts per line instead of the default 1.

This is a workaround for the DNS Client service in Windows causing networking issues when a large hosts file is present.
Includes the base localhost entries unless OMIT_BASE is set to True.
Includes a timestamp at the top of the file unless OMIT_TIMESTAMP is set to True.
Arguments are optional and default to hosts and hosts_compacted. Output file will be overwritten if it exists.

Usage:
    python hosts_compact.py [filename] [out_filename]
"""

from datetime import datetime
import sys

DEFAULT_FILENAME = "hosts"
DEFAULT_OUT_FILENAME = "hosts_compacted"
OMIT_BASE = False  # Set to True to omit base entries in output file
OMIT_TIMESTAMP = False  # Set to True to omit timestamp in first line of output file

BASE_HOSTS = [
    "127.0.0.1 localhost localhost.localdomain local",
    "255.255.255.255 broadcasthost",
    "::1 localhost ip6-localhost ip6-loopback",
    "fe80::1%lo0 localhost",
    "ff00::0 ip6-localnet ip6-mcastprefix",
    "ff02::1 ip6-allnodes",
    "ff02::2 ip6-allrouters",
    "ff02::3 ip6-allhosts",
    "0.0.0.0 0.0.0.0",
]

# These are added separately, no need to process them
REDUNDANT_DOMAINS = {
    "localhost",
    "localhost.localdomain",
    "local",
    "broadcasthost",
    "ip6-localhost",
    "ip6-loopback",
    "ip6-localnet",
    "ip6-mcastprefix",
    "ip6-allnodes",
    "ip6-allrouters",
    "ip6-allhosts",
    "127.0.0.1",
    "0.0.0.0",
}

filename = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILENAME
out_filename = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUT_FILENAME

domains_set = set()  # Remove duplicates by using a set
try:
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            # Skip comments and empty lines
            if not (line.startswith("127.0.0.1") or line.startswith("0.0.0.0")):
                continue
            line = line.split()
            if len(line) > 1:
                # In case the input file has multiple domains per line already
                line_domains = []
                for host in line:
                    # Remove comments with spaces
                    if host.startswith("#"):
                        break
                    elif host not in REDUNDANT_DOMAINS:
                        domains_set.add(host)
except FileNotFoundError:
    print(
        "File not found - supply input and optionally output filenames as arguments or make sure a file named 'hosts' is in this folder."
    )
    sys.exit(1)
if not domains_set:
    print("No valid entries found in the input file.")
    sys.exit(1)

domains_list = list(domains_set)  # Use list to create chunks
del domains_set

compacted_hosts = []
for i in range(0, len(domains_list), 9):
    domains_chunk = domains_list[i : i + 9]
    if domains_chunk:
        compacted_hosts.append("0.0.0.0 " + " ".join(domains_chunk))

out_hosts = compacted_hosts

if OMIT_BASE is True:
    print("Base entries omitted.")
else:
    out_hosts = BASE_HOSTS + out_hosts

if OMIT_TIMESTAMP is True:
    print("Timestamp omitted.")
else:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out_hosts = ["# " + timestamp] + out_hosts

try:
    with open(out_filename, "w") as file:
        for line in out_hosts:
            file.write(line + "\n")
        print(f"File {filename} compacted into {out_filename}.")
except IOError as e:
    print(f"Can't write to file {out_filename}: {e}.")
    sys.exit(1)
