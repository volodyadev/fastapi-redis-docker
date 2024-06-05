import uvicorn

from app.settings import settings


def main():
    if __name__ == "__main__":
        uvicorn.run("app.application:get_app", host="0.0.0.0", port=settings.FASTAPI_PORT)


if __name__ == "__main__":
    main()
