from flask import Flask, render_template, request,jsonify,url_for
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
import os
import csv
import time
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

application=Flask(__name__)
app=application

@app.route("/", methods = ['POST','GET'])
def index():
    is_failure=False
    message=''
    rows=[]
    if request.method == 'POST':
        try:
             url=request.form['item_url'].replace(" ","")
             headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
             #url=f"https://www.flipkart.com/godrej-180-l-direct-cool-single-door-3-star-refrigerator/product-reviews/itm90f2ef108b3d3?pid=RFRGZNRAW8MFVHDQ&lid=LSTRFRGZNRAW8MFVHDQMPJG6Q&marketplace=FLIPKART"
             response = requests.get(url)
             soup = BeautifulSoup(response.content, "html.parser")

             title=soup.find_all("p",{"class":"_2-N8zT"})
             rating=soup.find_all("div",{"class":"_3LWZlK _1BLPMq"})
             review=soup.find_all("div",{"class":"t-ZTKy"})
             user_name=soup.find_all("p",{"class":"_2sc7ZR _2V5EHH"})

             # field names 
             fields = ['Title', 'Rating', 'Review',"UserName"]

             rows=[]
             for i in range(len(rating)):
                row={'Title':title[i].getText(),'Rating':rating[i].getText()
                     ,'Review':review[i].getText(), 'UserName':user_name[i].getText()}
                rows.append(row)

             filename='flipkart_item_scraping.csv'
             span_name=soup.find("span",{"class":"B_NuCI"})
             if span_name != None:
                  import time
                  obj = time.gmtime(0)
                  epoch = time.asctime(obj)
                  curr_time = round(time.time()*1000)
                  filename=span_name.getText()[:10].replace(" ","")+ "_" + str(curr_time) +".csv"

             with open(filename, 'w',encoding='utf-8') as csvfile:
              # creating a csv dict writer object 
              writer = csv.DictWriter(csvfile, fieldnames = fields)
              # writing headers (field names) 
              writer.writeheader()
              # writing data rows 
              writer.writerows(rows)
              message='Data is imported in csv file successfully!'

        except Exception as e:
                    logging.info(e)
                    message = 'OOPs! Something is wrong.'
                    is_failure=True
    return render_template("index.html",flag=is_failure,msg=message,data=rows)

if __name__ == "__main__":
    app.run()
