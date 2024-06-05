import logging
import sys
from typing import Union

from loguru import logger

from app.settings import settings


class InterceptHandler(logging.Handler):
    """
    Хэндлер для логирования по умолчанию.

    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """
        Propagates logs to loguru.

        :param record: record to log.
        """
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def configure_logging() -> None:  # pragma: no cover
    # Вызываемый метод для инициализации логгера.
    loggers = (logging.getLogger(name) for name in logging.root.manager.loggerDict if name.startswith("uvicorn."))
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []

    # Изменение стандартного обработчика логов uvicorn.
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("uvicorn.access").handlers = [intercept_handler]

    # Настройка логгера.
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
    )
    if settings.ENABLE_LOGGING_FILE:
        logger.add(
            sink=settings.LOG_PATH,
            level=settings.LOG_LEVEL,
            rotation=settings.LOG_ROTATION,
            compression=settings.LOG_COMPRESSION,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message}",
        )
