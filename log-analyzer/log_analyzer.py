from pathlib import Path
import re


folder = Path(input("Enter folder path: "))


with open(folder / "text.log", "r") as f:
    content = f.read()


status_codes = re.findall(r'"\s([0-9]{3})\s[0-9]+', content)

print("Extracted CODE:")

codes = {}

for code in status_codes:
    if code in codes:
        codes[code] += 1
    else:
        codes[code] = 1

print("\nCODE Frequencies:")

for code, count in codes.items():
    print(f"{code}: {count}")



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

top_ips = sorted(ips.items(), key=lambda x: x[1], reverse=True)

print("\nTop IP Addresses:")

for ip, count in top_ips[:10]:
    print(f"{ip}: {count}")



    
used_methods = re.findall(r'"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)', content)

print("Extracted methods:")

methods = {}

for method in used_methods:
    if method in methods:
        methods[method] += 1
    else:
        methods[method] = 1

print("\nCODE Frequencies:")

for method, count in methods.items():
    print(f"{method}: {count}")


paths = re.findall(
    r'"(?:GET|POST|OPTIONS|HEAD|PUT|DELETE|PATCH)\s+([^\s]+)',
    content
)

path_counts = {}

for path in paths:
    if path in path_counts:
        path_counts[path] += 1
    else:
        path_counts[path] = 1

print("\nTop Requested Paths:")

top_paths = sorted(
    path_counts.items(),
    key=lambda x: x[1],
    reverse=True
)

for path, count in top_paths[:10]:
    print(f"{path}: {count}")
