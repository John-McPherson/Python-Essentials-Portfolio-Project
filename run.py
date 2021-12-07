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
    choice = input("would you like to input stock or sales?\n").lower()
    if choice == "sales":
        confirm_choice(choice)
        
    elif choice == "stock":
        confirm_choice(choice)
        
    else:
        print("you have made an incorrect selection. Please try again")
        stock_or_sales()

def confirm_choice(choice):
    """
    prompts the user to confirm their choice. 

    """
    confirm = input(f"you have chosen {choice} is that correct? y/n\n")
    if confirm == "y":
        print(f"Loading {choice} function")
    elif confirm == "n":
        stock_or_sales()
    else:
        print("you have made an incorrect selection. Please try again")
        confirm_choice(choice)

    

    

def main():
    """
    Runs all program functions
    """
    print("Welcome to the comic stock tracker.")
    
    stock_or_sales()

   
    

main()


