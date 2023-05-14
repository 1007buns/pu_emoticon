import datetime
import io
import sys

import chardet as chardet
import requests
from bs4 import BeautifulSoup
import os

sys.stdout.reconfigure(encoding='utf-8')


def create_directory(path):
    if not os.path.exists(path):
        os.mkdir(u"" + path)
    else:
        print(f"Directory {path} already exists. Skipping...")

def download_image(url, title, i):
    r = requests.get(url)
    with open(f"images/{title}/{i}.jpg", "wb") as f:
        f.write(r.content)


headers = {
'content-type': 'application/json;charset=utf-8',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",

}

url = "https://m.qqtn.com/bq/baozoubq"
response = requests.get(url, headers=headers)
encoding = chardet.detect(response.content)['encoding']
response.encoding = encoding
html = response.text

soup = BeautifulSoup(html, "html.parser")

img_list = soup.find("ul", {"class": "tab-con-tx tab-con-bq clearfix g-dome-list"})

for item in img_list.find_all("li"):
    title = item.find("span").text
    directory = f"images/{title}"
    print(directory)
    create_directory(directory)
    link = item.find("a")["href"]
    response = requests.get("https://m.qqtn.com" + link, headers=headers)

    html_doc = response.text
    sub_soup = BeautifulSoup(html_doc, "html.parser")
    img_list = sub_soup.find("article", {"class": "g-cms-content"})
    if img_list is not None:
        for i, img in enumerate(img_list.find_all("img")):
            url = img["src"]
            download_image(url, title, i + 1)
            print(f"{i + 1}. {url} downloaded.")
    else:
        print("Cannot find images on this page.")


# 获取当前时间
now = datetime.datetime.now()

# 打印日志
print(f"Crawling finished at {now}.")