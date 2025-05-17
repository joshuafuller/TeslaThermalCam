# Watchtower

Watchtower is a utility that monitors running Docker containers and automatically updates them whenever a new image is available. This project includes a Watchtower service in `docker-compose.yml` so your Raspberry Pi always runs the latest container image.

## How it Works

The Watchtower service connects to the Docker daemon and periodically checks if a newer image exists for each running container. If an update is found, Watchtower gracefully stops the existing container, pulls the new image and restarts the container using the same options. This means your TeslaThermalCam instance can stay current without manual intervention.

The relevant section in `docker-compose.yml`:

```yaml
  watchtower:
    image: containrrr/watchtower
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    command: --interval 30
    restart: always
```

## Configuration

- **Update interval**: The `--interval` option defines how often Watchtower checks for updated images, in seconds. Adjust this value in `docker-compose.yml` to suit your needs. For example, `--interval 86400` checks once a day.
- **Enabling or disabling**: Comment out the entire `watchtower` service block in `docker-compose.yml` to disable automatic updates. Re‑enable it by uncommenting the block.

After editing `docker-compose.yml`, restart the stack with `docker compose up -d` for changes to take effect.
