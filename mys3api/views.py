import os
import boto3

"""
  cut to the chase
"""

class ItemViewSet(viewsets.ModelViewSet):
  
  queryset = Item.objects.all()
  serializer_class = ItemSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
  
  #url: /upload
  @action(methods=['POST'], detail=True, permission_classes=[AllowAny], url_path='upload', url_name='upload')
  def upload(self, request, pk):
    if request.method == 'POST':
      s3 = boto3.client('s3')
      s3_bucket = 'arn:aws:s3:::mybucket'
      file_name = request.GET.get('name', '')
      presigned_post = s3.generate_presigned_post(
        Bucket = s3_bucket,
        Key = file_name,
        Fields = {"acl": "private", "Content-Type": file_type},
        Conditions = [
          {"acl": "public-read"},
          {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
      )
      return Response(presigned_post, status=status.HTTP_200_OK
