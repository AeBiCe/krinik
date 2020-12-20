import mysql.connector
'''
authors:
Nikolaos Papadopoulos
Kristoffer Björklund

'''
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="oldplayer11",
    database="krinik"
)

mycursor = mydb.cursor(buffered=True)

createTables = False
menuOptions = True
#First draft of create tables.
if createTables:
    mycursor.execute("DROP TABLE IF EXISTS Orders")
    mycursor.execute("DROP TABLE IF EXISTS Customer")
    mycursor.execute("DROP TABLE IF EXISTS Game")

    mycursor.execute("CREATE TABLE CUSTOMER (c_id INT AUTO_INCREMENT PRIMARY KEY, c_name VARCHAR(255) NOT NULL, "
                     "gender VARCHAR(255) NOT NULL)")
    mycursor.execute("CREATE TABLE GAME (g_id INT AUTO_INCREMENT PRIMARY KEY, price INT NOT NULL,"
                     " g_name VARCHAR(255) NOT NULL)")
    mycursor.execute("CREATE TABLE ORDERS (o_id INT AUTO_INCREMENT PRIMARY KEY, c_id INT NOT NULL, "
                     "g_id INT NOT NULL, total_price INT NOT NULL, "
                     "FOREIGN KEY(c_id) REFERENCES CUSTOMER(c_id), FOREIGN KEY(g_id) REFERENCES GAME(g_id))")


def register_customer():
    c_name = str(input("Enter Customer name: "))
    gender = str(input("Enter Customer gender: "))
    sql = "INSERT INTO CUSTOMER (c_name, gender) VALUES (%s,%s)"
    val = (c_name, gender)
    mycursor.execute(sql, val)
    mydb.commit()


def create_game():
    price = int(input("Enter price of the new game: "))
    g_name = str(input("Enter the name of the new game: "))
    sql = "INSERT INTO GAME (price, g_name) VALUES (%s,%s)"
    val = (price, g_name)
    mycursor.execute(sql, val)
    mydb.commit()


def place_order():
    # take customer id and game id from consol
    c_id = int(input("Enter Customer ID: "))
    g_id = int(input("Enter game ID: "))
    sql_get_price = ("select price from krinik.game where g_id = %s" % g_id)  # Query to select price from game id entered
    total_price = mycursor.execute(sql_get_price, g_id)  # Execute query and use game id entered as value
    tot_price = mycursor.fetchone() # Fetches value from cursor
    #print("PRICE: ",tot_price)  # Error handling
    final_price = int(tot_price[0]) # take first value since tot_price is a list
    sql = "INSERT INTO ORDER(c_id, g_id, total_price) VALUES (%s,%s,%s)"  # SQL query to insert order into the table
    val = (c_id, g_id, final_price)
    mycursor.execute(sql, val)
    mydb.commit()


if menuOptions:

    print("======MENU======")
    print("1.Register Customer\n2.Delete customer*TEMP*\n3.New order\n4.View Specific Order\n"
          "5.Show Store Statistics\n6.Add new game\n0.Quit")

    choice = int(input("Enter menu choice: "))
    if choice == 1:
        register_customer()
    elif choice == 2:
        print("Second choice")
    elif choice == 3:
        place_order()
    elif choice == 4:
        print("Fourth choice")
    elif choice == 5:
        print("Fifth choice")
    elif choice == 6:
        create_game()
    elif choice == 0:
        print("Game over.")
    else:
        print("Choice not an option.")


