import tkinter as tk

from utils import BG_COLOR, DARK_VIOLET, VIOLET, GREEN, DARK_GREEN
from utils import switch_frame

class SelectionFrame(tk.Frame):
  def __init__(self, parent):
    super().__init__(parent, bg=BG_COLOR)

    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(5, weight=1)
    self.grid_columnconfigure(0, weight=1)
  
    # Logo
    self.logoImage = tk.PhotoImage(file="byteme.png")
    self.logo_label = tk.Label(self, image=self.logoImage, bg=BG_COLOR)
    self.logo_label.grid(row=1, column=0, pady=10, sticky="nsew")

    # Label for selection
    self.selection_label = tk.Label(self, text="Select Interface", font="Roboto 32 bold", bg=BG_COLOR, fg='white', anchor="center")
    self.selection_label.grid(row=2, column=0, pady=10, sticky="nsew")

    # Admin button
    self.admin_button = tk.Button(self, text="Admin Interface", font="Roboto 16 bold", bg=VIOLET, relief="raised", borderwidth=2,highlightthickness=0, command=lambda: switch_frame(parent.admin_password_frame), fg="white", activebackground=DARK_VIOLET, activeforeground="white", padx=10, pady=5, width=20)
    self.admin_button.grid(row=3, column=0, pady=10)

    # Customer button
    self.customer_button = tk.Button(self, text="Customer Interface", font="Roboto 16 bold", bg=GREEN, relief="raised", borderwidth=2, highlightthickness=0, command=lambda: switch_frame(parent.customer_name_frame), fg="white", activebackground=DARK_GREEN, activeforeground="white", padx=10, pady=5, width=20)
    self.customer_button.grid(row=4, column=0, pady=10)

  def refresh_frame(self):
    pass