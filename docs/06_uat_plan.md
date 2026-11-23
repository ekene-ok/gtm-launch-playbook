# 06. User Acceptance Testing (UAT)

UAT ran from 16 to 25 February 2026 in the staging environment, with each requirement owner signing off their own test cases.

## Test cases

| ID | Requirement | Scenario | Expected result | Priority | Result |
|---|---|---|---|---|---|
| TC-01 | BR-01 | Starter admin opens the billing page | No Harbor Assist option shown | P1 | Pass |
| TC-02 | BR-01 | AE tries to quote the add-on for a Starter account | Quote tool blocks the line item | P1 | Pass |
| TC-03 | BR-02 | Compare price in checkout, quote and invoice | USD 8 per seat per month in all three | P1 | Pass |
| TC-04 | BR-03 | Self-serve admin tries to buy more seats than the plan has | Checkout blocks it with a message | P1 | Pass |
| TC-05 | BR-04 | AE applies 12%, 18% and 25% discounts | 12% goes through, 18% routes for approval, 25% is blocked | P1 | Pass |
| TC-06 | BR-05 | Team admin buys 10 seats with a card | Purchase completes in under 2 minutes | P1 | Pass |
| TC-07 | BR-06 | AE adds the add-on to a new Business quote | Line item on quote and order form | P1 | Pass |
| TC-08 | BR-06 | AE adds the add-on to an amendment | Line item on the amendment | P1 | Pass |
| TC-09 | BR-07 | Mid-term addition on a contract ending 31 December | Quote and invoice match to the cent | P1 | Pass |
| TC-10 | BR-08 | Self-serve purchase completes | Feature on for all seats within 15 minutes | P1 | Pass |
| TC-11 | BR-09 | Sales-led invoice marked paid | Feature on within 1 hour of payment | P1 | Pass |
| TC-12 | BR-11 | Invoice generated for a discounted order | Separate line with seats, price, discount and dates | P1 | Pass |
| TC-13 | BR-12 | Order booked | Monthly revenue schedule created | P1 | Pass |
| TC-14 | BR-13 | Place one order per channel and order type | All timestamps and fields populated | P1 | Pass |

## What UAT missed

TC-09 passed, but it only tested a contract ending at the end of a month. In that case, prorating by month and by day give the same answer. Real mid-term additions mostly landed mid-month, where the quote tool (by month) and billing (by day) disagreed. That gap caused the billing errors in the [90-day readout](07_post_launch_readout.md).

**Fix for future launches:** test each pricing rule with at least three dates (start of month, mid-month, end of term), and have Finance and Sales Ops review the same test case together.

## Test cases added after launch

| ID | Requirement | Scenario | Expected result |
|---|---|---|---|
| TC-09b | BR-07 | Mid-term addition on 17 March for a contract ending 30 September | Quote and invoice match to the cent |
| TC-09c | BR-07 | Mid-term addition on a leap-year contract | Quote and invoice match to the cent |
| TC-15 | D-06 | Sales-led order booked for a customer in good standing | Access on within 1 hour of booking |
