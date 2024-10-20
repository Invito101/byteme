import tkinter as tk

from utils import BG_COLOR, HEADER_COLOR, VIOLET, DARK_VIOLET, switch_frame, choose_bg_color, RED, GREEN
from utils import read_menu, append_menu, delete_menu_item, get_all_incomplete_orders, mark_order_as_completed

class OrderHistoryManager(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent, bg=BG_COLOR)
    self.parent = parent

    self.header()
    self.scrollable_frame()
    self.menu()

    self.status()

  def refresh_frame(self):
    self.status_dynamic()

  def header(self):
    self.admin_header_frame = tk.Frame(self, bg=HEADER_COLOR, height=75)
    self.admin_header_frame.pack(fill='x')

    self.admin_header_label = tk.Label(self.admin_header_frame, text="Admin Interface", font="Roboto 24 bold", bg=HEADER_COLOR, fg='white')
    self.admin_header_label.pack(side='left', padx=20, pady=20)

    self.admin_switch_button = tk.Button(self.admin_header_frame, text="Switch", font="Roboto 16 bold", command=lambda: switch_frame(self.parent.selection_frame), bg=VIOLET, relief="raised", borderwidth=2, highlightthickness=0, fg="white", activebackground=DARK_VIOLET, activeforeground="white", padx=10, pady=5) 
    self.admin_switch_button.pack(side='right', padx=20, pady=10)

  def scrollable_frame(self):
    # Scrollable Frame
    self.canvas = tk.Canvas(self, bg=BG_COLOR, bd=0, highlightthickness=0)
    self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
    self.scrollable_frame = tk.Frame(self.canvas, bg=BG_COLOR)

    # Configure the canvas
    self.scrollable_frame.bind(
        "<Configure>",
        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    )

    self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

    # Configure scrollbar
    self.canvas.configure(yscrollcommand=self.scrollbar.set)

    # Pack canvas and scrollbar
    self.scrollbar.pack(side="right", fill="y")
    self.canvas.pack(side="left", fill="both", expand=True)

    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)

  def menu(self):
    self.menu_frame_method()
    self.menu_static()
    self.menu_dynamic()

  def menu_frame_method(self):
    self.menu_frame = tk.Frame(self.scrollable_frame, bg=BG_COLOR, padx=20, pady=20)
    self.menu_frame.grid(row=0, column=0, sticky="nsew")

  def menu_static(self):
    # Menu Label (fixed)
    self.menu_label = tk.Label(self.menu_frame, text="Modify Menu Dishes", font="Roboto 20 bold", bg=BG_COLOR, fg='white')
    self.menu_label.grid(row=0, column=0, sticky="w")

    # Input Frame for Entry and Submit Button (fixed)
    self.input_frame = tk.Frame(self.menu_frame, bg=BG_COLOR)
    self.input_frame.grid(row=1, column=0, sticky="w", pady=10)

    self.item_name_label = tk.Label(self.input_frame, text="Item Name", font="Roboto 12 bold", bg=BG_COLOR, fg="white")
    self.item_name_label.grid(row=0, column=0, sticky="w", pady=10)

    self.item_price_label = tk.Label(self.input_frame, text="Item Price", font="Roboto 12 bold", bg=BG_COLOR, fg="white")
    self.item_price_label.grid(row=0, column=1, sticky="w")

    self.item_name_entry = tk.Entry(self.input_frame, font="Roboto 12 bold", bg=BG_COLOR, foreground="white", highlightcolor=DARK_VIOLET,insertbackground="white", width=20, relief="solid", bd=4)
    self.item_name_entry.grid(row=1, column=0, padx=(0, 10))

    self.item_price_entry = tk.Entry(self.input_frame, font="Roboto 12 bold", bg=BG_COLOR, foreground="white", highlightcolor=DARK_VIOLET,insertbackground="white", width=20, relief="solid", bd=4)
    self.item_price_entry.grid(row=1, column=1, padx=(0, 10))

    self.submit_button = tk.Button(self.input_frame, text="Add", command=lambda: self.add_item(), font="Roboto 14 bold", bg=VIOLET, relief="raised", borderwidth=2, highlightthickness=0, fg="white", activebackground=DARK_VIOLET, activeforeground="white", padx=10, pady=4)
    self.submit_button.grid(row=1, column=2)

  def add_item(self):
    item_name = self.item_name_entry.get()
    item_price = self.item_price_entry.get()
    if item_name != "" and item_price != "":
      item_price = float(self.item_price_entry.get())
      self.item_name_entry.delete(0, tk.END)  # Clear the item name field
      self.item_price_entry.delete(0, tk.END)  # Clear the item price field

      append_menu([item_name, item_price])
      self.menu_dynamic()

  def delete_item(self, index):
    delete_menu_item(index)
    self.menu_dynamic()

  def menu_dynamic(self):
    self.menu_items = []
    self.name_price_list = read_menu()

    self.menu_list_frame = tk.Frame(self.menu_frame, bg=BG_COLOR)
    self.menu_list_frame.grid(row=2, column=0, sticky="nsew")

    for index, val in enumerate(self.name_price_list):
      bg_color = choose_bg_color(index)
      self.menu_list_frame_detail = tk.Frame(self.menu_list_frame, bg=bg_color)
      self.menu_list_frame_detail.grid(row=index, column=0, sticky="nsew", padx=5, pady=5)

      new_item_name = tk.Label(self.menu_list_frame_detail, text=val[0], font="Roboto 12 bold", bg=bg_color, fg="white", width=60, height=2, anchor="w")
      new_item_name.grid(row=0, column=0, pady=5)

      new_item_price = tk.Label(self.menu_list_frame_detail, text=f"₹{val[1]}", font="Roboto 12 bold", bg=bg_color, fg="white", width=42, height=2, anchor="w")
      new_item_price.grid(row=0, column=1, padx=5, pady=5)
      
      delete_button = tk.Button(self.menu_list_frame_detail, text="Delete", command=lambda idx=index: self.delete_item(idx), font="Roboto 12 bold", fg="white", bg=bg_color, activebackground=RED, activeforeground="white", highlightthickness=0, relief="raised", border=2)
      delete_button.grid(row=0, column=2, pady=5)

      self.menu_items.append([val[0], float(val[1]), self.menu_list_frame_detail])

  def status(self):
    self.status_frame_method()
    self.status_dynamic()

  def status_frame_method(self):
    self.status_frame = tk.Frame(self.scrollable_frame, bg=BG_COLOR, padx=20, pady=20)
    self.status_frame.grid(row=1, column=0, sticky="nsew")

  def status_dynamic(self):
    # Status Label (fixed)
    self.status_label = tk.Label(self.status_frame, text="Order Status", font="Roboto 20 bold", bg=BG_COLOR, fg='white')
    self.status_label.grid(row=0, column=0, sticky="w")

    self.status_list_frame = tk.Frame(self.status_frame, bg=BG_COLOR)
    self.status_list_frame.grid(row=1, column=0, sticky="nsew")

    self.orders = get_all_incomplete_orders()
    self.status_list = []

    for index, val in enumerate(self.orders):
      bg_color = choose_bg_color(index)
      self.orders_list_frame_detail = tk.Frame(self.status_list_frame, bg=bg_color)
      self.orders_list_frame_detail.grid(row=index, column=0, sticky="nsew", padx=5, pady=5)

      order_id = tk.Label(self.orders_list_frame_detail, text=val[0], font="Roboto 12 bold", bg=bg_color, fg='white', width=4, height=2, anchor="w")
      order_id.grid(row=index, column=0, pady=5)

      customer_name = tk.Label(self.orders_list_frame_detail, text=val[1], font="Roboto 12 bold", bg=bg_color, fg='white', width=13, height=2, anchor="w")
      customer_name.grid(row=index, column=1, padx=4, pady=5, sticky="w")
      
      order = tk.Label(self.orders_list_frame_detail, text=val[2], font="Roboto 12 bold", bg=bg_color, fg='white', width=60, height=2, anchor="w")
      order.grid(row=index, column=2, pady=4, sticky="w")

      total_amount = tk.Label(self.orders_list_frame_detail, text=val[3], font="Roboto 12 bold", bg=bg_color, fg='white', width=20, height=2, anchor="w")
      total_amount.grid(row=index, column=3, padx=4, pady=5)

      completed_button = tk.Button(self.orders_list_frame_detail, text="Completed", command=lambda idx=index: self.mark_as_completed(idx), font="Roboto 12 bold", fg="white", bg=bg_color, activebackground=GREEN, activeforeground="white", highlightthickness=0, relief="raised", border=2)
      completed_button.grid(row=index, column=4, pady=5, sticky="e")

      self.status_list.append([val[0], self.orders_list_frame_detail])
  
  def mark_as_completed(self, index):
    id, frame = self.status_list[index]

    mark_order_as_completed(id)
    self.status_dynamic()

