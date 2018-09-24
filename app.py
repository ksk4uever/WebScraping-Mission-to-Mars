from flask import Flask, render_template, redirect
from flask_pymongo import MongoClient
import pymongo
from scrape_mars import scrape
import os

app = Flask(__name__)

client= pymongo.MongoClient('mongodb://localhost:27017/')
db = client['mars']


#---------------------------------------------------------
@app.route('/')
def index():
    mars = db.mars.find_one()
    return render_template('index.html', mars=mars)

#start scrape route; inserts results into  mars MongoDB
#---------------------------------------------------------
@app.route('/scrape')
def get():
    mars = db.mars
    data = scrape()
    mars.update({}, data, upsert=True)

    return redirect('http://localhost:5000/', code=302)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
