# Ground station server

The web interface for the ACRUX-2 ground station.

- `frontend`: Dashboard built with Dash/Plotly
- `backend`: REST API built on Flask

## Prerequisites

The easiest way to get started is with Docker.

- For most devices, see https://docs.docker.com/get-docker/
- For Raspberry Pi, see https://docs.docker.com/engine/install/debian/

Tests are written using `pytest` which can be installed using

```sh
pip install pytest
```

## Building and running

Once you have Docker installed, running the project involves

```sh
git clone https://github.com/MelbourneSpaceProgram/ground-station-server
cd ground-station-server
docker compose up
```

Sometimes you will need to rebuild the image to ensure the latest changes are included

```sh
docker compose up --build
```

Stopping the project

```sh
docker compose down
```
