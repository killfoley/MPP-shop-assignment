import csv
import os

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

    # method to return quantity of product
    def get_quantity(self):
        return self.quantity

    # method to update the quantity of stock after an order is processed
    def update_quantity(self, custQty):
        self.quantity -= custQty
        return self.quantity

    # method to return a product
    def return_product(self):
        return self.product
        
    # repr method to return product name and available stock
    def __repr__(self):
        return f"Product Name: {self.product}, Product Stock: {self.quantity:.0f} pcs"

# Create a customer class to store customer details
class Customer:

    def __init__(self):
        self.shopping_list = []
        self.fileName = input("Please enter customer file name (without extension): ")
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
        out_str += f"Here is {self.name}'s shopping list:"
        out_str += f"-----------------------------------"
        numItems = 0
        for item in self.shopping_list:
            out_str += f"{item.name()}, qty. {item.quantity}"
            cost = item.cost()
            numItems += item.quantity
            # out_str += f"\n{item}"
            if (cost == 0):
                out_str += f" {self.name} doesn't know how much that costs :("
            else:
                out_str += f" COST: {cost}"
        out_str += f"Total: {self.num_Products:.0f} Product(s) ({numItems:.0f} Item(s))\n"
        out_str += f"\nThe total cost of your bill today is \n\n{self.order_cost():.2f} for {numItems:.0f} items ({self.num_Products:.0f} product(s)).\n"
        return out_str 
        
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
    

    def __repr__(self):
        str = ""
        str += f'Shop has €{self.cash} in cash\n'
        for item in self.stock:
            str += f"{item}\n"
        return str

def shop_menu(self):
    while True: 
        print(f'\nShop Menu - Choose an option below\n')
        print(f'----------------------------------\n')
        print(f'Select 1 for Shop Output\n')
        print(f'Select 2 for Customer order\n')
        print(f'Select 3 for Live shop mode\n')
        print(f'Select 0 to Leave the shop \n')
        print(f'----------------------------------\n')

        self.choice = input("")



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
    # s.shop_menu()
    
    
    print(s)
    c = Customer()
    c.calculate_costs(s.stock)
    print(c)

    
if __name__ == "__main__":
    main()