# WILL NEED API'S ADDED (PAYPAL, ETC) TO MOVE ACTUAL MONEY 
# ESCROW TRANSACTION ENGINE, RELIES ON ACCRUAL ACCOUNTING PRINCIPLES WHERE MONEY IS HELD IN ESCROW UNTIL COMPLETION, CURRENT PERCENT CUTS HARDCODED, CAN BE CHANGED AND ADJUSTED
# CANNOT RUN ALONE, CAN ONLY BE RUN AND TESTED THROUGH UI
class EscrowTransaction: 
    def __init__(self, transaction_id, amount, client_username, driver_username, vendor_username, admin_username, status):
        self.transaction_id = transaction_id
        self.amount = amount
        self.client_username = client_username
        self.driver_username = driver_username
        self.vendor_username = vendor_username
        self.admin_username = admin_username
        self.status = status
        self.driver_cut = 0.10
        self.vendor_cut = 0.75
        self.admin_cut = 0.15


    def __str__(self):
        return f"EscrowTransaction(transaction_id={self.transaction_id}, amount={self.amount}, client_username={self.client_username}, driver_username={self.driver_username}, vendor_username={self.vendor_username}, admin_username={self.admin_username}, status={self.status}, driver_cut={self.driver_cut}, vendor_cut={self.vendor_cut}, admin_cut={self.admin_cut}, total_cut={self.driver_cut + self.vendor_cut + self.admin_cut})"

class EscrowTransactionManager:
    def __init__(self):
        self.transactions = {}

    def add_transaction(self, transaction_id, amount, client_username, driver_username, vendor_username, admin_username, status):
        if transaction_id in self.transactions:
            raise ValueError("Transaction ID already exists.")
        self.transactions[transaction_id] = EscrowTransaction(transaction_id, amount, client_username, driver_username, vendor_username, admin_username, status,)
        return self.transactions[transaction_id]

    def update_transaction(self, transaction_id, new_amount=None, new_client_username=None, new_driver_username=None, new_vendor_username=None, new_admin_username=None, new_status=None):
        if transaction_id not in self.transactions:
            raise ValueError("Transaction ID does not exist.")
        transaction = self.transactions[transaction_id]
        if new_amount:
            transaction.amount = new_amount
        if new_client_username:
            transaction.client_username = new_client_username
        if new_driver_username:
            transaction.driver_username = new_driver_username
        if new_vendor_username:
            transaction.vendor_username = new_vendor_username
        if new_admin_username:
            transaction.admin_username = new_admin_username
        if new_status:
            transaction.status = new_status
        print("Transaction information updated successfully.")
        return transaction

    def cancel_transaction(self, transaction_id, user_manager):
        # 1. Find the transaction
        if transaction_id not in self.transactions:
            raise ValueError("Transaction not found")
        transaction = self.transactions[transaction_id]
        
        # 2. Check it hasn't already been paid
        if transaction.status == "paid":
            raise ValueError("Transation already complete, unable to refund")
        
        # 3. Refund client - move money from escrow back to actual balance
        user_manager.users[transaction.client_username].escrow_balance -= transaction.amount
        user_manager.users[transaction.client_username].actual_balance += transaction.amount
        
        # 4. Delete the transaction
        del self.transactions[transaction_id]
        
        # 5. Confirm
        print(f"Transaction '{transaction_id}' has been cancelled and funds returned.")
    

    def display_transactions(self):
        if not self.transactions:
            print("No transactions available.")
        else:
            for transaction in self.transactions.values():
                print(transaction)

    def transaction_status(self, transaction_id):
        if transaction_id not in self.transactions:
            raise ValueError("Transaction ID does not exist.")
        transaction = self.transactions[transaction_id]
        if transaction.status == "completed":
            print(f"Transaction '{transaction_id}' is completed.")
        return transaction.status

    def escrow_release(self, transaction_id, user_manager):
        # 1. Find the transaction
        if transaction_id not in self.transactions:
            raise ValueError("Transaction ID does not exist.")
        transaction = self.transactions[transaction_id]
        
        # 2. Check status
        if transaction.status == "pending":
            raise ValueError("Transaction is pending. Cannot release funds.")
        if transaction.status != "completed":
            raise ValueError("Transaction is not completed")
        
        # 3. Calculate cuts
        driver_amount = transaction.amount * transaction.driver_cut
        vendor_amount = transaction.amount * transaction.vendor_cut
        admin_amount = transaction.amount * transaction.admin_cut
        
        # 4. Add to each user's actual_balance
        user_manager.users[transaction.driver_username].actual_balance += driver_amount 
        user_manager.users[transaction.vendor_username].actual_balance += vendor_amount
        user_manager.users[transaction.admin_username].actual_balance += admin_amount
        
        # 5. Subtract from client's escrow_balance
        user_manager.users[transaction.client_username].escrow_balance -= transaction.amount
        
        # 6. Set status to paid
        transaction.status = "paid"
        print(f"Transaction '{transaction_id}' status updated to 'paid'.")
        return (user_manager.users[transaction.client_username].escrow_balance, user_manager.users[transaction.client_username].actual_balance)
    
def main():
    user_manager = UserManager()
    escrow_manager = EscrowTransactionManager() 

    while True:
        print("\nTransaction Management System")
        print("1. Add")
        print("2. Update")
        print("3. Cancel")
        print("4. Display")
        print("5. Status")
        print("6. Release")

        choice = input("Enter your choice: ")

        if choice == '1':
            transaction_id = input ("Transaction ID: ")
            amount = input ("Transaction Amount: ")
            client_username = input ("Username: ")
            driver_username = input ("Driver: ")
            vendor_username = input ("Vendor: ")
            admin_username = input ("Admin: ")
            status = input ("Transaction Status: ")
            try:
                escrow_manager.add_transaction(transaction_id, amount, client_username, driver_username, vendor_username, admin_username, status)
                print(f"Transaction '{transaction_id}' added.")
            except ValueError as e:
                print(e)

        elif choice == '2':
            transaction_id = input("Update Transaction: ")
            new_amount = input("Update amount: ")
            new_client_username = input("Update user: ")
            new_driver_username = input("Update driver: ")
            new_vendor_username = input("Update vendor: ")
            new_admin_username = input("Update admin: ")
            new_status = input("Update order status")
            try:
                user = escrow_manager.update_transaction(transaction_id, new_amount, new_client_username, new_driver_username, new_vendor_username, new_admin_username, new_status)
                print(f"Transaction '{transaction_id}' updated.")
            except ValueError as e:
                print(e)

        elif choice == '3':
            transaction_id = input("Cancel order: ")
            try:
                escrow_manager.cancel_transaction(transaction_id, user_manager)
            except ValueError as e:
                print(e)

        elif choice == '4':
            escrow_manager.display_transactions()


        elif choice == '5':
            transaction_id = input("Enter Transaction ID: ")
            escrow_manager.transaction_status(transaction_id)

        elif choice == '6':
            transaction_id = input("Transaction ID: ")
            escrow_manager.escrow_release(transaction_id, user_manager)
            print("Completing Transaction")

        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()

