import random
import secrets
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS card(
id INTEGER,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0
);
""")
conn.commit()

end = True


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(k) for k in str(n)]

    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0


def create_an_account():
    while True:
        account_id = '{:0>9}'.format(random.randint(1, 99999999))
        cheksum = random.randint(1, 9)
        card_number = int(''.join([str(400000) + str(account_id) + str(cheksum)]))
        result = is_luhn_valid(card_number)
        if result is False:
            continue
        if result is True:
            card_pin(card_number, account_id)
            break


def card_pin(card_number, account_id):
    pin = int('{:0>4}'.format(secrets.randbelow(9999)))
    with conn:
        cur.execute("INSERT INTO card VALUES(:id,:number,:pin,:balance)",
                    {'id': account_id, 'number': str(card_number), 'pin': str(pin), 'balance': 0})
    print('\nYour card has been created')
    print('Your card number:')
    print(card_number)
    print('Your card PIN:')
    print(pin)
    print('')


def login():
    print('\nEnter your card number:')
    entered_card = int(input())
    print('Enter your PIN:')
    entered_pin = int(input())
    with conn:
        cur.execute("SELECT number, pin FROM card")
    for i in cur.fetchall():
        if str(entered_card) in i and str(entered_pin) in i:
            print('\nYou have successfully logged in!\n')
            logged_in_window(entered_card)
            break
    else:
        print('\nWrong card number or PIN!\n')


def income(card_n):
    print("Enter income:")
    income_am = int(input())
    with conn:
        cur.execute("UPDATE card SET balance = balance + (:income) WHERE number=(:card_n)",
                    {'income': income_am, 'card_n': str(card_n)})
    print("Income was added!\n")


def transfer(card_n, balance):
    print("\nTransfer")
    print("Enter card number:")
    card_number = str(input())
    result = is_luhn_valid(card_number)
    if result is False:
        print("\nProbably you made mistake in the card number. Please try again!\n ")
    if result is True:
        with conn:
            cur.execute("SELECT number FROM card")
        for i in cur.fetchall():
            if card_number in i:
                print('\nEnter how much money you want to transfer:\n')
                transfer_am = int(input())
                if transfer_am <= balance:
                    with conn:
                        cur.execute("UPDATE card SET balance = balance + (:transfer) WHERE number=(:card_number)",
                                    {'transfer': transfer_am, 'card_number': card_number})
                        cur.execute("UPDATE card SET balance = balance - (:transfer) WHERE number=(:card_n)",
                                    {'transfer': transfer_am, 'card_n': card_n})
                    print("\nSuccess!\n")
                else:
                    print("\nNot enough money!\n")
                break
        else:
            print("\nSuch a card does not exist.\n")


def closer(card_n):
    with conn:
        cur.execute("""DELETE FROM card
                            WHERE number=(:card_n)
                            """, {'card_n': str(card_n)})
    print("\nThe account has been closed!\n")


def logged_in_window(card_n):
    balance = 0
    login_end = True
    with conn:
        cur.execute("SELECT balance FROM card WHERE number=(:card_n)", {'card_n': card_n})
    for i in cur.fetchall():
        balance = int(*i)
    with conn:
        cur.execute("SELECT balance FROM card WHERE number=(:card_n)", {'card_n': str(card_n)})

    while login_end:
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')
        user_input = int(input())
        if user_input == 1:
            print(f'\nBalance: {balance}\n')
        elif user_input == 2:
            income(card_n)
            logged_in_window(card_n)
            break
        elif user_input == 3:
            transfer(card_n, balance)
            logged_in_window(card_n)
            break
        elif user_input == 4:
            closer(card_n)
            break
        elif user_input == 5:
            break
        elif user_input == 0:
            global end
            end = False
            break


while end:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    option = int(input())
    if option == 1:
        create_an_account()
    if option == 2:
        login()
    if option == 0:
        end = False
conn.close()
print('\nBye!')
