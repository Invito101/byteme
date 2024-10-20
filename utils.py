import tkinter as tk
import csv

BG_COLOR = "#0a0a0a"
HEADER_COLOR = "#262626"

DARK_RED = "#b91c1c"
RED = "#dc2626"

DARK_GREEN = "#15803d"
GREEN = "#16a34a"

DARK_VIOLET = "#4c1d95"
VIOLET = "#6d28d9"

GRAY = "#e5e5e5"

def switch_frame(frame):
  frame.tkraise()
  frame.refresh_frame()

def choose_bg_color(index):
  if (index % 2 == 0):
    return "#18181b"
  else:
    return "#09090b"

# l -> [["Butter", "10"]...]
def convert_to_menu_qty(l):
  d = {}
  for v in l:
    d[v[0]] = tk.IntVar(value=0)

  return d

# d -> {"butter": 5} name and quantity
# l -> [["butter", "100"]] name and price
def get_total_amount(d, l: list):
  count = 0
  for x in l:
    if x[0] in d:
      count += float(x[1]) * d[x[0]].get()

  return count

# CSV Utils

def handle_menu_file_not_found():
  print("menu.csv file not found, creating a file with appropriate headers")
  with open("menu.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(["Name", "Price"])

def read_menu():
  try:
    with open("menu.csv", "r") as csv_file:
      csv_reader = csv.reader(csv_file)
      next(csv_reader)

      return list(csv_reader)
  except FileNotFoundError:
    handle_menu_file_not_found()
    
    return list()
  
# l -> [name, price]
def append_menu(l):
  try:
    open("menu.csv", "r")
  except FileNotFoundError:
    handle_menu_file_not_found()

  with open("menu.csv", "a") as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(l)

def delete_menu_item(index):
  rows = read_menu()
  print(rows)

  if index < len(rows):
    rows.pop(index)

    with open("menu.csv", "w") as csv_file:
      csv_writer = csv.writer(csv_file)
      rows.insert(0, ["Name", "Price"])
      csv_writer.writerows(rows)

# Orders
# Get's incomplete order

def handle_orders_file_not_found():
  print("orders.csv file not found, creating a file with appropriate headers")
  with open("orders.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(["ID", "Customer Name", "Item Name and Quantity", "Total Amount", "Order Completed"])

def get_all_incomplete_orders():
  try:
    with open("orders.csv", "r") as csv_file:
      csv_reader = csv.reader(csv_file)
      next(csv_reader)
      return list(filter(lambda x: x[-1] == "False", list(csv_reader)))
  except FileNotFoundError:
    handle_orders_file_not_found()
    return list()

def get_all_orders():
  try:
    with open("orders.csv", "r") as csv_file:
      csv_reader = csv.reader(csv_file)
      next(csv_reader)
      return list(csv_reader)
  except:
    handle_orders_file_not_found()
    return list()
  
def get_next_customer_name():
  id = len(get_all_orders())+1
  return f"Customer {id}"

# menu_qty -> {"butter": 5} name and quantity in IntVar
# name -> customer name
# total-cost -> total cost of all the menu_qty as StringVar
def append_order(name, menu_qty, total_cost):
  items_ordered_string = ""
  for k,v in menu_qty.items():
    qty = v.get()
    if qty != 0: 
      items_ordered_string += f"{k} - {qty}, "

  actual_string = items_ordered_string[:-2]
  if not name:
    name = get_next_customer_name()

  id = len(get_all_orders())+1

  with open("orders.csv", "a") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([id, name, actual_string, total_cost.get(), False])

def mark_order_as_completed(order_id):
  rows = get_all_orders()

  for line in rows:
    if line[0] == order_id:
      line[-1] = True
    
  with open("orders.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    rows.insert(0, ["ID", "Customer Name", "Item Name and Quantity", "Total Amount", "Order Completed"])
    csv_writer.writerows(rows)