from pydantic import BaseModel


class DedupeKnn(BaseModel):
    LOGGER_NAME: str = "dedupeknn"
    LOG_FORMAT: str = '[%(asctime)s] p%(process)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
    LOG_LEVEL: str = "DEBUG"

    # Logging properties
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "dedupeknn": {"handlers": ["default"], "level": LOG_LEVEL},
    }