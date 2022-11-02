# forex_exchange

All three format are supported.
upto 100,000 entries are tested


1. cd to "FOREX_EXCHANGE" directory
2. type command "pip install -r requirements.txt" or "python<version_no> -m pip install -r requirements.txt"
3. type command "python main.py"

Note: 
If you are getting API error, please replace the API_KEY variable with API_KEY = "9WVv9DGww7BKMSuzjGTJGzSYdVRDCBA9" oon line 17 in views.py file



Solution: 
from Process File Page: 
from csv file unique combination of currency exchange is collected and current market rates are fetched using the 3rd- party API. 
rate fetched are used to calculate the conversion amount, data from csv file is converted to numpy array for faster computation.
The converted data is displayed and populated to the sqlite data base using bulk upload. 

On History page all the past transaction can be visulaised in a tabular format. 


