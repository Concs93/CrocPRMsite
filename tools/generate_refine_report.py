import json
import csv
from pathlib import Path


def _to_int(v: str) -> int:
    try:
        return int(v)
    except Exception:
        return 0


def load_refine_rows(csv_path: Path) -> dict[tuple[str, int, int], list[dict]]:
    """
    Map (group, item_level, refine_level) -> list[step dict]
    Step dict uses the same shape as refine_report_data.json policy_steps.
    """
    rows: dict[tuple[str, int, int], list[dict]] = {}
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            group = (r.get("group") or "").strip()
            item_level = _to_int(r.get("item_level") or "0")
            refine_level = _to_int(r.get("refine_level") or "0")
            if not group or item_level <= 0 or refine_level <= 0:
                continue

            step = {
                "refine_level": refine_level,
                "cost_type": (r.get("cost_type") or "").strip(),
                "rate_10000": _to_int(r.get("rate_10000") or "0"),
                "breaking_rate_10000": _to_int(r.get("breaking_rate_10000") or "0"),
                "downgrade_amount": _to_int(r.get("downgrade_amount") or "0"),
                "zeny": _to_int(r.get("zeny") or "0"),
                "material": (r.get("material") or "").strip(),
            }
            rows.setdefault((group, item_level, refine_level), []).append(step)

    return rows


def build_always_return_policy_steps_from_rows(
    *,
    group: str,
    item_level: int,
    max_refine: int,
    rows_map: dict[tuple[str, int, int], list[dict]],
) -> list[dict]:
    steps: list[dict] = []
    for refine_level in range(1, max_refine + 1):
        candidates = rows_map.get((group, item_level, refine_level), [])
        if not candidates:
            raise ValueError(f"missing refine rows for {group}|{item_level} refine_level={refine_level}")

        # "minério q volta o refino" => downgrade_amount > 0
        returning = [s for s in candidates if (s.get("downgrade_amount") or 0) > 0]
        pool = returning or candidates

        # Tie-break: higher success chance
        pool = sorted(pool, key=lambda s: (s.get("rate_10000") or 0), reverse=True)
        steps.append(pool[0])

    return steps


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src = repo_root / "assets" / "analysis" / "refine_report_data.json"
    dst = repo_root / "assets" / "analysis" / "refine_report_data.generated.json"
    refine_csv = repo_root / "assets" / "analysis" / "refine" / "refine_re_long.csv"

    data = json.loads(src.read_text(encoding="utf-8"))
    rows_map = load_refine_rows(refine_csv)

    series_map: dict = data.get("series") or {}
    for series_key, series in series_map.items():
        policies = series.get("policies") or {}
        if "hd" not in policies or "threshold50" not in policies:
            continue

        group = series.get("group")
        item_level = series.get("item_level")
        if not group or not item_level:
            continue

        # Use existing policy length as max_refine
        hd_steps = policies["hd"].get("policy_steps") or []
        max_refine = len(hd_steps) if hd_steps else 10

        always_steps = build_always_return_policy_steps_from_rows(
            group=str(group),
            item_level=int(item_level),
            max_refine=max_refine,
            rows_map=rows_map,
        )

        # Preserve shape used by existing policies (policy_steps + from0 if present)
        from0 = policies.get("threshold50", {}).get("from0")
        payload = {"policy_steps": always_steps}
        if from0 is not None:
            payload["from0"] = from0

        policies["always_return"] = payload

    dst.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote: {dst}")


if __name__ == "__main__":
    main()

