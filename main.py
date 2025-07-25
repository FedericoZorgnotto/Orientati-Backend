import asyncio
import uvicorn

from app.core.config import settings
from app.database import setup_database


async def main():
    await setup_database()

    if settings.ssl_enabled:
        uvicorn.run("app.server:app", host="0.0.0.0", port=settings.PORT, reload=True,
                    ssl_keyfile=settings.ssl_keyfile,
                    ssl_certfile=settings.ssl_certfile)
    else:
        uvicorn.run("app.server:app", host="0.0.0.0", port=settings.PORT, reload=True)


if __name__ == "__main__":
    # db_scheduler = BackgroundScheduler()
    # db_scheduler.add_job(elimina_utenti_temporanei, 'cron', hour=0,
    #                      minute=0)  # Pianifica il job per eseguire ogni giorno a mezzanotte
    # db_scheduler.start()

    asyncio.run(main())
