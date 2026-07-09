from __future__ import annotations

import json
import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Callable

import json_service


def setup_logger() -> logging.Logger:
    logs_dir = Path(__file__).resolve().parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("WeatherPulseLviv")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fh = logging.FileHandler(logs_dir / "app.log", encoding="utf-8")
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


LOGGER = setup_logger()

MODE_TO_TASK = {
    "summary": "task1_top_temp",
    "compare": "task2_profile_compare",
    "comfort": "task3_comfort_hours",
    "jumps": "task4_top_temp_jumps",
}
TWO_DAY_TASKS = {"task2_profile_compare", "task4_top_temp_jumps"}


def cs_exe_path() -> Path:
    return Path(__file__).resolve().parent / "cs_release" / "WeatherAnalytics1.exe"


def result_json_path(date_str: str, mode: str) -> Path:
    p = json_service.get_paths()
    p.results_dir.mkdir(parents=True, exist_ok=True)
    return p.results_dir / f"result_{mode}_{date_str}.json"


def run_cs(
    prepared_csv1: Path,
    out_json: Path,
    task: str,
    prepared_csv2: Optional[Path] = None,
    comfort_params: Optional[Dict[str, float]] = None,
) -> Dict:
    """
    WeatherAnalytics.exe <csv1> <out_json> <task> [csv2] [options...]
    Для task3_comfort_hours: options = targetTemp tempTol maxWind maxPrecip
    """
    exe = cs_exe_path()
    if not exe.exists():
        LOGGER.warning("C# exe not found: %s", exe)
        return {
            "error": "C# module not found",
            "exe": str(exe),
            "hint": "У cs_release мають бути exe + dll + runtimeconfig + deps (або self-contained publish).",
        }

    cmd = [str(exe), str(prepared_csv1), str(out_json), task]

    if task in TWO_DAY_TASKS:
        if prepared_csv2 is None:
            return {"error": "Second day CSV is required", "task": task}
        cmd.append(str(prepared_csv2))

    if task == "task3_comfort_hours" and comfort_params:
        cmd.extend(
            [
                str(comfort_params.get("target_temp", 20.0)),
                str(comfort_params.get("temp_tol", 2.0)),
                str(comfort_params.get("max_wind", 5.0)),
                str(comfort_params.get("max_precip", 0.2)),
            ]
        )

    LOGGER.info("Run C#: %s", " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        LOGGER.error("C# failed rc=%s stderr=%s", proc.returncode, proc.stderr.strip())
        return {
            "error": "C# failed",
            "returncode": proc.returncode,
            "stderr": proc.stderr.strip(),
        }

    if out_json.exists():
        try:
            return json.loads(out_json.read_text(encoding="utf-8"))
        except Exception as e:
            return {"error": "Invalid result.json", "details": str(e), "path": str(out_json)}

    s = proc.stdout.strip()
    if s.startswith("{"):
        try:
            return json.loads(s)
        except Exception:
            pass

    return {"error": "No result produced", "stdout": proc.stdout.strip()}


def _auto_yesterday(date_str: str) -> str:
    d1 = datetime.strptime(date_str, "%Y-%m-%d").date()
    d2 = d1 - timedelta(days=1)
    return d2.strftime("%Y-%m-%d")


def pipeline(date1_str: str, mode: str = "summary", date2_str: Optional[str] = None) -> Dict:
    """
    date2_str використовується тільки для режимів compare/jumps.
    Якщо не задано — береться вчора відносно date1_str.
    """
    LOGGER.info("=== Pipeline start: date1=%s date2=%s mode=%s ===", date1_str, date2_str, mode)

    task = MODE_TO_TASK.get(mode, "task1_top_temp")

    # 1) raw+prepared для day1
    raw1 = json_service.ensure_raw_json(date1_str)
    prepared1 = json_service.prepare_csv_for_cs(date1_str)

    # 2) якщо задача на 2 дні — готуємо day2
    used_date2 = None
    prepared2 = None

    if task in TWO_DAY_TASKS:
        used_date2 = (date2_str or "").strip() or _auto_yesterday(date1_str)
        json_service.ensure_raw_json(used_date2)
        prepared2 = json_service.prepare_csv_for_cs(used_date2)

    out_json = result_json_path(date1_str, mode)

    comfort_params = {"target_temp": 20.0, "temp_tol": 2.0, "max_wind": 5.0, "max_precip": 0.2}

    cs_result = run_cs(
        prepared_csv1=prepared1,
        out_json=out_json,
        task=task,
        prepared_csv2=prepared2,
        comfort_params=comfort_params,
    )

    py_summary = json_service.compute_python_summary(date1_str)

    LOGGER.info("=== Pipeline end: date1=%s mode=%s ===", date1_str, mode)

    return {
        "python_summary": py_summary,
        "cs_result": cs_result,
        "meta": {
            "mode": mode,
            "task": task,
            "date1": date1_str,
            "date2": used_date2,
        },
        "files": {
            "raw_json_day1": str(raw1),
            "prepared_csv_day1": str(prepared1),
            "prepared_csv_day2": str(prepared2) if prepared2 else None,
            "result_json": str(out_json),
        },
    }


def main() -> None:
    import gui
    gui.start_gui(pipeline)


if __name__ == "__main__":
    main()
