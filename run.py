import datetime
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

# Array that will be filled with data on initial load to reduce
# the amount of times the application has to get infomation from
# google sheets
comics = []


def stock_or_sales():
    """
    Allows the user to choose if they want to update stock or sales
    """
    while True:
        choice = input("Would you like to input stock or sales?\n").lower()
        if choice == "sales":
            if confirm_choice(f"You chose {choice}."):
                select_con_or_online()
                break
        elif choice == "stock":
            if confirm_choice(f"You chose {choice}."):
                select_book()
                break
        elif choice == "delete":
            if confirm_choice(f"You chose {choice}."):
                delete_data()
                break
        else:
            print("You have made an incorrect selection. Please try again")


def confirm_choice(choice):
    """
    Prompts the user to confirm their choice.
    """
    confirm = input(f"{choice} Is that correct? y/n\n")
    if confirm == "y":
        return True
    elif confirm == "n":
        return False
    else:
        print("You have made an incorrect selection. Please try again")
        confirm_choice(choice)


def select_book():
    """
    Allows the user to select which book they are updating the stock of.
    """
    while True:
        books = SHEET.worksheet("stock").get_all_values()[0]
        books.append("Add new book")
        i = 1
        print("Which book would you like to update?")
        for title in books:
            print(f"{i}. {title}")
            i = i + 1
        book = int(
            input(f"Please enter a number between 1 and {len(books)}\n")
        )
        book -= 1
        if book <= len(books):
            if book != len(books) - 1:
                restock_book(books[book], book)
                break
            else:
                if len(books) <= 6:
                    add_book(book)
                    break
                else:
                    print(
                        "Unforunatly the comics stock tracker cannot support"
                        "more than 6 books\n"
                    )
                    break
        print(
            f"Incorrect data. Please enter a number between 1 and {len(books)}\
            \n"
        )


def restock_book(book, index):
    """
    Allows the user to update stock levels of all comic books.
    """
    while True:
        print(f"Updating stock for {book}...")
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
            date = input(
                "What is the date of the order?\n"
                "Using the DD/MM/YYYY format\n"
            )
            if validate_date(date):
                stock.append(date)
                break
        stock.append(round(int(stock[1]) / int(stock[0]), 2))
        if confirm_choice(
            f"On {stock[2]}, you ordered {stock[0]} copies of {book} "
            f"for £{stock[1]} which works out at cpu £{stock[3]}"
        ):
            break
    update_sheet(stock, book)
    update_cpu_on_restock(index, book)
    update_stock_restock(restock, index)


def update_stock_levels(stock_data):
    """
    Updates total stock level adding books on a restock
    and removing them whenever sales are computed.
    """
    print("Updating total stock levels...")
    stock = SHEET.worksheet("stock")
    books = stock.get_all_values()
    new_stock_level = []
    col = 65
    # col is set to 65 as it is used to generate a letter from
    # a character code to be used to get the correct cell to be updated.
    counter = 0

    for ind in books[-1]:
        restock = int(ind) - int(stock_data[counter])
        if restock < 50:
            order_prompt(books[0][counter], counter)
            stock = SHEET.worksheet("stock")
            restock = stock.acell(chr(col) + "2").value
        counter += 1
        col += 1
        new_stock_level.append(restock)
    col = 65
    for cell_number in new_stock_level:
        stock.update(chr(col) + "2", cell_number)
        col += 1
    print("Total stock levels updated...")


def order_prompt(book, index):
    """
    Asks the user if they want to restock a book if stocks are low.
    """
    while True:
        choice = input(
            f"Stock level of {book} is low.\n Would you like to restock? y/n\n"
        )
        if choice == "y":
            restock_book(book, index)
            break
        elif choice == "n":
            break
        else:
            print("You have made an incorrect selection. Please try again")


def update_stock_restock(stock_data, index):
    """
    Updates stock tracking sheet, adding the restock value to current stock.
    """
    print("Updating total stock levels...")
    stock = SHEET.worksheet("stock")
    col = str(chr(65 + index)) + "2"
    current_stock = stock.acell(col).value
    if current_stock is None:
        current_stock = 0
    stock.update(col, int(stock_data) + int(current_stock))
    print("Total stock levels updated.")


