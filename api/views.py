from .models import Picture, Album
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import PictureSerializer, AlbumSerializer, UserSerializer, RegisterSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics, permissions
from rest_framework import status
from .pagination import StandardResultsSetPagination

@api_view(['GET'])
def api_root(request, format=None):
    """
    This is the base API Endpoint
    """
    return Response({
        'albums': reverse('album-list', request=request, format=format),
        'pictures': reverse('picture-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'register': reverse('register', request=request, format=format)
    })

class PictureList(generics.ListCreateAPIView):
    """
    Handles:
        GET Picture instances, or POST new Picture
    """
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'size', 'type']

    """
    Associate User to POST'd Picture
    """
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PictureDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles:
        Retrieve (GET), Update (PUT),
        and Destroy (DELETE) for a Picture instance.
    """
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class AlbumList(generics.ListCreateAPIView):
    """
    Handles:
        GET Album instances, or POST new Album
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'created_on']

    """
    Associate User to POST'd Album
    """
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    """
    Override DELETE in order to set a constraint
    on deleting Albums that have Pictures associated to them.
    """
    def delete(self, request, *args, **kwargs):
        album = self.get_object()
        if album.pictures.exists():
            return Response({'status': 'You cannot delete an Album that has Pictures!'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            album.delete()


class UserList(generics.ListAPIView):
    """
    List Users in the system.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    """
    Retrieve User details.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'username': user.username
        })
    
# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    def get(self, request, format=None):
        return Response()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer