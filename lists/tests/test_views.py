from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List
from django.utils.html import escape
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

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get(f"/lists/{list_.id}/")
		self.assertTemplateUsed(response, "list.html")

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text="itemey 1", list=correct_list)
		Item.objects.create(text="itemey 2", list=correct_list)
		
		other_list = List.objects.create()
		Item.objects.create(text="other list item 1", list=other_list)
		Item.objects.create(text="other list item 2", list=other_list)

		response = self.client.get(f"/lists/{correct_list.id}/")

		self.assertContains(response, "itemey 1")
		self.assertContains(response, "itemey 2")
		self.assertNotContains(response, "other list item 1")
		self.assertNotContains(response, "other list item 2")

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get(f"/lists/{correct_list.id}/")
		self.assertEqual(response.context["list"], correct_list)


	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(f"/lists/{correct_list.id}/", 
			data={"item_text": "A new item for an existing list"})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, "A new item for an existing list")
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			f"/lists/{correct_list.id}/",
			data={"item_text": "A new item for an existing list"}
			)

		self.assertRedirects(response, f"/lists/{correct_list.id}/")

	def test_validation_errors_end_up_on_lists_page(self):
		list_ = List.objects.create()
		response = self.client.post(
			f"/lists/{list_.id}/", data={"item_text": ""}
			)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, "list.html")
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)

class NewListTest(TestCase):

	def test_can_save_a_POST_request(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, "A new list item")

	def test_redirect_after_POST(self):
		response = self.client.post("/lists/new", data={'item_text': 'A new list item'})
		new_list = List.objects.first()
		self.assertRedirects(response, f"/lists/{new_list.id}/")

	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)

	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)