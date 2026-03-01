from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    """
    Custom API response
    """

    def success(message="Success", data=None, status_code=status.HTTP_200_OK):
        response = {
            "status": True,
            "message": message,
        }
        if data is not None:
            response["data"] = data

        return Response(response, status=status_code)

    def created(message="Created successfully", data=None):
        return APIResponse.success(
            message=message,
            data=data,
            status_code=status.HTTP_201_CREATED
        )

    def bad_request(message="Bad request", errors=None):
        response = {
            "status": False,
            "message": message,
        }
        if errors:
            response["errors"] = errors

        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def unauthorized(message="Unauthorized"):
        return Response(
            {
                "status": False,
                "message": message,
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    def forbidden(message="Forbidden"):
        return Response(
            {
                "status": False,
                "message": message,
            },
            status=status.HTTP_403_FORBIDDEN
        )

    def server_error(message="Internal server error"):
        return Response(
            {
                "status": False,
                "message": message,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )