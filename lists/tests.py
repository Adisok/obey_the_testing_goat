from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

from lists.views import home_page # Widok, ktory uzyjemy zaraz, przechowywany w folderze lists w pliku views.py


class  HomePageTest(TestCase):

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

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, "A new list item")

	def test_redirect_after_POST(self):
		response = self.client.post("/", data={"item_text": ""})
		self.assertEqual(response.status_code,302)
		self.assertEqual(response["location"], "/lists/the-only-list-in-the-world/")

	def test_only_saves_items_when_necessary(self):
		self.client.get("/")
		self.assertEqual(Item.objects.count(), 0 )

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

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get("/lists/the-only-list-in-the-world/")
		self.assertTemplateUsed(response, "list.html")

	def test_displays_all_items(self):
		Item.objects.create(text="itemey 1")
		Item.objects.create(text="itemey 2")
		
		response = self.client.get("/lists/the-only-list-in-the-world/")
		print(f"RESPONE={response.content}")
		self.assertContains(response, "itemey 1")
		self.assertContains(response, "itemey 2")
