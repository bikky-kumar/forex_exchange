from flask import Blueprint, render_template, request, redirect, flash
import requests
from flask import current_app as app
import csv
import pandas as pd
import os
import json
import numpy as np

from FxExchange.models import Transaction
from . import db


#blueprint for fals application

views = Blueprint('views', __name__)
API_KEY = "hLHlDeHkPh7x2C9idZVeURZMyMIXjtwi"




#route

@views.route('/')
def home():
    return render_template("index.html")



@views.route('/view_transaction.html', methods=['GET','POST'])
def view_transaction():
    data_list = []
    results = db.session.query(Transaction).all()
    for result in results:
        data = []
        data.append(result.from_currency) 
        data.append(result.to_currency) 
        data.append(result.amount_to_convert) 
        data.append(result.current_rate)
        data.append(result.timestamp) 
        data.append(result.converted_amount) 
        data_list.append(data)
    df = pd.DataFrame(data_list, columns = ['From Currency','To Currency', "Current Amount","Current Rate",  "timestamp", "Converted Amount"])
    return render_template("view_transaction.html", data=df.to_html(classes='forex_table', header=True, index=False))
    

    

@views.route('/processForeignExchange.html', methods=['GET','POST'])
def processForeignExchange():
    if request.method == 'POST':
        data = []
        f = request.files['file1']
        string_data = f.read().decode("utf-8") 
        reader = csv.reader(string_data.split('\n'), delimiter=',')
        for row in reader:
            data.append(row)
        df = pd.DataFrame(data)
        df.columns = df.iloc[0]
        converted = doConversion(df)
        df = pd.DataFrame(converted, columns = ['ID','From Currency','To Currency', "Current Amount","Current Rate",  "timestamp", "Converted Amount"])
        if len(df.index) > 0 :
            #doing a bulk update to save time
            objects = []
            for fx in converted:
                from_currency =  fx[1]
                to_currency =  fx[2]
                amount_to_convert =  fx[3]
                current_rate =  fx[4]
                timestamp = fx[5]
                converted_amount =  fx[6]
                new_transactions = Transaction(from_currency, to_currency, amount_to_convert, current_rate, timestamp, converted_amount )
                objects.append(new_transactions)
      
            db.session.bulk_save_objects(objects)
            db.session.commit() 
            flash('File Processed Successfully', category='success')
            return render_template("data.html", data=df.to_html(classes='forex_table', header=True, index=False))
        else:
            flash('Cannot Process the File', category='error')
            return redirect("processForeignExchange.html")
    else:
        return render_template("processForeignExchange.html")


def doConversion(df):
    converted = []
    df = df.dropna()
    forex_array = df.to_numpy()[1:]
    currency_pair = set() 
    currency_pair = {each[1]+"_"+each[2] for each in forex_array}
    currency_rates = findRates(currency_pair)
    if len(currency_rates)>1:
        conversion_rate = [currency_rates[items[1]+"_"+items[2]] for items in forex_array]
        converted = np.column_stack((forex_array,conversion_rate))
        conversion_amount = [round(float(each[3])*each[4], 2) for each in converted]
        converted  = np.column_stack((converted,conversion_amount))
    else:
        flash("API call Failed : ", "error")
    return converted

def findRates(currency_pair):
    payload = {}
    headers= {
    "apikey": API_KEY
    }

    currency_rates = {}
    for each in currency_pair:
        from_currency, to_currency = each.split("_")
        #getting conversion of only unique pair to make the conversion faster for large forex conversion files.
        url = "https://api.apilayer.com/fixer/convert?to={}&from={}&amount={}".format(to_currency, from_currency, 1)
        response = requests.request("GET", url, headers=headers, data = payload)
        status_code = response.status_code
        result = response.text
        if status_code == 200:
            api_result = json.loads(result)
            print("api_result : ", api_result)
            currency_rates[each] = [api_result['info']['rate'],api_result['info']['timestamp']]
            
    return currency_rates

        