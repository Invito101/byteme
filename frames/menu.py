import tkinter as tk
from tkinter import ttk

from utils import BG_COLOR, switch_frame, convert_to_menu_qty, get_total_amount, append_order, get_next_customer_name
from utils import read_menu, GREEN, DARK_GREEN, HEADER_COLOR, choose_bg_color, GRAY, DARK_RED

class Menu(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent, bg=BG_COLOR)
    self.parent = parent
    
    self.header()
    self.scrollable_frame()
    self.menu_frame_method()
    self.menu()
  
  def refresh_frame(self):
    self.menu()

  def header(self):
    self.customer_header_frame = tk.Frame(self, bg=HEADER_COLOR, height=75)
    self.customer_header_frame.pack(fill='x')

    self.customer_header_label = tk.Label(self.customer_header_frame, text="Customer Interface", font="Roboto 24 bold", bg=HEADER_COLOR, fg='white')
    self.customer_header_label.pack(side='left', padx=20, pady=20)

    self.customer_switch_button = tk.Button(self.customer_header_frame, text="Switch", font="Roboto 16 bold", bg=GREEN, relief="raised", borderwidth=2,highlightthickness=0, command=lambda: switch_frame(self.parent.selection_frame), fg="white", activebackground=DARK_GREEN, activeforeground="white", padx=10, pady=5)
    self.customer_switch_button.pack(side='right', padx=20, pady=10)

  # Method just makes it scrollable, only UI
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

  def menu_frame_method(self):
    self.menu_frame = tk.Frame(self.scrollable_frame, bg=BG_COLOR, padx=20, pady=20)
    self.menu_frame.grid(row=0, column=0, sticky="nsew")

  def menu(self):
    self.menu_static()
    self.menu_list()
    separator = ttk.Separator(self.menu_frame, orient='horizontal')
    separator.grid(row=3, column=0, sticky="we")

    self.order_tax()

  def menu_static(self):
    self.name_price_list = read_menu()
    # [['Mooshrooom', '1000.56'], ['Dosa', '2121.43'], ['Idly', '3322.2']]
    self.menu_label = tk.Label(self.menu_frame, text=f"Menu", font="Roboto 20 bold", bg=BG_COLOR, fg='white')
    self.menu_label.grid(row=0, column=0, sticky="w")

  def increase(self, name):
    self.menu_qty[name].set(self.menu_qty[name].get() + 1)

    self.update_total_amount(get_total_amount(self.menu_qty, self.name_price_list))

  def decrease(self, name):
    if (self.menu_qty[name].get() != 0):
      self.menu_qty[name].set(self.menu_qty[name].get() - 1)

    self.update_total_amount(get_total_amount(self.menu_qty, self.name_price_list))

  def update_total_amount(self, amount):
    self.total_amount.set(f"+₹{amount:.2f}")
    self.handle_taxes()

  def handle_taxes(self):
    self.taxes_amount.set(f"+₹{(0.18 * float(self.total_amount.get()[2:])):.2f}")
    self.total_after_tax.set(f"₹{(1.18 * float(self.total_amount.get()[2:])):.2f}")

  def menu_list(self):
    self.menu_qty = convert_to_menu_qty(self.name_price_list)
    # {'Mooshrooom': <tkinter.IntVar object at 0x7f72aad970a0>, 'Dosa': <tkinter.IntVar object at 0x7f72aad97100>, 'Idly': <tkinter.IntVar object at 0x7f72aad97160>}
    self.menu_items = []

    self.menu_list_frame = tk.Frame(self.menu_frame, bg=BG_COLOR)
    self.menu_list_frame.grid(row=2, column=0, sticky="nsew")

    self.total_amount = tk.StringVar(value="+₹0")
    self.taxes_amount = tk.StringVar(value="+₹0")
    self.total_after_tax = tk.StringVar(value="₹0")

    for index, val in enumerate(self.name_price_list):
      bg_color = choose_bg_color(index)
      self.menu_list_frame_detail = tk.Frame(self.menu_list_frame, bg=bg_color)
      self.menu_list_frame_detail.grid(row=index, column=0, sticky="nsew", padx=5, pady=5)

      new_item_name = tk.Label(self.menu_list_frame_detail, text=val[0], font="Roboto 12 bold", bg=bg_color, fg='white', width=32, anchor="w")
      new_item_name.grid(row=index, column=0, padx=5, pady=5, sticky="ew")

      new_item_price = tk.Label(self.menu_list_frame_detail, text=f"₹{val[1]}", font="Roboto 12 bold", bg=bg_color, fg='white', anchor="w", width=18)
      new_item_price.grid(row=index, column=1, padx=(0,5), pady=5, sticky="w")
      
      decrease_button = tk.Button(self.menu_list_frame_detail, text="-",  font="Roboto 12 bold", command=lambda name=val[0]: self.decrease(name), width=1, height=1, fg="black", bg=GRAY, activebackground=DARK_RED, activeforeground="white", highlightthickness=0, relief="raised", border=2)
      decrease_button.grid(row=index, column=2, pady=5, sticky="e")
      
      quantity = tk.Label(self.menu_list_frame_detail, textvariable=self.menu_qty[val[0]], font="Roboto 12 bold", anchor="center", background=bg_color, foreground="white", width=6)
      quantity.grid(row=index, column=3, pady=2, padx=10)

      increase_button = tk.Button(self.menu_list_frame_detail, text="+", font="Roboto 12 bold", command=lambda name=val[0]: self.increase(name), width=1, height=1, fg="black", bg=GRAY, activebackground=DARK_GREEN, activeforeground="white", highlightthickness=0, relief="raised", border=2)
      increase_button.grid(row=index, column=4, pady=5, sticky="e")

      self.menu_items.append([val[0], float(val[1]), new_item_name, new_item_price, decrease_button, increase_button])

    self.menu_list_frame.columnconfigure(0, weight=1)

  def order_tax(self):
    self.order_tax_frame = tk.Frame(self.menu_frame, bg=BG_COLOR)
    self.order_tax_frame.grid(row=4, column=0, sticky="nsew", pady=20)

    self.order_tax_frame.columnconfigure(0, weight=1)
    self.order_tax_frame.columnconfigure(1, weight=1)
    
    total_amount_label = tk.Label(self.order_tax_frame, text=f"Amount Before Tax", font="Roboto 12 bold", bg=BG_COLOR, fg="white", width=32, anchor="w")
    total_amount_label.grid(row=0, column=0, pady=5, sticky="w")

    total_amount = tk.Label(self.order_tax_frame, textvariable=self.total_amount, font="Roboto 12 bold", bg=BG_COLOR, fg="white", anchor="e")
    total_amount.grid(row=0, column=1, pady=5, sticky="e")

    taxes_label = tk.Label(self.order_tax_frame, text=f"18% GST", font="Roboto 12 bold", bg=BG_COLOR, fg="white", width=32, anchor="w")
    taxes_label.grid(row=1, column=0, pady=5, sticky="w")

    taxes_amount_label = tk.Label(self.order_tax_frame, textvariable=self.taxes_amount, font="Roboto 12 bold", bg=BG_COLOR, fg="white", anchor="e")
    taxes_amount_label.grid(row=1, column=1, pady=5, sticky="e")

    total_amount_after_tax_label = tk.Label(self.order_tax_frame, text=f"Total Amount", font="Roboto 18 bold", bg=BG_COLOR, fg="white", width=32, anchor="w")
    total_amount_after_tax_label.grid(row=2, column=0, pady=5, sticky="w")

    total_amount_after_tax = tk.Label(self.order_tax_frame, textvariable=self.total_after_tax, font="Roboto 18 bold", bg=BG_COLOR, fg="white", anchor="e")
    total_amount_after_tax.grid(row=2, column=1, pady=5, sticky="e")

    place_order_button = tk.Button(self.order_tax_frame, text="Place Order",  font="Roboto 16 bold", bg=GREEN, relief="raised", borderwidth=2,highlightthickness=0, command=self.place_order, fg="white", activebackground=DARK_GREEN, activeforeground="white", padx=10, pady=5)
    place_order_button.grid(row=3, column=1, pady=5, sticky="e")

  def place_order(self):
    if float(self.total_amount.get()[2:]) == 0:
      return
    append_order(self.parent.customer_name.get(), self.menu_qty, self.total_after_tax)
    self.update_total_amount(0)
    self.menu_qty = convert_to_menu_qty(self.name_price_list)
    self.menu_list()

    switch_frame(self.parent.customer_order_confirmation_frame)