def update_sheet(update_data, sheet):
    """
    Updates worksheets and adds new row with data provided.
    Adapted from the love_sandwiches code along project.
    """
    print(f"Updating {sheet} worksheet...")
    worksheet = SHEET.worksheet(sheet)
    worksheet.append_row(update_data)
    print(f"{sheet.capitalize()} worksheet updated successfully.\n")


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
            print("You have made an incorrect selection. Please try again")


def recalculate_cpu(sheet):
    """
    Works out the average CPU
    """
    worksheet = SHEET.worksheet(sheet).col_values(4)
    total = 0
    for ind in range(1, len(worksheet)):
        total = total + float(worksheet[ind])
    cpu = total / (len(worksheet) - 1)
    return round(cpu, 2)


def update_cpu_on_restock(index, book):
    """
    updates comic list with correct cpu on restock
    """
    comics[index].update({"cpu": recalculate_cpu(book)})


def select_con_or_online():
    """
    Allows the user to enter the source of the sale.
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
            print("You have made an incorrect selection. Please try again")


def update_sales(source):
    """
    Updates the spreadsheet with sale info
    """
    sales_sheet = SHEET.worksheet("sales").get_all_values()
    books = sales_sheet[0]
    profit_per_sale = get_book_info("profit per sale")
    sale_price = get_book_info("sale price")
    while True:
        output = [source]
        gross_profit = []
        net_profit = []
        summary = ""
        counter = 0
        while True:
            date = input(
                "Please enter the date of sale\n"
                "Using the DD/MM/YYYY format\n"
            )
            if validate_date(date):
                output.append(date)
                break
        for ind in range(2, len(sales_sheet[0])):
            while True:
                choice = input(f"Enter sale numbers for {books[ind]}\n")
                if validate_input(choice):
                    gross_profit.append(
                        int(choice) * float(sale_price[counter])
                    )
                    net_profit.append(
                        int(choice) * float(profit_per_sale[counter])
                    )
                    output.append(choice)
                    summary += f"{choice} copies of {books[ind]}\n"
                    counter += 1
                    break
        if confirm_choice(
            f"You are updating sales for {date} \n"
            "Sales as follows;" + summary
        ):
            update_sheet(output, "sales")
            update_stock_levels(output[2:None])
            if source != "online":
                update_con_costs(source, date, gross_profit, net_profit)
            else:
                print(
                    "Online Sales Report:\n"
                    f"Gross profit is £{total_profit(gross_profit)}\n"
                    f"Net profit is £{total_profit(net_profit)}\n"
                )
            break


def total_profit(profit_array):
    """
    Works out sum of total profit when passed an array.
    """
    total = 0
    for ind in profit_array:
        total += ind
    return total


def update_con_costs(source, date, gross_profit, net_profit):
    """
    Updates the cons sheet with all costs incurred and uses
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
        output.append(total_costs)
        output.append(total_profit(gross_profit))
        output.append(total_profit(net_profit) - total_costs)
        if confirm_choice(
            f"You are updating the sales for {source} convention.\n"
            f"Table costs are £{output[3]}\n"
            f"Travel costs are £{output[4]}\n"
            f"Misc costs are £{output[5]}\n"
        ):
            print(
                f"Sales report for {source} convention\n"
                f"Total costs are £{total_costs}\n"
                f"Gross profit is £{total_profit(gross_profit)}\n"
                f"Net profit is £{total_profit(net_profit) - total_costs}\n"
            )
            update_sheet(output, "cons")
            break


def validate_book_title(comic_title):
    """
    Checks to ensure that when adding a book title
    it is not already in use.
    """
    titles = []
    book_exists = False
    for ind in comics:
        titles.append(ind.get("title"))
    for book in titles:
        if comic_title == book:
            print(f"There is already a book with the title {book}")
            book_exists = True
    if book_exists is True:
        while True:
            choice = input("Do you want to add a different title? y/n\n")
            if choice == "y":
                return False
            elif choice == "n":
                run_again()
                break
            else:
                print(
                    "You have made an incorrect choice. Please select y or n"
                )
    else:
        return True


