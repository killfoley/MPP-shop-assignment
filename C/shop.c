// This program is a project for Multi-Paradigm Programming 2021
// The program is a shop which can process csv orders or run in a live mode where products can be purchased
// Program was created by Killian Foley - G00387875
// Include C libraries
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Declare struct for products (name and price)
struct Product {
	char *name;
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
	char *name;
	double budget;
	struct ProductStock shoppingList[10];
	int index;
};

// Function to print product details from the shop. Name an Price
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

void printShop(struct Shop *shop)
{
	printf("The Shop opening float is €%.2f cash\n", shop->cash);
	for (int i = 0; i < shop->index; i++)
	{
		printProduct(shop->stock[i].product);
		printf("Product Quantity: %d pcs\n", shop->stock[i].quantity);
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

    printf("\nEnter Customer order file name (without extension): ");
    scanf("%s", fileName);
    
    // Conatentate strings to make the customer filename. http://www.cplusplus.com/reference/cstring/strcat/
	// "../"+"filename"+".csv"
    strcat(fileName, ".csv");
    char filePath[256] = "../files/";
    strcat(filePath, fileName);

    fp = fopen(filePath, "r"); 
	
	// error handling if no such file exists
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
        // strcpy from n to pname to avoid it being overwritten during the while loop
		strcpy(pname, n);
        // create a Product Struct and ProductStock struct for each item on shopping list
        struct Product product = { pname }; 
        struct ProductStock custItem = { product, quantity };
        // increment index
        customer.shoppingList[customer.index++] = custItem;
    }
    // return customer struct
    return customer;  
}

// print customer details and their shopping list. return price
double printCustomer(struct Customer *cust, struct Shop *shop)
{
	printf("-------------\n");
	printf("Customer Name: %s \nCustomer Budget: %.2f\n", cust->name, cust->budget);
	
  // declare grand total variable
  double grandTotal = 0.0;

  // print customer's shopping list
  printf("\nHere is %s's shopping list:\n", cust->name);
  printf("----------\n");

	for (int i = 0; i < cust->index; i++) // incremenet index variable as looping through the list)
  {
    // Print out shopping list name and quantity
    printf("%s, qty. %d.\n", cust->shoppingList[i].product.name, cust->shoppingList[i].quantity); // using pointers to access shopping list
	}
	// check for product match from customer's shopping list with shop products in stock. Set to 0 to start and increment when a product matches
  int billProducts = 0;
  // declare a total quantity variable for the final bill
  int totalQuantity = 0;
  printf("\nChecking Stock...\n\n");
  //loop over the items in the customer shopping list
  for (int i = 0; i < cust->index; i++) // incremenet index variable as looping through the list)
  {
    // Print out current product from shopping list
    printf("Product %i x %i: %s\n", i+1, cust->shoppingList[i].quantity ,cust->shoppingList[i].product.name); // using pointers to access shopping list

    // Declare variable for sub total of shopping bill. Each item will be added to this
    double subTotal = 0;
    // declare matchExists variable to track if a product matches. This is inside the for loop.
    int matchExists = 0;
    // declare Customer Product name variable shopping list items
    char *CustomerProductName = cust->shoppingList[i].product.name; 

    // Iterate through shop stock list to match items from customer's shopping list
	  // This is inside the customer shopping list loop so use j here as iterator variable.
    for (int j = 0; j < shop->index; j++)
    {
      char *ShopProductName = shop->stock[j].product.name;
	    // if true, both product names are identical
      if (strcmp(CustomerProductName, ShopProductName) == 0) 
      {
        matchExists++; // increment by one when there is a match
        billProducts++; // add to bill items
        // check if shop has enough stock
        if (cust->shoppingList[i].quantity <= shop->stock[j].quantity)
        {
          // Calculate cost for item completely in stock
          double subTotalItem = cust->shoppingList[i].quantity * shop->stock[j].product.price; // List qty * price
          printf("In Stock! Line item cost will be €%.2f.\n", subTotalItem); // Prints total cost of the product
          subTotal = subTotalItem; // sub total cost for the current item
          totalQuantity = totalQuantity + cust->shoppingList[i].quantity;
        }
		    // customer wants more than in stock
        else
        {
          // check max that can be purchased
          int partialProductQty = cust->shoppingList[i].quantity - (cust->shoppingList[i].quantity - shop->stock[j].quantity); // Set to all available stock

          // calculate cost for partial order quantity
          double subTotalPartial = partialProductQty * shop->stock[j].product.price; // partial qty * price
          printf("Unfortunately only %d in stock. Line item cost will be €%.2f.\n", partialProductQty, subTotalPartial); // Prints out cost of all items of the product
          // add to subTotal
          subTotal = subTotalPartial;
          // add to quantity value
          totalQuantity = totalQuantity + partialProductQty;
        }
        // add sub total to grandTotal
        grandTotal = grandTotal + subTotal;
      }
    }
    // if customer wants a product that is not in the shop
    if (matchExists == 0) // there is no match of product
    {
      printf("Unfortunately %s is not in stock. You will not be charged \n", cust->shoppingList[i].product.name); // Prints out cost of all items of the product
    }
  }
  // printf("%i", billProducts);
  printf("\nThe total cost of your bill today is \n€%.2f for %i items (%i products). \n\n", grandTotal, totalQuantity, billProducts); // Prints out cost of all items of the product
  
  return grandTotal;
}

