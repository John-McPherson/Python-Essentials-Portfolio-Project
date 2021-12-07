import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('comic_sales')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

def stock_or_sales():
    """
    Allows the user to choose if they want to update stock or sales
    """
    while True:
        choice = input("would you like to input stock or sales?\n").lower()
        if choice == "sales":
            print("This feature has not been enabled yet")
            
        elif choice == "stock":
            if confirm_choice(f"You chose {choice}."):
                stock("Deadbeat")
                break

        else:
            print("you have made an incorrect selection. Please try again")
            

def confirm_choice(choice):
    """
    prompts the user to confirm their choice. 

    """
    confirm = input(f"{choice} is that correct? y/n\n")
    if confirm == "y":
        return True
    elif confirm == "n":
        return False
    else:
        print("you have made an incorrect selection. Please try again")
        confirm_choice(choice)

def stock(data):
    """
    function that allows the user to update stock levels of all comic books.
    """    
    while True:
        print(f"updating stock for {data}...")
        stock = []
        stock.append(input("How much stock have you ordered?\n"))
        stock.append(input("How much did the restock cost?\n"))
        stock.append(input("What is the date of the order?\n"))
        stock.append(round(int(stock[1])/int(stock[0]),2))
       
        if confirm_choice(f"On {stock[2]}, you ordered {stock[0]} copies of {data} for £{stock[1]} which works out at cpu £{stock[3]}"):
            print("updating stock")
            break
        
    return stock
            


    # worksheet = SHEET.worksheet('deadbeat')

    # print(deadbeat)


    

def main():
    """
    Runs all program functions
    """
    print("Welcome to the comic stock tracker.")
    
    stock_or_sales()

   
    

main()


