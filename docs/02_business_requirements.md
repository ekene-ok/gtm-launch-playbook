# 02. Business Requirements

Each requirement has one accountable owner and acceptance criteria that UAT tests against ([06_uat_plan.md](06_uat_plan.md)). Priority: P1 must be live at launch, P2 can follow within 30 days.

## Eligibility and pricing

| ID | Requirement | Owner | Priority | Acceptance criteria |
|---|---|---|---|---|
| BR-01 | Only Team, Business and Enterprise accounts can buy Harbor Assist | Product | P1 | Starter accounts see no purchase option and cannot be quoted |
| BR-02 | List price is USD 8 per seat per month, billed annually | Finance | P1 | Price is identical in the product checkout, the quote tool and the invoice |
| BR-03 | Seats bought cannot exceed the account's core plan seats | Product | P1 | Checkout and quote tool both block a higher seat count, with a clear message |
| BR-04 | Sales-led discounts up to 15% need no approval; 16 to 20% need Sales Ops approval; above 20% is not allowed | Sales Ops | P1 | Quote tool routes 16 to 20% for approval and blocks anything higher |

## Purchase and quoting

| ID | Requirement | Owner | Priority | Acceptance criteria |
|---|---|---|---|---|
| BR-05 | Self-serve admins can buy the add-on in the billing page | Product | P1 | Purchase completes with a card in under 2 minutes |
| BR-06 | Account executives can add Harbor Assist to new quotes and to amendments of existing contracts | Sales Ops | P1 | Add-on appears as a line item on quotes and order forms |
| BR-07 | Mid-term additions are prorated to the end of the current contract term, by day | Finance | P1 | Quote amount and invoice amount match to the cent for a mid-term addition |

## Access and entitlement

| ID | Requirement | Owner | Priority | Acceptance criteria |
|---|---|---|---|---|
| BR-08 | Self-serve purchases grant access immediately | Engineering | P1 | Feature is on for all purchased seats within 15 minutes |
| BR-09 | Sales-led purchases grant access once the invoice is paid (see decision D-03) | Engineering | P1 | Feature turns on within 1 hour of the payment being recorded |
| BR-10 | Admins can assign Harbor Assist seats to specific users | Product | P2 | Admin console shows assigned and unassigned seats |

## Billing

| ID | Requirement | Owner | Priority | Acceptance criteria |
|---|---|---|---|---|
| BR-11 | Invoices show Harbor Assist as its own line item | Finance | P1 | Separate line with seats, unit price, discount and term dates |
| BR-12 | Revenue is recognized monthly over the term | Finance | P1 | Revenue schedule created for every order |

## Reporting

| ID | Requirement | Owner | Priority | Acceptance criteria |
|---|---|---|---|---|
| BR-13 | Every order records channel, order type, order time, payment time and access time | Analytics | P1 | Fields populated for 100% of orders in the launch dataset |
| BR-14 | A launch dashboard tracks SC-1 to SC-4 by channel, updated daily | Analytics | P1 | Dashboard live on launch day |

## Open questions closed during requirements

| Question | Answer | Recorded as |
|---|---|---|
| Should sales-led customers get access before they pay? | No, at launch access waits for payment | D-03 |
| Do we prorate mid-term additions by month or by day? | By day, to match how core plans are billed | BR-07 |
| Is Starter in scope? | No, revisit after the 90-day readout | D-01 |
