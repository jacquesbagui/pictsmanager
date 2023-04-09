from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Album, Picture
import io
from PIL import Image

class PictureTests(TestCase):

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.album = Album.objects.create(title='Test Album', body='This is a test album.', user=self.user)
        self.picture = Picture.objects.create(name='Test Picture', album=self.album, user=self.user)

    def test_get_picture_list(self):
        response = self.client.get('/api/pictures/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.picture.name)
    
    def test_create_picture(self):
        self.client.force_login(self.user)
        image = self.generate_photo_file()
        thumbnailUrl = self.generate_photo_file()
        data = { 'album': self.album.id, 'user': self.user.id, 'name': 'New Picture', 'url':image, 'thumbnailUrl': thumbnailUrl}
        response = self.client.post('/api/pictures/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(Picture.objects.count(), 2)
        #self.assertEqual(Picture.objects.get(id=2).name, 'New Picture')

    def test_update_picture(self):
        self.client.force_login(self.user)
        image = self.generate_photo_file()
        thumbnailUrl = self.generate_photo_file()
        data = {'name': 'Updated Picture', 'url':image, 'thumbnailUrl': thumbnailUrl,  'album': self.album.id, 'user': self.user.id}
        response = self.client.put('/api/pictures/{}/'.format(self.picture.id), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Picture.objects.get(id=self.picture.id).name, 'Updated Picture')

    def test_delete_picture(self):
        self.client.force_login(self.user)
        response = self.client.delete('/api/pictures/{}/'.format(self.picture.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Picture.objects.count(), 0)