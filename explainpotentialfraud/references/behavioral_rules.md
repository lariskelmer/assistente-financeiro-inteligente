# Behavioral Profiling Decision Rules

When analyzing an inbound transaction request against a user's historical baseline, look for the following threshold anomalies:

1. **Velocity Violations:** Look for rapid successive transactions. If a cardholder has a history of 1 transaction per day, 3 transactions within 15 minutes is a behavioral break regardless of location.
2. **Channel Shifts:** A sudden transition from purely physical POS terminals (`POS_CHIP`, `POS_TAP`) to remote `ONLINE` processing infrastructure marks a high-risk transition window.
3. **Ticket Scaling:** A transaction amount exceeding **3x** the historical max ticket calculation requires heightened structural cross-examination of tracking cookies or device fingerprints.