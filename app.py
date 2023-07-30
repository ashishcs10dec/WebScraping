from flask import Flask, render_template, request,jsonify
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import os

application=Flask(__name__)
app=application

@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
