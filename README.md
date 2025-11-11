# Plex Session Metrics

## Overview

Plex Session Metrics is a Python application that monitors active Plex Media Server sessions and exposes session data as Prometheus metrics. It periodically queries the Plex API to gather information about current users, their devices, IP addresses, and stream bandwidth consumption, then makes this data available for monitoring and alerting via Prometheus.

## Project Description

This project bridges Plex Media Server and Prometheus monitoring by:

- **Fetching Active Sessions**: Connects to a Plex Media Server instance via its API to retrieve real-time information about active streaming sessions
- **Extracting Session Details**: Captures user information, device details, remote IP addresses, bandwidth consumption, and content being watched
- **Exposing Metrics**: Exposes this data as Prometheus metrics on port 8989, allowing integration with monitoring stacks like Prometheus + Grafana
- **Continuous Monitoring**: Runs continuously, updating metrics every 5 minutes to provide up-to-date session information

## Technical Stack

- **Python 3.9**: Core application runtime
- **Prometheus Client**: Exports metrics in Prometheus format
- **Requests**: HTTP library for API communication with Plex
- **python-dotenv**: Manages environment configuration variables
- **Docker**: Containerization for easy deployment

## Metrics Exposed

The application exposes a single Prometheus metric:
- `Plex_Session_User`: A gauge metric with labels for:
  - `User`: Plex user account name
  - `ip_address`: Remote public IP address of the streaming client
  - `device`: Device name/model streaming content
  - `bandwith`: Bandwidth consumption in Mbps
  - `watching`: Title of content currently being watched

## Build and Run

### Build Container

```bash
docker build -t jromeo/plex_session_metrics:0.0.1.RELEASE .
```

### Create Config Directory and .env File

Create a directory for Docker to mount:
```bash
mkdir ./plex_session_metrics/config
```

Create a `.env` file in the `config` directory with the following variables:

```bash
PLEX_URL=<Plex hostname>
PLEX_PORT=<Plex Port>
PLEX_API_TOKEN=Xxxxx-xxxxxxx
```

### Start Container

```bash
docker container run -d --name plex_session_metrics -p 8989:8989 -v ./plex_session_metrics/config:/app/config jromeo/plex_session_metrics:0.0.1.RELEASE
```

### Access Metrics

Once running, Prometheus metrics are available at:
```
http://localhost:8989/metrics
```

## Configuration

The application requires three environment variables to be set in the `.env` file:

- `PLEX_URL`: Hostname or IP address of your Plex Media Server
- `PLEX_PORT`: Port number on which Plex is running (typically 32400)
- `PLEX_API_TOKEN`: Your Plex API token for authentication

## Requirements

See `requirements.txt` for full dependency list:
- requests==2.28.1
- python-dotenv==1.0.1
- prometheus_client==0.20.0
