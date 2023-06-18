#importing important libraries
import os
import csv
import json
from typing import List, Dict

# Function to read customer data from CSV file
def read_customer_data():
    customers = {}
    with open(r"C:\Users\Mohit\Downloads\Revolve Solutions - Python Assignment\python-assignment-level2-6ed53b4e828af18bc24b1770a3a3e3e70706e785\input_data\starter\customers.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            customer_id = row.get('customer_id')
            loyalty_score = int(row.get('loyalty_score', 0))
            customers[customer_id] = {
                'customer_id': customer_id,
                'loyalty_score': loyalty_score
            }
    return customers

# Function to read product data from CSV file
def read_product_data():
    products = {}
    with open(r"C:\Users\Mohit\Downloads\Revolve Solutions - Python Assignment\python-assignment-level2-6ed53b4e828af18bc24b1770a3a3e3e70706e785\input_data\starter\products.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_id = row.get('product_id')
            product_category = row.get('product_category')

            products[product_id] = {
                'product_id': product_id,
                'product_category': product_category
            }
    return products

# Function to read Transactions for every month
def read_transaction_data() -> List[Dict[str, str]]:
    transactions = []
    folder_path = "C:/Users/Mohit/Downloads/Revolve Solutions - Python Assignment/python-assignment-level2-6ed53b4e828af18bc24b1770a3a3e3e70706e785/input_data/starter/transactions/"
    # Iterate over months
    for month_folder in os.listdir(folder_path):
        month_folder_path = os.path.join(folder_path, month_folder)

        # Check if it's a directory
        if os.path.isdir(month_folder_path):
            json_file_path = os.path.join(month_folder_path, 'transactions.json')

            # Check if the JSON file exists
            if os.path.isfile(json_file_path):
                with open(json_file_path, 'r') as transactions_file:
                    for line in transactions_file:
                        transaction = json.loads(line)
                        transactions.append(transaction)

    return transactions

# Getting all the files together
def concate_data():
    # Loading customers, transactions, and products data
    customers = read_customer_data()
    transactions = read_transaction_data()
    products = read_product_data()

    # Create a dictionary to store the complete data
    complete_data = {}

    # Iterate over transactions
    for transaction in transactions:
        customer_id = transaction['customer_id']
        basket = transaction['basket']

        # Check if the customer exists in the complete data dictionary
        if customer_id not in complete_data:
            complete_data[customer_id] = {
                'customer_id': customer_id,
                'loyalty_score': customers[customer_id]['loyalty_score'],
                'purchases': {}
            }

        # Iterate over the products in the basket
        for product in basket:
            product_id = product['product_id']

            # Check if the product exists in the complete data dictionary
            if product_id not in complete_data[customer_id]['purchases']:
                product_category = products[product_id]['product_category']
                complete_data[customer_id]['purchases'][product_id] = {
                    'product_id': product_id,
                    'product_category': product_category,
                    'purchase_count': 0
                }

            # Increment the purchase count for the product
            complete_data[customer_id]['purchases'][product_id]['purchase_count'] += 1

    # Convert the complete data dictionary to a list of customer records
    
    return list(complete_data.values())




# Main function to orchestrate the data pipeline
def main():
    # Write output data
    with open('my_output.json', 'w') as output_file:
        json.dump(concate_data(), output_file)

if __name__ == '__main__':
    main()


