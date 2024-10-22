#!/usr/bin/python3
import re
import subprocess

hostinzb = "myicecast" # CHANGE

# URL to get data
url = f"https://{hostinzb}/listeners"

# Execute curl request with -L flag to follow redirects
result = subprocess.run(
    [
        "curl", "-s", "-L", "-H",
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        url
    ],
    capture_output=True,
    text=True
)
if result.returncode != 0:
    print(f"Error executing curl request: {result.stderr}")
    exit(1)

response_text = result.stdout

# Search for the number of listeners in the response text
match = re.search(r'/internet\s*;\s*(\d+)', response_text)
if match:
    listeners_count = int(match.group(1))
    print(f"Number of listeners: {listeners_count}")

    # Send data to Zabbix
    result = subprocess.run(
        ["/usr/local/bin/zabbix_sender", "-z", "127.0.0.1", "-s", hostinzb, "-k", "Count.Listener.Icecast.hostzabbix", "-o", str(listeners_count)],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("Data successfully sent to Zabbix")
        print(f"Zabbix response: {result.stdout}")
    else:
        print(f"Error sending data to Zabbix: {result.stderr}")
        print(f"Standard output: {result.stdout}")
else:
    print("Failed to find listener information.")