def add_book(index):
    """
    Adds comic book to the comics list to allow data to be easily accessed.
    """
    keys = ["title", "sale price", "cpu", "profit per sale"]
    book = {}
    while True:
        title = input("What is the title of the book?\n")
        if validate_book_title(title):
            break
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
    except ValueError as event:
        print(f"Invalid data: {event}, please try again\n")
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
                "The date inputed is incorrect."
                "Please provide date in the following format dd/mm/yyyy"
            )

        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))

    except ValueError as event:
        print(f"Invalid data: {event}, please try again\n")
        return False
    return True


def new_spreadsheet(title):
    """
    Creates a new worksheet to track stock levels.
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
    try:
        num = len(stock.get_all_values()[0])
    except IndexError:
        num = 0
    stock_row = chr(num + 65) + "1"
    sales_row = chr(num + 67) + "1"
    stock.update(stock_row, title)
    sales_sheet.update(sales_row, title)


def update_price(title, price):
    """
    Updates the price of a new book onto the price worksheet
    """
    pricework = SHEET.worksheet("price")
    cell_number = len(pricework.get_all_values()) + 1
    title_cell = "A" + str(cell_number)
    price_cell = "B" + str(cell_number)
    pricework.update(title_cell, title)
    pricework.update(price_cell, price)


def populate_comic_list():
    """
    Creates a dictionary with sales data for each book.
    """
    print("Loading application data...")
    keys = ["title", "sale price", "cpu", "profit per sale"]
    book = {}
    titles = data[0]
    counter = 0
    for ind in range(2, len(titles)):
        price = SHEET.worksheet("price")
        book[keys[0]] = titles[ind]
        book[keys[1]] = float(price.get_all_values()[counter][1])
        book[keys[2]] = recalculate_cpu(titles[ind])
        book[keys[3]] = book[keys[1]] - book[keys[2]]
        counter += 1
        comics.append(book.copy())
    print("Application data loaded.")


def get_book_info(key):
    """
    Generates an array from comics dictionary based on key.
    """
    value_list = []
    for ind in comics:
        value_list.append(ind.get(key))
    return value_list


def delete_data():
    """
    allows the user to delete all data from the worksheet for testing purposes.
    """
    if confirm_choice("You are deleting all data from all sheets."):
        if confirm_choice("This is irreversable."):
            print("Deleting data...")
            titles = get_book_info("title")
            for title in titles:
                print(f"deleteing {title}")
                SHEET.del_worksheet(SHEET.worksheet(title))
            SHEET.worksheet("price").clear()
            SHEET.worksheet("stock").clear()
            SHEET.worksheet("sales").clear()
            SHEET.worksheet("cons").clear()
            add_headers_setup(["source", "date"], "sales")
            add_headers_setup(
                [
                    "con",
                    "date",
                    "table",
                    "travel",
                    "parking",
                    "misc",
                    "total costs",
                    "gross profit",
                    "net profit",
                ],
                "cons",
            )
            print("Data deleted.")
    else:
        run_again()


def add_headers_setup(headings, worksheet):
    """
    Readds the headers to the con and sales sheets after deletion.
    Called as part of the delete_data function.
    """
    # sales_headings = ["source", "date"]
    sheet = SHEET.worksheet(worksheet)
    col = 65
    counter = 0
    for ind in headings:
        sheet.update(str(chr(col) + str(1)), ind)
        counter += 1
        col += 1


def set_up():
    """
    Checks to ensure there is data inputed. If not
    prompts used to add data.
    """
    print("Welcome to the comic stock tracker.")
    if comics == []:
        print(
            "This is the first time you have used the comics sale tracker \n"
            "Running intial set up...\n"
            "Adding first book...\n"
        )
        add_book(0)
    else:
        stock_or_sales()


def main():
    """
    Runs all program functions
    """
    populate_comic_list()
    set_up()
    run_again()


main()
