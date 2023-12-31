# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestLikeDislikeLaughButtonTests():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  

  def test_1CreateUserTest(self):
    self.driver.get("http://127.0.0.1:5001/auth/login?next=%2F")
    self.driver.set_window_size(1059, 1097)
    self.driver.find_element(By.LINK_TEXT, "Click to Register!").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("Joshua")
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("themanjamesgreen@gmail.com")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("Test1238")
    self.driver.find_element(By.ID, "password2").click()
    self.driver.find_element(By.ID, "password2").send_keys("Test1238")
    self.driver.find_element(By.ID, "submit").click()
    self.driver.close()
  
  def test_2MakePostTest(self):
    self.driver.get("http://127.0.0.1:5001/auth/login?next=%2F")
    self.driver.set_window_size(1059, 1097)
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("Joshua")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("Test1238")
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.ID, "post").click()
    self.driver.find_element(By.ID, "post").send_keys("Hello from Selenium Webdriver!")
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.close()
  
  def test_3LikePostTest(self):
    self.driver.get("http://127.0.0.1:5001/auth/login?next=%2F")
    self.driver.set_window_size(1059, 1097)
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("Joshua")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("Test1238")
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.close()
  
  def test_4DislikePostTest(self):
    self.driver.get("http://127.0.0.1:5001/auth/login?next=%2F")
    self.driver.set_window_size(1059, 1097)
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("Joshua")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("Test1238")
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    element = self.driver.find_element(By.ID, "dislike-btn-1")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.close()
  
  def test_5LaughPostTest(self):
    self.driver.get("http://127.0.0.1:5001/auth/login?next=%2F")
    self.driver.set_window_size(1059, 1097)
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("Joshua")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("Test1238")
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.ID, "laugh-btn-1").click()
    self.driver.find_element(By.ID, "laugh-btn-1").click()
    element = self.driver.find_element(By.ID, "laugh-btn-1")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.ID, "laugh-btn-1").click()
    self.driver.find_element(By.ID, "laugh-btn-1").click()
    self.driver.find_element(By.ID, "laugh-btn-1").click()
    self.driver.find_element(By.ID, "laugh-btn-1").click()
    self.driver.find_element(By.ID, "laugh-btn-1").click()
    self.driver.find_element(By.ID, "laugh-btn-1").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.close()
  
  def test_6LikeDislikeButtonsTest(self):
    self.driver.get("http://127.0.0.1:5001/auth/login?next=%2F")
    self.driver.set_window_size(1059, 1097)
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("Joshua")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("Test1238")
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "like-count-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    element = self.driver.find_element(By.ID, "dislike-btn-1")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    element = self.driver.find_element(By.ID, "like-btn-1")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "like-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "like-count-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.ID, "dislike-btn-1").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.close()
  
 

