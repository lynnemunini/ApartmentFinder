from bs4 import BeautifulSoup
import requests
import lxml
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
google_form = "https://forms.gle/8WGSJ74EdwztZWpa6"
URL = "https://www.buyrentkenya.com/flats-apartments-for-rent/nairobi?max-price=100000&min-price=20000"
response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "lxml")
listings = soup.find_all("div", {"data-cy": "card-price"})
# print(listings)
pricing = [price.text.strip().split()[1].replace(",", "") for price in listings]
link_addresses = []
locations = soup.find_all("p", {"class": "text-md md:text-sm font-normal text-grey-darker mt-1 md:mt-0"})
location_addresses = [location.text.strip() for location in locations]
# print(location_addresses)
for listing in listings:
    anchor = listing.find("a", {"class": "no-underline"})
    address = anchor['href']
    full_address = "https://www.buyrentkenya.com"+address
    link_addresses.append(full_address)

# print(link_addresses)

# Fill out the form
s = Service("/home/lynne/Programs/Development/chromedriver")
driver = webdriver.Chrome(service=s)
driver.implicitly_wait(5)
driver.get(google_form)
times = 1
count = 0
for _ in pricing:
    if times <= len(pricing):
        time.sleep(5)
        location = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
        location.send_keys(location_addresses[count])
        price = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
        price.send_keys(pricing[count])
        link = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input")
        link.send_keys(link_addresses[count])
        count += 1
        submit = driver.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span")
        submit.click()
        time.sleep(3)
        another_response = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
        another_response.click()
        time.sleep(2)
    else:
        driver.close()


