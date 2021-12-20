import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("comic_sales")

sales = SHEET.worksheet("sales")

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
        books = SHEET.worksheet("stock").get_all_values()[0]
        books.append("Add new book")
        i = 1
        print("which book would you like to update?")
        for x in books:
            print(f"{i}. {x}")
            i = i + 1
        book = (
            int(input(f"Please enter a number between 1 and {len(books)}\n"))
            - 1
        )
        if book <= len(books):
            if book != len(books) - 1:
                print(len(books))
                print(book)
                print(book)
                restock_book(books[book], book)
                break
            else:
                add_book(book)
                break
        print(
            f"Incorrect data. Please enter a number between 1 and {len(books)}\
            \n"
        )


def restock_book(book, index):
    """
    function that allows the user to update stock levels of all comic books.
    """
    print("test stock")
    while True:
        print(f"updating stock for {book}...")
        stock = []
        while True:
            restock = input("How much stock have you ordered?\n")
            if validate_input(restock):
                stock.append(restock)
                break
        while True:
            cost = input("How much did the restock cost?\n")
            if validate_input(cost):
                stock.append(cost)
                break
        while True:
            date = input("What is the date of the order?\n")
            if validate_date(date):
                stock.append(date)
                break
        stock.append(round(int(stock[1]) / int(stock[0]), 2))
        if confirm_choice(
            f"On {stock[2]}, you ordered {stock[0]} copies of {book} for £{stock[1]} "
            f"which works out at cpu £{stock[3]}"
        ):
            print("updating stock")
            break
    update_sheet(stock, book)
    update_stock_restock(restock, index)


def update_stock_levels(stock_data):
    """
    Updates total stock level adding books on a restock
    and removing them whenever sales are computed.
    """
    print("updating total stock levels...")
    stock = SHEET.worksheet("stock")
    books = stock.get_all_values()
    new_stock_level = []
    col = 65
    x = 0

    for ind in books[-1]:
        restock = int(ind) - int(stock_data[x])
        if restock < 50:
            order_prompt(books[0][x], x)
            stock = SHEET.worksheet("stock")
            restock = stock.acell(chr(col) + "2").value
        x += 1
        col += 1
        new_stock_level.append(restock)
    col = 65
    for x in new_stock_level:
        stock.update(chr(col) + "2", x)
        col += 1
    print("Total stock levels updated...")


def order_prompt(book, index):
    """
    Asks the user if they want to restock a book if stocks are low.
    """
    while True:
        choice = input(
            f"stock level of {book} is low.\n Would you like to restock? y/n\n"
        )
        if choice == "y":
            restock_book(book, index)
            break
        elif choice == "n":
            break
        else:
            print("you have made an incorrect selection. Please try again")


def update_stock_restock(stock_data, index):
    """
    updates stock tracking sheet, adding the restock value to current stock.
    """
    print("Updating total stock levels...")
    stock = SHEET.worksheet("stock")
    col = str(chr(65 + index)) + "2"
    current_stock = stock.acell(col).value
    if current_stock is None:
        current_stock = 0
    stock.update(col, int(stock_data) + int(current_stock))
    print(f"{col} {int(stock_data)+int(current_stock)}")
    print("Total stock levels updated.")


def update_sheet(update_data, sheet):
    """
    Updates worksheets and adds new row with data provided.
    Adapted from the love_sandwiches code along project.
    """
    print(f"Updating {sheet} worksheet...")
    worksheet = SHEET.worksheet(sheet)
    worksheet.append_row(update_data)
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
    for ind in range(1, len(worksheet)):
        total = total + float(worksheet[ind])
    cpu = total / (len(worksheet) - 1)
    return cpu


def select_con_or_online():
    """
    allows the user to enter the source of the sale.
    Either online or convention sales. If convention sales
    are chosen then it prompts for the name of the convention.
    """
    while True:
        source = input("Are you updating online or convention sales?\n")
        if source == "online":
            if confirm_choice(f"You are updating {source} sales."):
                update_sales(source)
                break
        elif source == "convention":
            if confirm_choice(f"You are updating {source} sales."):
                convention = input("Which convention are you updating?\n")
                update_sales(convention)
                break
        else:
            print("you have made an incorrect selection. Please try again")


def update_sales(source):
    """
    updates the spreadsheet with sale info
    """
    sales_sheet = SHEET.worksheet("sales").get_all_values()
    books = sales_sheet[0]
    output = [source]
    profit = []
    profit_per_sale = get_profit_per_sale()
    y = 0
    while True:
        date = input("Please enter the date of sale\n")
        if validate_date(date):
            output.append(date)
            break
    for ind in range(2, len(sales_sheet[0])):
        while True:
            x = input(f"Enter sale numbers for {books[ind]}\n")
            if validate_input(x):
                profit.append(int(x) * float(profit_per_sale[y]))
                output.append(x)
                y += 1
                break
    update_sheet(output, "sales")
    update_stock_levels(output[2:None])
    profit = total_profit(profit)
    if source != "online":
        update_con_costs(source, date, profit)


