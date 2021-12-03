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


// Stocking the struct shop previously declared with the following function
struct Shop createAndStockShop()
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

	// Open the file in "r" read only mode.
    fp = fopen("../files/stock.csv", "r");
    
	// Error handling if file not found
	if (fp == NULL)
	{
		printf("No customer file was found");
		exit(EXIT_FAILURE);
	}
	
	// method to read the first line which has the opening cash balance of the shop
	read = getline(&line, &len, fp);
	// Opening cash balance
	float startingCash = atof(line);
	// printf("cash in shop is %.2f\n", cash);
	
	// Assigning cash balance to the shop struct
	struct Shop shop = {startingCash};

	// While loop to get data from input file
	// variables n, p, q are variables for product.name; product.price productstock.quantity
    while ((read = getline(&line, &len, fp)) != -1) {
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");
		// convert to int and floats
		int quantity = atoi(q);
		double price = atof(p);
		// Dynamically allocate memory for proudct name
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

/// read in customer from csv file
struct Customer createCustomer()
{   
    FILE * fp;
    //allocate enough memory for filename
    char *fileName = malloc(sizeof(char) * 1000);
    char *line = NULL;
    size_t len = 0;
    ssize_t read;

    printf("\nEnter Customer order file name: ");
    scanf("%s", fileName);
    
    // Conatentate strings to make the customer filename. http://www.cplusplus.com/reference/cstring/strcat/
	// "../"+"filename"+".csv"
    strcat(fileName, ".csv");
    char filePath[256] = "../files/";
    strcat(filePath, fileName);

    fp = fopen(filePath, "r"); 
	
	if (fp == NULL)
	{
		printf("No %s file was found\n", fileName);
		exit(EXIT_FAILURE);
	}

	// the first line has the customer name and budget
    read = getline(&line, &len, fp);
    // read the first line, break into 2 pieces using the tokeniser, customer name, customer budget
    char *n = strtok(line, ","); 
    char *b = strtok(NULL, ","); 
    char *name = malloc(sizeof(char) * 100);
    // avoid overwriting name each time by strtok
    strcpy(name, n);
    double budget = atof(b); // make it a double
    //create a customer struct 
    struct Customer customer = {name, budget}; 

    // add while loop to read rest of csv file
    while ((read = getline(&line, &len, fp)) != -1) {
        // need to strcpy for product name to stop it being overwritten when using strtok
        // product name n, quantity q on each line after line 1
        char *n = strtok(line, ","); 
        char *q = strtok(NULL, ","); 
        int quantity = atoi(q); // convert to integer
        // dynamically allocate new memory for storing the product name
        char *pname = malloc(sizeof(char) * 20); 
        // strcpy from pname to p to pname to avoid it being overwritten during the while loop
		strcpy(pname, n);
        // create a Product Struct and ProductStock struct for each item on shopping list
        struct Product product = { pname }; 
        struct ProductStock custItem = { product, quantity };
        //increment index
        customer.shoppingList[customer.index++] = custItem;
    }
    // return customer struct
    return customer;
    // this would exit the program completely but need to be the same as other versions
    //exit(EXIT_FAILURE);        
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
// Function to display menu
void shopMenu() {
	fflush(stdin);
    printf("\n");   
    printf("\nShop Menu - Choose an option below\n");
    printf("----------------------------------\n");
    printf("Select 1 for Shop Overview\n");
    printf("Select 2 for Customer order\n");
    printf("Select 3 for Live shop mode\n");
    printf("Select 0 to Leave the shop \n\n");
}

int main(void) 
{

	struct Shop shop = createAndStockShop();
	// printShop(shop);
	struct Customer customer = createCustomer();
	printCustomer(customer);
	printf("\n");

    return 0;
}


