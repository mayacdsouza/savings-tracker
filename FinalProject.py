import pandas as pd
import csv
import matplotlib.pyplot as plt
import time


def new_line():
    """Prints 50 blank lines to make the console appear cleared."""
    print('\n'*50)


def opening_menu():
    """Prints opening menu and prompts user for potential menu options."""

    new_line()
    print("SAVINGS TRACKER")
    print("1 = Data Menu")
    print("2 = How to/FAQ's")
    print("3 = Report an Issue/ Make a Suggestion")
    print("4 = Exit the Program")

    option = int(input("Enter a number: "))
    if option == 1:  # takes user to menu for entering data
        data_menu()
    if option == 2:  # takes user to menu to see FAQ's
        print_faqs()
    if option == 3:  # takes user to menu to make a suggestion
        make_a_suggestion()
    if option == 4:  # exits program
        exit()


def make_a_suggestion():
    new_line()
    file = "suggestions.txt"
    entry_file = open(file, 'a')
    suggestion = input("Enter your suggestion to improve the program: ")
    entry_file.write(suggestion + "\n")

    print("Press 1 to return to main menu and 2 to enter another suggestion: ")
    option = input()
    if option == '1':
        opening_menu()
    if option == '2':
        make_a_suggestion()


def print_faqs():
    """Prints out FAQ's about how to use the program."""

    new_line()
    print("HOW TO AND FREQUENTLY ASKED QUESTIONS")
    print()

    print("1. How do I enter my savings data?")
    print("You can enter your savings data in the following format: ")
    print("Account,Type,Balance,Month,Year. Account should be the nickname")
    print(" you use for your account. Type can be Investment, Savings, or ")
    print("Debt. Balance is the amount in your account. Please enter debt as ")
    print("a positive number. Month should be the number 1 to 12 for the ")
    print("month. For example 1=January, 2=February, and so on. Year should")
    print(" be YYYY (.i.e. 2007). Using the format, an acceptable entry could")
    print("be 401k,Investment,10000,1,2022. Note there are no spaces after")
    print("commas and no commas in the balance value.")
    print()

    print("2. How do I delete an entry?")
    print("To delete an entry, you can first view your entries. Each entry")
    print(" has a number, so you can pick the number of the entry you wish")
    print("to delete and that row of data will be erased.")
    print()

    print("3. What does each graph and chart show?")
    print("There are 2 charts you can see. The individual accounts shows ")
    print("the current value in each account. It will do this by displaying")
    print(" the latest account entry. The total accounts shows your total")
    print("savings, investments, debt, and net worth. There are 2 graphs")
    print("you can see. The individual account graph will graph your ")
    print("account balances over time. The total accounts graph will ")
    print("graph the sum of your account types (Savings, Investments, Debt,")
    print(" and Net Worth) over time.")
    print()

    print("4. How do I choose which charts and graphs I want to see?")
    print("When you go to the menu to see your charts and graphs,")
    print("you will be prompted to choose.")
    print()

    print("5. What is the purpose of each chart and graph?")
    print('The individual account chart shows your current')
    print("balance in each account. The total account chart shows")
    print("the current total balance across account types. The ")
    print("individual account graph allows you to see your account")
    print(" balances over time while the total account graph shows you")
    print("your account type balances")
    print('over time.')

    print()
    print("1 = Return to Main Screen")
    option = int(input("Enter a number: "))

    if option == 1:
        opening_menu()


def data_menu():
    """
    Allows user to enter, modify data, delete data, and view graphs and charts.
    """
    new_line()  # clear console

    print("DATA MENU")
    print("1 = Enter Data")
    print("2 = Display Data")
    print("3 = View, Modify, or Delete Entries")
    print("4 = Estimate retirement savings")
    print("5 = Return to Main Menu")

    option = int(input("Enter a Number: "))
    if option == 1:
        enter_data()
    if option == 2:
        display_data_menu()
    if option == 3:
        view_or_edit_menu()
    if option == 4:
        retirement()
    if option == 5:
        opening_menu()


def enter_data():
    """Allows user to make one savings entry."""

    new_line()  # clear console

    # instructions
    print("Enter data in the following format")
    print("Account Name,Type,Balance,Month,Year")
    print("See FAQ for allowed options for each category.")

    # read data to file Entries.txt
    entry = input("Data entry: ")
    entry_file = open('Entries.txt', 'a')
    entry_file.write(entry + "\n")
    entry_file.close()

    # Let user make another entry or return to data menu
    print("Would you like to make another entry?")
    print("Press 1 for yes.")
    print("Press 2 to return to data menu.")
    option = int(input())
    if option == 1:
        enter_data()
    if option == 2:
        data_menu()


