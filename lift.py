"""
Offline-to-online lift calculator (illustrative).

For each TV spot, compare website sessions in the minutes right after it aired
against a baseline taken from the minutes right before it aired. The difference
is the estimated lift from that spot. Results roll up by station so spend can
be compared on cost per lifted session.

Data in this repo is made up for demonstration.
"""
import csv
import datetime as dt
from collections import defaultdict

BASELINE_MINUTES = 10   # window before the spot used as the baseline
RESPONSE_MINUTES = 8    # window after the spot counted as response
FMT = "%Y-%m-%d %H:%M"

def load_sessions(path):
    with open(path, newline="") as f:
        return {dt.datetime.strptime(r["minute"], FMT): int(r["sessions"]) for r in csv.DictReader(f)}

def load_spots(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def spot_lift(sessions, air_time):
    before = [sessions.get(air_time - dt.timedelta(minutes=k)) for k in range(1, BASELINE_MINUTES + 1)]
    after = [sessions.get(air_time + dt.timedelta(minutes=k)) for k in range(1, RESPONSE_MINUTES + 1)]
    before = [v for v in before if v is not None]
    after = [v for v in after if v is not None]
    if not before or not after:
        return None  # not enough data around this spot
    baseline_per_min = sum(before) / len(before)
    return sum(after) - baseline_per_min * len(after)

def main():
    sessions = load_sessions("sessions_by_minute.csv")
    spots = load_spots("spots.csv")
    by_station = defaultdict(lambda: {"lift": 0.0, "cost": 0.0, "spots": 0})

    print(f"{'Spot':<5}{'Station':<11}{'Aired':<18}{'Lift':>7}")
    for s in spots:
        air_time = dt.datetime.strptime(s["air_time"], FMT)
        lift = spot_lift(sessions, air_time)
        if lift is None:
            continue
        print(f"{s['spot_id']:<5}{s['station']:<11}{s['air_time']:<18}{lift:>7.1f}")
        st = by_station[s["station"]]
        st["lift"] += lift
        st["cost"] += float(s["cost_usd"])
        st["spots"] += 1

    print(f"\n{'Station':<11}{'Spots':>6}{'Lift':>8}{'Cost':>9}{'Cost/Lift':>11}")
    for name, st in sorted(by_station.items(), key=lambda kv: kv[1]["cost"] / max(kv[1]["lift"], 0.1)):
        cpl = st["cost"] / st["lift"] if st["lift"] > 0 else float("inf")
        print(f"{name:<11}{st['spots']:>6}{st['lift']:>8.1f}{st['cost']:>9.0f}{cpl:>11.2f}")

if __name__ == "__main__":
    main()
