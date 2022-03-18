# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 18:58:02 2022

@author: jared
"""

import mysql.connector
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)
pd.set_option('display.max_rows', None)

#invoiceNumLookup = 1001
ceis236db = mysql.connector.connect(
  host="10.10.0.2",
  user="ceis236",
  password="ceis236",
  database="CEIS236"
)

cursor = ceis236db.cursor()

def invoiceQuery(invID):
    cursor.execute("SELECT INVOICE.*, CUSTOMER.*, LINE.*, PRODUCT.* \
                   FROM INVOICE \
                   INNER JOIN CUSTOMER ON \
                   CUSTOMER.CUS_CODE = INVOICE.CUS_CODE \
                   INNER JOIN LINE ON \
                   LINE.INV_NUMBER = INVOICE.INV_NUMBER \
                   INNER JOIN PRODUCT ON \
                   PRODUCT.P_CODE = LINE.P_CODE \
                   WHERE INVOICE.INV_NUMBER = %s",(invID,))
    df = pd.DataFrame(cursor.fetchall())
    return(df)

@app.route('/invoice/<path:path>', methods=['POST', 'GET'])
def invoiceGen(path):
    invoiceDF = invoiceQuery(path)
    invoiceNum = invoiceDF.iloc[0][0]
    cusNum = invoiceDF.iloc[0][1]
    invoiceDate = invoiceDF.iloc[0][2].to_pydatetime()
    invoiceDate = invoiceDate.strftime("%m/%d/%Y")
    if(invoiceDF.iloc[0][6] != None):
        cusNameTup = str(invoiceDF.iloc[0][5]), str(invoiceDF.iloc[0][6]), \
        str(invoiceDF.iloc[0][4])
    else:
        cusNameTup = str(invoiceDF.iloc[0][5]), str(invoiceDF.iloc[0][4])
        
    cusName = ' '.join(cusNameTup)
    cusPhone = '(' + str(invoiceDF.iloc[0][7]) + ')' + str(invoiceDF.iloc[0][8])
    cusBalance = float(invoiceDF.iloc[0][9])
    invoiceDF = invoiceDF.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 17,
                                18, 19, 22], axis=1)
    invoiceDF = invoiceDF.rename(columns={11: "Line", 12: "Product Code",
                                          13: "Quantity", 16: "Description",
                                          20: "Price", 21: "Discount"})
    invoiceDF['Line'] = invoiceDF['Line'].astype(float)
    invoiceDF['Quantity'] = invoiceDF['Quantity'].astype(float)
    invoiceDF['Price'] = invoiceDF['Price'].astype(float)
    invoiceDF['Discount'] = invoiceDF['Discount'].astype(float)
    
    invoiceDF = invoiceDF.set_index('Line')
    fullInvoice = {"Customer": str(cusName), "Phone Number": str(cusPhone), 
                   "Customer Number": int(cusNum), 
                   "Invoice Number": int(invoiceNum), 
                   "Invoice Date": str(invoiceDate), 
                   "Balance": int(cusBalance), 
                   "Invoice": invoiceDF.to_dict('index')}
    
    return jsonify(fullInvoice)
    
    
    
# Run the sumnab
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)