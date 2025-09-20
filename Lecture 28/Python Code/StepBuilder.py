class HttpRequest:
    def __init__(self):
        self.url = ""
        self.method = ""
        self.headers = {}
        self.query_params = {}
        self.body = ""
        self.timeout = 30  # default timeout

    def execute(self):
        print(f"Executing {self.method} request to {self.url}")

        if self.query_params:
            print("Query Parameters:")
            for k, v in self.query_params.items():
                print(f"  {k}={v}")

        if self.headers:
            print("Headers:")
            for k, v in self.headers.items():
                print(f"  {k}: {v}")

        if self.body:
            print(f"Body: {self.body}")

        print(f"Timeout: {self.timeout} seconds")
        print("Request executed successfully!")


# Step Builder Interfaces
class UrlStep:
    def with_url(self, url: str):
        raise NotImplementedError


class MethodStep:
    def with_method(self, method: str):
        raise NotImplementedError


class OptionalStep:
    def with_header(self, key: str, value: str):
        raise NotImplementedError

    def with_query_param(self, key: str, value: str):
        raise NotImplementedError

    def with_body(self, body: str):
        raise NotImplementedError

    def with_timeout(self, timeout: int):
        raise NotImplementedError

    def build(self) -> HttpRequest:
        raise NotImplementedError


# Concrete Step Builder
class HttpRequestStepBuilder(UrlStep, MethodStep, OptionalStep):
    def __init__(self):
        self.req = HttpRequest()

    # UrlStep implementation
    def with_url(self, url: str) -> MethodStep:
        self.req.url = url
        return self

    # MethodStep implementation
    def with_method(self, method: str) -> OptionalStep:
        self.req.method = method
        return self

    # OptionalStep implementations
    def with_header(self, key: str, value: str) -> OptionalStep:
        self.req.headers[key] = value
        return self

    def with_query_param(self, key: str, value: str) -> OptionalStep:
        self.req.query_params[key] = value
        return self

    def with_body(self, body: str) -> OptionalStep:
        self.req.body = body
        return self

    def with_timeout(self, timeout: int) -> OptionalStep:
        self.req.timeout = timeout
        return self

    def build(self) -> HttpRequest:
        if not self.req.url:
            raise ValueError("URL cannot be empty")
        if not self.req.method:
            raise ValueError("HTTP Method cannot be empty")
        return self.req

    @staticmethod
    def get_builder() -> UrlStep:
        return HttpRequestStepBuilder()


# ==========================
# Usage Example
# ==========================
if __name__ == "__main__":
    request = (
        HttpRequestStepBuilder.get_builder()
        .with_url("https://api.example.com/products")
        .with_method("POST")
        .with_header("Content-Type", "application/json")
        .with_header("Accept", "application/json")
        .with_query_param("key", "12345")
        .with_body('{"product": "Laptop", "price": 49999}')
        .with_timeout(45)
        .build()
    )

    request.execute()
