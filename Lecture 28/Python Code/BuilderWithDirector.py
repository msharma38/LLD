class HttpRequest:
    def __init__(self):
        # Private-like (by convention) attributes
        self._url = None
        self._method = None
        self._headers = {}
        self._query_params = {}
        self._body = None
        self._timeout = 0

    def execute(self):
        print(f"Executing {self._method} request to {self._url}")

        if self._query_params:
            print("Query Parameters:")
            for k, v in self._query_params.items():
                print(f"  {k}={v}")

        print("Headers:")
        for k, v in self._headers.items():
            print(f"  {k}: {v}")

        if self._body:
            print(f"Body: {self._body}")

        print(f"Timeout: {self._timeout} seconds")
        print("Request executed successfully!")


class HttpRequestBuilder:
    def __init__(self):
        self._req = HttpRequest()

    def with_url(self, url: str):
        self._req._url = url
        return self

    def with_method(self, method: str):
        self._req._method = method
        return self

    def with_header(self, key: str, value: str):
        self._req._headers[key] = value
        return self

    def with_query_param(self, key: str, value: str):
        self._req._query_params[key] = value
        return self

    def with_body(self, body: str):
        self._req._body = body
        return self

    def with_timeout(self, timeout: int):
        self._req._timeout = timeout
        return self

    def build(self) -> HttpRequest:
        if not self._req._url:
            raise ValueError("URL cannot be empty")
        return self._req


class HttpRequestDirector:
    @staticmethod
    def create_get_request(url: str) -> HttpRequest:
        return (
            HttpRequestBuilder()
            .with_url(url)
            .with_method("GET")
            .build()
        )

    @staticmethod
    def create_json_post_request(url: str, json_body: str) -> HttpRequest:
        return (
            HttpRequestBuilder()
            .with_url(url)
            .with_method("POST")
            .with_header("Content-Type", "application/json")
            .with_header("Accept", "application/json")
            .with_body(json_body)
            .build()
        )


if __name__ == "__main__":
    # Normal Request using Builder directly
    normal_request = (
        HttpRequestBuilder()
        .with_url("https://api.example.com")
        .with_method("POST")
        .with_header("Content-Type", "application/json")
        .with_header("Accept", "application/json")
        .with_query_param("key", "12345")
        .with_body('{"name": "Aditya"}')
        .with_timeout(60)
        .build()
    )
    normal_request.execute()

    print("\n----------------------------\n")

    # Using Director for GET
    get_request = HttpRequestDirector.create_get_request("https://api.example.com/users")
    get_request.execute()

    print("\n----------------------------\n")

    # Using Director for JSON POST
    post_request = HttpRequestDirector.create_json_post_request(
        "https://api.example.com/users",
        '{"name": "Aditya", "email": "aditya@example.com"}'
    )
    post_request.execute()
