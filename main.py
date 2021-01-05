import mysql.connector
from faker import Faker
import random
import queries as q

'''
Authors:
Nikolaos Papadopoulos
Kristoffer Björklund

Version:
1.0

'''
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="oldplayer11",
    database="krinik"
)

mycursor = mydb.cursor(buffered=True)
# Two variables to track total amount of customers and game when filling tables
tot_customer = 0
tot_games = 0

# ================================ METHODS TO FILL DATABASE =====================================
def fill_customers():
    global tot_customer
    fake = Faker()  # module to create fake names
    genders = ["male","female"]  # two gender for simplicity
    for x in range(100):  # loop 100 times to add 100 new customers
        tot_customer = tot_customer+ 1  # increase global counter of customers
        # set name and gender of new customer
        gender = random.choice(genders)
        if gender == "male":
            c_name = fake.name_male()
        else:
            c_name = fake.name_female()
        sql = "INSERT INTO CUSTOMER (c_name, gender) VALUES (%s,%s)"
        val = (c_name, gender)
        mycursor.execute(sql, val)  # query into database
        mydb.commit()

def fill_games():
    global tot_games
    # Read the text file with games
    with open('games.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content]  # read and add them to list
    prices = [50,30,56,100,299,198,29,99,150,10,1000,499,90,333,45,1337,666] # list of different prices
    for game in content:
        tot_games = tot_games+1
        price = random.choice(prices) # set random price to random game
        g_name = game
        sql ="INSERT IGNORE INTO GAME (price, g_name) VALUES (%s,%s)"
        val = (price, g_name)
        mycursor.execute(sql, val)  # query games into database
        mydb.commit()

def fill_order(c_id, g_id):
    # take customer id and game id from consol
    sql_get_price = ("select price from krinik.game where g_id = %s" % g_id)  # Query to select price from game id entered
    total_price = mycursor.execute(sql_get_price, g_id)  # Execute query and use game id entered as value
    total_price = mycursor.fetchone()  # Fetches value from cursor
    #print("PRICE: ",tot_price)  # Error handling
    final_price = total_price[0]  # take first value since tot_price is a list
    sql = "INSERT IGNORE INTO ORDERS(c_id, total_price) VALUES (%s,%s)"  # SQL query to insert order into the table
    val = (c_id, final_price)
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "SELECT MAX(o_id) FROM krinik.orders"
    mycursor.execute(sql)
    o_id = mycursor.fetchone()
    sql = "INSERT IGNORE INTO ORDERINFO(o_id,game) VALUES(%s,%s)"
    val = (o_id[0], g_id)
    mycursor.execute(sql, val)
    mydb.commit()
# ==============================================================================================================

# Variables to set to true/false depending on what is desired

menuOptions = True  # Leave as true

def create_tables():
    # DROP TABLES IF THEY ALREADY EXIST
    mycursor.execute("DROP TABLE IF EXISTS Game")
    mycursor.execute("DROP TABLE IF EXISTS ORDERINFO")
    mycursor.execute("DROP TABLE IF EXISTS Orders")
    mycursor.execute("DROP TABLE IF EXISTS Customer")
    # TABLE CREATION
    mycursor.execute("use krinik;")
    mycursor.execute("CREATE TABLE CUSTOMER (c_id INT AUTO_INCREMENT PRIMARY KEY, c_name VARCHAR(255) NOT NULL, "
                     "gender VARCHAR(255) NOT NULL);")
    mycursor.execute("CREATE TABLE ORDERS(o_id INT AUTO_INCREMENT PRIMARY KEY, total_price INT NOT NULL,"
                     "c_id INT NOT NULL, FOREIGN KEY(c_id) REFERENCES CUSTOMER(c_id))")
    mycursor.execute("CREATE TABLE GAME (g_id INT AUTO_INCREMENT PRIMARY KEY, price INT NOT NULL,"
                     " g_name VARCHAR(255) NOT NULL);")
    mycursor.execute("CREATE TABLE ORDERINFO (info_id INT AUTO_INCREMENT PRIMARY KEY,o_id INT NOT NULL, "
                     "FOREIGN KEY(o_id) REFERENCES ORDERS(o_id)"
                     ", game VARCHAR(255) NOT NULL)")


def  fill_tables():
    fill_customers()
    fill_games()
    for x in range(500):
        c_id = random.randint(1,tot_customer)
        g_id = random.randint(1,tot_games)
        fill_order(c_id,g_id)

# ======================================METHODS FOR MENU BELOW================================================


def register_customer():
    # take name and gender input
    c_name = str(input("Enter Customer name: "))
    gender = str(input("Enter Customer gender: "))
    sql = "INSERT INTO CUSTOMER (c_name, gender) VALUES (%s,%s)"
    val = (c_name, gender)
    mycursor.execute(sql, val)  # query info into database
    mydb.commit()


def create_game():
    # take price and name as input
    price = int(input("Enter price of the new game: "))
    g_name = str(input("Enter the name of the new game: "))
    sql = "INSERT IGNORE INTO GAME (price, g_name) VALUES (%s,%s)"
    val = (price, g_name)
    mycursor.execute(sql, val)  # query info into database
    mydb.commit()


def place_order():
    not_done = True # Variable to check if the customer wants to continue shopping
    basket = [] # order basket
    final_price = 0 # Final price of the order
    c_id = input("Enter Customer ID: ")

    while not_done: # Continue adding games to basket until satisfied
        item = input("Enter a game ID to add to basket or type X to exit: ")

        if item == 'x' or item == 'X':
            break
        else:
            basket.append(item)
    for g_id in basket: # Calculate total price of the order
        sql_get_price = ("select price from krinik.game where g_id = %s" % g_id)  # Query to select price from game id entered
        mycursor.execute(sql_get_price, g_id)  # Execute query and use game id entered as value
        total_price = mycursor.fetchone()  # Fetches value from cursor
        final_price += total_price[0]  # take first value since tot_price is a list


    sql = "INSERT IGNORE INTO ORDERS(c_id, total_price) VALUES (%s,%s)"# SQL query to insert order into the table
    val = (c_id, final_price)
    mycursor.execute(sql, val)
    mydb.commit()

    sql = "SELECT MAX(o_id) FROM krinik.orders"  # Select the latest order ID which is MAX
    mycursor.execute(sql)
    o_id = mycursor.fetchone()
    sql = "INSERT IGNORE INTO ORDERINFO(o_id,game) VALUES(%s,%s)"
    # Insert order ID and game ID to order info
    for game in basket:
        val = (o_id[0], int(game))
        mycursor.execute(sql, val)
        mydb.commit()

    if len(basket) == 0:
        print("No order was placed, basket was empty!") # If basket was empty at checkout the user is notified
    else:
        print("NEW ORDER PLACED INTO DATABASE")


def view_specific_order():
    sql = "drop view if exists price;"
    mycursor.execute(sql)
    sql = " create view price as select price, g_id from game;"
    mycursor.execute(sql)
    o_id = input("Enter order ID: ")
    sql = ("SELECT o.o_id, p.price, o.c_id, oi.game from orders o inner join orderinfo as oi on oi.o_id = o.o_id join "
           "price as p on oi.game = p.g_id where o.o_id = %s" % o_id)  # Query to select specific order
    mycursor.execute(sql, o_id)
    result = mycursor.fetchall()  # Fetch the result into a list
    for order in result:
        print("Order ID:",order[0], "| Order price:$",order[1], "| Customer ID: ",order[2], "| Game ID: ",order[3])


def most_sold_game():
    mycursor.execute("DROP VIEW IF EXISTS topFiveGames")  # if view exists then drop it to create new.
    # We create a view and left join it with table game to only get games that are sold.
    sql = "CREATE VIEW topFiveGames as select ord.game, gm.g_name from krinik.orderinfo as ord " \
          "left join game as gm on ord.game = gm.g_id;"
    mycursor.execute(sql)  # execute first query to create view
    # We select the name of the game and the copies sold of that game from the view that we created.
    sql2 = "Select g_name, COUNT(g_name) as copies from topFiveGames GROUP BY g_name ORDER BY copies DESC LIMIT 5"
    mycursor.execute(sql2)
    result = mycursor.fetchall()
    print("Printing top five sold games\n=========================================")
    for row in result:
        print("Game name: ",row[0], )
        print("Copies Sold: ",row[1])
        print("=========================================")


def avg_game_cost():
    sql = "select AVG(price) as av from krinik.game"
    mycursor.execute(sql)
    avg_cost = mycursor.fetchone()
    print("The average cost of all games is: ",avg_cost[0])

def loyal_customer():
    mycursor.execute("DROP VIEW IF EXISTS loyalCustomer")  # if view exists we drop it
    # We create a view with customer id, customer name and prices from orders and join that with out customer table
    sql = "CREATE VIEW loyalCustomer as select ord.c_id, cs.c_name, ord.total_price from orders as ord " \
          "left join customer as cs on ord.c_id = cs.c_id"
    mycursor.execute(sql)  # execute sql above
    mycursor.execute("DROP VIEW IF EXISTS customersum")  # If customersum view exists we drop it
    # We create a new view with customer name and the sum of all of the customers purchases taken from previous view
    sql2 = "create view customerSum as SELECT distinct c_name as cus_name, sum(total_price) " \
           "as the_sum from loyalcustomer group by c_name"
    mycursor.execute(sql2) # execute query above
    # We select the customer with the highest amount purchased
    sql3 = "select cus_name, MAX(the_sum) as top from customersum group by the_sum order by the_sum DESC LIMIT 1"
    mycursor.execute(sql3) # execute query above
    most_loyal = mycursor.fetchone()
    print("Customer name: ",most_loyal[0],", Total amount spent: $",most_loyal[1])


def popular_gender_game():
    genders = ["male","female"]
    #drop views if exist to create new
    mycursor.execute("drop view if exists firstView;")
    mycursor.execute("drop view if exists getCustomer;")
    mycursor.execute("drop view if exists genderStat;")
    mycursor.execute("drop view if exists popGender;")
    #Create views to get game ID and order ID together
    mycursor.execute("create view firstView as SELECT oi.game, o.o_id from orderinfo as oi " \
          "left join orders as o on o.o_id = oi.o_id;")
    #Get customer ID and and game ID together
    mycursor.execute("create view getCustomer as SELECT o.c_id, fv.game from orders as o " \
          "left join firstView as fv on o.o_id = fv.o_id;")
    #Select the genders of the clients
    mycursor.execute("CREATE view genderStat as SELECT o.game, c.gender from getcustomer as o " \
          "right join customer as c on o.c_id = c.c_id;")
    gender = input("What gender do you want to look up (male or female): ")  # take input
    
    while gender not in genders:
        gender = input("What gender do you want to look up (male or female): ")

    # create view and select game id and the amount of times it occurs
    # to find the most sold game where the gender matches
    sql = ("create view popGender as select game, count(game) as times from genderStat where BINARY gender = '%s'" \
          " group by game order by times DESC LIMIT 5;" %gender)
    mycursor.execute(sql, gender)
    # We select the game name and the copies sold of that game from previous table
    mycursor.execute("SELECT times, g_name from popGender as p right join game as g on p.game = g.g_id" \
           " group by g_name order by times DESC LIMIT 1")
    result = mycursor.fetchone()
    print("Game name: ",result[1],", Copies sold: ",result[0])

# ================================ MENU ========================================


if menuOptions:

    options = ["0","1","2","3","4","5","6","7"] # Options for error handling
    print("======MENU======")
    print("1.Register Customer\n2.New order\n3.View Specific Order\n"
          "4.Show Store Statistics\n5.Add new game\n6.Fill tables with info\n7.Create new tables.\n0.Quit")

    choice = input("Enter menu choice: ")
    while choice not in options: # Error handling loop
        choice = input("Enter a valid menu choice (0-7): ")

    choice = int(choice) # converts input to int from str
    
    if choice == 1:
        register_customer()
    elif choice == 2:
        place_order()
    elif choice == 3:
        view_specific_order()
    elif choice == 4:
        print("\nSTATISTICS\n1.View most sold games.\n2.Average game cost.\n3.Our most loyal customer"
              "\n4.View gender statistics.")
        choice = int(input("\nWhat statistic do you want to view?: "))
        if choice == 1:
            most_sold_game()
        elif choice == 2:
            avg_game_cost()
        elif choice == 3:
            loyal_customer()
        elif choice == 4:
            popular_gender_game()
    elif choice == 5:
        create_game()
    elif choice == 6:
        fill_tables()
        print("Tables now filled with test data.")
    elif choice == 7:
        create_tables()
        print("New tables successfully created.")
    elif choice == 0:
        print("Game over.")
    else:
        print("Choice not an option.")


