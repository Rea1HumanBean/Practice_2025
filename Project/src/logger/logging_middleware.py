import uuid
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.logger.log_trace_context import trace_id_var, get_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        trace_id = request.headers.get("X-TRACE-ID", str(uuid.uuid4()))
        trace_id_var.set(trace_id)

        start_time = time.time()

        get_logger().info({
            "event": "request_received",
            "header": dict(request.headers),
            "client_ip": request.client.host,
            "user_agent": request.headers["user-agent"],
            "method": request.method,
            "url": str(request.url),
            "query_params":  self.mask_sensitive_data(dict(request.query_params)),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M", time.gmtime(start_time))
        })

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            get_logger().exception({
                "event": "request_failed",
                "error": str(exc)
            })
            raise exc

        end_time = time.time()
        process_time = round(end_time - start_time, 4)
        response_body_length = len(response.body) if hasattr(response, "body") else None
        response.headers["X-TRACE-ID"] = trace_id

        get_logger().info({
                "event": "response_sent",
                "status_code": response.status_code,
                "process_time_seconds": process_time,
                "content_length_bytes": response_body_length,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M", time.gmtime(end_time)),
            })

        return response

    @staticmethod
    def mask_sensitive_data(data: dict) -> dict:
        def mask_value():
            return "***"

        return {
            k: mask_value() if k.lower() in "user_id" else v
            for k, v in data.items()
        }
