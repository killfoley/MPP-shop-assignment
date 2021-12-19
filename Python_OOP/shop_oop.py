import csv
import os
from sys import exit

# Create a product class
class Product:

    def __init__(self, name, price=0):
        self.name = name
        self.price = price
    
    def __repr__(self):
        return f'Product: {self.name} Price: €{self.price}'

# Create a ProductStock class
class ProductStock:
    
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
    
    # method to return product name
    def name(self):
        return self.product.name;
    
    # method to return unit price
    def unit_price(self):
        return self.product.price;
        
    # method to return cost of a product/ line item
    def cost(self):
        return self.unit_price() * self.quantity

    # method to return product
    def get_product(self):
        return self
        
    # repr method to return product name and available stock
    def __repr__(self):
        return f'\nName:\t{self.product.name}\nPrice:\t€{self.product.price:.2f}\nStock:\t{self.quantity:.0f} pcs\n{"-"*15}\n'

# Create a customer class to store customer details
class Customer:

    def __init__(self):
        self.shopping_list = []
        self.fileName = input("\bPlease enter customer file name (without extension): ")
        filePath = "../files/" + self.fileName + ".csv"
        with open(filePath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])
                p = Product(name)
                ps = ProductStock(p, quantity)
                self.shopping_list.append(ps) 
                
    def calculate_costs(self, price_list):
        # loop through items in shop first
        for shop_item in price_list:
            # loop through items in the customers list
            for list_item in self.shopping_list:
                if (list_item.name() == shop_item.name()):
                    list_item.product.price = shop_item.unit_price()
    
    # method to calculate item using productstock cost method
    def order_cost(self):
        totalCost = 0
        # loop through list items in list to calculate cost        
        for list_item in self.shopping_list:
            totalCost += list_item.cost()
        return totalCost
    
    # method to return number ofr
    def num_products(self):
        numProd = len(self.shopping_list)
        return numProd

    def __repr__(self):
        out_str = f"\nCustomer Name: {self.name} \nCustomer Budget: €{self.budget:.2f}\n"
        out_str += f"\nHere is {self.name}'s shopping list:\n"
        out_str += f"-----------------------------------\n\n"
        numItems = 0
        for item in self.shopping_list:
            out_str += f"{item.name()}, qty. {item.quantity:.0f}\n"
            cost = item.cost()
            numItems += item.quantity
            # out_str += f"\n{item}"
            if (cost == 0):
                out_str += f"No price available. Product might be out of stock.\n"
            else:
                out_str += f"Cost: €{cost:.2f} @ €{item.unit_price():.2f} ea.\n"
        out_str += f"\nBasket summary: {self.num_products():.0f} Product(s) ({numItems:.0f} Item(s))\n"
        out_str += f"\nThe total cost of your bill today is \n\n€{self.order_cost():.2f} for {numItems:.0f} items ({self.num_products():.0f} product(s)).\n"
        return out_str 
        
# Create a live mode sub class of customer to use customer methods
class Live_Mode(Customer):
    def __init__(self, Shop):
        self.shopping_list = []
        self.name = input("Please enter your name: ")
        self.budget = float(input("\nPlease enter your budget: "))
        print(f'\nWelcome {self.name} your budget today is €{self.budget:.2f}\n')     
        print(f'The following products are available in the shop:\n')
        print(Shop) 
        
    # Method to get the live customer list
    def get_list(self, Shop):
        # declare product and quantity variables to append to shopping list. Similar to csv file input
        productName = ""
        quantity = 0
        # while loop to take customer products
        while (productName != "q"):
            productName = input("\nPlease enter a product name (Note: Products are case sensitive. Enter 'q' when done): ")
            # loop through shop items for a match. This wouldn't be efficient for a larger stock. But deemed sufficient here.
            for shop_item in Shop.stock:
                # if there is a product match then request quantity and append to shopping list.
                if (productName == shop_item.name()): #(productName != "q") and 
                    quantity = int(input("\nEnter desired quantity: "))
                    # append the items to the shopping list
                    p = Product(productName)
                    ps = ProductStock(p, quantity)
                    self.shopping_list.append(ps)
                    break;
                elif (productName == "q"):
                    return None
            else:
                print(f'\nSorry item not in stock please try another product.')
        # for testing print(self.shopping_list)

