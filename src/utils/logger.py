import logging
import logging.handlers
import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from logging import LogRecord, Formatter
from contextvars import ContextVar
from dotenv import load_dotenv

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
log_context: ContextVar[str] = ContextVar(name="request_id", default='-')


class CustomFormatter(Formatter):
    def formatTime(self, record: LogRecord, datefmt: str = "%Y-%m-%d %H:%M:%S"):
        dt = datetime.fromtimestamp(record.created, VN_TZ)
        return dt.strftime(datefmt)

    def format(self, record: LogRecord):
        timestamp = self.formatTime(record)
        file_info = f"{record.filename}:{record.funcName}:{record.lineno}"
        message = record.getMessage()
        request_id = log_context.get()
        log = f"[{timestamp}] [{request_id}] [{record.levelname}] [{file_info}] {message}"
        error_context = getattr(record, "error_context", None)

        if error_context is not None:
            log = f"{log}. Error context:\n{json.dumps(error_context, indent=4, ensure_ascii=False)}\n"

        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            log = f"{log}\n{exc_text}"

        return log


log_level_mapping = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "error": logging.ERROR
}

load_dotenv(dotenv_path="../.env")
logger = logging.getLogger(os.getenv("LOG_NAME"))
logger.setLevel(log_level_mapping.get(os.getenv("LOG_LEVEL")))

handler = logging.handlers.RotatingFileHandler(
    filename=f"../logs/{os.getenv("LOG_FILE")}",
    maxBytes=int(os.getenv("LOG_MAX_BYTES")),
    backupCount=int(os.getenv("LOG_BACKUP_COUNT")),
    encoding="utf-8",
)

formatter = CustomFormatter()
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)
