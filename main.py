# * Calculates expenses per paycheck (pay period)
import sys
from datetime import date, timedelta, datetime
from colorama import Fore, Style

_first_payday = date(2022, 6, 3)


def main(startDate):
    # get next pay period after start date
    payPeriod = getNextPayPeriod(_first_payday, startDate)
    days = getDaysInPayPeriod(payPeriod)
    # get Income for pay period
    incomeLines = getIncome()
    billLines = getBills()
    expenses = getExpenses()
    # get bills for pay period
    currentBills = getBillsInPayPeriod(billLines, days)
    # sum income for period
    totalIncome = sum([line[1] for line in incomeLines])
    # sum bills within pay period
    totalBills = sumCurrentBills(currentBills)
    totalExpenses = sumCurrentExpenses(expenses)
    # Output
    print(Fore.RESET + "----------------------------")
    print(Fore.CYAN + "Pay Period: ", payPeriod[0].isoformat(), " to ", payPeriod[1].isoformat() + Style.RESET_ALL)
    printBills(currentBills + expenses)
    print(Fore.GREEN + "Total Income: ", totalIncome)
    print(Fore.RED + "Total Bills: ", totalBills)
    print("Total Expenses: ", totalExpenses)
    print(Fore.GREEN + f"Net Income: {totalIncome - totalBills - totalExpenses}")
    print('')


def getNextPayPeriod(seedPayDay, startDate):
    while startDate > seedPayDay:
        seedPayDay += timedelta(days=14)

    return [seedPayDay, seedPayDay + timedelta(days=14)]


def getDaysInPayPeriod(payPeriod):
    days = []
    day = payPeriod[0]
    while day != payPeriod[1]:
        days.append(day.day)
        day += timedelta(days=1)
    return days


def getIncome():
    incomeLines = []
    with open('income.txt') as file:
        for line in file:
            tempLine = list(line.replace(' ', '').split('|'))
            tempLine[1] = int(tempLine[1])
            start = tempLine[2].strip()
            tempLine[2] = datetime.strptime(str(start), '%Y-%m-%d').date()
            incomeLines.append(tempLine)
    return incomeLines


def getBills():
    billLines = []
    with open('bills.txt') as file:
        for line in file:
            tempLine = list(line.replace(' ', '').split('|'))
            tempLine[1] = int(tempLine[1])
            tempLine[2] = int(tempLine[2])
            billLines.append(tempLine)
    return billLines


def getExpenses():
    expenses = []
    with open('expenses.txt') as file:
        for line in file:
            tempLine = list(line.replace(' ', '').split('|'))
            tempLine[1] = int(tempLine[1])
            expenses.append(tempLine)
    return expenses


def getBillsInPayPeriod(billLines, days):
    return [b for b in billLines if b[2] in days]


def sumCurrentBills(currentBills):
    return sum(b[1] for b in currentBills)


def sumCurrentExpenses(expenses):
    return sum(e[1] for e in expenses)


def printBills(bills):
    print("===================")
    print(Fore.YELLOW + 'Bills/Expenses Due:' + Fore.RESET)
    print('-------------------')
    for bill in bills:
        print(Fore.LIGHTBLACK_EX + bill[0], bill[1], Fore.RESET)
    print('-------------------')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.argv.append('1')

    for x in range(-1, int(sys.argv[1]) - 1):
        main(date.today() + timedelta(days=x * 14))
