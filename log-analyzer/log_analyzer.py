from pathlib import Path
import re


folder = Path(input("Enter folder path: "))


with open(folder / "sample.log", "r") as f:
    content = f.read()


ip_addresses = re.findall(
    r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
    content
)

print("Extracted IP Addresses:")

ips = {}

for ip in ip_addresses:
    if ip in ips:
        ips[ip] += 1
    else:
        ips[ip] = 1

print("\nIP Address Frequencies:")

for ip, count in ips.items():
    print(f"{ip}: {count}")
