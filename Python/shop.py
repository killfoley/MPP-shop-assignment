# This program simulates a shop using procedural programming in Python
from dataclasses import dataclass, field
from typing import List
import csv
import os

@dataclass
class Product:
    """Class for storing product data: name and price"""
    name: str
    price: float = 0.0

@dataclass 
class ProductStock:
    """Class for storing Product Stock information: Product and Quantity"""
    product: Product
    quantity: int

@dataclass 
class Shop:
    """Class for storing the shops cash and list of product stock"""
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    """Class for storing customer information: Budget & Shopping List"""
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list)

def create_and_stock_shop():
    s = Shop()
    with open('../files/stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
            #print(ps)
    return s
    
def read_customer():
    fileName = str(input("\nPlease enter customer file name (without extension): "))
    file_path = "../files/" + fileName + ".csv"
    c = Customer()
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        cust = Customer(first_row[0], float(first_row[1]))
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            cust.shopping_list.append(ps)
        return cust 
        
# Function to print product name and price
def print_product(p):
    if p.price == 0:
        print(f'\nProduct Name: {p.name}\n')
    else:
        print(f'\nProduct Name: {p.name} \nProduct Price: €{p.price:.2f}\n')

# Function to print customer
def print_customer(cust, shop):
    print(f'\nCustomer Name: {cust.name} \nCustomer Budget: {cust.budget}\n')
    # grandTotal variable for shopping
    grandTotal = 0.0
    billProducts = 0
    totalQuantity = 0
    # For loop to access all shopping list items print the customer shopping list
    print(f"Here is {cust.name}'s shopping list")
    numProd = len(cust.shopping_list)
    numItems = 0
    print(f'---------------')
    for item in cust.shopping_list:
        print(f'{item.product.name} qty. {item.quantity}')
        numItems += item.quantity
        # print_product(item.product)
        # print(f'{cust.name} orders {item.quantity} of above product\n')
        # cost = item.quantity * item.product.price
        # print(f'The cost to {cust.name} will be €{cost}')
    print(f'Total: {numProd:.0f} Products ({numItems:.0f} Items)')
    print(f'\nProcessing.......\n')
    # loop through shopping list to calculate cost
    for index, item in enumerate(cust.shopping_list):
        print(f'Product {index+1} x {item.quantity:.0f}: {item.product.name}')
        # declare variable for subtotal
        subTotal = 0.0
        # Loop through shop stock
        for prod in shop.stock:
            if (item.product.name == prod.product.name):
                # if there is a match add to products on the bill
                billProducts += 1
                # Check stock in the shop
                if (item.quantity <= prod.quantity):
                    lineTotal = item.quantity * prod.product.price
                    # add to bill subTotal
                    subTotal += lineTotal
                    # add to bill item quantity
                    totalQuantity += item.quantity
                    print(f'In Stock! @ €{prod.product.price:.2f} ea. Line item cost will be €{lineTotal:.2f}.\n')
                else:
                    # check the amount that can be bought
                    partialLineItem = item.quantity - (item.quantity - prod.quantity)
                    partialLineSubTot = partialLineItem * prod.product.price
                    print(f'Unfortunately only {partialLineItem:.0f} in stock. @ {prod.product.price:.2f} ea. Line item cost will be €{partialLineSubTot:.2f}.\n')
                    # Add to Products on the bill and subTotal
                    totalQuantity += partialLineItem
                    subTotal += partialLineSubTot
                grandTotal += subTotal
            elif (item.product.name != prod.product.name):
                print(f'Unfortunately {item.product.name} is not in stock. You will not be charged \n')
    print(f'The total cost of your bill today is \n€{grandTotal:.2f} for {totalQuantity:.0f} items ({billProducts:.0f} products).\n')
    return grandTotal

def process_order(cust, shop, grandTotal):
    print(f'Processing your order...\n')
    # Check if the customer can afford their order
    if (cust.budget < grandTotal):
        print(f'Sorry, you have insufficient funds, you are short by €{grandTotal - cust.budget:.2f}\n')
        print(f'Your order cannot be fulfilled at this time.\n')
        print(f'Please try again with a smaller quantity!\n')
    # or if customer does have enough money
    else:
        print(f'Updating the shop...\n\n')

# Function to print shop stock and price
def print_shop(shop):
    print(f'Shop has {shop.cash} in cash')
    for item in shop.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above product')


def shopMenu():
    print(f'\nShop Menu - Choose an option below\n')
    print(f'----------------------------------\n')
    print(f'Select 1 for Shop Output\n')
    print(f'Select 2 for Customer order\n')
    print(f'Select 3 for Live shop mode\n')
    print(f'Select 0 to Leave the shop \n')
    print(f'----------------------------------\n')

def main():
    s = create_and_stock_shop()
    print_shop(s)
    c = read_customer()
    print_customer(c, s)
    # shopMenu()




if __name__ == "__main__":
    main()