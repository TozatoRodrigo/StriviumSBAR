import datetime
import json
import logging
from typing import Any


class GCPJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        current_time = datetime.datetime.now(tz=datetime.UTC)
        timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+00:00"
        default_fields = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "taskName",
        }
        extra = {k: v for k, v in record.__dict__.items() if k not in default_fields}

        log_data: dict[str, Any] = {
            "message": record.getMessage(),
            "context": {},
            "channel": record.name,
            "extra": extra,
            "severity": record.levelname,
            "time": timestamp,
        }

        if record.exc_info:
            log_data["context"]["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    handler = logging.StreamHandler()
    handler.setFormatter(GCPJsonFormatter())

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger


logger = setup_logging()
