import json
import sys

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup  # BeautifulSoup is in bs4 package
import requests

driver = webdriver.Chrome('chromedriver.exe')
driver.set_window_size(1024, 600)
driver.maximize_window()
try:
    driver.get("https://secure.indeed.com/account/login?")
except:
    print("Something Went Wrong")
    sys.exit(1)

# LOGIN CODE
email = ""
password = ""
try:
    enter_email = driver.find_element_by_id("login-email-input")
    for character in email:
        enter_email.send_keys(character)
        time.sleep(random.random())
    time.sleep(random.random())
except:
    print("Something went wrong while login to the file: ")
    print("Please Try again or report error!")
    sys.exit(1)

try:
    enter_password = driver.find_element_by_id("login-password-input")
    for character in password:
        enter_password.send_keys(character)
        time.sleep(random.random())
    time.sleep(random.random())
    enter_password.send_keys(Keys.ENTER)
except:
    print("Something went wrong while login to the file: ")
    print("Please Try again or report error!")
    sys.exit(1)

try:
    driver.get("https://resumes.indeed.com/")
    input_resume = input("Find resume for:")
    input_location = input("Location:")
except:
    print("Error Loading Website")
    print("check your internet connection and try again!")
    sys.exit(1)


try:
    resume_of = driver.find_element_by_id("input-q")
    resume_of.clear()
    resume_of.send_keys(Keys.CONTROL + "a")
    resume_of.send_keys(Keys.DELETE)
    for character in input_resume:
        resume_of.send_keys(character)
        time.sleep(random.random())
    time.sleep(random.random())
except:
    print("something went wrong try again!")
    sys.exit(1)

try:
    enter_location = driver.find_element_by_id("input-l")
    enter_location.clear()
    enter_location.send_keys(Keys.CONTROL + "a")
    enter_location.send_keys(Keys.DELETE)
    for character in input_location:
        enter_location.send_keys(character)
        time.sleep(random.random())
    enter_location.send_keys(Keys.ENTER)
    time.sleep(random.random())
except:
    print("something went wrong try again!")
    sys.exit(1)
time.sleep(2)
data = {}
data['Resumes'] = []
links = []
loop = 1
while loop == 1:
    try:
        resume_links = driver.find_elements_by_xpath("//div[@class ='rezemp-ResumeSearchCard-contents']//span/a")
        for l in resume_links:
            links.append(l.get_attribute("href"))
    except:
        print("No Jobs Found!")
    try:
        driver.find_element_by_xpath("//span[@class = 'icl-TextLink icl-TextLink--primary rezemp-pagination-nextbutton']").click()
        time.sleep(2)
        try:
            WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@class ='rezemp-ResumeSearchCard-contents']//span/a")))
        except TimeoutException as es:
            loop = 2
    except:
        print("End jobs")
        loop = 2

for url in links:
    driver.get(url)
    resumes = driver.find_elements_by_xpath("//div[@id = 'resume']//div[@class = 'vcard single_form-content']/*")
    print(len(resumes))
    resume_size = int(len(resumes)/2)
    l = {}
    for i in range(0, resume_size):
        if i == 0:
            title = "Basic Info"
            section_summary = resumes[i].text
            section_summary = section_summary.translate({ord(i): None for i in '\n'})
            l.update({title: section_summary})
        else:
            title = resumes[i].text
            title = title.split("\n")
            t = title[0].translate({ord(i): None for i in '\n'})
            section_summary = resumes[i].text
            section_summary = section_summary[len(title[0]):]
            section_summary = section_summary.translate({ord(i): None for i in '\n'})
            l.update({t: section_summary})
    print("----------")
    print(l)
    data['Resumes'].append(l)
    with open('Output.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

print('\nSTATUS: Scraping complete. Check "Output.json" for scraped data')
print('STATUS: Press any key to exit scraper')
exit = input('')
driver.quit()