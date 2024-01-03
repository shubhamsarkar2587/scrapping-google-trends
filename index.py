import time, json
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

base_url = "https://trends.google.com/trends/trendingsearches/daily?geo=IN&hl=en-US"

options = Options()
options.add_argument("window-size=1200,600")
user_agent = UserAgent().random
options.add_argument(f"user-agent={user_agent}")
driver = webdriver.Chrome(options=options)

driver.get(base_url)


wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "/html/body/div[3]/div[2]/div/div[2]/div/div[1]/ng-include/div/div",
        )
    )
)

page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

trending_items = soup.find_all(
    "div",
    "feed-item-header",
)

req_data = []

for item in trending_items:
    trend_detail = {
        "title": None,
        "summary": None,
        "source": None,
        "article_time": None,
        "no_of_searches": None,
        "post_img": None,
        "article_url": None,
    }
    # article_wrapper
    details = item.find("div", "title")
    nasty_title = details.find("span").get_text()
    trend_detail["title"] = nasty_title.strip().replace("\n", "").strip()

    trend_detail["no_of_searches"] = item.find("div", "search-count-title").get_text()

    article_source_time = item.find("div", "source-and-time").get_text(separator="•", strip=True).split("•")
    trend_detail["source"] = article_source_time[0].strip()
    trend_detail["article_time"] = article_source_time[3].strip() if len(article_source_time) > 3 else None

    # article_image_wrapper
    img_wrapper = item.find("div", "image-link-wrapper")

    article_url = img_wrapper.find("a").get("href")
    trend_detail["article_url"] = article_url

    article_summary = img_wrapper.find("a").get("title")
    trend_detail["summary"] = article_summary

    article_img = img_wrapper.find("img").get("src")
    trend_detail["post_img"] = article_img

    req_data.append(trend_detail)

file_name = "google_trend_data/google_trend_data.json"
with open(file_name, "w") as file:
    json.dump(req_data, file, indent=2)
pprint(req_data)