def display_data_menu():
    """
    Lets user select which charts/graphs they wish to see and displays them.
    """
    new_line()  # clear console

    sort_data()  # make sure data is sorted by date and account type

    # ask user if they wish to see each of the 4 charts and graphs
    # display them if so
    print("Would you like to see a chart for your individual accounts?")
    answer = input("yes or no? ")
    if answer == 'yes':
        individual_account_chart()

    print()
    print("Would you like to see a graph for your individual accounts?")
    answer = input("yes or no? ")
    if answer == 'yes':
        individual_account_graph()

    new_line()
    print("Would you like to see a chart for your total across accounts? ")
    answer = input("yes or no? ")
    if answer == 'yes':
        total_account_chart()

        # add future projected balance to aggregate_entries.txt
        with open('invest.txt', 'r') as fp:
            lines = fp.readlines()
        output = float(lines[0]) + float(lines[1])
        output = int(output)
        output = str(output)
        with open("aggregate_entries.txt", 'a') as fp:
            fp.write("Projected Future Balance,"+output)
        # read data and display it
        a_entry_file = "aggregate_entries.txt"
        open(a_entry_file, "r")
        print(pd.read_csv(a_entry_file))

    print()
    print("Would you like to see a graph for your total across accounts?")
    answer = input("yes or no? ")
    if answer == 'yes':
        total_account_graph()

    # return to data menu
    print("Press 1 to return to data_menu: ")
    option = int(input())
    if option == 1:
        data_menu()


def aggregate_data_for_charts():
    """
    Prepares data for charts.
    """

    sort_data()  # sorts the data in Entries.txt

    # read data from Entries.txt
    with open('Entries.txt', newline='') as entry_file:
        reader = csv.reader(entry_file)
        data = list(reader)

    # initialize dictionary
    dictionary = {}

    # store key:value pairs in dictionary in format
    # account_name:[type, balance, month, year]
    for i in range(1, len(data)):
        account_name = data[i][0]
        value = [data[i][1], data[i][2], data[i][3], data[i][4]]
        dictionary[account_name] = value

    # clear aggregate_entries.txt
    aggregate_entries = open('aggregate_entries.txt.', 'w')
    aggregate_entries.truncate(0)
    aggregate_entries.close()

    # write data from dictionary to file
    a_entry_file = "aggregate_entries.txt"
    agg_entry_file = open(a_entry_file, 'a')
    agg_entry_file.write("AccountName,Type,Balance,Month,Year" + "\n")
    for key in dictionary:
        value = dictionary[key]
        string = str(key)
        string += ',' + value[0]
        string += ',' + value[1]
        string += ',' + value[2]
        string += ',' + value[3]
        agg_entry_file.write(string + "\n")
    agg_entry_file.close()


def individual_account_chart():
    """Shows current balance in each account."""

    # write aggregate data to aggregate_entries.txt
    aggregate_data_for_charts()

    # read data from aggregate_entries.txt and display it
    a_entry_file = "aggregate_entries.txt"
    open(a_entry_file, "r")
    print(pd.read_csv(a_entry_file))


def is_greater_then(entry1, entry2):
    """
    Determines order of 2 individual account entries
    for individual accounts charts and graphs.
    Returns true is entry1 > entry2 and False if not.
    """

    # check which account type is first alphabetically
    if entry1[1] > entry2[1]:
        return True
    elif entry1[1] < entry2[1]:
        return False

    # if account type was equal
    # check which account name is first alphabetically
    elif entry1[0] > entry2[0]:
        return True
    elif entry1[0] < entry2[0]:
        return False

    # if account name was the same
    # check with year is first
    elif int(entry1[4]) > int(entry2[4]):
        return True
    elif int(entry1[4]) < int(entry2[4]):
        return False

    # if year was the same
    # check which month is first
    elif int(entry1[3]) > int(entry2[3]):
        return True
    elif int(entry1[3]) < int(entry2[3]):
        return False


