## hosts_compact

### What is this?

This is a simple Python script which reduces the amount of entries in a hosts file by assigning up to 9 hosts per line instead of the default 1. Also removes empty lines and comments.

### Reasoning

This is a workaround for the DNS Client service in Windows causing networking issues when a large hosts file is present. The best way of dealing with this issue is to simply disable the DNS Client service, but this script might prove useful if you would rather keep the service running or cannot disable it for whatever reason.

### Notes

- Includes the base localhost entries unless OMIT_BASE is set to True in the script.
- Arguments are optional and default to hosts and hosts_compacted.
- Place your hosts file in the same folder as the script and run it with `python hosts_compact.py`, or e.g. `python hosts_compact.py hosts.txt hosts` if you want to use custom filenames. Output file will be overwritten if it is already present in the folder.
