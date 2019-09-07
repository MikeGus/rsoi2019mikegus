from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status
from .decorators import validate_request
from .models import Sweet
from .serializers import SweetSerializer


class ListSweetView(generics.ListCreateAPIView):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer

    @validate_request
    def post(self, request, *args, **kwargs):
        new_sweet = self.queryset.create(
            title=request.data["title"],
            calories=request.data["calories"]
        )
        return Response(
            data=SweetSerializer(new_sweet).data,
            status=status.HTTP_201_CREATED
        )


class SweetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer

    def get(self, request, *args, **kwargs):
        try:
            sweet = self.queryset.get(pk=kwargs["pk"])
            return Response(self.serializer_class(sweet).data)
        except Sweet.DoesNotExist:
            return Response(
                data={
                    "msg": "Sweet with id: {:d} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    @validate_request
    def put(self, request, *args, **kwargs):
        try:
            sweet = self.queryset.get(pk=kwargs["pk"])
            updated_sweet = self.serializer_class().update(sweet, request.data)
            return Response(self.serializer_class(updated_sweet).data)
        except Sweet.DoesNotExist:
            return Response(
                data={
                    "msg": "Sweet with id: {:d} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


    def delete(self, request, *args, **kwargs):
        try:
            sweet = self.queryset.get(pk=kwargs["pk"])
            sweet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Sweet.DoesNotExist:
            return Response(
                data={
                    "msg": "Sweet with id: {:d} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
