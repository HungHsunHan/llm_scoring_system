def validate_file_type(file_path, allowed_extensions):
    """
    Validates if the file type is allowed based on the extension.
    """
    return file_path.lower().endswith(tuple(allowed_extensions))


import functools
import time


def retry(max_attempts=3, delay=2, exceptions=(Exception,)):
    """
    Decorator to retry a function on specified exceptions.

    Args:
        max_attempts (int): Maximum number of attempts.
        delay (int or float): Delay between attempts in seconds.
        exceptions (tuple): Exception types to catch and retry on.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == max_attempts:
                        print(f"[Retry] Failed after {max_attempts} attempts.")
                        raise
                    print(
                        f"[Retry] Attempt {attempt} failed with error: {e}. Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)

        return wrapper

    return decorator
