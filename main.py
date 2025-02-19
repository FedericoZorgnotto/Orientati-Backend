import asyncio
import threading

import sentry_sdk
import uvicorn

from app.config import settings
from app.database import setup_database
from app.services import update_stats


async def main():
    await setup_database()

    threading.Thread(target=asyncio.run, args=(update_stats(),), daemon=True).start()

    if settings.ssl_enabled:
        uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True,
                    ssl_keyfile=settings.ssl_keyfile,
                    ssl_certfile=settings.ssl_certfile)
    else:
        uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

    # db_scheduler = BackgroundScheduler()
    # db_scheduler.add_job(elimina_utenti_temporanei, 'cron', hour=0,
    #                      minute=0)  # Pianifica il job per eseguire ogni giorno a mezzanotte
    # db_scheduler.start()

    # uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True)

    asyncio.run(main())