def is_greater_then_2(entry1, entry2):
    """
    Checks 2 individual entries for aggregate account
    charts and graphs. Returns True if entry1 > entry2
    and False if not.
    """

    # Check account type
    if entry1[1] > entry2[1]:
        return True
    elif entry1[1] < entry2[1]:
        return False

    # If account type is the same
    # Check Year
    elif int(entry1[4]) > int(entry2[4]):
        return True
    elif int(entry1[4]) < int(entry2[4]):
        return False

    # If year is the same
    # Check Month
    elif int(entry1[3]) > int(entry2[3]):
        return True
    elif int(entry1[3]) < int(entry2[3]):
        return False


def sort_data():
    """
    Sorts a_list in ascending order for individual account data.
    """

    # read data from Entries.txt
    with open('Entries.txt', newline='') as entry_file:
        reader = csv.reader(entry_file)
        data = list(reader)
    title = [data[0]]
    data = data[1:]

    # sort data
    for index in range(0, len(data)):
        value = data[index]
        pos = index - 1
        while pos >= 0 and is_greater_then(data[pos], value):
            data[pos + 1] = data[pos]
            pos -= 1
        data[pos + 1] = value

    data = title + data

    # clear Entries.txt
    file_entries = open('Entries.txt.', 'w')
    file_entries.truncate(0)
    file_entries.close()

    # write data back to Entries.txt (now sorted)
    entry_file = open("Entries.txt", 'a')
    for i in range(0, len(data)):
        string = ""
        for j in range(0, len(data[i])-1):
            string += data[i][j] + ','
        string += data[i][-1]
        entry_file.write(string + "\n")
    entry_file.close()


def sort_data_2():
    """
    Sorts data in ascending order for total account data.
    """

    # read data from Entries.txt
    with open('Entries.txt', newline='') as entry_file:
        reader = csv.reader(entry_file)
        data = list(reader)
    title = [data[0]]
    data = data[1:]

    # sort data
    for index in range(0, len(data)):
        value = data[index]
        pos = index - 1
        while pos >= 0 and is_greater_then_2(data[pos], value):
            data[pos + 1] = data[pos]
            pos -= 1
        data[pos + 1] = value

    data = title + data

    # clear Entries.txt
    file_entries = open('entries.txt.', 'w')
    file_entries.truncate(0)
    file_entries.close()

    # write data back to Entries.txt (now sorted)
    entry_file = open("Entries.txt", 'a')
    for i in range(0, len(data)):
        string = ""
        for j in range(0, len(data[i])-1):
            string += data[i][j] + ','
        string += data[i][-1]
        entry_file.write(string + "\n")
    entry_file.close()


def total_account_chart():
    """Shows current balance in each account type."""

    # update aggregate_entries.txt to show balance in each account
    aggregate_data_for_charts()

    # store this data in data
    with open('aggregate_entries.txt', newline='') as a_entry_file:
        reader = csv.reader(a_entry_file)
        data = list(reader)

    # initialize balances at 0
    savings = 0
    debt = 0
    investments = 0

    # add each account balance to its account type
    for i in range(1, len(data)):
        if data[i][1] == "Savings":
            savings += int(data[i][2])
        if data[i][1] == "Investment":
            investments += int(data[i][2])
        if data[i][1] == "Debt":
            debt += int(data[i][2])

    # sum account types to find net worth
    net_worth = savings+investments-debt

    # clear aggregate_entries.txt
    aggregate_entries = open('aggregate_entries.txt.', 'w')
    aggregate_entries.truncate(0)
    aggregate_entries.close()

    # write current balance in savings,investments, debt
    # and net worth to file
    a_entry_file = open('aggregate_entries.txt', 'a')
    a_entry_file.write("Category,balance" + "\n")
    a_entry_file.write("Savings," + str(savings) + "\n")
    a_entry_file.write("Investments," + str(investments) + "\n")
    a_entry_file.write("Debt," + str(debt) + "\n")
    a_entry_file.write("Net Worth," + str(net_worth) + "\n")
    a_entry_file.close()

    # return savings and investments balances
    return savings, investments


