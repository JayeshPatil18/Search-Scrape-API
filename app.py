from flask import Flask, jsonify
import json

import MySQLdb
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
flipkart = "https://www.flipkart.com"
amazon = "https://www.amazon.com"
snapdeal = "https://www.snapdeal.com"
mg1 = "https://www.1mg.com"

@app.route('/<keyword>')
def hello_world(keyword):

  product_url = []
  title = []
  price = []
  img_url = []
  reviews = []

#   ******* Flipkart *******
  url = f'{flipkart}/search?q={keyword}'
  source = requests.get(url ,headers=headers).text
  soup = BeautifulSoup(source, 'lxml')

# product_url
  for i in soup.find_all('a', class_='s1Q9rs'):
      string = flipkart + i.get('href')
      product_url.append(string.strip())

# title
  for i in soup.find_all('a', class_='s1Q9rs'):
      string = i.text
      title.append(string.strip())

# price
  for i in soup.find_all('div', class_='_30jeq3'):
      string = i.text.replace('₹', '')
      price.append(string)

# img_url
  for i in soup.find_all('img', class_='_396cs4'):
      string = i.get('src')
      img_url.append(string.strip())

# reviews
  for i in soup.find_all('div', class_='_3LWZlK'):
      string = i.text
      reviews.append(string.strip())

#   **************

# #   ******* Amazon *******
#   url = f'{amazon}/s?k={keyword}'
#   source = requests.get(url ,headers=headers).text
#   soup = BeautifulSoup(source, 'lxml')


# # product_url
#   for i in soup.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'):
#       string = amazon + i.get('href')
#       product_url.append(string.strip())

# # title
#   for i in soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal'):
#       string = i.text
#       title.append(string.strip())

# # price
#   for i in soup.find_all('span', class_='a-price-whole'):
#       string = i.text.replace('₹', '')
#       price.append(string)

# # img_url
#   for i in soup.find_all('img', class_='s-image'):
#       string = i.get('src')
#       img_url.append(string.strip())

# # reviews
#   for i in soup.find_all('span', class_='a-icon-alt'):
#       string = i.text
#       reviews.append(string.strip())

# #   **************

# #   ******* Snapdeal *******
#   url = f'{snapdeal}/search?keyword={keyword}'
#   source = requests.get(url ,headers=headers).text
#   soup = BeautifulSoup(source, 'lxml')

# # product_url
#   for i in soup.find_all('a', class_='dp-widget-link noUdLine hashAdded'):
#       string = i.get('href')
#       product_url.append(string.strip())

# # title
#   for i in soup.find_all('p', class_='product-title'):
#       string = i.text
#       title.append(string.strip())

# # price
#   for i in soup.find_all('span', class_='lfloat product-price'):
#       string = i.text.replace('₹', '')
#       price.append(string)

# # img_url
#   for i in soup.find_all('img', class_='product-image wooble'):
#       string = i.get('src')
#       img_url.append(string.strip())

# # reviews
#   for i in soup.find_all('div', class_='grey-stars -ws-data-preview-element'):
#       string = i.text
#       reviews.append(string.strip())

#   **************

# #   ******* 1 MG *******
#   url = f'{mg1}/search/all?name={keyword}'
#   source = requests.get(url ,headers=headers).text
#   soup = BeautifulSoup(source, 'lxml')

# # product_url
#   for i in soup.find_all('a', class_='style__product-link___1hWpa'):
#       string = i.get('href')
#       product_url.append(string.strip())

# # title
#   for i in soup.find_all('div', class_='style__pro-title___3G3rr'):
#       string = i.text
#       title.append(string.strip())

# # price
#   for i in soup.find_all('div', class_='style__price-tag___KzOkY'):
#       string = i.text.replace('₹', '')
#       price.append(string)

# # img_url
#   for i in soup.find_all('img', class_='Scalpe+ Expert Anti Dandruff Shampoo'):
#       string = i.get('src')
#       img_url.append(string.strip())

# # reviews
#   for i in soup.find_all('span', class_='CardRatingDetail__weight-700___27w9q'):
#       string = i.text
#       reviews.append(string.strip())

# #   **************

  mydb = MySQLdb.connect(
    host="ecommerce.ccqvdwpue8ea.ap-south-1.rds.amazonaws.com",
    user="admin",
    password="passwrong",
    database="ecommerce_db"
  )

  mycursor = mydb.cursor()

#   delete_query = "DELETE FROM searched"
#   mycursor.execute(delete_query)

#   print(product_url[0])
#   print(title[0])
#   print(price[0])
#   print(img_url[0])
#   print(reviews[0])

  length = min(len(product_url), len(title), len(price), len(img_url), len(reviews))

#   print(length)

  for i in range(length):
      sql = "INSERT INTO searched (title, price, img_url, reviews, product_url) VALUES (%s, %s, %s, %s, %s)"
      val = (title[i], price[i], img_url[i], reviews[i], product_url[i])
      mycursor.execute(sql, val)

  mydb.commit()

  data = []
  for i in range(length):
    product = {
        "title": title[i],
        "price": price[i],
        "img_url": img_url[i],
        "reviews": reviews[i],
        "product_url": product_url[i]
    }
    data.append(product)

  jsonData = json.dumps(data)
  return jsonify(jsonData)

if __name__ == '__main__':
  app.run()