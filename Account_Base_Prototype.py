# PROBS THE COOLEST BIT, THIS SETS UP THE ACCOUNTS NEEDED FOR EVERYONE TO BE ABLE TO INTERACT WITH BOTH EACHOTHER AND THE SITE
# INTERACTION REFERS TO BEING A CLIENT, DRIVER, VENDOR, ETC. ADMIN IS THE SITE ITSELF SO THE SITE CAN PROFIT FROM EACH TRANSACTION
# CREATES USER CLASS HERE

class User:
    def __init__(self, username, email, password, interaction): # INTERACTION BEING DRIVER/VENDOR/CLIENT/ETC
        self.username = username
        self.email = email
        self.password = password
        self.interaction = interaction
        self.escrow_balance = 0
        self.actual_balance = 0
        

    def __str__(self):
        return f"User(username={self.username}, email={self.email}, password={self.password}, interaction={self.interaction})"

# CREATES USER MANAGER TO BE ABLE TO MANAGE OWN ACCOUNT, AND TO MANAGE ACCOUNTS AT THE ADMIN LEVEL 
# PASSWORDS AND OTHER DATA WILL NEED TO BE ENCRYPTED AND PROPERLY RECORDED IN LINE WITH GDPR, USE HEXKEY ENCRYPTION OF PERSONAL DATA AND ADD STORAGE LAYER FOR STORAGE AND RETREVAL OF USER DATA
class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_funds(self, username, amount):
        if username not in self.users:
            raise ValueError("Username does not exist.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.users[username].actual_balance += amount
        print(f"Added {amount} to actual balance.")
        return self.users[username].escrow_balance, self.users[username].actual_balance

# ALLOWS THE ESCROW ENGINE TO WORK BY MOVING ACTUAL MONEY BALANCE INTO A WAITING ZONE (ESCROW) TO ENSURE FUNDS ARE ACCEPTABLE BEFORE CARRYING OUT TRANSACTION - HIGHLY NECESSARY
    def actual_to_escrow_balance(self, username, amount):
        if username not in self.users:
            raise ValueError("Username does not exist.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if amount > self.users[username].actual_balance:
            raise ValueError("Insufficient funds.")
        self.users[username].escrow_balance += amount
        self.users[username].actual_balance -= amount
        print(f"Transferred {amount} from actual balance to escrow balance.")
        return self.users[username].escrow_balance, self.users[username].actual_balance
   
    def register(self, username, email, password, interaction):
        if username in self.users:
            raise ValueError("Username already exists.")
        self.users[username] = User(username, email, password, interaction)
        return self.users[username]

    def login(self, username, password):
        if username not in self.users:
            raise ValueError("Username does not exist.")
        user = self.users[username]
        if user.password != password:
            raise ValueError("Incorrect password.")
        return user
    
    def delete_user(self, username):
        if username not in self.users:
            raise ValueError("Username does not exist.")
        del self.users[username]
        print (f"User '{username}' has been deleted.")

    def update_user(self, username, new_username=None, new_email=None, new_password=None, new_interaction=None):
        if username not in self.users:
            raise ValueError("Username does not exist.")
        user = self.users[username]
        if new_username:
            if new_username in self.users:
                raise ValueError("New username already exists.")
            del self.users[username]
            user.username = new_username
            self.users[new_username] = user
        if new_email:
            user.email = new_email
        if new_password:
            user.password = new_password
        if new_interaction:
            user.interaction = new_interaction  
        print ("User information updated successfully.")
        return user 
        

    def display_users(self):
        if not self.users:
            print("No users registered.")
        else:
            for user in self.users.values():
                print(user)


def main():
    user_manager = UserManager()

    while True:
        print("\nUser Management System")
        print("1. Register")
        print("2. Login")
        print("3. Delete User")
        print("4. Update User")
        print("5. Display Users")
        print("6. Add funds")
        print("7. Actual to Escrow")
        print("8. Exit")
        

        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            interaction = input("Enter interaction: ")
            try:
                user_manager.register(username, email, password, interaction)
                print(f"User '{username}' registered successfully.")
            except ValueError as e:
                print(e)

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            try:
                user = user_manager.login(username, password)
                print(f"User '{user.username}' logged in successfully.")
            except ValueError as e:
                print(e)

        elif choice == '3':
            username = input("Enter username to delete: ")
            try:
                user_manager.delete_user(username)
            except ValueError as e:
                print(e)

        elif choice == '4':
            username = input("Enter username to update: ")
            new_username = input("Enter new username (leave blank to keep current): ")
            new_email = input("Enter new email (leave blank to keep current): ")
            new_password = input("Enter new password (leave blank to keep current): ")
            new_interaction = input("Enter new interaction (leave blank to keep current): ")
            try:
                updated_user = user_manager.update_user(
                    username,
                    new_username=new_username if new_username else None,
                    new_email=new_email if new_email else None,
                    new_password=new_password if new_password else None,
                    new_interaction=new_interaction if new_interaction else None
                )
                print(f"User '{updated_user.username}' updated successfully.")
            except ValueError as e:
                print(e)

        elif choice == '5':
            user_manager.display_users()

        elif choice == '6':
            username = input("Enter Username: ")
            amount = input("Enter Amount: ")
            try:
                user_manager.add_funds(username, amount)
                print("Funds added successfully!")
            except ValueError as e:
                print(e)

        elif choice == '7':
            username = input("Username: ")
            amount = input("Amount: ")
            user_manager.actual_to_escrow_balance (username, amount)
            print ("Moving funds")

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

      

if __name__ == "__main__":
    main()


    
    
