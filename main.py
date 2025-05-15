from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import tls_client
import uvicorn
from util import get_version, get_user_agent, IndexResponse, HealthResponse

app = FastAPI()

@app.get("/")
def index():
    res = IndexResponse(
        msg="Solvearr is ready!",
        version=get_version(),
        userAgent=get_user_agent()
    )
    return res.model_dump()

@app.get("/health")
def health():
    res = HealthResponse(status="ok")
    return res.model_dump()

@app.post("/v1")
async def proxy_tls_client(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"status": "error", "message": "No JSON body provided."}, status_code=400)
    
    # Accept both PascalCase/camelCase and lowercase keys
    data = {k.lower(): v for k, v in data.items()}
    cmd = data.get("cmd")
    url = data.get("url")
    max_timeout = data.get("maxtimeout", 60000)
    cookies = data.get("cookies", [])
    post_data = data.get("postdata")
    proxy = data.get("proxy")
    return_only_cookies = data.get("returnonlycookies", False)
    session = tls_client.Session(
        client_identifier="chrome120",
        random_tls_extension_order=True
    )

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="120", "Google Chrome";v="120", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': get_user_agent(),
    }

    # Add cookies to session if provided
    if cookies:
        for cookie in cookies:
            session.cookies.set(cookie["name"], cookie["value"])
    # Add proxy if provided (tls_client supports proxies via session.proxies)
    if proxy and "url" in proxy:
        session.proxies = {"http": proxy["url"], "https": proxy["url"]}

    start_ts = int(time.time() * 1000)
    try:
        if cmd == "request.get":
            resp = session.get(url, headers=headers, timeout_seconds=int(max_timeout/1000))
        elif cmd == "request.post":
            resp = session.post(url, headers=headers, data=post_data, timeout_seconds=int(max_timeout/1000))
        else:
            return JSONResponse({"status": "error", "message": "Unknown cmd"}, status_code=400)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
    end_ts = int(time.time() * 1000)


    # Format cookies for response
    cookie_list = []
    for c in session.cookies:
        cookie_list.append({
            "name": c.name,
            "value": c.value,
            "domain": c.domain,
            "path": c.path,
            "expires": c.expires,
            "size": len(c.value),
            "httpOnly": getattr(c, "_rest", {}).get("HttpOnly", False),
            "secure": c.secure,
            "session": c.expires is None,
            "sameSite": getattr(c, "_rest", {}).get("SameSite", "None")
        })

    
    # Prepare response
    solution = {
        "url": str(resp.url),
        "status": resp.status_code,
        "headers": dict(resp.headers),
        "response": resp.text if not return_only_cookies else None,
        "cookies": cookie_list,
        "userAgent": headers["user-agent"]
    }
    return {
        "solution": solution,
        "status": "ok",
        "message": "",
        "startTimestamp": start_ts,
        "endTimestamp": end_ts,
        "version": get_version()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8191)
