# Stage 3 review answer guide

This branch deliberately changes two conditions in the teaching implementation.

1. Threshold: `cents >= 50000` incorrectly sends exactly $500.00 to finance. FIN-01 requires the standard route at $500.00. Run the boundary test or submit 500.00 and compare the response with the approved specification.
2. Authorization: the finance-role guard is disabled, so an authorized support identity can approve a pending refund. Submit $500.01 as demo-support, then approve it using the same token. The expected result is 403 and unchanged pending state; this branch instead permits the approval. This is a release blocker.

Additional real-scope blockers remain even after fixing these deliberate defects: demo tokens, editable local SQLite audit, no remaining balance check and no real payment provider. Do not claim CI, independent approval, staging or rollback without actual evidence.
