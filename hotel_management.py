import tkinter as tk
from tkinter import ttk, messagebox
import datetime

guests = []
rooms = {
    "Single": 5,
    "Double": 3,
    "Suite": 2
}
room_rates = {"Single": 800, "Double": 1200, "Suite": 2000}

def is_valid_phone(phone):
    if len(phone) != 10:
        return False
    for ch in phone:
        if ch < '0' or ch > '9':
            return False
    return True

def book_room():
    name = entry_name.get().strip()
    phone = entry_phone.get().strip()
    room_type = combo_room.get()
    nights_str = entry_nights.get().strip()

    if not is_valid_phone(phone):
        messagebox.showerror("Invalid Phone", "Phone number must be exactly 10 digits, digits only.")
        return
    if not name:
        messagebox.showerror("Missing Name", "Name is required.")
        return
    if nights_str == "":
        messagebox.showerror("Invalid Nights", "Please enter number of nights.")
        return

    nights = 0
    for ch in nights_str:
        if ch < '0' or ch > '9':
            messagebox.showerror("Invalid Nights", "Nights must be a positive integer.")
            return
        nights = nights * 10 + (ord(ch) - ord('0'))

    if nights < 1:
        messagebox.showerror("Invalid Nights", "Nights must be at least 1.")
        return

    if rooms[room_type] <= 0:
        messagebox.showwarning("No Vacancy", "No vacant {} rooms!".format(room_type))
        return

    checkin = datetime.date.today().isoformat()
    checkout = (datetime.date.today() + datetime.timedelta(days=nights)).isoformat()

    rooms[room_type] = rooms[room_type] - 1
    guest = {"Name": name, "Phone": phone, "Room": room_type, "Nights": nights, "CheckIn": checkin, "CheckOut": checkout}
    guests.append(guest)

    update_table()

    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_nights.delete(0, tk.END)
    combo_room.current(0)

    messagebox.showinfo("Success", "Room booked for {}!".format(name))

def update_table():
    for row in guest_table.get_children():
        guest_table.delete(row)
    idx = 0
    for guest in guests:
        guest_table.insert("", "end", iid=idx, values=(
            guest["Name"],
            guest["Phone"],
            guest["Room"],
            guest["Nights"],
            guest["CheckIn"],
            guest["CheckOut"]
        ))
        idx = idx + 1

def checkout_guest():
    selected = guest_table.selection()
    if len(selected) == 0:
        messagebox.showwarning("Select Guest", "No guest selected.")
        return
    idx = int(selected[0])
    guest = guests.pop(idx)
    rooms[guest["Room"]] = rooms[guest["Room"]] + 1
    update_table()
    label_bill.config(text="Select a guest above to see their bill.")
    messagebox.showinfo("Checked Out", "{} has checked out.".format(guest["Name"]))

def show_bill(event):
    selected = guest_table.selection()
    if len(selected) == 0:
        label_bill.config(text="Select a guest above to see their bill.")
        return
    idx = int(selected[0])
    guest = guests[idx]
    total = guest["Nights"] * room_rates[guest["Room"]]
    text = "Bill for {} - Room: {}\nNights: {} x ₹{} = ₹{}".format(
        guest["Name"], guest["Room"], guest["Nights"], room_rates[guest["Room"]], total)
    label_bill.config(text=text)

root = tk.Tk()
root.title("Hotel Lodge Management System")

reg_frame = tk.LabelFrame(root, text="Guest Registration", padx=10, pady=10)
reg_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

tk.Label(reg_frame, text="Name").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(reg_frame)
entry_name.grid(row=0, column=1)

tk.Label(reg_frame, text="Phone").grid(row=1, column=0, sticky="w")
entry_phone = tk.Entry(reg_frame)
entry_phone.grid(row=1, column=1)

tk.Label(reg_frame, text="Room Type").grid(row=2, column=0, sticky="w")
combo_room = ttk.Combobox(reg_frame, values=list(rooms.keys()), state="readonly")
combo_room.grid(row=2, column=1)
combo_room.current(0)

tk.Label(reg_frame, text="Nights").grid(row=3, column=0, sticky="w")
entry_nights = tk.Entry(reg_frame)
entry_nights.grid(row=3, column=1)

btn_register = tk.Button(reg_frame, text="Book Room", command=book_room)
btn_register.grid(row=4, column=0, columnspan=2, pady=5)

list_frame = tk.LabelFrame(root, text="Current Guests", padx=10, pady=10)
list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

guest_table = ttk.Treeview(list_frame, columns=("Name", "Phone", "Room", "Nights", "CheckIn", "CheckOut"),
                           show="headings", height=6)
for col in guest_table["columns"]:
    guest_table.heading(col, text=col)
guest_table.grid(row=0, column=0, sticky="nsew")

btn_checkout = tk.Button(list_frame, text="Check Out Guest", command=checkout_guest)
btn_checkout.grid(row=1, column=0, pady=5)

bill_frame = tk.LabelFrame(root, text="Billing", padx=10, pady=10)
bill_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

label_bill = tk.Label(bill_frame, text="Select a guest above to see their bill.")
label_bill.pack()

guest_table.bind("<<TreeviewSelect>>", show_bill)

root.mainloop()