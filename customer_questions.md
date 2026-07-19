# Six Questions for Apex Capital Before We Commit to Delivery

The first four questions target real operational ambiguity discovered in the dataset and the applied rules engine. The last two address the production delivery boundary, where this prototype's inputs and outputs actually need to plug into Apex's existing systems.

### 1. Does the 24 hour "Late Booking" clock pause for weekends and holidays?
The current logic strictly flags any trade where `booking_timestamp minus execution_timestamp > 24 hours` as an L3 Escalation. If a trade is executed at 4:00 PM on Friday and booked at 9:00 AM on Monday, it will trigger an L3 flag. Do we need to integrate a business hours calendar to accurately calculate booking delays, or is the strict 24 hour absolute clock the correct regulatory requirement?

### 2. Should the 3% Price Outlier rule be applied globally across all instruments?
The engine currently flags any trade with an execution price variance > 3% from the market price as an L3 Escalation. However, a 3% variance in a highly liquid large cap Equity is fundamentally different from a 3% variance in an illiquid bespoke Fixed Income instrument. Does Apex Capital intend for this threshold to be instrument agnostic, or should we be looking up asset class specific volatility thresholds?

### 3. Do compounding L3 flags ever warrant an automatic L4 escalation?
Currently, a trade under $25M is routed to L3 even if it hits *multiple* severe flags simultaneously (e.g., Restricted List AND Related Party AND >3% Price Variance). Only a notional value > $25M guarantees an L4 routing. Is there a scenario where multiple L3 violations combined should automatically trigger Head of Compliance (L4) oversight, regardless of the notional value?

### 4. Where should trades with malformed or unparseable data be routed?
The LOA matrix defines routing by notional and by qualitative flags, but is silent on what happens when a trade record itself fails validation (missing timestamp, non numeric notional, price <= 0, etc.). The current engine fails closed, it escalates any such row to a human rather than auto clearing it, but deliberately does not assign it a notional tier, since a row that cannot be parsed cannot be reliably sized. Should these malformed records route to the Head of Compliance, to a data operations queue for correction, or be rejected back to the originating desk? This is a business or operational decision rather than an engineering one, and we would want to confirm the preferred workflow before delivery.

### 5. What are the upstream ingest and downstream audit logging destinations?
Right now, the prototype processes a flat batch CSV and prints results to stdout. For production delivery, we need to clarify the exact infrastructure boundaries. What specific system is generating and hosting these daily batch files? On the output side, where should the immutable audit logs be shipped? We can stream these directly to an enterprise aggregator like Splunk or AWS CloudWatch, or a lightweight system like Google Sheets if that matches your current compliance stack.

### 6. How do we track and sync the post review actions for human approvals and declines?
Once our system triages the 65% of trades that require human intervention, those reviewers will explicitly approve or decline those trades. To maintain a complete regulatory trail, those human decisions must be synced back to our audit logs. We need to define where those reviews happen. Are analysts interacting with a custom web UI we build, or an existing internal tool? Additionally, because these actions alter compliance records, we will need to align on your Role Based Access Control requirements to ensure only authorized analysts can sign off on escalations.
