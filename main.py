'''
authors:
Nikolaos Papadopoulos
Kristoffer Björklund

'''

print("======MENU======")
print("1.Register Customer\n2.Change customer info*TEMP*\n3.New order\n4.View Specific Order\n"
      "5.Show Store Statistics\n0.Quit")



choice = int(input("Enter menu choice: "))
if choice == 1:
    print("First choice")
elif choice == 2:
    print("Second choice")
elif choice == 3:
    print("Third choice")
elif choice == 4:
    print("Fourth choice")
elif choice == 5:
    print("Fifth choice")
elif choice == 0:
    print("Game over.")
else:
    print("Choice not an option.")