class CustomerNameFrame(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent, bg=BG_COLOR)
    self.parent = parent

    self.main()
  
  def refresh_frame(self):
    self.parent.customer_name.set(get_next_customer_name())

  def submit(self):
    if self.parent.customer_name.get() and self.parent.customer_name.get() != "":
      switch_frame(self.parent.customer_frame)

  def main(self):
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(5, weight=1)
    self.grid_columnconfigure(0, weight=1)

    # Logo
    self.logoImage = tk.PhotoImage(file="byteme.png")
    self.logo_label = tk.Label(self, image=self.logoImage, bg=BG_COLOR)
    self.logo_label.grid(row=1, column=0, pady=10, sticky="nsew")

    # Label for customer
    self.customer_label = tk.Label(self, text="Customer Interface", font="Roboto 16 bold", bg=BG_COLOR, fg='white', anchor="center")
    self.customer_label.grid(row=2, column=0, pady=10, sticky="nsew")

    # Name Label
    self.name_label = tk.Label(self, text="What is your name?", font="Roboto 24 bold", bg=BG_COLOR, fg='white', anchor="center")
    self.name_label.grid(row=2, column=0, pady=10, sticky="nsew")

    # Name Entry
    self.customer_header_name = tk.Entry(self, textvariable=self.parent.customer_name, font="Roboto 12 bold", bg=BG_COLOR, foreground="white", highlightcolor=DARK_GREEN, insertbackground="white", width=20, relief="solid", bd=2)
    self.customer_header_name.grid(row=3, column=0, pady=10)

    # Submit
    self.submit_button = tk.Button(self, text="Submit", font="Roboto 16 bold", bg=GREEN, relief="raised", borderwidth=2,highlightthickness=0, command=self.submit, fg="white", activebackground=DARK_GREEN, activeforeground="white", padx=10, pady=5, width=20)
    self.submit_button.grid(row=4, column=0, pady=10)

class CustomerOrderConfirmationFrame(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent, bg=BG_COLOR)
    self.parent = parent

    self.main()
  
  def refresh_frame(self):
    pass

  def main(self):
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(4, weight=1)
    self.grid_columnconfigure(0, weight=1)

    # Logo
    self.logoImage = tk.PhotoImage(file="byteme.png")
    self.logo_label = tk.Label(self, image=self.logoImage, bg=BG_COLOR)
    self.logo_label.grid(row=1, column=0, pady=10, sticky="nsew")

    # Label for customer
    self.customer_label = tk.Label(self, text="Order Confirmed", font="Roboto 32 bold", bg=BG_COLOR, fg='white', anchor="center")
    self.customer_label.grid(row=2, column=0, pady=10, sticky="nsew")

    self.customer_switch_button = tk.Button(self, text="Switch", font="Roboto 16 bold", bg=GREEN, relief="raised", borderwidth=2,highlightthickness=0, command=lambda: switch_frame(self.parent.selection_frame), fg="white", activebackground=DARK_GREEN, activeforeground="white", padx=10, pady=5, width=20)
    self.customer_switch_button.grid(row=3, column=0, pady=10)
