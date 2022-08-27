import sys


def udf_exception(udf_method):
    def exception_method(*args, **kwargs):
        try:
            result = udf_method(*args, **kwargs)
            return result
        except Exception as e:
            print(e)
            sys.exit(1)
    return exception_method
