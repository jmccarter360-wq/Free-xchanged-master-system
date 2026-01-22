import logging
import json

class CustomJsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            'time': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.msg,
        }
        return json.dumps(log_obj)

def setup_logging():
    logger = logging.getLogger('structured_logger')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()  # Can be changed to a file handler if needed
    handler.setFormatter(CustomJsonFormatter())

    logger.addHandler(handler)

    return logger

# Usage
if __name__ == '__main__':
    logger = setup_logging()
    logger.info('This is a structured log message.')
