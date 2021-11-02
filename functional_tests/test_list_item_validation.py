from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip
	
MAX_WAIT = 10 #maksymalny czas czekania na glicze

class ItemValidationTest(FunctionalTest):

	@skip
	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box

		# The home page refreshes, and there is an error message saying
		# that list items acnnot be blank

		# She tries again awith some text for the item, which now works

		# Perversely, she now decides to submit a second blank list item

		# She receives a similar warning on the list page

		# And she can correct it by filling some text in
		self.fail("Write me!")

