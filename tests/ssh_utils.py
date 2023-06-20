import functools
from unittest import IsolatedAsyncioTestCase
from ssh_key_rotator.connections import ServerContext
from ssh_key_rotator.util import get_default_authorized_keys_path

def with_ssh_server(port: int, authorized_keys_path = get_default_authorized_keys_path()):
    def decorator_server(func):
        @functools.wraps(func)
        async def test_with_server(*args, **kwargs):
            async with ServerContext(port):
                return func(*args, *kwargs)
        return test_with_server
    return decorator_server

#DOES NOT WORK YET, DO NOT USE
# def SSHTestCase(port:int):
#     def class_decorator(cls):
#         methods_in_base_class = {func for func in dir(IsolatedAsyncioTestCase) if callable(func)}
#         methods_in_this_class = {func for func in dir(cls) if callable(func) and not func.startsWith("__")}
#         test_methods = methods_in_this_class.difference(methods_in_base_class)
#         @functools.wraps(cls)
#         def class_wrapper(*args, **kwargs):
#             print('At wrapper')
#             for base_class_method in methods_in_base_class:
#                 cls.setattr(cls, base_class_method, base_class_method)
#             for test_method in methods_in_this_class:
#                 print(test_method)
#                 cls.setattr(cls, test_method, with_ssh_server(port)(test_method))
#             return cls(*args, **kwargs)
#         return class_wrapper
#     return class_decorator

def with_ssh_server_and_keys():
    def generate_keys_wrapper(*args, **kwargs):
        with TemporaryDirectory() as temp_dir:
            public_key = generate_private_public_key_in_file(temp_dir)
            authorized_keys_file_path = os.path.join(temp_dir, "authorized_keys")
            with open(authorized_keys_file_path, mode="wb") as authorized_keys_file:
                authorized_keys_file.write(public_key)
    return generate_keys_wrapper