# Solvearr: Cloudflare Bypass Proxy API (Better FlareSolverr Alternative)

This project, **Solvearr**, is a Cloudflare bypass proxy API designed to access and scrape sites protected by Cloudflare, such as [https://www.1377x.to/](https://www.1377x.to/). It provides a simple HTTP API that is fully compatible with the [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) specification, making it a drop-in replacement for existing integrations.

## Features
- Bypasses Cloudflare and similar anti-bot protections using advanced TLS fingerprint tampering (no browser emulation).
- More lightweight and memory-efficient than FlareSolverr, as it does not use browser emulation.
- Compatible with **Prowlarr**, **Sonarr**, and **Radarr** as an indexer proxy.
- Implements the same API as FlareSolverr for seamless integration.
- Supports GET and POST requests, cookies, custom headers, and proxy settings.

## Installation

### Supported Architectures
The container supports the following architectures:
- `linux/amd64`: Standard desktop/laptop computers
- `linux/arm64`: Modern Raspberry Pi (3, 4, and newer)

### Docker Run
```bash
docker run -d \
  --name=solvearr \
  -p 8191:8191 \
  --restart unless-stopped \
  nabilak/solvearr
```

### Docker Compose
```yaml
version: "3"
services:
  solvearr:
    image: nabilak/solvearr
    container_name: solvearr
    ports:
      - 8191:8191
    restart: unless-stopped
```

### Parameters
| Parameter | Function |
|-----------|----------|
| `-p 8191:8191` | The port the application runs on |
| `--restart unless-stopped` | Restart the container unless it is explicitly stopped |

### Manual Installation
If you prefer to run Solvearr without Docker, follow these steps:

1. Ensure you have Python installed:
```bash
python --version
```

2. Install uv (Python package installer):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Clone the repository:
```bash
git clone https://github.com/nabilak/solvearr.git
cd solvearr
```

4. Install dependencies and the project:
```bash
uv sync --frozen --no-dev
```

5. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8191
```

The application will be available at `http://localhost:8191`.

## Usage Example

You can set up **Solvearr** as an indexer proxy in **Prowlarr**, **Sonarr** or **Radarr** to bypass Cloudflare for your indexers. Here's how:

1. Go to **Settings > Indexers** in Prowlarr.
2. Click the **+** button to add a new indexer proxy.
3. Select **FlareSolverr** as the proxy type.
4. Set the **Host** field to your Solvearr server URL, e.g.:
   - `http://localhost:8000/` (if running locally)
5. Set the **Request Timeout** as desired (e.g., `60` seconds).
6. Click **Test** to verify the connection.
7. Click **Save** to apply the settings.

<img src="https://i.imgur.com/UZMGuuB.png" alt="Prowlarr Indexer Proxy Setup" width="1000"/>


### Manual Request Example

Send a request to open a Cloudflare-protected site:
```bash
curl -X POST "http://localhost:8000/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://www.1377x.to/",
    "maxTimeout": 60000
  }'
```

## API Specification

### Endpoint
`POST /v1`

### Request Body
JSON object with the following fields:

| Parameter           | Type     | Required | Description                                                                 |
|---------------------|----------|----------|-----------------------------------------------------------------------------|
| cmd                 | string   | Yes      | "request.get" or "request.post"                                            |
| url                 | string   | Yes      | Target URL to open                                                          |
| maxTimeout          | integer  | No       | Timeout in milliseconds (default: 60000)                                    |
| cookies             | array    | No       | List of cookies (objects with name/value)                                   |
| returnOnlyCookies   | boolean  | No       | If true, only cookies are returned                                          |
| proxy               | object   | No       | Proxy settings (e.g., {"url": "http://127.0.0.1:8888"})                   |
| postData            | string   | No       | POST data (for "request.post"), must be x-www-form-urlencoded string        |

#### Example Request (GET)
```json
{
  "cmd": "request.get",
  "url": "https://www.1377x.to/",
  "maxTimeout": 60000
}
```

#### Example Request (POST)
```json
{
  "cmd": "request.post",
  "url": "https://somesite.com/login",
  "postData": "username=foo&password=bar",
  "maxTimeout": 60000
}
```

### Response Body
```json
{
  "solution": {
    "url": "https://www.1377x.to/",
    "status": 200,
    "headers": { ... },
    "response": "<html>...</html>",
    "cookies": [ ... ],
    "userAgent": "..."
  },
  "status": "ok",
  "message": "",
  "startTimestamp": 1594872947467,
  "endTimestamp": 1594872949617,
  "version": "1.0.0"
}
```

## Integration

You can configure Prowlarr, Sonarr, or Radarr to use this API as a FlareSolverr endpoint for indexer proxying and Cloudflare bypass.
