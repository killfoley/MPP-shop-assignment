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
        print(f'\nProduct Name: {p.name}')
    else:
        print(f'\nProduct Name: {p.name} \nProduct Price: €{p.price:.2f}')

# Function to print customer
def print_customer(cust, shop):
    print(f'\nCustomer Name: {cust.name} \nCustomer Budget: €{cust.budget:.2f}\n')
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
        print(f'{item.product.name} qty. {item.quantity:.0f}')
        numItems += item.quantity
        # print_product(item.product)
        # print(f'{cust.name} orders {item.quantity} of above product\n')
        # cost = item.quantity * item.product.price
        # print(f'The cost to {cust.name} will be €{cost}')
    print(f'Total: {numProd:.0f} Product(s) ({numItems:.0f} Item(s))')
    print(f'\nProcessing.......\n')
    # loop through shopping list to calculate cost
    for index, item in enumerate(cust.shopping_list):
        print(f'Product {index+1} x {item.quantity:.0f}: {item.product.name}')
        # declare variable for subtotal
        subTotal = 0.0
        #declare counter variable for a match
        valueMatch = 0
        # Loop through shop stock
        for prod in shop.stock:
            if (item.product.name == prod.product.name):
                # add 1 to valueMatch
                valueMatch += 1
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
                # Check zero condition first
                elif (prod.quantity == 0):
                    print(f'{item.product.name} is currently not in stock. You will not be charged.\n')
                elif (item.quantity > prod.quantity):
                    # check the amount that can be bought
                    partialLineItem = item.quantity - (item.quantity - prod.quantity)
                    partialLineSubTot = partialLineItem * prod.product.price
                    print(f'Unfortunately only {partialLineItem:.0f} in stock. @ {prod.product.price:.2f} ea. Line item cost will be €{partialLineSubTot:.2f}.\n')
                    # Add to Products on the bill and subTotal
                    totalQuantity += partialLineItem
                    subTotal += partialLineSubTot
                # add the subtotal to the grand total
                grandTotal += subTotal
        if (valueMatch == 0):
            print(f'Unfortunately {item.product.name} is not in stock. You will not be charged \n')
    print(f'The total cost of your bill today is \n\n€{grandTotal:.2f} for {totalQuantity:.0f} items ({billProducts:.0f} products).\n')
    return grandTotal

def process_order(cust, shop, grandTotal):
    print(f'Processing your order...\n')
    # Check if the customer can afford their order
    if (cust.budget < grandTotal):
        print(f'Sorry, you have insufficient funds, you are short by €{grandTotal - cust.budget:.2f}\n')
        print(f'\nYour order cannot be fulfilled at this time.')
        print(f'\nPlease try again with a smaller quantity!\n')
    # or if customer does have enough money
    else:
        print(f'Updating the shop...\n')
        print(f'********************\n')
        # iterate through shopping list items
        for item in cust.shopping_list:
            # declare valueMatch counter for product match
            valueMatch = 0
            for prod in shop.stock:
                if (item.product.name == prod.product.name):
                    valueMatch += 1
                    #check product availability
                    if (item.quantity <= prod.quantity):
                        prod.quantity = prod.quantity - item.quantity
                        print(f"Stock update: {prod.product.name} now has {prod.quantity:.0f} pcs in stock.\n")
                    # if customer wants more than in stock
                    elif (item.quantity > prod.quantity):
                        partialOrderQty = item.quantity - (item.quantity - prod.quantity)
                        # calculate this cost
                        partialOrderCost = partialOrderQty * prod.product.price
                        # update the stock
                        prod.quantity = prod.quantity - partialOrderQty
                        # Print stock update
                        print(f"Stock Update: {prod.product.name} now has {prod.quantity:.0f} pcs in stock.\n")
            if (valueMatch == 0): 
                print(f'Product: {item.product.name} is currently not in stock.\n')
        # update the shop's cash
        shop.cash += grandTotal
        # Update the customer's budget
        cust.budget -= grandTotal
        print(f"The shop now has €{shop.cash:.2f} in cash.\n")
        print(f"{cust.name}'s new budget is €{cust.budget:.2f} in cash.\n")

# Function to print shop stock and price
def print_shop(shop):
    print(f'Shop has {shop.cash} in cash')
    for item in shop.stock:
        print_product(item.product)
        print(f'Product Quantity: {item.quantity:.0f} pcs')

