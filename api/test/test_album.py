from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Album


class AlbumTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.album = Album.objects.create(title='Test Album', body='This is a test album.', user=self.user)

    def test_get_album_list(self):
        response = self.client.get('/api/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.album.title)

    def test_create_album(self):
        self.client.force_login(self.user)
        data = {'title': 'New Album', 'body': 'This is a new album.'}
        response = self.client.post('/api/albums/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(Album.objects.get(id=2).title, 'New Album')

    def test_update_album(self):
        self.client.force_login(self.user)
        data = {'title': 'Updated Album', 'body': 'This is an updated album.'}
        response = self.client.put('/api/albums/{}/'.format(self.album.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Album.objects.get(id=self.album.id).title, 'Updated Album')

    #def test_delete_album(self):
    #    self.client.force_login(self.user)
    #    response = self.client.delete('/api/albums/{}/'.format(self.album.id))
        #self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #self.assertEqual(Album.objects.count(), 0)
