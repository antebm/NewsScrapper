from bs4 import BeautifulSoup
import requests
import csv
import os
import urllib.request

def dl_img(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)
    return full_path

# url = input('Enter BBC/news URL to scrpe: ')

url = 'https://www.bbc.com/news'

dirName = 'images'
 
try:
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")


response = requests.get(url)
print(response.status_code)

soup = BeautifulSoup(response.text, 'lxml')

csv_file = open('bbc_news.csv', 'a')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['headline', 'summary', 'image_link', 'category'])

file = open('imgcount', 'r+')
i = ord(file.read())
file.close()

for article in soup.find_all('div', class_='gs-c-promo'):
  
    try:
        title = article.find(class_='gs-c-promo-heading__title').text
    except Exception as e:
        title = None
  
    try:
        summary = article.find(class_='gs-c-promo-summary').text
    except Exception as e:
        summary = None
  
 
    try:
        category = article.find(class_='gs-c-section-link').text.strip()
    except Exception as e:
        category = None
  
    try:
        image_tag = str(article.find('img'))
        elements = image_tag.split('src="')
        image_link = elements[1].split('"')[0]
    except Exception as e:
        image_link = 'None'
   

    print(title)
    print(summary)
    print(category)
    print(image_link)
    
    file_name = f'img_{i}'
    try:
        image_link_local = dl_img(image_link, 'images/', file_name)
        i += 1
    except Exception as identifier:
        image_link_local = "EXTERNAL: " + image_link
        i += 1


    csv_writer.writerow([title, summary, image_link_local, category])

file = open('imgcount', 'w+')
file.write(str(i))
file.close()

csv_file.close()