# create a shop class
# the shop class stores the stock, calculates cost based off customer basket 
class Shop:
    
    def __init__(self, path):
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = ProductStock(p, float(row[2]))
                self.stock.append(ps)
    
    # representation of the shop
    def __repr__(self):
        str = ""
        str += f'Shop has €{self.cash:.2f} in cash\n'
        str += f'\nProduct Details:\n'
        for item in self.stock:
            str += f"{item}"
        return str

    # method to check and update stock
    def check_stock(self, list_item):
        # checking the stock
        for shop_item in self.stock:
            # if the shop does stock the customer item
            if (list_item.name() == shop_item.name()):
                # assign shop_item name to product_name variable
                self.product_name = shop_item.name()
                # get the product stock details and return the product for the update stock method to use
                self.product = shop_item.get_product()
                # checking if there is enough stock 
                if list_item.quantity <= shop_item.quantity:
                    # update the shop stock
                    shop_item.quantity -= list_item.quantity
                    # enough in stock. Line item cost = qty * price
                    self.lineItemCost = list_item.quantity * shop_item.product.price
                    # store the line item quantity for updating shop stock
                    self.lineQty = list_item.quantity
                    return self.lineItemCost, self.product, self.lineQty, self.product_name,
                
                # check zero stock condition first
                elif shop_item.quantity == 0:
                    print(f'{shop_item.name()} is currently not in stock. You will not be charged.\n')
                
                # checking if the customer order quantity is more than shop has in stock
                elif (list_item.quantity > shop_item.quantity):
                    # total product cost is based on partial order if thats all that is available   
                    self.lineItemCost = shop_item.quantity *shop_item.product.price
                    self.lineQty = shop_item.quantity
                    print(f"Sorry only {shop_item.quantity:.0f} pcs available of {list_item.name()}. Line item cost will be €{self.lineItemCost:.2f}.\n")
                    # update the stock
                    shop_item.quantity -= self.lineQty
                    return self.lineItemCost, self.product, self.lineQty, self.product_name

            # if the customer product is not stocked, sale quantity is zero and no cost to customer. Avoid printing out later
            if (list_item.name() != shop_item.name()):
                self.product = list_item
                self.lineQty = 0
                self.lineItemCost = 0

    # method to update cash in the shop
    def update_cash(self,c):
        custTotal = c.order_cost()
        # only print for actual sale quantities
        if self.lineQty>0:
            print(f"Product: {self.product.name()}\nProduct total = €{self.lineItemCost:.2f} for {self.lineQty} pc(s).\n")
            self.cash += self.lineItemCost
            c.budget -= self.lineItemCost
        # if customer cannot pay, then sale does not go ahead. 
        elif c.budget < self.lineItemCost:
            print(f"Sorry you have insufficient funds, you are short by €{custTotal - c.budget:.2f}\n")
            print(f"Your order cannot be fulfilled at this time.\n\nPlease try again with a smaller quantity!\n")
        return c.budget, self.cash
            
    # method for processing order. inputs self and customer. Returns customer new budget
    def process_order(self,c):
        # create a list of items for stock updates
        self.stock_items = []
        print(f"Processing your order\n")
        self.lineItemCost = 0
        print(f"Calculating costs\n")
        for list_item in c.shopping_list:
            for shop_item in self.stock:
                if (list_item.name() == shop_item.name()):
                    self.stock_items.append(shop_item)
        for list_item in c.shopping_list:
            # call the method to check stock
            self.check_stock(list_item)
            # call the method to update cash or not
            self.update_cash(c)
        # print stock updates for purchased items
        print(f"Updating shop\n")
        for stock_item in self.stock_items:
            print(f"Stock update: {stock_item.name()} now has {stock_item.quantity:.0f} pcs in stock\n")
        # print out new shop float
        print(f"The shop now has €{self.cash:.2f} in cash.\n")
        # print out new customer budget
        print(f"{c.name}\'s new budget is €{c.budget:.2f}\n")

    def shop_menu(self):
        while True: 
            print(f'**********************************\n')
            print(f'Shop Menu - Choose an option below\n')
            print(f'**********************************\n')
            print(f'Select 1 for Shop Output\n')
            print(f'Select 2 for Customer order\n')
            print(f'Select 3 for Live shop mode\n')
            print(f'Select 0 to Leave the shop \n')
            print(f'**********************************\n')

            self.choice = input("Please select an option from the menu: ")

            if (self.choice == "1"):
                print(f"\nOption 1: Displaying Shop stock\n")
                print(self)

            elif (self.choice == "2"):
                print(f"\nOption 2: Process Customer Order\n")  
                # Create a customer by uploading a customer csv file
                c = Customer()
                # perform a check if customer has a budget
                if (c.budget == 0):
                    print(f'Customer has no money.\n')
                    self.shop_menu()
                # if customer budget != proceed.
                else:
                    # Calculate grandTotal of customer order
                    c.calculate_costs(self.stock)
                    grandTotal = c.order_cost()
                    # if customer order total > than their budget let them know to reduce order qtys
                    if (grandTotal > c.budget):
                        print(f"\nSorry you have insufficient funds, you are short by €{grandTotal - c.budget:.2f}\n")
                        print(f"Your order cannot be fulfilled at this time.\n\nPlease try again with a smaller quantity!\n")
                        self.shop_menu()
                    # check if customer total is 0
                    elif (grandTotal == 0):
                        print(f"Please update your shopping list to include items currently in stock.\n")
                        self.shop_menu()
                    # if customer has enough money then process their order
                    else:
                        c.calculate_costs(self.stock)
                        print(c)
                        self.process_order(c)
                        self.shop_menu()
                # c.calculate_costs(self.stock)
                # print out the customer order and basket details
                #print(c)
                # 
                #self.process_order(c)


            elif (self.choice == "3"):
                print(f"\nOption 3: Live Shop Mode\n")
                c = Live_Mode(self)
                c.get_list(self)
                # calculate live method similar to csv method
                c.calculate_costs(self.stock)
                # print out the customer order and basket details
                print(c)
                # process the customer order
                self.process_order(c)


            elif (self.choice == "0"):
                print(f"\n======================================\n")
                print(f"Thanks for shopping in 'Shop in Python'\n")
                print(f"======================================\n")
                exit()

            else:
                print(f'\nInvalid option please try again')

def clear_screen():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def main():
    clear_screen()
    print(f"Shop in Python (object oriented) project by Killian Foley.\n")
    # create and stock the shop
    s = Shop("../files/stock.csv")
    s.shop_menu()
    
    
if __name__ == "__main__":
    main()