# Discovery Questions for Apex Capital Before We Commit to Delivery

The first four questions target real operational ambiguity discovered in the dataset and the applied rules engine. The last four address the production delivery boundary, where this prototype's inputs and outputs actually need to plug into Apex's existing systems, timelines, and governance requirements.

### 1. Does the 24 hour "Late Booking" clock pause for weekends and holidays?
The current logic strictly flags any trade where `booking_timestamp minus execution_timestamp > 24 hours` as an L3 Escalation. If a trade is executed at 4:00 PM on Friday and booked at 9:00 AM on Monday, it will trigger an L3 flag. Do we need to integrate a business hours calendar to accurately calculate booking delays, or is the strict 24 hour absolute clock the correct regulatory requirement?

### 2. Should the 3% Price Outlier rule be applied globally across all instruments?
The engine currently flags any trade with an execution price variance greater than 3% from the market price as an L3 Escalation. However, a 3% variance in a highly liquid large cap Equity is fundamentally different from a 3% variance in an illiquid bespoke Fixed Income instrument. Does Apex Capital intend for this threshold to be instrument agnostic, or should we be looking up asset class specific volatility thresholds?

### 3. Do compounding L3 flags ever warrant an automatic L4 escalation?
Currently, a trade under $25M is routed to L3 even if it hits multiple severe flags simultaneously, such as a Restricted List breach and a Related Party violation at the same time. Only a notional value greater than $25M guarantees an L4 routing. Is there a scenario where multiple L3 violations combined should automatically trigger Head of Compliance (L4) oversight, regardless of the notional value?

### 4. Where should trades with malformed or unparseable data be routed?
The LOA matrix defines routing by notional and by qualitative flags, but is silent on what happens when a trade record itself fails validation, such as a missing timestamp or a non numeric notional. The current engine fails closed. It escalates any such row to a human rather than auto clearing it, but deliberately does not assign it a notional tier since a row that cannot be parsed cannot be reliably sized. Should these malformed records route to the Head of Compliance, to a data operations queue for correction, or be rejected back to the originating desk?

### 5. What are the upstream ingest and downstream audit logging destinations?
Right now the prototype processes a flat batch CSV and prints results to stdout. For production delivery, we need to clarify the exact infrastructure boundaries. What specific system is generating and hosting these daily batch files? On the output side, where should the immutable audit logs be shipped? We can stream these directly to an enterprise aggregator like Splunk or AWS CloudWatch, or a lighter weight system like Google Sheets if that better matches your current compliance stack.

### 6. What regulatory framework should the audit trail architecture be built around?
Different regulatory environments carry different retention periods and formatting expectations for audit logs. Rather than assume a specific framework, we want to confirm which regulatory requirements govern your audit trail from day one, so the logging architecture is built correctly the first time instead of retrofitted later.

### 7. How time sensitive are escalated trades, and does triage need to block settlement?
Once a trade is escalated, we need to understand the operational clock it runs on. Are there strict, same day cutoffs that mean a flagged trade must be blocked from settlement while it awaits human review, or can review happen asynchronously without holding up the trade? This determines whether our system needs to sit in the critical path of a live trading day or can operate alongside it.

### 8. Where do post review actions happen, and what are the access control requirements?
Once a human approves or declines an escalated trade, that decision needs to sync back to the audit log to keep the regulatory trail complete. We need to define where that review actually happens. Are analysts working in a custom interface we build, or an existing internal tool? Because these actions alter compliance records, we will also need to align on your Role Based Access Control requirements, so only authorized analysts can sign off on escalations.