def individual_account_graph():
    """ Display graph of individual account data."""

    # sort entries in Entries.txt
    sort_data()

    # make a dictionary with key account names and value [x_list,y_list]
    with open('Entries.txt', newline='') as entry_file:
        reader = csv.reader(entry_file)
        data = list(reader)
    dictionary = {}
    for i in range(1, len(data)):
        key = data[i][0]
        x = (int(data[i][3])-1)/12+int(data[i][4])
        y = int(data[i][2])
        if key in dictionary:
            dictionary[key][0].append(x)
            dictionary[key][1].append(y)
        else:
            dictionary[key] = [[x], [y]]

    # convert dictionary to a key and list of x and y values
    # plot values
    for key in dictionary:
        x = dictionary[key][0]
        y = dictionary[key][1]
        plt.plot(x, y, label=key)

    # add labels to graph and display it
    plt.xlabel('Year')
    plt.ylabel('Account Balance')
    plt.title('Individual Accounts')
    plt.legend()
    plt.show()


def total_account_graph():
    """Display a graph of total account data."""

    # sort entries in Entries.txt
    sort_data_2()

    # read entries in data (will be a list of lists)
    with open('Entries.txt', newline='') as entry_file:
        reader = csv.reader(entry_file)
        data = list(reader)

    # make a dictionary with key account types and value [x_list,y_list]
    dictionary = {}
    for i in range(1, len(data)):
        key = data[i][1]
        x = (int(data[i][3])-1)/12+int(data[i][4])
        y = int(data[i][2])
        if key in dictionary:
            if x in dictionary[key][0]:
                for index in range(0, len(dictionary[key][0])):
                    if x == dictionary[key][0][index]:
                        dictionary[key][1][index] += y
            else:
                dictionary[key][0].append(x)
                dictionary[key][1].append(y)
        else:
            dictionary[key] = [[x], [y]]

    # convert dictionary to a key and list of x and y values
    # plot values
    for key in dictionary:
        x = dictionary[key][0]
        y = dictionary[key][1]
        plt.plot(x, y, label=key)

    # add labels to graph and display it
    plt.xlabel('Year')
    plt.ylabel('Account Balance')
    plt.title('Total Accounts')
    plt.legend()
    plt.show()


def individual_account_entries():
    """ Display all user savings entries."""
    entry_file = "entries.txt"
    open(entry_file, "r")
    print(pd.read_csv(entry_file))


def view_or_edit_menu():
    """ Allows user to view their entries and delete any if needed."""

    individual_account_entries()  # Display all entries

    print("Press row of entry number to delete and entry.")
    print("Press r to return to data menu.")
    request = input()

    if request == 'r':  # return to data menu
        data_menu()

    else:  # delete requested entry
        print("Are you sure you want to delete entry " + request + " ?")
        answer = input("yes or no? ")
        if answer == "yes":
            with open("Entries.txt", 'r') as fp:
                lines = fp.readlines()
            with open("Entries.txt", 'w') as fp:
                for number, line in enumerate(lines):
                    if number != int(request) + 1:
                        fp.write(line)

    view_or_edit_menu()  # go back to displaying entries


def retirement():
    """Calculates future projected balance at retirement."""

    new_line()  # clear console

    # ask user for their monthly contributions and APY for savings/investments
    monthly_savings = str(input("How much do you put in savings monthly? "))
    monthly_invts = str(input("How much do you put in investments monthly? "))
    savings_interest = str(input("What % APY do you receive on savings? "))
    invts_interest = str(input("What % APY do you receive on investments? "))

    # find their current savings and investments balance from their entries
    savings_balance, investments_balance = total_account_chart()

    # ask user when they plan to retire
    years = str(input("In how many years do you plan to retire? "))

    # write all the input data to future_earnings.txt
    output1 = "["+str(savings_balance) + "," + monthly_savings + ","
    output1 += savings_interest + "," + years + "]"+"\n"
    output2 = "[" + str(investments_balance) + "," + monthly_invts + ","
    output2 += invts_interest + "," + years + "]"
    service = open('future_earnings.txt', 'w')
    service.write(output1)
    service.write(output2)
    service.close()

    # write data from future_earnings.txt to invest.txt
    with open("future_earnings.txt", 'r') as fp:
        lines = fp.readlines()
    with open('invest.txt', 'w') as fp:
        fp.write('run' + '\n')
        for number, line in enumerate(lines):
            fp.write(line)

    time.sleep(3)  # wait for compound investment microservice to run

    # read data and display it
    with open('invest.txt', 'r') as fp:
        lines = fp.readlines()
    output = float(lines[0])+float(lines[1])
    output = int(output)
    print("Your projected future earnings are $" + str(output) + ".")

    answer = input("Press 1 to return to data menu.")
    if answer == '1':
        data_menu()


opening_menu()  # starts program at opening menu
