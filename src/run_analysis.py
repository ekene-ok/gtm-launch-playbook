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


def style(ax):
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=0, labelsize=11, colors=INK)


def chart_access(df):
    df = df[df.channel.notna()].set_index("channel")
    labels = {"self_serve": "Self-serve", "sales_led": "Sales-led"}
    order = ["self_serve", "sales_led"]
    vals = [df.loc[c, "pct_within_24h"] for c in order]
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    bars = ax.bar([labels[c] for c in order], vals, width=0.5,
                  color=[GREY, HIGHLIGHT])
    for b, v, c in zip(bars, vals, order):
        med = df.loc[c, "median_days"]
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}%", ha="center", fontsize=14, color=INK)
        ax.text(b.get_x() + b.get_width() / 2, v + 9, ("instant access" if med < 0.1 else f"median wait {med:.1f} days"), ha="center", fontsize=9.5, color=MUTED)
    ax.axhline(95, color=brand.HAIRLINE, linewidth=1)
    ax.text(1.42, 95, "target 95%", va="center", fontsize=9.5, color=MUTED)
    ax.set_ylim(0, 118)
    style(ax)
    ax.set_title("Sales-led customers waited days for access", loc="left", fontsize=13, color=INK, pad=24)
    ax.text(0, 1.03, "Orders with working access within 24 hours", transform=ax.transAxes, fontsize=10, color=MUTED, va="bottom")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    brand.source(fig, "Simulated launch data; queries in sql/")
    fig.savefig(IMG / "01_access_within_24h.png", facecolor="white")
    plt.close(fig)


def chart_activation(df):
    labels = [w.split(". ")[1] for w in df.wait_for_access]
    vals = df.activation_pct.tolist()
    colors = [GREY] + [HIGHLIGHT] * (len(vals) - 1)
    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)
    bars = ax.bar(labels, vals, width=0.55, color=colors)
    for b, v, n, c in zip(bars, vals, df.orders, colors):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}%", ha="center", fontsize=13, color=INK)
        ax.text(b.get_x() + b.get_width() / 2, 3, f"{n:,} orders", ha="center", fontsize=9, color=INK if c == GREY else "white")
    ax.set_ylim(0, 90)
    style(ax)
    ax.set_title("Activation fell once the wait passed three days", loc="left", fontsize=13, color=INK, pad=24)
    ax.text(0, 1.03, "Accounts using the add-on within 14 days, by wait for access", transform=ax.transAxes, fontsize=10, color=MUTED, va="bottom")
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    brand.source(fig, "Simulated launch data; queries in sql/")
    fig.savefig(IMG / "02_activation_by_wait.png", facecolor="white")
    plt.close(fig)


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
