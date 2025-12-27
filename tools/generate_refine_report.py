import json
from pathlib import Path


def build_always_return_policy_steps(hd_steps: list[dict], thr_steps: list[dict]) -> list[dict]:
    if len(hd_steps) != len(thr_steps):
        raise ValueError(f"policy_steps length mismatch: hd={len(hd_steps)} threshold50={len(thr_steps)}")

    out: list[dict] = []
    for a, b in zip(hd_steps, thr_steps):
        candidates = [s for s in (a, b) if s is not None]
        if not candidates:
            raise ValueError("empty candidates while building always_return")

        # "minério que volta o refino" => downgrade_amount > 0
        returning = [s for s in candidates if (s.get("downgrade_amount") or 0) > 0]
        pool = returning or candidates

        # Tie-break: higher success chance (rate_10000)
        pool = sorted(pool, key=lambda s: (s.get("rate_10000") or 0), reverse=True)
        out.append(pool[0])

    return out


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src = repo_root / "assets" / "analysis" / "refine_report_data.json"
    dst = repo_root / "assets" / "analysis" / "refine_report_data.generated.json"

    data = json.loads(src.read_text(encoding="utf-8"))

    series_map: dict = data.get("series") or {}
    for series_key, series in series_map.items():
        policies = series.get("policies") or {}
        if "hd" not in policies or "threshold50" not in policies:
            continue

        hd_steps = policies["hd"].get("policy_steps") or []
        thr_steps = policies["threshold50"].get("policy_steps") or []
        always_steps = build_always_return_policy_steps(hd_steps, thr_steps)

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

