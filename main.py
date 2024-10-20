import tkinter as tk

from utils import BG_COLOR
from utils import switch_frame
from utils import get_next_customer_name
from frames.selection_frame import SelectionFrame
from frames.order_history_manager import OrderHistoryManager, AdminPasswordFrame
from frames.menu import Menu, CustomerNameFrame, CustomerOrderConfirmationFrame

def main():
  app = RestaurantUI()
  app.mainloop()

class RestaurantUI(tk.Tk):
  def __init__(self):
    super().__init__()
    self.title("byteme - Restaurant Management System")
    self.geometry("800x800")
    self.configure(bg = BG_COLOR)
    self.grid_rowconfigure(0, weight=100)
    self.grid_columnconfigure(0, weight=100)

    self.customer_name = tk.StringVar(value=get_next_customer_name())

    self.selection_frame = SelectionFrame(self)
    self.admin_frame = OrderHistoryManager(self)
    self.customer_frame = Menu(self)
    self.customer_name_frame = CustomerNameFrame(self)
    self.customer_order_confirmation_frame = CustomerOrderConfirmationFrame(self)
    self.admin_password_frame = AdminPasswordFrame(self)

    for frame in (self.selection_frame, self.admin_frame, self.customer_frame, self.customer_name_frame, self.customer_order_confirmation_frame, self.admin_password_frame):
      frame.grid(row=0, column=0, sticky='nsew')

    switch_frame(self.selection_frame)

    self.update()

if __name__ == "__main__":
  main()