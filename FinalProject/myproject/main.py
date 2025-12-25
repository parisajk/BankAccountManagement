from data_manager import DataManager
from bank_account_management import BankAccountManagement

dm = DataManager()

try:
    accounts = dm.get()
except FileNotFoundError:
    accounts = dict()
    print("Data file not found, starting with empty accounts.")
except Exception as e:
    accounts = dict()
    print(f"Error loading data: {e}")
    
bam = BankAccountManagement(accounts)

def show_menu():
    print('\n\n\n------------------')
    print('1- Show All Accounts')
    print('2- Add user')
    print('3- Transfer')
    print('4- Deposit')
    print('5- Withdraw')
    print('6- Show Account Details')
    print('7- Delete User')
    print('8- Exit')
    

def handle_action(result):
    if result['status'] == 'ok':
        dm.set(accounts)
        print("Operation completed successfully.")
    else:
        print(result['msg'])
  

def add_user():
    name = input('Insert name: ').strip()
    if not name:
        print('Name cannot be empty')
        return
    
    first_amount = input('Insert initial amount: ')
    result = bam.add_user(name, first_amount)
    handle_action(result)

def transfer():
    from_who = input('From who (User ID): ')
    to_whom = input('To whom (User ID): ')
    amount = input('Amount: ')
    result = bam.transfer(from_who, to_whom, amount)
    handle_action(result)
       

def deposit():
    user_id = input("User ID: ")
    amount = input("Amount: ")
    result = bam.deposit(user_id, amount)
    handle_action(result)

def withdraw():
    user_id = input("User ID: ")
    amount = input("Amount: ")
    result = bam.withdraw(user_id, amount)
    handle_action(result)

def show_user_details():
    user_id = input("Enter User ID: ").strip()
    if user_id in accounts:
        acc = accounts[user_id]
        status = acc.get('status', 'active')
        print(f"\n---- Account Details ----")
        print(f"Name: {acc['name']}")
        print(f"Balance: ${acc['balance']}")
        print(f"Status: {status}")
        print("\nTransaction History:")
        if acc['history']:
            for h in acc['history']:
                print(f" - [{h['time']}] {h['type'].capitalize()} ${h['amount']}")
        else:
            print("No transactions yet.")
        input("\nPress Enter to continue...")
    else:
        print("User not found.")



def delete_user():
    user_id = input("Enter User ID to delete: ")
    confirm = input("Are you sure? (y/n): ").lower()

    if confirm != 'y':
        print("Delete cancelled.")
        return

    result = bam.delete_user(user_id)
    handle_action(result)


def main():
    while True:
        show_menu()
        command = input('Select from menu: ').strip()

        if command == '1':
            bam.show_info()
            input("\nPress Enter to continue...")

        elif command == '2':
            add_user()

        elif command == '3':
            transfer()

        elif command == '4':
            deposit()

        elif command == '5':
            withdraw()

        elif command == '6':
            show_user_details()

        elif command == '7':
            delete_user()

        elif command == '8':
            print('Exiting...')
            break

        else:
            print('Wrong choice, try again')
            


                
        
try:
    main()
except KeyboardInterrupt:
    print('\nProgram closed by user.')
