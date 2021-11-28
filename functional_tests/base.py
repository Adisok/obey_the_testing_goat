from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.core import mail
from selenium import webdriver
import time
import os

MAX_WAIT = 10 #maksymalny czas czekania na glicze

def wait(fn):
	def modified_fn(*args, **kwargs):
		start_time = time.time()
		while True:
			try:
				return fn(*args, **kwargs)
			except Exception as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
	return modified_fn

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

	def get_item_input_box(self):
		return self.browser.find_element_by_id("id_text")

	def add_list_item(self, item_text):
		num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
		self.get_item_input_box().send_keys(item_text)
		self.get_item_input_box().send_keys(Keys.ENTER)
		item_number = num_rows + 1	
		self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

	@wait
	def wait_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
	
	@wait
	def wait_for(self, fn):
		return fn()

	@wait
	def wait_to_be_logged_in(self, email):
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_elements_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	@wait
	def wait_to_be_logged_out(self, email):
		self.browser.find_element_by_name("email")
		navbar = self.browser.find_elements_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)

	@wait
	def wait_for_email(self, test_email, subject):
		email = mail.outbox[0]
		self.assertIn(test_email, email.to)
		self.assertEqual(email.subject, subject)
		return email.body