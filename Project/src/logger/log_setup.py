import json
from pathlib import Path
from loguru import logger


def setup_logger():
    logger.remove()
    Path("logs").mkdir(exist_ok=True)

    def custom_sink(message):
        record = message.record
        msg_content = record["message"]

        try:
            msg_content = json.loads(msg_content.replace("'", '"'))
        except Exception:
            pass

        log_line = {
            "trace_id": record["extra"].get("trace_id", "missing"),
            "message": msg_content
        }

        with open("logs/app.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_line, ensure_ascii=False) + "\n")

    logger.add(
        sink=custom_sink,
        level="INFO",
        enqueue=True,
        backtrace=False,
        diagnose=False
    )