from src.errors.error_types.http_conflict import HttpConflictError
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.http_types.http_response import HttpResponse


def handle_error(error: Exception) -> HttpResponse:
    if isinstance(error, (HttpConflictError, HttpNotFoundError)):
        return HttpResponse(
            body={
                "errors": [{"title": error.name, "details": error.message}],
            },
            status_code=error.status_code,
        )

    return HttpResponse(body={"errors": [{"title": "Error", "details": str(error)}]})
