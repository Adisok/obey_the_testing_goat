from django.test import TestCase
from django.urls import resolve
from lists.views import home_page # Widok, ktory uzyjemy zaraz, przechowywany w folderze lists w pliku views.py

class SmokeTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/') # Resolve odpowiada za powiazanie URL do Widoku,   
		self.assertEqual(found.func, home_page) #"/" - oznacza home_page,

