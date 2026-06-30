# NECESSARY IMPORTS FOR BASE APP INTERFACE 
import tkinter as tk
from tkinter import messagebox
import time

# NECESSARY IMPORTS FROM OWN FILES 
from Account_Base_Prototype import UserManager
from Escrow_Transaction_Engine import EscrowTransactionManager
from Stock_Scraper import ProductManager, ScrapeManager

# SETS UP OWN FILE IMPORTS FOR USE THROUGHOUT 
user_manager = UserManager()
escrow_manager = EscrowTransactionManager()
product_manager = ProductManager()

# URLS TO BE SCRAPED BY STOCK_SCRAPER - WILL NEED TO BE ADDED TO
vendor_urls = {
    "Morrisons": "https://groceries.morrisons.com",
    "Tesco": "https://www.tesco.com/groceries/en-GB"
}
scrape_manager = ScrapeManager(vendor_urls, product_manager)
scrape_manager.refresh_cache()

# CREATES APP CLASS
class App:
   
    def __init__(self, root):
        self.root = root
        self.root.title("Prototype Marketplace")
        self.root.geometry("420x480")
        self.current_frame = None
        self.show_login_screen()

    def switch_to(self, build_frame_function):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = build_frame_function(self.root, self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # ---- screen switchers -------------------------------------------------
    def show_login_screen(self):
        self.switch_to(build_login_screen)

    def show_register_screen(self):
        self.switch_to(build_register_screen)

    def show_dashboard_screen(self, username):
        self.switch_to(lambda root, app: build_dashboard_screen(root, app, username))

    def show_browse_screen(self, username):
        self.switch_to(lambda root, app: build_browse_screen(root, app, username))

    def show_add_funds_screen(self, username):
        self.switch_to(lambda root, app: build_add_funds_screen(root, app, username))

    def show_checkout_screen(self, username):
        self.switch_to(lambda root, app: build_checkout_screen(root, app, username))


# ---------------------------------------------------------------------------
# SCREEN 1 — Login
# ---------------------------------------------------------------------------
def build_login_screen(root, app):
    frame = tk.Frame(root)

    tk.Label(frame, text="Login", font=("Arial", 18, "bold")).pack(pady=(0, 20))

    tk.Label(frame, text="Username").pack(anchor="w")
    username_entry = tk.Entry(frame)
    username_entry.pack(fill="x", pady=(0, 10))

    tk.Label(frame, text="Password").pack(anchor="w")
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(fill="x", pady=(0, 20))

# USES LOGIC IN OWN FILES - REPEATED THROUGHOUT - WILL BE OBVIOUS WHERE
    def on_login_click():
        username = username_entry.get()
        password = password_entry.get()
        try:
            user = user_manager.login(username, password)
            app.show_dashboard_screen(username)
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))
    tk.Button(frame, text="Login", command=on_login_click).pack(fill="x", pady=5)
    tk.Button(frame, text="Need an account? Register", command=app.show_register_screen).pack(fill="x")

    return frame


# ---------------------------------------------------------------------------
# SCREEN 2 — Register
# ---------------------------------------------------------------------------
def build_register_screen(root, app):
    frame = tk.Frame(root)

    tk.Label(frame, text="Register", font=("Arial", 18, "bold")).pack(pady=(0, 20))

    fields = {}
    for field_name in ["Username", "Email", "Password", "Interaction (client/driver/vendor/admin)"]:
        tk.Label(frame, text=field_name).pack(anchor="w")
        entry = tk.Entry(frame, show="*" if field_name == "Password" else "")
        entry.pack(fill="x", pady=(0, 10))
        fields[field_name] = entry

    def on_register_click():
        username = fields["Username"].get()
        email = fields["Email"].get()
        password = fields["Password"].get()
        interaction = fields["Interaction (client/driver/vendor/admin)"].get()
        try:
            user_manager.register(username, email, password, interaction)
            messagebox.showinfo("Registered", "User Registered Succesfully") 
            app.show_login_screen()
        except ValueError as e:
            messagebox.showerror("Registration Failed, Please try again. If issue persists, email moderator", str(e))

    tk.Button(frame, text="Register", command=on_register_click).pack(fill="x", pady=5)
    tk.Button(frame, text="Back to login", command=app.show_login_screen).pack(fill="x")

    return frame


