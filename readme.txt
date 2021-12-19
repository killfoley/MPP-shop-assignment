This file contains instructions for running each program and loading customer files in accordance with any of the shop programs.

To run shop.c first compile the shop.c file then run this file.
to run the python file navigate to the directory in terminal (mac) or windows equivalent

The following commands will run either program in the command line.
python shop.py
python shop_oop.py

The user will be prompted with a menu in the console.
choices are
customer csv orders or
live interactive mode.

The user can alternate between these options as the state of the shop will update after every order.
Note. Customer csv files are not edited after processing

stock.csv - This file is used to setup the shop initially with cash and product stock
customer.csv - This file will be executed correctly if selected initially.
john.csv - Test case for too many Coke Cans. Order should return not enough coke cans in stock but process everything else.
ann.csv - Test case. Ann only has enough money for 1 coke can. She orders 2
pete.csv - Test case. Pete tries to order 400 loaves of bread only 30 in stock initially (depending when file is loaded).
The program should partially fulfil Petes order.
