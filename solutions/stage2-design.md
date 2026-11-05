# Stage 2 reference design

Browser -> FastAPI validation and identity adapter -> authorization and business rule -> SQLite transaction for refund, audit and fake effect. A valid amount at or below $500 takes the standard path. Above $500 enters pending finance approval; no effect occurs until finance approves. Duplicate keys are checked against a request fingerprint inside the transaction. All attempts write audit metadata without reason text. Demo tokens and SQLite are teaching fixtures only.

Compare your solution and test results with reference_app.py and reference_tests.py. Follow README.md in this folder to run the reference. An alternative design may be valid if it meets the specification and has evidence.
