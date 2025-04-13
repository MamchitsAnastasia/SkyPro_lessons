def log(filename=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            inputs = f"Inputs: {args}, {kwargs}"
            start_message = f"{func_name} started. {inputs}"
            if filename:
                with open(filename, 'a') as f:
                    f.write(start_message + '\n')
            else:
                print(start_message)

            try:
                result = func(*args, **kwargs)
                message = f"{func_name} ok"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(message + '\n')
                else:
                    print(message)

                return result

            except Exception as e:
                error_type = type(e).__name__
                message = f"{func_name} error: {error_type}. {inputs}"
                if filename:
                    with open(filename, 'a') as f:
                        f.write(message + '\n')
                else:
                    print(message)

                raise
        return wrapper
    return decorator