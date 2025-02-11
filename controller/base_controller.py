from functools import wraps

class BaseController:
    @staticmethod
    def exception_handler(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"خطا: {e}")
                return None
        return wrapper
