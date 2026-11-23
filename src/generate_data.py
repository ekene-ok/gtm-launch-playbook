"""Generate synthetic data for the Harbor Assist launch.

Harbor Docs and Harbor Assist are fictional. Every number here is simulated.
Run: python src/generate_data.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 26
LAUNCH = pd.Timestamp("2026-03-02")
WINDOW_DAYS = 90
OUT = Path(__file__).resolve().parents[1] / "data"


def main():
    rng = np.random.default_rng(SEED)
    OUT.mkdir(exist_ok=True)

    # Accounts: Starter is not eligible for the add-on (BR-01)
    n = 20000
    plan = rng.choice(["Starter", "Team", "Business", "Enterprise"], n, p=[0.15, 0.50, 0.27, 0.08])
    channel = np.where(plan == "Enterprise", "sales_led",
               np.where(plan == "Business", rng.choice(["self_serve", "sales_led"], n, p=[0.45, 0.55]), "self_serve"))
    seats = np.where(plan == "Starter", rng.integers(1, 4, n),
             np.where(plan == "Team", rng.integers(3, 30, n),
              np.where(plan == "Business", rng.integers(20, 250, n), rng.integers(200, 2000, n))))
    accounts = pd.DataFrame({
        "account_id": [f"A{i:05d}" for i in range(n)],
        "plan": plan, "channel": channel, "seats": seats,
        "region": rng.choice(["NA", "EMEA", "APAC"], n, p=[0.55, 0.30, 0.15]),
    })

    # Orders within the 90-day window
    eligible = accounts[accounts.plan != "Starter"].copy()
    p_attach = np.where(eligible.channel == "self_serve", 0.098, 0.052)
    buyers = eligible[rng.random(len(eligible)) < p_attach].copy()
    m = len(buyers)
    order_date = LAUNCH + pd.to_timedelta(rng.integers(0, WINDOW_DAYS - 14, m), unit="D")
    sales = (buyers.channel == "sales_led").to_numpy()
    seats_bought = np.maximum(1, (buyers.seats * rng.uniform(0.3, 1.0, m)).round()).astype(int)
    discount = np.where(sales, rng.choice([0, 5, 10, 15, 20], m, p=[0.35, 0.2, 0.2, 0.15, 0.1]), 0)
    order_type = np.where(sales & (rng.random(m) < 0.32), "mid_term", "new_term")
    list_price = seats_bought * 8.0 * 12  # USD 8 per seat per month, annual
    orders = pd.DataFrame({
        "order_id": [f"O{i:05d}" for i in range(m)],
        "account_id": buyers.account_id.to_numpy(), "channel": buyers.channel.to_numpy(),
        "order_date": order_date, "order_type": order_type, "seats_purchased": seats_bought,
        "discount_pct": discount, "list_amount": list_price,
    })

    # Provisioning: self-serve is instant; sales-led waits for payment (the launch design)
    pay_lag = np.where(sales,
                       np.where(rng.random(m) < 0.33, rng.uniform(0, 0.8, m), rng.gamma(2.2, 3.4, m)),
                       0.0)
    sys_lag = np.where(sales, rng.uniform(0.05, 0.4, m),
                       np.where(rng.random(m) < 0.012, rng.uniform(1, 3, m), rng.uniform(0, 0.02, m)))
    days_to_access = (pay_lag + sys_lag).round(2)
    orders["paid_at"] = orders.order_date + pd.to_timedelta(pay_lag, unit="D")
    orders["provisioned_at"] = orders.order_date + pd.to_timedelta(days_to_access, unit="D")
    orders["days_to_access"] = days_to_access

    # Billing: mid-term upgrades hit a proration rule gap (BR-07)
    expected = orders.list_amount * (1 - orders.discount_pct / 100)
    expected = np.where(orders.order_type == "mid_term", expected * rng.uniform(0.25, 0.95, m), expected).round(2)
    err = np.where(orders.order_type == "mid_term", rng.random(m) < 0.09, rng.random(m) < 0.002)
    billed = np.where(err, expected * rng.choice([1.0 / 0.6, 2.0, 0.5], m), expected).round(2)
    orders["expected_amount"] = expected
    orders["billed_amount"] = billed

    # Usage: activation drops the longer customers wait for access
    p_act = np.clip(0.71 - 0.045 * days_to_access, 0.22, 0.75)
    orders["activated_14d"] = rng.random(m) < p_act
    orders["active_seat_share_14d"] = np.where(orders.activated_14d, rng.uniform(0.3, 0.8, m), rng.uniform(0, 0.29, m)).round(3)

    accounts.to_csv(OUT / "accounts.csv", index=False)
    orders.to_csv(OUT / "orders.csv", index=False)
    print(f"accounts: {len(accounts):,}  orders: {len(orders):,}  -> {OUT}")


if __name__ == "__main__":
    main()
