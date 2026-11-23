# 05. Launch Readiness and Go / No-Go

Reviewed at the go / no-go meeting on 26 February 2026. Launch goes ahead only if every P1 item is complete or has an accepted workaround recorded in the decision log.

## Readiness checklist

| Area | Item | Owner | Status |
|---|---|---|---|
| Product | Add-on available in checkout for eligible plans only | Product | Complete |
| Product | Seat limit enforced in checkout | Product | Complete |
| Sales Ops | Add-on available on new quotes and amendments | Sales Ops | Complete |
| Sales Ops | Discount approval routing live | Sales Ops | Complete |
| Finance | Price, proration and invoice line item configured | Finance | Complete |
| Finance | Revenue schedules generating | Finance | Complete |
| Engineering | Instant access for self-serve | Engineering | Complete |
| Engineering | Access on payment for sales-led | Engineering | Complete, with known wait (R-02) |
| Enablement | Talk track, pricing sheet and quote walkthrough delivered | Enablement | Complete |
| Support | Macros, known issues list and escalation path | Support | Complete |
| Analytics | Launch dashboard live with SC-1 to SC-4 by channel | Analytics | Complete |
| Program | UAT sign-off from every owner | Program lead | Complete |
| Program | Hypercare rota for the first two weeks | Program lead | Complete |

## Go / no-go criteria

| Criterion | Result |
|---|---|
| All P1 requirements built | Met |
| All P1 test cases passed | Met (14 of 14) |
| No open severity 1 defects | Met |
| Rollback plan tested | Met |
| Known risks accepted by the sponsor | Met (R-02 accepted, see D-05) |

**Decision:** Go for launch on 2 March 2026 (D-05).

## Hypercare (2 to 13 March)

- Daily 15-minute stand-up with Engineering, Finance, Sales Ops and Support
- Daily report on sales-led orders that were paid but not yet live, and on invoices flagged by Support
- Issues logged as GitHub issues with the `hypercare` label and an owner
- Handed off to the system owners on 13 March
