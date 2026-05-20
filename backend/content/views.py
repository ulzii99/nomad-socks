from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ContactSubmissionSerializer, NewsletterSubscribeSerializer


class ContactSubmitView(APIView):
    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Message received. We'll get back to you soon."},
            status=status.HTTP_201_CREATED,
        )


class NewsletterSubscribeView(APIView):
    def post(self, request):
        serializer = NewsletterSubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Successfully subscribed."},
            status=status.HTTP_201_CREATED,
        )