def total_profit(profit_array):
    """
    works out sum of total profit when passed an array.
    """
    total = 0
    for ind in profit_array:
        total += ind
    return total


def update_con_costs(source, date, profit):
    """
    updates the cons sheet with all costs incurred and uses
    these to work out the total profit
    """
    while True:
        output = [source, date]
        while True:
            table_costs = input(
                f"Please enter the table costs for {source} convention\n"
            )
            if validate_input(table_costs):
                output.append(table_costs)
                break
        while True:
            travel_costs = input(
                f"Please enter the travel costs for {source} convention\n"
            )
            if validate_input(travel_costs):
                output.append(travel_costs)
                break
        while True:
            parking_costs = input(
                f"Please enter the parking costs for {source} convention\n"
            )
            if validate_input(parking_costs):
                output.append(parking_costs)
                break
        while True:
            misc_costs = input(
                f"Please enter any misc costs for {source} convention\n"
            )
            if validate_input(misc_costs):
                output.append(misc_costs)
                break
        total_costs = 0
        for ind in range(2, len(output)):
            total_costs = total_costs + int(output[ind])
        net_profit = profit - total_costs
        output.append(net_profit)
        output.append(total_costs)
        if confirm_choice(
            f"You are updating the sales for {source} convention.\n"
            f"Table costs are £{output[3]} \n Travel costs are £{output[4]}\n"
            f"Misc costs are £{output[5]}\n"
        ):
            update_sheet(output, "cons")
            break


comics = []


def add_book(index):
    """
    adds comic book to the comics list to allow data to be easily accessed.
    """
    keys = ["title", "sale price", "cpu", "profit per sale"]
    book = {}
    title = input("What is the title of the book?\n")
    while True:
        price = input("What is the sale price of the book?\n")
        if validate_input(price):
            book[keys[0]] = title
            book[keys[1]] = price
            book[keys[2]] = 0
            book[keys[3]] = float(book[keys[1]]) - book[keys[2]]
            break
    comics.append(book)
    new_spreadsheet(title)
    update_headers(title)
    update_price(title, price)
    restock_book(title, index)


def validate_input(user_input):
    """
    Checks the user input and confirms that the
    input is the expected data type.
    """
    try:
        float(user_input)
    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False
    return True


def validate_date(user_input):
    """
    Checks the user input and confirms that the input is the a valid date.
    """
    date = str(user_input).split("/")
    try:
        if len(date) != 3:
            raise ValueError(
                "The date inputed is incorrect.\
                 Please provide date in the following format dd/mm/yyyy"
            )
        import datetime

        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))

    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False
    return True


def new_spreadsheet(title):
    """
    creates a new worksheet to track stock levels.
    """
    SHEET.add_worksheet(title=title, rows="100", cols="20")
    update_sheet(["restock", "cost", "date", "cost per unit"], title)


def update_headers(title):
    """
    Updates headers for the stock and sales
    worksheet whenever a new book is added.
    """
    stock = SHEET.worksheet("stock")
    sales_sheet = SHEET.worksheet("sales")
    num = len(stock.get_all_values()[0])
    stock_row = chr(num + 65) + "1"
    sales_row = chr(num + 67) + "1"
    stock.update(stock_row, title)
    sales_sheet.update(sales_row, title)


def update_price(title, price):
    """
    updates the price of a new book onto the price worksheet
    """
    pricework = SHEET.worksheet("price")
    y = len(pricework.get_all_values()) + 1
    title_cell = "A" + str(y)
    price_cell = "B" + str(y)
    pricework.update(title_cell, title)
    pricework.update(price_cell, price)


def populate_comic_list():
    """
    creates a dictionary with sales data for each book.
    """
    print("loading application data...")
    keys = ["title", "sale price", "cpu", "profit per sale"]
    book = {}
    titles = data[0]
    x = 0
    for ind in range(2, len(titles)):
        stock = SHEET.worksheet(titles[ind])
        price = SHEET.worksheet("price")
        book[keys[0]] = titles[ind]
        book[keys[1]] = float(price.get_all_values()[x][1])
        book[keys[2]] = float(stock.col_values(4)[-1])
        book[keys[3]] = book[keys[1]] - book[keys[2]]
        x += 1
        comics.append(book.copy())
    print("Application data loaded.")


def get_profit_per_sale():
    """
    generates an array with the profit per sale for each book.
    """
    profit_list = []
    for ind in comics:
        profit_list.append(ind.get("profit per sale"))
    return profit_list


def main():
    """
    Runs all program functions
    """
    populate_comic_list()
    print("Welcome to the comic stock tracker.")
    stock_or_sales()
    run_again()


main()
