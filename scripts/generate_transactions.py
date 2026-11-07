"""Create reproducible, entirely fictional payment transactions for portfolio analysis."""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SEED = 20261106
N = 50_000
RNG = random.Random(SEED)
START = datetime(2026, 1, 1)
END = datetime(2026, 4, 1)
OUT = Path(__file__).resolve().parents[1] / "data" / "transactions.csv"
FIELDS = ["transaction_id", "payment_reference", "customer_id", "created_at", "channel", "payment_type", "amount_usd", "status", "processing_seconds", "failure_reason", "is_simulated_duplicate"]
CHANNELS = ["Mobile App", "Web", "Branch", "API"]
CHANNEL_WEIGHTS = [55, 25, 6, 14]
TYPES = ["Transfer", "Bill Payment", "Card Payment", "P2P"]
TYPE_WEIGHTS = [35, 26, 21, 18]
FAILURE_REASONS = ["Insufficient Funds", "Timeout", "Validation Error", "Bank Rejection"]
rows = []
for i in range(1, N + 1):
    dt = START + timedelta(seconds=RNG.randint(0, int((END - START).total_seconds()) - 1))
    channel = RNG.choices(CHANNELS, weights=CHANNEL_WEIGHTS, k=1)[0]
    kind = RNG.choices(TYPES, weights=TYPE_WEIGHTS, k=1)[0]
    amount = round(min(RNG.lognormvariate(4.4, 1.1), 20_000), 2)
    fail_probability = {"Mobile App": 0.035, "Web": 0.05, "Branch": 0.025, "API": 0.065}[channel]
    if dt.hour in (0, 1, 2, 3):
        fail_probability += 0.025
    is_failed = RNG.random() < fail_probability
    status = "Failed" if is_failed else "Completed"
    reason = RNG.choice(FAILURE_REASONS) if is_failed else ""
    delay = RNG.randint(2, 48) + (RNG.randint(180, 900) if RNG.random() < 0.035 else 0)
    rows.append({
        "transaction_id": f"TXN{i:07d}",
        "payment_reference": f"PAY{i:07d}",
        "customer_id": f"CUST{RNG.randint(1, 12000):06d}",
        "created_at": dt.strftime("%Y-%m-%d %H:%M:%S"),
        "channel": channel,
        "payment_type": kind,
        "amount_usd": f"{amount:.2f}",
        "status": status,
        "processing_seconds": delay,
        "failure_reason": reason,
        "is_simulated_duplicate": 0,
    })
# Introduce a repeat payment reference for a subset of transactions.
# These are potential duplicate attempts, NOT proven double charges.
for idx in RNG.sample(range(400, N), 300):
    prior = RNG.randint(max(0, idx - 350), idx - 1)
    rows[idx]["payment_reference"] = rows[prior]["payment_reference"]
    rows[idx]["customer_id"] = rows[prior]["customer_id"]
    rows[idx]["amount_usd"] = rows[prior]["amount_usd"]
    rows[idx]["is_simulated_duplicate"] = 1
RNG.shuffle(rows)
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows)
print(f"Generated {len(rows):,} synthetic transactions: {OUT}")
