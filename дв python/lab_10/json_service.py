from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List

import requests

LVIV_LAT = 49.8397
LVIV_LON = 24.0297
TIMEZONE = "Europe/Kyiv"

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


@dataclass(frozen=True)
class Paths:
    root: Path
    raw_dir: Path
    prepared_dir: Path
    results_dir: Path


def get_paths() -> Paths:
    root = Path(__file__).resolve().parent
    data_dir = root / "data"
    return Paths(
        root=root,
        raw_dir=data_dir / "raw",
        prepared_dir=data_dir / "prepared",
        results_dir=data_dir / "results",
    )


def ensure_dirs() -> None:
    p = get_paths()
    p.raw_dir.mkdir(parents=True, exist_ok=True)
    p.prepared_dir.mkdir(parents=True, exist_ok=True)
    p.results_dir.mkdir(parents=True, exist_ok=True)


def _parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def raw_json_path(date_str: str) -> Path:
    ensure_dirs()
    p = get_paths()
    return p.raw_dir / f"lviv_{date_str}.json"


def prepared_csv_path(date_str: str) -> Path:
    ensure_dirs()
    p = get_paths()
    return p.prepared_dir / f"prepared_{date_str}.csv"


def fetch_weather_json(date_str: str, timeout_s: int = 25) -> Dict:
    d = _parse_date(date_str)
    today = date.today()
    url = ARCHIVE_URL if d <= today else FORECAST_URL

    params = {
        "latitude": LVIV_LAT,
        "longitude": LVIV_LON,
        "hourly": "temperature_2m,windspeed_10m,precipitation",
        "wind_speed_unit": "ms",
        "precipitation_unit": "mm",
        "temperature_unit": "celsius",
        "timeformat": "iso8601",
        "timezone": TIMEZONE,
        "start_date": date_str,
        "end_date": date_str,
    }

    r = requests.get(url, params=params, timeout=timeout_s)
    r.raise_for_status()
    return r.json()


def ensure_raw_json(date_str: str, retries: int = 2) -> Path:
    path = raw_json_path(date_str)
    if path.exists():
        return path

    last_exc: Exception | None = None
    for _ in range(retries + 1):
        try:
            data = fetch_weather_json(date_str)
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return path
        except Exception as e:
            last_exc = e

    raise RuntimeError(f"Не вдалося отримати дані за {date_str}: {last_exc}") from last_exc


def _validate_open_meteo_structure(data: Dict) -> None:
    if "hourly" not in data:
        raise ValueError("JSON не містить ключ 'hourly'.")
    hourly = data["hourly"]
    for k in ("time", "temperature_2m", "windspeed_10m", "precipitation"):
        if k not in hourly:
            raise ValueError(f"JSON hourly не містить ключ '{k}'.")
    n = len(hourly["time"])
    for k in ("temperature_2m", "windspeed_10m", "precipitation"):
        if len(hourly[k]) != n:
            raise ValueError(f"Довжини масивів не збігаються: time vs {k}.")


def prepare_csv_for_cs(date_str: str) -> Path:
    ensure_dirs()
    raw_path = ensure_raw_json(date_str)
    data = json.loads(raw_path.read_text(encoding="utf-8"))
    _validate_open_meteo_structure(data)

    hourly = data["hourly"]
    times = hourly["time"]
    temps = hourly["temperature_2m"]
    winds = hourly["windspeed_10m"]
    precs = hourly["precipitation"]

    out_path = prepared_csv_path(date_str)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "temp_c", "wind_ms", "precip_mm"])
        for t, tc, wm, pm in zip(times, temps, winds, precs):
            w.writerow([t, tc, wm, pm])

    return out_path


def load_prepared_csv(date_str: str) -> Dict[str, List]:
    path = prepared_csv_path(date_str)
    if not path.exists():
        prepare_csv_for_cs(date_str)

    times: List[str] = []
    temps: List[float] = []
    winds: List[float] = []
    precs: List[float] = []

    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            times.append(row["timestamp"])
            temps.append(float(row["temp_c"]))
            winds.append(float(row["wind_ms"]))
            precs.append(float(row["precip_mm"]))

    return {"time": times, "temp_c": temps, "wind_ms": winds, "precip_mm": precs}


def compute_python_summary(date_str: str) -> Dict:
    d = load_prepared_csv(date_str)
    temps = d["temp_c"]
    winds = d["wind_ms"]
    precs = d["precip_mm"]

    if not temps:
        raise ValueError("Немає даних у prepared.csv.")

    avg_temp = sum(temps) / len(temps)
    total_prec = sum(precs)

    return {
        "date": date_str,
        "temp_min": min(temps),
        "temp_max": max(temps),
        "temp_avg": avg_temp,
        "wind_max": max(winds) if winds else None,
        "precip_sum": total_prec,
        "points": len(temps),
    }
