import time

from di import (
    LogMiddleware,
    TimeMiddleware,
    container_builder_middleware,
    inject_dependency_middleware,
    logger_middleware,
    pipeline,
    time_middleware,
    typed_request_middleware,
)
from flask import Flask, request
from greeting import AppConfig, GreetingHttpRequest, GreetingService
from injector import Injector

shared_pipeline = pipeline(container_builder_middleware, LogMiddleware, TimeMiddleware)


@pipeline(shared_pipeline)
class Foo:
    def do_something(self, x: int, y: int) -> int:
        print(f"Inside do_something: x={x}, y={y}")
        return x + y

    def long_operation(self) -> str:
        time.sleep(0.5)
        return "Finished operation"


@pipeline(shared_pipeline)
def add_numbers(a: int, b: int) -> int:
    print(f"Inside add_numbers: a={a}, b={b}")
    return a + b


@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    typed_request_middleware,
    logger_middleware,
    time_middleware,
)
def say_hello_ultimate_http_v1(
    request: GreetingHttpRequest, greeting_service: GreetingService, injector: Injector
):

    app_config = injector.get(AppConfig)

    print(app_config)

    full_name = f"{request.first_name} {request.last_name}"

    greeting_response = greeting_service.greet(full_name)

    return greeting_response


sub_pipeline = pipeline(logger_middleware, time_middleware)


@pipeline(
    container_builder_middleware,
    inject_dependency_middleware,
    typed_request_middleware,
    sub_pipeline,
)
def say_hello_ultimate_http_v2(
    request: GreetingHttpRequest,
    greeting_service: GreetingService,
    app_config: AppConfig,
    **kwargs,
):

    print(app_config)

    full_name = f"{request.first_name} {request.last_name}"

    greeting_response = greeting_service.greet(full_name)

    return greeting_response


if __name__ == "__main__":

    app = Flask(__name__)

    with app.test_request_context(
        # Simulate a POST request to "/greet" with query params and JSON body
        path="/greet?first_name=John&last_name=Doe",
        method="POST",
        json={"first_name": "Jane", "last_name": "Smith"},
    ):
        say_hello_ultimate_http_v1(request)
        say_hello_ultimate_http_v2(request)
        print()

    print(add_numbers(3, 4))

    f = Foo()
    result = f.do_something(2, 5)
    print("Got result:", result)
    print(f.long_operation())
