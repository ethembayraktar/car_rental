from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from assist.serializers import UploadSerializer
from attachment.models import Attachment
from attachment.serializers import AttachmentCreateSerializer
from utils.schemas import upload_request_body, \
    upload_response_schema_dict


class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]
    temp_files = []

    @swagger_auto_schema(request_body=upload_request_body, responses=upload_response_schema_dict)
    def create(self, request):
        print(request.data)
        print(request.POST)
        attachments = []

        try:

            for k, v in request.FILES.items():
                file_uploaded = request.FILES.get(k)

                new_attachment = Attachment.objects.create(original=file_uploaded,
                                                           created_by_id=request.user.id,
                                                           title=request.data["title"] if "title" in request.data else None
                                                           )
                attachments.append(new_attachment)

            return Response(AttachmentCreateSerializer(attachments, many=True).data, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "Error",
                             "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