def live_shop_mode(shop):
    print(f"Welcome to Shop in Python live mode")
    print(f"-----------------------------------")
    customerName = input("\nPlease enter your name: ")
    budget = float(input("\nPlease enter your budget: "))
    print(f"\nWelcome {customerName} your budget today is €{budget:.2f}\n")
    # declare input variables
    productName = ""
    quantity = 0
    # declare total for shoppers bill
    liveTotal = 0
    print(f'The following products are available in the shop:\n')
    print_shop(shop)
    # start while loop for shopper to purchase products
    while productName != "q":
        productName = input("\nPlease enter a product name (Note: Products are case sensitive. Enter 'q' when done): ")
        # check for match with shop products
        valueMatch = 0
        for prod in shop.stock:
            subTotal = 0
            # if there is a match get the shoppers quantity
            if (productName == prod.product.name):
                valueMatch += 1
                quantity = int(input("\nEnter desired quantity: "))
                # check product stock
                if (quantity <= prod.quantity):
                    subTotal = quantity * prod.product.price
                    liveTotal += subTotal
                    # Check if the customer can afford the order
                    if (budget >= subTotal):
                        budget = budget - subTotal
                        print(f"\nSuccess. Product cost was €{subTotal:.2f} Your new budget is: €{budget:.2f}.\n")
                        # Update the shop stock
                        prod.quantity = prod.quantity - quantity
                        # Update the cash in the shop
                        shop.cash += subTotal
                        print(f"Stock quantity of {prod.product.name} in shop updated to: {prod.quantity:.0f}.\n\nCash in shop now: €{shop.cash:.2f}.");
                    else:
                        print(f"Sorry you have insufficient funds. The difference is €{subTotal - budget:.2f}.\n")
                # Customer requests more than in stock
                else:
                    # check how many can be bought
                    partialProductQty = quantity - (quantity - prod.quantity)
                    # calculate sub total for line item
                    subTotalPartial = partialProductQty * shop.product.price
                    liveTotal += subTotalPartial
                    # Print out cost to customer                                             
                    print(f"Sorry only {partialProductQty:.0f} pcs available. Line item cost will be €{subTotal:.2f}.\n")
                    # update the customer's budget
                    budget = budget - subTotalPartial
                    print(f"Your new budget is: €{budget:.2f}.\n")
                    # update the shop stock (partial order) and cash
                    prod.quantity = prod.quantity - partialProductQty
                    # update the shop cash
                    shop.cash += subTotalPartial
                    print(f"Product {prod.product.name} is now out of stock (stock: {prod.quantity}).\nThe shop float is now: €{shop.case:.2f}.\n")
        if (valueMatch == 0):
            print(f"Product not found. Please try again.\n")
    # Customer has quit. Print their total.
    print(f"Your total today was €{liveTotal:.2f}\n")
    print(f"Thank you for shopping in Python live mode!\n")
            
# clear screen function depending on os
# https://www.geeksforgeeks.org/clear-screen-python/
def clear_screen():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def shop_menu():
    print(f'\nShop Menu - Choose an option below\n')
    print(f'----------------------------------\n')
    print(f'Select 1 for Shop Output\n')
    print(f'Select 2 for Customer order\n')
    print(f'Select 3 for Live shop mode\n')
    print(f'Select 0 to Leave the shop \n')
    print(f'----------------------------------\n')

def main():
    clear_screen()
    print(f"Shop in Python (procedural) project by Killian Foley.\n")
    # Create and stock the shop
    print(f"Opening today's shop.")
    shop = create_and_stock_shop()
    # display menu first time
    shop_menu()
    # forever loop
    while True:
        # display the menu
        choice = input("Please select an option from the menu: ")

        if (choice == "1"):
            print(f"\nOption 1: Displaying Shop stock")
            print_shop(shop)
            shop_menu()

        elif (choice == "2"):
            print(f"\nOption 2: Process Customer Order")
            customer = read_customer()
            if(customer.budget == 0):
                print(f"Customer has no money.")
                shop_menu()
            else:
                grandTotal = print_customer(customer, shop)
                # check customer budget before processing order
                if (grandTotal > customer.budget):
                    print(f"Sorry you have insufficient funds, you are short by €{grandTotal - customer.budget:.2f}\n")
                    print(f"Your order cannot be fulfilled at this time.\n\nPlease try again with a smaller quantity!\n")
                    shop_menu()
                else:
                    process_order(customer, shop, grandTotal)
                    shop_menu()
        
        elif (choice == "3"):
            print(f"\nOption 3: Live Shop Mode\n")
            live_shop_mode(shop)
            shop_menu()
    
        elif(choice == "0"):
            print(f"\n======================================\n")
            print(f"Thanks for shopping in 'Shop in Python'\n")
            print(f"======================================\n")
            break;

        else:
            shop_menu()

if __name__ == "__main__":
    main()