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
            if confirm_choice(f"You chose {choice}."):
                select_con_or_online()
                break       
        elif choice == "stock":
            if confirm_choice(f"You chose {choice}."):
                select_book()
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

def select_book():
    """
    allows the user to select which book they are updating the stock of.
    """
    while True:
        books = SHEET.worksheet('stock').get_all_values()[0]
        books.append("Add new book")
        i = 1
        print("which book would you like to update?")
        for x in books:
            print(f"{i}. {x}")
            i=i+1
        book = int(input(f"Please enter a number between 1 and {len(books)}\n"))-1
        if book <= len(books):
            if book != len(books)-1:
                print(len(books))
                print (book)
                stock(books[book])
                break
            else:
                add_book()
                break
        print(f"Incorrect data. Please enter a number between 1 and {len(books)}\n")    
    
def stock(book):
    """
    function that allows the user to update stock levels of all comic books.
    """    
    while True:
        print(f"updating stock for {book}...")
        stock = []
        stock.append(input("How much stock have you ordered?\n"))
        stock.append(input("How much did the restock cost?\n"))
        stock.append(input("What is the date of the order?\n"))
        stock.append(round(int(stock[1])/int(stock[0]),2))
       
        if confirm_choice(f"On {stock[2]}, you ordered {stock[0]} copies of {book} for £{stock[1]} which works out at cpu £{stock[3]}"):
            print("updating stock")
            break
        
    update_sheet(stock, book)
            
def update_sheet(data, sheet):
    """
    Updates worksheets and adds new row with data provided.
    Adapted from the love_sandwiches code along project. 
    """
    print(f"Updating {sheet} worksheet...")
    worksheet = SHEET.worksheet(sheet)
    worksheet.append_row(data)
    print(f"{sheet} worksheet updated successfully.\n")

def run_again():
    """
    Gives the user the option to rerun the program after it finishes
    """
    while True:
        choice = input("Do you want to update another input? y/n \n")
        if choice == "y":
            stock_or_sales()
        elif choice == "n":
            print("Thank you for using the comic stock tracker.")
            break
        else:
            print("you have made an incorrect selection. Please try again")

def recalculate_cpu(sheet):
    """
    Reworks out the average CPU 
    """
    print("Recalculating cost per unit...") 
    worksheet = SHEET.worksheet(sheet).col_values(4)
    total = 0
    for ind in range(1,len(worksheet)):
        total = total + float(worksheet[ind])
    cpu = total / (len(worksheet)-1)
    return cpu

def select_con_or_online():
    """
    allows the user to enter the source of the sale. Either online or convention sales. 
    If convention sales are chosen then it prompts for the name of the convention. 
    """
    while True: 
        source = input(f"Are you updating online or convention sales?\n")
        if source == "onlinye":
            if confirm_choice(f"You are updating {source} sales."):
                sales(source)
                break
        elif source == "convention":
            if confirm_choice(f"You are updating {source} sales."):
                convention = input(f"Which convention are you updating?\n")
                sales(convention)
                break
        else:
            print("you have made an incorrect selection. Please try again")


def sales(source):
    """
    updates the spreadsheet with sale info
    """
    sales = SHEET.worksheet("sales").get_all_values()
    books = sales[0]
    data = [source]
    date = input(f"Please enter the date of sale\n")
    data.append(date)
    for ind in range(2,len(sales[0])):
        data.append(input(f"Enter sale numbers for {books[ind]}\n"))
    update_sheet(data, "sales")
    if source != "online":
        update_con_costs(source, date)

def update_con_costs(source, date):
    """
    updates the cons sheet with all costs incurred and uses these to work out the total profit
    """
    while True: 
        data = [source, date]
        data.append(input(f"Please enter the table costs for {source} convention\n"))
        data.append(input(f"Please enter the travel costs for {source} convention\n"))
        data.append(input(f"Please enter the parking costs for {source} convention\n"))
        data.append(input(f"Please enter any misc costs for {source} convention\n"))
        total_costs = 0
        for ind in range(2,len(data)):
            total_costs = total_costs + int(data[ind])
        data.append(total_costs)
        if confirm_choice(f"You are updating the sales for {source} convention. \n Table costs are £{data[3]} \n Travel costs are £{data[4]} \n Misc costs are £{data[5]}\n"):
            update_sheet(data, "cons")
            break
comics = []
def add_book():
    """
    adds comic book to the comics list to allow data to be easily accessed. 
    """
    keys = ["title","sale price","cpu","profit per sale"]
    book = {}
    title = input(f"What is the title of the book?\n")
    price = input(f"What is the sale price of the book?\n")
    book[keys[0]] = title
    book[keys[1]] = price
    book[keys[2]] = 0
    book[keys[3]] = float(book[keys[1]])- book[keys[2]]
    comics.append(book)
    new_spreadsheet(title)
    update_headers(title)

    

def new_spreadsheet(title):
    """
    creates a new worksheet to track stock levels. 
    """
    worksheet = SHEET.add_worksheet(title= title, rows="100", cols="20")
    update_sheet(["restock","cost","date","cost per unit", "price"], title)

def update_headers(title):
    stock = SHEET.worksheet("stock")
    sales = SHEET.worksheet("sales")
    num = len(stock.get_all_values()[0])
    stock_row = chr(num+65)+"1"
    sales_row = chr(num+67)+"1"
    stock.update(stock_row,title)
    sales.update(sales_row,title)
    
def update_price(title, price):
    """
    updates the price of a new book onto the price worksheet
    """
    pricework = SHEET.worksheet("price")
    y = len(pricework.get_all_values())+1
    title_cell = "A"+str(y)
    price_cell = "B"+str(y)
    pricework.update(title_cell, title)
    pricework.update(price_cell, price)

        

def populate_comic_list():
    """
    creates a dictionary with sales data for each book.
    """
    print("loading application data...")
    keys = ["title","sale price","cpu","profit per sale"]
    book = {}
    sales = SHEET.worksheet('sales').get_all_values()
    titles = data[0]
    for ind in range(2,len(titles)):
        stock = SHEET.worksheet(titles[ind])
        book[keys[0]] = titles[ind]
        book[keys[1]] = float(stock.col_values(5)[-1])
        book[keys[2]] = float(stock.col_values(4)[-1])
        book[keys[3]] = book[keys[1]]- book[keys[2]]
        comics.append(book.copy())
    print("Application data loaded.")



def main():
    """
    Runs all program functions
    """
    populate_comic_list()
    print("Welcome to the comic stock tracker.")
    stock_or_sales()
    run_again()

# main()


