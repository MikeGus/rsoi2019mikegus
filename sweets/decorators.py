from rest_framework.response import Response
from rest_framework.views import status


def validate_request(fn):
    def decorated(*args, **kwargs):
        title = args[0].request.data.get("title", "")
        calories = args[0].request.data.get("calories", "")
        if not title or not calories:
            return Response(
                data={
                    "msg": "Both title and calories are required to add a sweet"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        elif calories < 0:
            return Response(
                data={
                    "msg": "Calories can't be negative"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated

