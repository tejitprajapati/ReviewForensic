import os
from fastapi.responses import RedirectResponse
import csv, io, json, sqlite3
from pathlib import Path
from datetime import datetime, timezone
from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .analyzer import analyze
ROOT = Path(__file__).resolve().parent.parent

PUBLIC_DEMO = os.getenv("PUBLIC_DEMO", "false").lower() == "true"

DB = (
    ROOT / "database" / "public_demo.db"
    if PUBLIC_DEMO
    else ROOT / "database" / "history.db"
)

DB.parent.mkdir(exist_ok=True)
app=FastAPI(title='ReviewForensic AI',version='1.0')
app.mount(
    "/static",
    StaticFiles(directory=str(ROOT / "app" / "static")),
    name="static"
)
templates=Jinja2Templates(directory=str(ROOT/'app'/'templates'))

def connect():
    c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
    c.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, created TEXT, review TEXT, label TEXT, score REAL, sentiment TEXT, engine TEXT, reasons TEXT)')
    c.commit();return c

def save(result):
    if PUBLIC_DEMO:
        return None
    with connect() as c:
        cursor=c.execute('INSERT INTO history(created,review,label,score,sentiment,engine,reasons) VALUES (?,?,?,?,?,?,?)',
        (datetime.now(timezone.utc).isoformat(timespec='seconds'),result['review'],result['label'],result['score'],result['sentiment'],result['engine'],json.dumps(result['reasons'])))
        return cursor.lastrowid


@app.get('/', response_class=HTMLResponse)
def home(request: Request, result_id: int | None = None):
    with connect() as c:
        rows = [
            dict(x) for x in c.execute(
                'SELECT * FROM history ORDER BY id DESC LIMIT 25'
            )
        ]

        total = c.execute(
            'SELECT COUNT(*) FROM history'
        ).fetchone()[0]

        fake = c.execute(
            "SELECT COUNT(*) FROM history WHERE label='Potentially Fake'"
        ).fetchone()[0]

        result = None

        if result_id is not None:
            row = c.execute(
                'SELECT * FROM history WHERE id=?',
                (result_id,)
            ).fetchone()

            if row:
                result = dict(row)

                stored_reasons = json.loads(
                    result.get("reasons") or "[]"
                )

                result["reasons"] = (
                    stored_reasons
                    if isinstance(stored_reasons, list)
                    else []
                )

                result["explanations"] = [
                    item
                    for item in stored_reasons
                    if isinstance(item, dict)
                    and all(
                        key in item
                        for key in ("word", "impact", "direction")
                    )
                    and isinstance(item["impact"], (int, float))
                ] if isinstance(stored_reasons, list) else []
    return templates.TemplateResponse(
        request=request,
        name='index.html',
        context={
            'rows': rows,
            'total': total,
            'fake': fake,
            'result': result
        }
    )


@app.post('/analyze')
def review(request: Request, text: str = Form(...)):
    try:
        r = analyze(text)
    except ValueError as e:
        raise HTTPException(400, str(e))

    if PUBLIC_DEMO:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "rows": [],
                "total": 0,
                "fake": 0,
                "result": r,
            },
        )

    review_id = save(r)

    return RedirectResponse(
        url=f"/?result_id={review_id}",
        status_code=303,
    )
@app.post('/api/analyze')
async def api_analyze(request:Request):
    try:
        payload = await request.json()
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON request"
        )
    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=400,
            detail="JSON body must be an object"
        )

    text = payload.get("text")

    if not isinstance(text, str):
        raise HTTPException(
            status_code=400,
            detail="Review text must be a string"
        )

    try:r=analyze(text)
    except ValueError as e: raise HTTPException(400,str(e))
    save(r);return r
@app.post("/bulk")
async def bulk(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Upload a CSV file")

    raw = await file.read(2_000_001)

    if len(raw) > 2_000_000:
        raise HTTPException(413, "CSV must be below 2 MB")

    try:
        reader = csv.DictReader(
            io.StringIO(raw.decode("utf-8-sig"))
        )

        if not reader.fieldnames or "text" not in reader.fieldnames:
            raise ValueError("CSV must contain a text column")

        out = []

        for i, row in enumerate(reader):
            if i >= 500:
                break

            text = (row.get("text") or "").strip()

            if not text:
                continue

            r = analyze(text)
            save(r)

            out.append({
                "text": text,
                "prediction": r["label"],
                "fake_probability_percent": r["score"],
                "sentiment": r["sentiment"],
                "method": r["engine"]
            })

    except (UnicodeDecodeError, ValueError, csv.Error) as e:
        raise HTTPException(400, str(e))

    stream = io.StringIO()

    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "text",
            "prediction",
            "fake_probability_percent",
            "sentiment",
            "method"
        ]
    )

    writer.writeheader()
    writer.writerows(out)

    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=review_results.csv"
            }
    )


@app.post("/history/clear")
def clear_history():
    if PUBLIC_DEMO:
        raise HTTPException(
            status_code=403,
            detail="History deletion is disabled in public demo mode."
        )

    with connect() as c:
        c.execute("DELETE FROM history")
        c.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.get('/health')
def health():return {'status':'ok'}
