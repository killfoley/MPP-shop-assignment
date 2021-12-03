#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Declare struct for products (name and price)
struct Product {
	char* name;
	double price;
};

// Declare the struct for the quantity of the product
struct ProductStock {
	struct Product product;
	int quantity;
};

// Declare the struct for the shop containing available cash float and product stock quantity.
// An index is declare for looping through the rows in the file 
struct Shop {
	double cash;
	struct ProductStock stock[20];
	int index;
};

// Declare the struct for a Customer containing their name and budget variables
// An index is declare for looping through the rows in the file
struct Customer {
	char* name;
	double budget;
	struct ProductStock shoppingList[10];
	int index;
};

// Function to print product details from the shop. Name an PRice
void printProduct(struct Product p)
{
	printf("-------------\n");
	printf("Product Name: %s \nProduct Price: €%.2f\n", p.name, p.price);
}

void printCustomer(struct Customer c)
{
	printf("-------------\n");
	printf("Customer Name: %s \nCustomer Budget: %.2f\n", c.name, c.budget);
	printf("-------------\n");
	for(int i = 0; i < c.index; i++)
	{
		printProduct(c.shoppingList[i].product);
		printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity);
		double cost = c.shoppingList[i].quantity * c.shoppingList[i].product.price; 
		printf("The cost to %s will be €%.2f\n", c.name, cost);
	}
}

// Stocking the struct shop previously declared with the following function
struct Shop createAndStockShop()
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

	// Open the file in "r" read only mode.
    fp = fopen("../files/stock.csv", "r");
    if (fp == NULL)
	{
		printf("No stock file was found");
		exit(EXIT_FAILURE);
	}
	
	// method to read the first line which has the opening cash balance of the shop
	read = getline(&line, &len, fp);
	// Opening cash balance
	float startingCash = atof(line);
	// printf("cash in shop is %.2f\n", cash);
	
	// Assigning cash balance to the shop struct
	struct Shop shop = {startingCash};

    while ((read = getline(&line, &len, fp)) != -1) {
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");
		int quantity = atoi(q);
		double price = atof(p);
		char *name = malloc(sizeof(char) * 50);
		strcpy(name, n);
		struct Product product = { name, price };
		struct ProductStock stockItem = { product, quantity };
		shop.stock[shop.index++] = stockItem;
    }
	
	return shop;
}

void printShop(struct Shop s)
{
	printf("\nThe Shop opening float is €%.2f cash\n", s.cash);
	for (int i = 0; i < s.index; i++)
	{
		printProduct(s.stock[i].product);
		printf("Product Quantity: %d pcs\n", s.stock[i].quantity);
	}
}

int main(void) 
{
	struct Shop shop = createAndStockShop();
	printShop(shop);
	printf("\n");
	
    return 0;
}