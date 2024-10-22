# icecast-statistic-in-zabbix
# Icecast Listener Stats Reporter

## Overview
This repository provides a set of scripts to monitor the number of listeners on an Icecast streaming server and integrate the results into a Zabbix monitoring setup. The solution is implemented using Python, a Flask web application, Nginx, and Zabbix.

### Key Components:
- **Icecast (KH fork version 2.0.4-kh22)**: Streaming server for delivering audio streams.
- **Nginx (version 1.26.2)**: Reverse proxy for the Flask web service that exposes listener data.
- **Python (with Flask, Requests, lxml, re, subprocess)**: Python scripts for retrieving and handling listener data.
- **Zabbix (version 6.0.8)**: Server for monitoring metrics, including listener counts.

## Requirements
- **Operating System**: Ubuntu 24.04
- **Icecast KH Version**: 2.0.4-kh22 [(GitHub Repository)](https://github.com/karlheyes/icecast-kh)
- **Nginx Version**: 1.26.2
- **Python Modules**:
  - Flask
  - Requests
  - lxml
  - re
  - subprocess
- **Zabbix Version**: 6.0.8

## System Architecture
This solution uses the following architecture:

1. **Icecast Server**: Streams audio content and provides listener statistics. The listener stats are fetched using a Python script.
2. **Flask Web Application**: Runs on the Icecast server. It fetches listener data from Icecast and provides an endpoint for Nginx to access.
3. **Nginx**: Acts as a reverse proxy that listens for requests at `/listeners` and forwards them to the Flask app running on localhost.
4. **Zabbix Server**: A Zabbix agent runs a script that queries listener data every minute, parses it, and sends it back to Zabbix using `zabbix_sender`.

## How It Works
### 1. Icecast Flask Service
- The script `icecast-flask.py` runs a local Flask server that retrieves listener information from the local Icecast server.
- **Service File**: The Flask application runs as a systemd service (`icecast-flask.service`) to ensure it's always running.
- When a request is made to `https://myserver/listeners`, the Flask app gathers listener data and returns it.

### 2. Nginx Configuration
Nginx acts as a reverse proxy for the Flask application, making it available publicly under `/listeners`. Below is the configuration used in Nginx:

```nginx
location = /listeners {
    proxy_pass http://127.0.0.1:9000; # Forward to Flask application
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```
This setup ensures that anyone accessing `https://myserver/listeners` will receive the data from the Flask server, which ultimately collects it from Icecast.

### 3. Zabbix Server Integration
- On the Zabbix server, a cron job runs the script `icecast-req-stat.py` every minute.
- This script uses `curl` to fetch listener data from the web server's `/listeners` endpoint, parses it, and sends the data to Zabbix using `zabbix_sender`.
- **Item Configuration** in Zabbix for Listener Count:
  - **Name**: `Get Listeners Data`
  - **Type**: `Zabbix trapper`
  - **Key**: `Count.Listener.Icecast.hostzabbix`
  - **Type of information**: `Numeric (unsigned)`

### Scripts
1. **icecast-flask.py**: A Flask application script that interacts with the local Icecast server to obtain the current number of listeners. It serves the data at `http://127.0.0.1:9000/listeners`.
2. **icecast-req-stat.py**: A script that uses `curl` to fetch listener data from the Flask app and sends the parsed count to Zabbix.

## Installation and Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/repository.git
   cd repository
   ```

2. **Install Required Packages**
   ```bash
   sudo apt update
   sudo apt install nginx python3 python3-pip
   pip3 install flask requests lxml
   ```

3. **Setup Flask Application**
   - Copy `icecast-flask.py` to a suitable directory.
   - Create a systemd service to run the Flask application (`icecast-flask.service`).
   - Enable and start the service:
     ```bash
     sudo systemctl enable icecast-flask.service
     sudo systemctl start icecast-flask.service
     ```

4. **Configure Nginx**
   - Add the above location configuration to Nginx and restart:
     ```bash
     sudo systemctl restart nginx
     ```

5. **Configure Zabbix**
   - Add the script `icecast-req-stat.py` to the Zabbix server.
   - Set up a cron job to run this script every minute:
     ```bash
     */1 * * * * /usr/bin/python3 /path/to/icecast-req-stat.py
     ```

6. **Zabbix Configuration**
   - Create a new item in Zabbix with the given configuration.

## Example Usage
To manually run the listener count script and see the output:
```bash
./icecast-req-stat.py
```
This command will fetch the current number of listeners and push the data to Zabbix.

## Contributing
If you would like to contribute to this project, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.

