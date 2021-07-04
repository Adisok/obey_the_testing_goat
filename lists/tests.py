from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page # Widok, ktory uzyjemy zaraz, przechowywany w folderze lists w pliku views.py


class SmokeTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/') # Resolve odpowiada za powiazanie URL do Widoku,   
		self.assertEqual(found.func, home_page) #"/" - oznacza home_page,

	def test_home_page_returns_correct_html(self):
		request = HttpRequest() # tworzymy requesta, czyli to Django zobaczy jak uzytkownik zapyta sie przegladary o strone
		response = home_page(request) # Przekazujemy requesta do naszego widoku co da na odpowiedz (instancja klasy HttpResponse)
		html = response.content.decode('utf8') # dobieramy sie do zawartosci i konwertujemy na htmla
		self.assertTrue(html.startswith('<html>')) # sprawdzamy poczatkowy tag 
		self.assertIn('<title>To-Do lists</title>', html) # sprawdzamy czy w tytule jest 'To-Do lists'
		self.assertTrue(html.endswith('</html>')) # sprawdzamy koncowy tag
		