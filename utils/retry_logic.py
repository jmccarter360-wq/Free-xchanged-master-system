import time
import functools
import logging

def retry(max_attempts=3, delay=1, backoff=2):
    """
    Decorator for retrying failed function calls with exponential backoff.
    
    Args:
        max_attempts (int): Maximum number of retry attempts
        delay (int): Initial delay in seconds between retries
        backoff (int): Multiplier for delay after each attempt
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            current_delay = delay
            last_exception = None
            
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logging.warning(
                            f"Attempt {attempt} failed for {func.__name__}. "
                            f"Retrying in {current_delay} seconds..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    attempt += 1
            
            logging.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    return decorator