class AdminPasswordFrame(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent, bg=BG_COLOR)
    self.parent = parent

    self.main()
  
  def refresh_frame(self):
    pass

  def submit(self):
    if self.password.get() == "password":
      switch_frame(self.parent.admin_frame)
      self.password_entry.delete(0, tk.END)

  def main(self):
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(5, weight=1)
    self.grid_columnconfigure(0, weight=1)

    self.password = tk.StringVar()

    # Logo
    self.logoImage = tk.PhotoImage(file="byteme.png")
    self.logo_label = tk.Label(self, image=self.logoImage, bg=BG_COLOR)
    self.logo_label.grid(row=1, column=0, pady=10, sticky="nsew")

    # Label for admin
    self.admin_label = tk.Label(self, text="Admin Interface", font="Roboto 16 bold", bg=BG_COLOR, fg='white', anchor="center")
    self.admin_label.grid(row=2, column=0, pady=10, sticky="nsew")

    # Name Label
    self.password_label = tk.Label(self, text="Enter the password", font="Roboto 24 bold", bg=BG_COLOR, fg='white', anchor="center")
    self.password_label.grid(row=2, column=0, pady=10, sticky="nsew")

    # Name Entry
    self.password_entry = tk.Entry(self, textvariable=self.password, font="Roboto 12 bold", bg=BG_COLOR, foreground="white", highlightcolor=DARK_VIOLET, insertbackground="white", width=20, relief="solid", bd=2, show="•")
    self.password_entry.grid(row=3, column=0, pady=10)

    # Submit
    self.submit_button = tk.Button(self, text="Submit", font="Roboto 16 bold", bg=VIOLET, relief="raised", borderwidth=2,highlightthickness=0, command=self.submit, fg="white", activebackground=DARK_VIOLET, activeforeground="white", padx=10, pady=5, width=20)
    self.submit_button.grid(row=4, column=0, pady=10)
