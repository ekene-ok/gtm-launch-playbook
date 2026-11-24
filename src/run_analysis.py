"""Run the post-launch analysis: SQL results to results/, charts to images/.

Run: python src/run_analysis.py   (generates the synthetic data first if needed)
"""
from pathlib import Path
import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent))
import brand_style as brand

ROOT = Path(__file__).resolve().parents[1]
DATA, SQL, RES, IMG = ROOT / "data", ROOT / "sql", ROOT / "results", ROOT / "images"
HIGHLIGHT, GREY, INK, MUTED = brand.PROJECT["gtm-launch-playbook"], brand.CONTEXT, brand.INK, brand.MUTED


def load():
    if not (DATA / "orders.csv").exists():
        import generate_data
        generate_data.main()
    con = duckdb.connect()
    con.execute(f"CREATE TABLE accounts AS SELECT * FROM read_csv_auto('{DATA / 'accounts.csv'}')")
    con.execute(f"CREATE TABLE orders AS SELECT * FROM read_csv_auto('{DATA / 'orders.csv'}')")
    return con


def run(con):
    RES.mkdir(exist_ok=True)
    out = {}
    for f in sorted(SQL.glob("*.sql")):
        df = con.execute(f.read_text()).df()
        df.to_csv(RES / f"{f.stem}.csv", index=False)
        out[f.stem] = df
        print(f"\n== {f.stem} ==\n{df.to_string(index=False)}")
    return out


def chart_access(df):
    df = df[df.channel.notna()].set_index("channel")
    vals = [df.loc[c, "pct_within_24h"] for c in ["self_serve", "sales_led"]]
    med = df.loc["sales_led", "median_days"]
    fig, ax = brand.chart(height=3.4, label_in=1.15)
    brand.hbar(ax, ["Self-serve", "Sales-led"], vals, {1}, lambda v: f"{v:.0f}%", HIGHLIGHT, xmax=100)
    ax.axvline(95, color=brand.HAIRLINE, linewidth=1, zorder=0)
    ax.text(95, 1.5, "95% target", ha="center", va="bottom", fontsize=9, color=MUTED)
    brand.titles(fig, "Sales-led customers waited days for access",
                 f"Orders with working access within 24 hours. Sales-led median wait: {med:.1f} days")
    brand.credit(fig, "Simulated launch data; queries in sql/")
    brand.save(fig, IMG / "01_access_within_24h.png")


def chart_activation(df):
    labels = [f"{w.split('. ')[1]}\n{n:,} orders" for w, n in zip(df.wait_for_access, df.orders)]
    fig, ax = brand.chart(height=4.2, label_in=0.0, xaxis=True, right_in=0.3)
    brand.vbar(ax, labels, df.activation_pct.tolist(), set(range(1, len(df))), lambda v: f"{v:.0f}%", HIGHLIGHT)
    brand.titles(fig, "Activation fell once the wait passed three days",
                 "Accounts using the add-on within 14 days, by wait for access")
    brand.credit(fig, "Simulated launch data; queries in sql/")
    brand.save(fig, IMG / "02_activation_by_wait.png")


def main():
    IMG.mkdir(exist_ok=True)
    out = run(load())
    chart_access(out["02_time_to_access"])
    chart_activation(out["03_activation_by_wait"])
    print("\ncharts saved to images/")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    main()
