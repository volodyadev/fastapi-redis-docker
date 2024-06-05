import os
import time

from fastapi import APIRouter, FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import UJSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app import logging
from app.settings import settings
from app.views import router


def register_offline_docs(app: FastAPI) -> None:
    """Регистрация swagger из папки static.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Returns:
        None:
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_files_abs_path = os.path.join(current_dir, "../static/docs")

    app.mount(
        "/static",
        StaticFiles(directory=static_files_abs_path),
        name="static",
    )

    docs_router = APIRouter()

    @docs_router.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url or "",
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @docs_router.get(
        app.swagger_ui_oauth2_redirect_url or "/oauth2-redirect/",
        include_in_schema=False,
    )
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @docs_router.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url or "",
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )

    app.include_router(router=docs_router, prefix=settings.API_URL)


def register_logging_middleware(app: FastAPI) -> None:
    """Middlware для логирования промежетучных запросов.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Returns:
        None:
    """

    @app.middleware("http")
    async def log_request_and_timing(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        logger.debug(
            f"Method: {request.method}, URL: {request.url}, Time: {end_time - start_time:=.2f} sec",  # noqa E501
        )
        return response


def register_global_responses(app: FastAPI) -> None:
    """Middleware for handling global responses.

    Args:
        app (FastAPI): FastAPI application instance.

    Returns:
        None
    """

    @app.middleware("http")
    async def global_response_middleware(request, call_next):
        response: Response = await call_next(request)

        # Handling global responses
        if response.status_code == 404:
            response.body = b"Page not found"
        elif response.status_code == 500:
            response.body = b"Internal server error"

        return response


def register_cors_middleware(app: FastAPI) -> None:
    """Middlware для обработки CORS.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Returns:
        None:
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_logging_middleware(app: FastAPI) -> None:
    """Middlware для логирования промежетучных запросов.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Returns:
        None:
    """

    @app.middleware("http")
    async def log_request_and_timing(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        logger.debug(
            f"Method: {request.method}, URL: {request.url}, Time: {end_time - start_time:=.2f} sec",  # noqa E501
        )
        return response


def get_app() -> FastAPI:

    app = FastAPI(
        title=settings.API_NAME,
        default_response_class=UJSONResponse,
        openapi_url=f"{settings.API_URL}/openapi.json",
    )

    logging.configure_logging()

    # Добавление событий запуска и завершения.
    # register_startup_event(app)
    # register_shutdown_event(app)

    app.openapi_version = "3.0.0"

    register_logging_middleware(app)
    register_cors_middleware(app)
    register_global_responses(app)
    register_offline_docs(app)

    # Основной роутер для API.
    app.include_router(router=router, prefix=settings.API_URL)

    return app