// Function to process the order. i.e. update shop stock and float
void processOrder(struct Customer *cust, struct Shop *shop, double *grandTotal)
{
    printf("Processing Order...");
  // Check if the customer can afford their order
  if (cust->budget < *grandTotal) // insufficient customer funds
  {
    printf("Sorry you have insufficient funds, you are short by €%.2f.\n", (*grandTotal - cust->budget));
    printf("Your order cannot be fulfilled at this time.\n");
    printf("Please try again with a smaller quantity!\n");
  }
  else // customer has enough money
  {
    printf("Updatng the shop...\n");
    //loop over the items in the customer shopping list
    for (int i = 0; i < cust->index; i++) // Using index defined in struct to keep track of items
    {
      // check whether the product from customer's shopping list matches with the shop stock list of products
      int matchExists = 0; // initialy set to zero, assuming there is no match
      char *customerProductName = cust->shoppingList[i].product.name; // create temp variables for cust item and shop item to make strcmp easier

      // Iterate through shop stock list to match items from customer's shopping list
      for (int j = 0; j < shop->index; j++)
      {
        char *shopProductName = shop->stock[j].product.name; // assign the j-th product from the shop stock list as a shorthand

        if (strcmp(customerProductName, shopProductName) == 0) // if true, both product names are identical
        {
          matchExists++; // increment when there is a match
          //check products availability
          if (cust->shoppingList[i].quantity <= shop->stock[j].quantity) // The shop has enough stock
          {
            // Update the shop's stock by subtracting the customer order
            shop->stock[j].quantity = shop->stock[j].quantity - cust->shoppingList[i].quantity;
            printf("Stock update: %s now has %d pcs in stock.\n", cust->shoppingList[i].product.name, shop->stock[j].quantity);
          }

          else // customer wants more than in stock
          {
            // Return maximum amount available
            int partialProductQty = cust->shoppingList[i].quantity - (cust->shoppingList[i].quantity - shop->stock[j].quantity); // Set to all available stock

            // calculate the total cost for this item price * qty
            double subTotalPartial = partialProductQty * shop->stock[j].product.price; // partial qty * price
            
            // update the shop's stock for this item
            shop->stock[j].quantity = shop->stock[j].quantity - partialProductQty;

            printf("Stock update: %s now has %d pcs in stock.\n", cust->shoppingList[i].product.name, shop->stock[j].quantity);
          }
        }
      }
      // if customer wants a product that is not in the shop
      if (matchExists == 0) // there is no match of product
      {
        printf("Product: %s is currently not in stock.\n", cust->shoppingList[i].product.name); // Prints out cost of all items of the product
      }
    }

    // update the cash in shop
    shop->cash = shop->cash + *grandTotal;

    // update the customer's money
    cust->budget = (cust->budget - *grandTotal);

    printf("\nThe shop now has €%.2f in cash.\n", shop->cash);
    printf("\n%s's new budget is €%.2f in cash.\n", cust->name, cust->budget);
    printf("\n");
  };

  return; 
}
// function for live shop mode
void shopLiveMode(struct Shop *shop)
{
  fflush(stdin);
  // declare customer name variable. Allocate enough memory
  char *customer_name = malloc(sizeof(char)*10); 
  double budget;
  printf("\nWelcome to Shop in C live mode\n");
  printf("-------------------------\n");
  // get user's name
  printf("Please enter your name: ");
  scanf("%s", customer_name);
  // Get the users budget
  fflush(stdin);
  printf("\nPlease enter your budget: ");
  scanf("%lf", &budget);
  printf("\nWelcome %s! Your budget today is %.2f.\n", customer_name, budget);

  // declare shop variables for product name and quantity
  char productName[100];
  double quantity;
  // declare liveshop total spend
  double liveTotal;
  // print shops stock
  printf("\nThe following products are available in the shop:\n");
  printShop(&(*shop));
  // Clear the input
  // fflush(stdin);
  // Use a forever loop for desired product entry until '' is entered
  while (strcmp(productName, "q") != 0)
  { 
    // Clear input. Print was printing twice
    fflush(stdin);
    // get customer to enter product
    printf("\nPlease enter a product name (Note: Products are case sensitive. Enter 'q' when done): ");
    // https://www.tutorialspoint.com/c_standard_library/c_function_fgets.htm
    fgets(productName, (int) sizeof(productName), stdin);
    // https://stackoverflow.com/questions/18168722/using-fgets-and-strcmp-in-c?lq=1
    // Strip the new line character 
    productName[strlen(productName)-1] = '\0';
    // Iterate through shop stock list to match items from customer's shopping list
    for (int i = 0; i < shop->index; i++) 
    {
      // declare subtotal for each line item. Set to 0
      double subTotal = 0;
      // assign shop stock to temporary variable to compare to shopping list items
      char *shopProductName = shop->stock[i].product.name;
      // match condition
      if (strcmp(productName, shopProductName) == 0)
      {
        printf("\nEnter desired quantity: ");
        scanf("%lf", &quantity);
        //check products availability
        if (quantity <= shop->stock[i].quantity) // sufficient amount of the product in the shop stock
        {
          // check product price and calculate sub-total cost (price*qty)
          subTotal = shop->stock[i].product.price * quantity;
          liveTotal = liveTotal + subTotal;
          // check if customer can afford it
          if (budget >= subTotal)
          {
            // update customer's budget
            budget = budget - subTotal;
            printf("\nSuccess. Product cost was €%.2f. Your new budget is: €%.2f.\n", subTotal, budget);
            // update the shop stock (full order)
            shop->stock[i].quantity = shop->stock[i].quantity - quantity;
            // update the shops cash
            shop->cash = shop->cash + subTotal;
            printf("\nStock quantity of %s in shop updated to: %d. Cash in shop now: %.2f.\n", productName, shop->stock[i].quantity, shop->cash);
          }
          // Budget < than subTotal
          else
          {
            printf("\nSorry you have insufficient funds. The difference is €%.2f.\n", (subTotal - budget));
          }
          }
          // customer requests more than in stock
          else
          {
          // check how many can be bought
          int partialProductQty = quantity - (quantity - shop->stock[i].quantity); // will buy all that is in stock
          // calculate sub total for line item
          double subTotalPartial = partialProductQty * shop->stock[i].product.price;
          liveTotal = liveTotal + subTotalPartial;
          // Print out cost to customer                                             
          printf("\nSorry only %d units available. Line item cost will be €%.2f.\n", partialProductQty, subTotalPartial);
          // update the customer's budget
          budget = budget - subTotalPartial;
          printf("\nYour new budget is: €%.2f.\n", budget);
          // update the shop stock (partial order) and cash
          shop->stock[i].quantity = shop->stock[i].quantity - partialProductQty;
          // update the shop cash
          shop->cash = shop->cash + subTotalPartial;
          printf("\nProduct %s is now out of stock (stock: %d).\nThe shop float is now: €%.2f.\n",shop->stock[i].product.name, shop->stock[i].quantity, shop->cash);
        }
      }
      else if (strcmp(productName, shopProductName) != 0) // product not available in stock
      {
        printf("");
      }
    }
  }
printf("\nYour total today was €%.2f.\n", liveTotal);
printf("\nThank you for shopping in C live mode!\n");

}

