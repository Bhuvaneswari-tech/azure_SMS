import httpx

async def notify_webhook(event: str, status: str, detail: dict = None):
    url = "http://127.0.0.1:8000/webhook"
    payload = {"event": event, "status": status}
    if detail:
        payload["detail"] = detail
    async with httpx.AsyncClient() as client:
        try:
            await client.post(url, json=payload)
        except Exception as e:
            pass  # Optionally log the error
