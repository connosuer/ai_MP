from flask import Flask, render_template, request, redirect, url_for, flash
from web3 import Web3
import json
from marketplace_interface import list_model, purchase_model, get_model_count, get_model_details

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Load contract ABI and address
with open("contract_abi.json", "r") as file:
    contract_abi = json.load(file)

with open("contract_address.txt", "r") as file:
    contract_address = file.read().strip()

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    model_count = get_model_count()
    models = []
    for i in range(1, model_count + 1):
        model = get_model_details(i)
        if model:
            model['id'] = i
            models.append(model)
    return render_template('index.html', models=models)

@app.route('/list_model', methods=['GET', 'POST'])
def list_model_route():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = w3.to_wei(float(request.form['price']), 'ether')
        from_address = request.form['from_address']
        
        receipt = list_model(name, description, price, from_address)
        if receipt:
            flash('Model listed successfully!', 'success')
        else:
            flash('Failed to list model.', 'error')
        return redirect(url_for('index'))
    return render_template('list_model.html')

@app.route('/purchase_model/<int:model_id>', methods=['POST'])
def purchase_model_route(model_id):
    from_address = request.form['from_address']
    model = get_model_details(model_id)
    if model and model['isAvailable']:
        receipt = purchase_model(model_id, model['price'], from_address)
        if receipt:
            flash('Model purchased successfully!', 'success')
        else:
            flash('Failed to purchase model.', 'error')
    else:
        flash('Model is not available for purchase.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)