// Function to display menu
void shopMenu() {
	fflush(stdin); 
    printf("\nShop Menu - Choose an option below\n");
    printf("----------------------------------\n");
    printf("Select 1 for Shop Output\n");
    printf("Select 2 for Customer order\n");
    printf("Select 3 for Live shop mode\n");
    printf("Select 0 to Leave the shop \n");
    printf("----------------------------------\n");
}

// Function to clear the screen depending on the operating system
// https://iq.opengenus.org/detect-operating-system-in-c/
void clearScreen(){
  #if _WIN32
    system("cls");
  #elif __linux__
    system("clear");
  #elif __unix__
    system("clear");
  #elif __APPLE__
    system("clear");
  #endif
}

int main(void) 
{
  // Clearing screen
  clearScreen();
  printf("Shop in C project by Killian Foley\n\n");
  // Create and stock the shop
  printf("Opening today's shop.\n");
	struct Shop shop = createAndStockShop();
  // Display the shopping menu
  shopMenu();
  // While loop for shop menu
  int choice = -1;
  while (choice != 0){
    // clear input
    fflush(stdin);
    // Prompt for user choice
    printf("Please select an option from the menu: ");
    scanf("%d", &choice);
    
    if (choice == 1){
      printf("\nOption 1: Displaying Shop Stock\n");
      printShop(&shop);
      shopMenu();
    }
    else if (choice == 2){
      printf("\nOption 2: Process Customer Order\n");
      struct Customer customer = createCustomer();
      if (customer.budget == 0){
        printf("Customer has no money\n");  
        shopMenu();
      }
      else {
        double grandTotal = printCustomer(&customer, &shop);
        // Check customer budget before processing order
          if (grandTotal > customer.budget){
              printf("Sorry you have insufficient funds, you are short by €%.2f.\n", (grandTotal - customer.budget));
              printf("Your order cannot be fulfilled at this time. Please try again with a smaller quantity!\n\n");
          }
          else {
              processOrder(&customer, &shop, &grandTotal);
              shopMenu();
              }
        }  
    }  
    else if (choice == 3){
        printf("\nOption 3: Live Shop Mode\n");
        shopLiveMode(&shop);
        shopMenu();
    }
  }
  printf("\n======================================\n");
  printf("\n\nThanks for shopping in 'Shop in C'\n\n");
  printf("\n======================================\n");
  return 0;
}