# ---------------------------------------------------------------------------
# SCREEN 3 — Dashboard (shown after successful login)
# ---------------------------------------------------------------------------
def build_dashboard_screen(root, app, username):
    frame = tk.Frame(root)

    user = user_manager.users[username]

    tk.Label(frame, text=f"Welcome, {username}", font=("Arial", 18, "bold")).pack(pady=(0, 10))

    tk.Label(frame, text=f"Balance: £{user.actual_balance}").pack(pady=5)
    tk.Label(frame, text=f"In escrow: £{user.escrow_balance}").pack(pady=5)

    tk.Button(frame, text="Browse Products", command=lambda: app.show_browse_screen(username)).pack(fill="x", pady=5)
    tk.Button(frame, text="Add Funds", command=lambda: app.show_add_funds_screen(username)).pack(fill="x", pady=5)
    tk.Button(frame, text="Log out", command=app.show_login_screen).pack(fill="x", pady=(20, 0))

    return frame


# ---------------------------------------------------------------------------
# SCREEN 4 — Browse products
# ---------------------------------------------------------------------------
def build_browse_screen(root, app, username):
    frame = tk.Frame(root)

    tk.Label(frame, text="Browse Products", font=("Arial", 18, "bold")).pack(pady=(0, 10))

    listbox = tk.Listbox(frame)
    listbox.pack(fill="both", expand=True, pady=(0, 10))

    for product in product_manager.products.values():
        listbox.insert(tk.END, f"{product.name} - {product.vendor} - £{product.price}")

    tk.Button(frame, text="Proceed to Checkout", command=lambda: app.show_checkout_screen(username)).pack(fill="x", pady=5)
    tk.Button(frame, text="Back to dashboard", command=lambda: app.show_dashboard_screen(username)).pack(fill="x")

    return frame


# ---------------------------------------------------------------------------
# SCREEN 5 — Add funds
# ---------------------------------------------------------------------------
def build_add_funds_screen(root, app, username):
    frame = tk.Frame(root)

    tk.Label(frame, text="Add Funds", font=("Arial", 18, "bold")).pack(pady=(0, 20))

    tk.Label(frame, text="Amount").pack(anchor="w")
    amount_entry = tk.Entry(frame)
    amount_entry.pack(fill="x", pady=(0, 20))

    def on_add_funds_click():
        amount = amount_entry.get()
        try:
            amount = float(amount)
            user_manager.add_funds(username, amount)
            messagebox.showinfo("Congratulations", "Funds Added Successfully")
            app.show_dashboard_screen(username)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
       
    tk.Button(frame, text="Add Funds", command=on_add_funds_click).pack(fill="x", pady=5)
    tk.Button(frame, text="Back to dashboard", command=lambda: app.show_dashboard_screen(username)).pack(fill="x")

    return frame


# ---------------------------------------------------------------------------
# SCREEN 6 — Checkout
# ---------------------------------------------------------------------------
def build_checkout_screen(root, app, username):
    frame = tk.Frame(root)

    tk.Label(frame, text="Checkout", font=("Arial", 18, "bold")).pack(pady=(0, 20))

    fields = {}
    for field_name in ["Amount", "Driver Username", "Vendor Username", "Admin Username"]:
        tk.Label(frame, text=field_name).pack(anchor="w")
        entry = tk.Entry(frame)
        entry.pack(fill="x", pady=(0, 10))
        fields[field_name] = entry

    def on_checkout_click():
        try:
            amount = float(fields["Amount"].get())
            driver_username = fields["Driver Username"].get()
            vendor_username = fields["Vendor Username"].get()
            admin_username = fields["Admin Username"].get()
            user_manager.actual_to_escrow_balance(username, amount)
            transaction_id = f"txn_{int(time.time())}"
            escrow_manager.add_transaction(transaction_id, amount, username, driver_username, vendor_username, admin_username, "pending")
            escrow_manager.update_transaction(transaction_id, new_status="completed")
            escrow_manager.escrow_release(transaction_id, user_manager)
            messagebox.showinfo("Success", "Purchase complete!")
            app.show_dashboard_screen(username)
        except ValueError as e:
            messagebox.showerror("Checkout Failed", str(e))

    tk.Button(frame, text="Confirm Purchase", command=on_checkout_click).pack(fill="x", pady=5)
    tk.Button(frame, text="Back to dashboard", command=lambda: app.show_dashboard_screen(username)).pack(fill="x")

    return frame


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()