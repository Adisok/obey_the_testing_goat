from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
import time
import os

MAX_WAIT = 10 #maksymalny czas czekania na glicze

class FunctionalTest(StaticLiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Safari()
		staging_server = os.environ.get("STAGING_SERVER")
		if staging_server:
			self.live_server_url = "http://" + staging_server
		
	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()	
	
	# Edith has heard about a cool new online to-do app. She goes
	# to check out its homepage

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
					#Lapiemy wyjatki, WebDriverException, czyli gdy strona sie nie zaladowala,
					# i Selenium nie moze znalezc elementu na stronie,
					# AssertionError, gdy tabela jest na stronie ale pewnie jest to przed odswiezeniem,
					# wiec nie ma naszych wierszy
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def wait_for(self, fn):
		start_time = time.time()
		while True:
			try:
				return fn()
			except (AssertionError, WebDriverException) as e:
					#Lapiemy wyjatki, WebDriverException, czyli gdy strona sie nie zaladowala,
					# i Selenium nie moze znalezc elementu na stronie,
					# AssertionError, gdy tabela jest na stronie ale pewnie jest to przed odswiezeniem,
					# wiec nie ma naszych wierszy
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def get_item_input_box(self):
		return self.browser.find_element_by_id("id-text")