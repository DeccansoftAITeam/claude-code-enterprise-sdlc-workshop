# Running the completed reference

This reference is a teaching solution using demo identities and fake payment effects. To run it in an isolated copy, copy `solutions/reference_app.py` to a new folder as `app.py`, copy `solutions/reference_tests.py` as `test_app.py`, copy `solutions/reference-ui.html` as `review.html`, and copy the root `requirements.txt`. Append the following to `app.py`:

```python
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():
    return Path(__file__).with_name("review.html").read_text(encoding="utf-8")
```

Install the requirements in a fresh virtual environment, run `python -m pytest -q`, then run `python -m uvicorn app:app` and open http://127.0.0.1:8000. The page title indicates a training build; this reference is not the deliberately defective stage 3 code. Use a unique idempotency key for each new request. Compare the behavior with the approved specification, not with real payment behavior. Local SQLite audit is editable by anyone with file access, and remaining order balance and real provider integration are not implemented.
