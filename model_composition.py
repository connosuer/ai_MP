import importlib
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from web3 import Web3
import json

composition_bp = Blueprint('composition', __name__)

# Load contract ABI and address
with open("contract_abi.json", "r") as file:
    contract_abi = json.load(file)

with open("contract_address.txt", "r") as file:
    contract_address = file.read().strip()

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Create contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@composition_bp.route('/compose', methods=['GET', 'POST'])
def compose_model():
    if 'user_address' not in session:
        flash('Please log in to compose models.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        model_ids = request.form.getlist('model_ids')
        composition_name = request.form['composition_name']
        composition_description = request.form['composition_description']

        if validate_composition(model_ids):
            try:
                # Call smart contract to create composition
                tx_hash = contract.functions.createComposition(
                    composition_name,
                    composition_description,
                    model_ids
                ).transact({'from': session['user_address']})
                w3.eth.wait_for_transaction_receipt(tx_hash)
                flash('Model composition created successfully!', 'success')
                return redirect(url_for('marketplace.index'))
            except Exception as e:
                flash(f'Error creating composition: {str(e)}', 'error')
        else:
            flash('Invalid composition. Please check your selected models.', 'error')

    # Fetch available models for composition
    model_count = contract.functions.getModelCount().call()
    available_models = []
    for i in range(1, model_count + 1):
        model = contract.functions.getModel(i).call()
        available_models.append({
            'id': i,
            'name': model[0],
            'description': model[1]
        })

    return render_template('compose_model.html', available_models=available_models)

def validate_composition(model_ids):
    # Implement composition validation logic
    # For now, just check if at least two models are selected
    return len(model_ids) >= 2

def execute_composition(composition_id):
    composition = contract.functions.getComposition(composition_id).call()
    model_ids = composition[3]  # Assuming model_ids are in the fourth position
    
    results = []
    input_data = None  # This would typically come from user input
    
    for model_id in model_ids:
        model = contract.functions.getModel(model_id).call()
        model_name = model[0]
        ipfs_hash = model[5]  # Assuming ipfs_hash is in the sixth position
        
        # Here we would typically download the model from IPFS
        # For this example, we'll assume models are Python modules in a 'models' directory
        model_module = importlib.import_module(f'models.{model_name}')
        
        # Execute the model
        if input_data is None:
            input_data = get_initial_input()  # Function to get initial input from user
        output = model_module.run(input_data)
        
        results.append({
            'model_name': model_name,
            'output': output
        })
        
        input_data = output  # Use this model's output as input for the next model
    
    return results

def get_initial_input():
    # In a real application, this would get input from the user
    return {"text": "Sample input for the model composition"}

@composition_bp.route('/execute/<int:composition_id>', methods=['GET', 'POST'])
def execute_composition_route(composition_id):
    if request.method == 'POST':
        results = execute_composition(composition_id)
        return jsonify(results)
    return render_template('execute_composition.html', composition_id=composition_id)

@composition_bp.route('/compositions')
def view_compositions():
    composition_count = contract.functions.getCompositionCount().call()
    compositions = []
    for i in range(1, composition_count + 1):
        composition = contract.functions.getComposition(i).call()
        compositions.append({
            'id': i,
            'name': composition[0],
            'description': composition[1],
            'creator': composition[2],
            'model_ids': composition[3]
        })
    return render_template('view_compositions.html', compositions=compositions)