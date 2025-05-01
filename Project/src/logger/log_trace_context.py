from contextvars import ContextVar
from loguru import logger

trace_id_var: ContextVar[str] = ContextVar("trace_id", default="undefined")


def get_logger():
    return logger.bind(trace_id=trace_id_var.get())
