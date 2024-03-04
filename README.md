# Build and run container

## Build container

```bash
docker build -t jromeo/plex_session_metrics:0.0.1.RELEASE .
```

## Create config directory and .env file

create a directory for the docker to mount to mount
```bash
mkdir ./plex_session_merics/config
```

Create .env file and place into config\
.env file needs to include 3 variables

.env:
```bash
PLEX_URL=<Plex hostname>
PLEX_PORT=<Plex Port>
PLEX_API_TOKEN=Xxxxx-xxxxxxx
```

## Start container

```bash
docker container run -d --name plex_session_metrics -p 8989:8989 -v ./plex_session_merics/config:/app/config jromeo/plex_session_metrics:0.0.1.RELEASE
```
