import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# URL we want to monitor
URL = "https://midran82.github.io/fjellby-it/"

# JSON output file
OUTPUT = Path("output/status.json")


def check_website():
    request = Request(
        URL,
        headers={"User-Agent": "Fjellby-Monitor/1.0"}
    )

    start_time = time.perf_counter()

    try:
        with urlopen(request, timeout=10) as response:
            elapsed_time = time.perf_counter() - start_time

            response_time = round(elapsed_time * 1000)
            http_status = response.status

            if 200 <= http_status < 400:
                status = "online"
            else:
                status = "warning"

            return status, http_status, response_time

    except HTTPError as error:
        elapsed_time = time.perf_counter() - start_time

        return (
            "offline",
            error.code,
            round(elapsed_time * 1000)
        )

    except URLError:
        return "offline", None, None


status, http_status, response_time = check_website()

data = {
    "status": status,
    "http_status": http_status,
    "response_time": response_time,
    "last_update": datetime.now(ZoneInfo("Europe/Oslo")).strftime("%Y-%m-%d %H:%M:%S")
}

OUTPUT.parent.mkdir(exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

print("Fjellby Monitor")
print("----------------")
print(f"Target:        {URL}")
print(f"Status:        {status}")
print(f"HTTP status:   {http_status}")
print(f"Response time: {response_time} ms")
print(f"Last update:   {data['last_update']}")