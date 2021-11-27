from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from .management.commands.create_session import create_pre_authenticated_session
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()


class MyListTest(FunctionalTest):

	def create_pre_authenticated_session(self, email):
		session_key = create_pre_authenticated_session(email)
		## to set a cookie we need to first visit the domain.
		## 404 pages load the quickest!
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path="/",
			))

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		# Edith is a logged-in user
		self.create_pre_authenticated_session("test@example.com")

		# She goes to the home page and starts a list
		self.browser.get(self.live_server_url)
		self.add_list_item("Reticulate splines")
		self.add_list_item("Immanentize eschaton")
		first_list_url = self.browser.current_url

		# She notices a "My lists" link, for the first time.
		self.browser.find_element_by_link_text("My lists").click()

		# She sees that her list is in there, named according to its first list item
		self.wait_for(
			lambda: self.browser.find_element_by_link_text("Reticulate splines")
			)
		self.browser.find_element_by_link_text("Reticulate splines").click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
			)

		# She decides to start another lists, jus to see
		self.browser.get(self.live_server_url)
		self.add_list_item("Click cows")
		second_list_url = self.browser.current_url

		# Under "My lists", her new lists appears
		self.browser.find_element_by_link_text("My lists").click()
		self.wait_for(
			lambda: self.find_element_by_link_text("Click cows")
			)
		self.browser.find_element_by_link_text("Click cows").click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, second_list_url)
			)

		# She logs out. The "My lists" option disappears
		self.browser.find_element_by_link_text("Log out").click()
		self.wait_for(
			lambda: self.assertEqual(
				self.browser.find_element_by_link_text("My lists"),
				[]
				)
			)
