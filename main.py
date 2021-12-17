from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

DRIVER_PATH = r"C:\Users\mrspm\Downloads\chromedriver.exe"
GOOGLE_FORM = "https://forms.gle/gyZUxsJKFJkyQ6vPA"
URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
	"Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
	"User-Agent": "Chrome/92.0.4515.159"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()
data = response.text
soup = BeautifulSoup(data, 'html.parser')
all_link_elements = soup.select(".list-card-top a")

all_links = []
for link in all_link_elements:
	href = link["href"]
	if "http" not in href:
		all_links.append(f"https://www.zillow.com{href}")
	else:
		all_links.append(href)

all_address_elements = soup.select(".list-card-info address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]

all_price_elements = soup.select(".list-card-heading")
all_prices = []
for element in all_price_elements:
	# Get the prices. Single and multiple listings have different tag & class structures
	try:
		# Price with only one listing
		price = element.select(".list-card-price")[0].contents[0]

	except IndexError:
		print('Multiple listings for the card')
		# Price with multiple listings
		# price = element.select(".list-card-details li")[0].contents[0]
	finally:
		all_prices.append(price)

driver = webdriver.Chrome(executable_path=DRIVER_PATH)

for n in range(len(all_links)):
	driver.get(GOOGLE_FORM)

	time.sleep(2)
	address = driver.find_element_by_xpath(
		'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
	price = driver.find_element_by_xpath(
		'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
	link = driver.find_element_by_xpath(
		'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
	submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

	address.send_keys(all_addresses[n])
	price.send_keys(all_prices[n])
	link.send_keys(all_links[n])
	submit_button.click()