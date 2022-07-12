import pymongo
import requests
from datetime import datetime
from pymongo import MongoClient
from flask import Flask,render_template,request,url_for,redirect,flash
import pandas as pd
import json

app=Flask(__name__)
app.secret_key="myweathersystem@12"

client = pymongo.MongoClient("mongodb+srv://ajithMongo:ajith123mongo@cluster1.3mmhuy7.mongodb.net/test")

mydb = client["WEATHER"]

mycol = mydb["forecast"]


@app.route("/")
def home():
    all_post = list(mycol.find())
    return render_template("home.html",datas=all_post)
    
@app.route("/search",methods=['GET','POST'])
def search():
    if request.method=='POST':
        
        City=request.form['city']
        url= 'https://api.openweathermap.org/data/2.5/weather?q={}&lat=35&lon=139&appid=a9b6c45fc92b19f0d95ec6697d56df56'.format(City)
        res= requests.get(url)
        data= res.json()

        Temperature=(int((data['main']['temp'])-273.15))
        Temp_min=(int((data['main']['temp_min'])-273.15))
        Temp_max=(int((data['main']['temp_max'])-273.15))
        Wind_spd=data['wind']['speed']
        Humidity=data['main']['humidity']
        Description=data['weather'][0]['description']
        Date=datetime.now().strftime('%d %b %Y | %I:%M:%S %p')
       
        mycol.insert_one({"City":City,"Date":Date,"Temp":Temperature,"Temp_min":Temp_min,"Temp_max":Temp_max,"Wind_spd":Wind_spd,"Humidity":Humidity,"Description":Description})
        flash('Weather Fetched Successfully!') 
        return redirect(url_for('home'))
        Title = request.form['city']
        mycol.delete_one({"City":Title})
    return render_template("add.html")
    
@app.route("/delete",methods=['GET','POST'])
def delete():
    if request.method=='POST': 
        Title = request.form['title']
        mycol.delete_one({"City":Title})
        flash('Deleted!',category='success')
        return redirect(url_for("home"))
    return render_template("delete.html")    

if __name__=='__main__':
    app.run(debug=True)