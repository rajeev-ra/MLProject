import time
from linkedin_scraper import Person, Company
from selenium import webdriver

emailId = ""
psswrd = ""

driver = webdriver.Chrome()

company = Company("https://www.linkedin.com/company/tata-consultancy-services/", driver = driver, scrape=False, get_employees = True)
time.sleep(2)

e = driver.find_elements_by_class_name("form-toggle")
e[len(e) - 1].click();
time.sleep(1);

e = driver.find_element_by_id("login-email")
for a in emailId:
    e.send_keys(a)

e = driver.find_element_by_id("login-password")
for a in psswrd:
    e.send_keys(a)

driver.find_element_by_id("login-submit").click()

time.sleep(2);

company.scrape()
print(company)
print(company.total)