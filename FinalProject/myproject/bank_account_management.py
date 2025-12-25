from datetime import datetime as dt

class BankAccountManagement:
    def __init__(self, accounts:dict):
        self.accounts = accounts
        
    def show_info(self):
        for id, acc in self.accounts.items():
            if acc.get('status', 'active') != 'deleted':  
                print(f"{id}- {acc['name']} ({acc['balance']})")

   
    def add_user(self, name: str, first_amount: float):
        if not name:
            return {'status': 'error', 'msg': 'Name cannot be empty'}
            
        try:
            first_amount = float(first_amount)
        except ValueError:
            return {'status': 'error', 'msg': 'Amount must be a number'}
        if first_amount < 0:
            return {'status': 'error', 'msg': 'Initial amount cannot be negative'}
            
        id = str(max(map(int, self.accounts.keys()), default=0) + 1)
        self.accounts.update({
            str(id): {
                    'name': name, 
                    'balance': first_amount, 
                    'history': [
                        {'time': dt.now().strftime('%Y-%m-%d %H:%M'), 'type': 'deposit', 'amount': first_amount},
                    ],
                    'status': 'active'     
                }
        })
        return {'status': 'ok'}
    
        # Delete a user account by user ID
    def delete_user(self, user_id: str):
        try:
            user_id = str(int(user_id.strip()))
        except ValueError:
            return {'status': 'error', 'msg': 'User ID is not valid'}

        if user_id not in self.accounts:
            return {'status': 'error', 'msg': 'User does not exist'}

        self.accounts[user_id]['status'] = 'deleted'
        return {'status': 'ok'}


    def transfer(self, from_who: str, to_whom: str, amount: str):
        # convert and check data type 
        try:
            from_who = str(int(from_who.strip()))
            to_whom = str(int(to_whom.strip()))
            amount = float(amount)
        except ValueError:
            return {'status': 'error', 'msg': 'Inputs are not valid'}

        # check if ids are same
        if from_who == to_whom:
            return {'status': 'error', 'msg': 'Cannot transfer to the same account'}

        # check if ids exist
        if from_who not in self.accounts:
            return {'status': 'error', 'msg': 'Sender does not exist'}
        if to_whom not in self.accounts:
            return {'status': 'error', 'msg': 'Receiver does not exist'}

        # check account status
        if self.accounts[from_who].get('status') == 'deleted' or \
        self.accounts[to_whom].get('status') == 'deleted':
            return {'status': 'error', 'msg': 'One of the accounts is deleted'}

        # check amount
        if amount <= 0:
            return {'status': 'error', 'msg': 'Amount must be positive'}

        if self.accounts[from_who]['balance'] < amount:
            return {'status': 'error', 'msg': 'Insufficient balance'}

        # do transfer
        self.accounts[from_who]['balance'] -= amount
        self.accounts[to_whom]['balance'] += amount

        self.accounts[from_who]['history'].append({
            'time': dt.now().strftime('%Y-%m-%d %H:%M'),
            'type': 'withdraw',
            'amount': amount
        })

        self.accounts[to_whom]['history'].append({
            'time': dt.now().strftime('%Y-%m-%d %H:%M'),
            'type': 'deposit',
            'amount': amount
        })

        return {'status': 'ok'}

    
    
    def deposit(self, user_id: str, amount: str):
        # Validate types
        try:
            user_id = str(int(user_id.strip()))
            amount = float(amount)
        except ValueError:
            return {'status': 'error', 'msg': 'Inputs are not valid'}

        # Validate amount
        if amount <= 0:
            return {'status': 'error', 'msg': 'Amount must be positive'}

        # Check if user exists
        if user_id not in self.accounts:
            return {'status': 'error', 'msg': 'User does not exist'}

        # Update balance
        self.accounts[user_id]['balance'] += amount

        # Add to history
        self.accounts[user_id]['history'].append(
            {
                'time': dt.now().strftime('%Y-%m-%d %H:%M'),
                'type': 'deposit',
                'amount': amount
            }
        )

        return {'status': 'ok'}


    def withdraw(self, user_id: str, amount: str):
        # Validate types
        try:
            user_id = str(int(user_id.strip()))
            amount = float(amount)
        except ValueError:
            return {'status': 'error', 'msg': 'Inputs type are not valid'}

        # Validate amount
        if amount <= 0:
            return {'status': 'error', 'msg': 'Amount must be positive'}

        # Check if user exists
        if user_id not in self.accounts:
            return {'status': 'error', 'msg': 'User does not exist'}

        # Check if enough balance
        if self.accounts[user_id]['balance'] < amount:
            return {'status': 'error', 'msg': 'Not enough balance'}

        # Update balance
        self.accounts[user_id]['balance'] -= amount

        # Add to history
        self.accounts[user_id]['history'].append(
            {
                'time': dt.now().strftime('%Y-%m-%d %H:%M'),
                'type': 'withdraw',
                'amount': amount
            }
        )

        return {'status': 'ok'}


