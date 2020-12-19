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

mycursor = mydb.cursor()

createTables = True
#First draft of create tables.
if createTables:
    mycursor.execute("CREATE TABLE ORDERS (o_id VARCHAR(255), cus_id VARCHAR(255), game_id VARCHAR(255), total_price VARCHAR(255))")
    mycursor.execute("CREATE TABLE CUSTOMER (c_id VARCHAR(255), c_name VARCHAR(255), gender VARCHAR(255))")
    mycursor.execute("CREATE TABLE GAME (g_id VARCHAR(255), price VARCHAR(255), g_name VARCHAR(255))")


# print("======MENU======")
# print("1.Register Customer\n2.Change customer info*TEMP*\n3.New order\n4.View Specific Order\n"
#       "5.Show Store Statistics\n0.Quit")
#
# choice = int(input("Enter menu choice: "))
# if choice == 1:
#     print("First choice")
# elif choice == 2:
#     print("Second choice")
# elif choice == 3:
#     print("Third choice")
# elif choice == 4:
#     print("Fourth choice")
# elif choice == 5:
#     print("Fifth choice")
# elif choice == 0:
#     print("Game over.")
# else:
#     print("Choice not an option.")


