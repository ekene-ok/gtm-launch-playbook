# 03. RACI and Decision Log

## RACI

R = Responsible (does the work), A = Accountable (signs off), C = Consulted, I = Informed

| Workstream | Program lead | Product | Sales Ops | Finance | Engineering | Enablement | Support | Analytics |
|---|---|---|---|---|---|---|---|---|
| Scope and success criteria | A | C | C | C | C | I | I | C |
| Eligibility and pricing rules | R | A | C | C | I | I | I | I |
| Self-serve checkout | C | A | I | C | R | I | I | I |
| Quotes and order forms | C | I | A | C | I | C | I | I |
| Proration and invoicing | C | I | C | A | R | I | I | I |
| Access and entitlement | C | C | I | C | A | I | C | I |
| Sales enablement | C | C | C | I | I | A | I | I |
| Support readiness | C | C | I | I | C | I | A | I |
| Launch dashboard | C | I | I | I | C | I | I | A |
| UAT coordination | A | R | R | R | R | I | C | C |
| Go / no-go | A | C | C | C | C | C | C | C |
| 90-day readout | A | C | C | C | C | I | I | R |

## Decision log

| ID | Date | Decision | Options considered | Tradeoff accepted | Decided by |
|---|---|---|---|---|---|
| D-01 | 12 Dec 2025 | Starter plan excluded at launch | Include Starter; exclude Starter | Smaller market at launch, but fewer low-value, high-support accounts | Product, VP RevOps |
| D-02 | 16 Dec 2025 | Single annual price, no monthly option | Annual only; annual and monthly | Simpler billing and quoting; may slow some self-serve purchases | Finance, Product |
| D-03 | 14 Jan 2026 | Sales-led access starts when the invoice is paid | Access on booking; access on payment | Protects against unpaid usage; **customers may wait for access** (flagged as risk R-02) | Finance, VP RevOps |
| D-04 | 21 Jan 2026 | Discount approval threshold set at 15% | 10%; 15%; 20% | Faster deals; some margin risk on 16 to 20% deals routed for approval | Sales Ops, Finance |
| D-05 | 26 Feb 2026 | Go for launch on 2 March | Go; delay one week | Launch on time with one known gap (R-02) monitored daily | All owners at go / no-go |
| D-06 | 8 Jun 2026 | Move sales-led access to booking for customers in good standing (proposed) | Keep D-03; change it | See the [90-day readout](07_post_launch_readout.md) | Pending VP RevOps |
