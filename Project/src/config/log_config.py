import uuid
import json
import time
from loguru import logger
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


def setup_logger():
    logger.remove()

    logger.add(
        sink=lambda msg: print(json.dumps(json.loads(msg), ensure_ascii=False)),
        serialize=True,
        backtrace=True,
        diagnose=True,
    )


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())

        start_time = time.time()

        query_params = dict(request.query_params)

        with logger.contextualize(trace_id=trace_id):
            logger.info({
                "event": "request_received",
                "method": request.method,
                "url": str(request.url),
                "query_params": query_params,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(start_time)),
            })

            try:
                response: Response = await call_next(request)
            except Exception as exc:
                logger.exception({
                    "event": "request_failed",
                    "error": str(exc)
                })
                raise exc

            end_time = time.time()
            process_time = round(end_time - start_time, 4)
            response_body_length = len(response.body) if hasattr(response, 'body') else None
            response.headers["X-TRACE-ID"] = trace_id

            logger.info({
                "event": "response_sent",
                "status_code": response.status_code,
                "process_time_seconds": process_time,
                "content_length_bytes": response_body_length,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(end_time)),
            })

            return response
