from rest_framework import serializers
from .models import Picture, Album
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class PictureSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        """
        album: The associated Album to this Picture.
        user: The associated User to this Picture.
        """
        model = Picture
        fields = ('id', 'album', 'user', 'name', 'url', 'thumbnailUrl')


class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    pictures = PictureSerializer(many=True, read_only=True)

    class Meta:
        """
        user: The associated User to this Album.
        pictures: The associated picture objects to this Album.
        """
        model = Album
        fields = ('id', 'title', 'user', 'pictures')


class UserSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)
    pictures = PictureSerializer(many=True, read_only=True)

    class Meta:
        """
        albums: The associated Albums to this User.
        pictures: The associated Pictures to this User.
        """
        model = User
        fields = ('id', 'username', 'albums', 'pictures')



#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password=validated_data['password'])
        return user
