from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

from lists.views import home_page # Widok, ktory uzyjemy zaraz, przechowywany w folderze lists w pliku views.py


class SmokeTest(TestCase):

	def test_uses_home_template(self):
		response = self.client.get('/') #podajem klientowi URL ktore chcemy przetestowac
		self.assertTemplateUsed(response, 'home.html') # od TestCase, pozwala na sprawdzenie,
													   # ktora templatka zostala uzyta do wyrenderowania odpowiedzi,
													   # bedzie tylko dzialac dla odpowiedzi zwroconych przez test clienta

		# request = HttpRequest() # tworzymy requesta, czyli to Django zobaczy jak uzytkownik zapyta sie przegladary o strone
		# response = home_page(request) # Przekazujemy requesta do naszego widoku co da na odpowiedz (instancja klasy HttpResponse)
		# html = response.content.decode('utf8') # zostawiamy stare testy tylko po to zeby sprawdzic czy jest git
		# self.assertTrue(html.startswith('<html>'))
		# self.assertIn('<title>To-Do lists</title>', html)
		# self.assertTrue(html.strip().endswith('</html>'))

	def test_can_save_a_POST_request(self):
		response = self.client.post('/', data={'item_text': 'A new list item'})
		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):

	def test_saving_and_retirving_items(self):
		first_item = Item()
		first_item.text = "The First (ever) list item"
		first_item.save()

		second_item = Item()
		second_item.text = "Item the second"
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]

		self.assertEqual(first_saved_item.text, "The First (ever) list item")
		self.assertEqual(second_saved_item.text, "Item the second")