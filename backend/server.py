from flask import Flask, request, jsonify
import products_dao
from sql_connection import get_sql_connection

app = Flask(__name__)

@app.route('/getproducts', methods=['GET'])
def get_products():
    connection = get_sql_connection()  # Added line to get the database connection
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    connection.close()  # Added line to close the connection after use
    return response

@app.route('/deleteproducts',methods=['POST'])
def delete_product():
    return_id=products_dao.delete_product(connection,request.form['product_id'])
    response = jsonify({
        'product_id':return_id
    })
    response.headers.add('Access-Control-Allow-Origin','*')
    return response


if __name__=="__main__":
    print("Starting Python Flask Server For NVDS Grocery store Managemeny System")
    app.run(port=5000)