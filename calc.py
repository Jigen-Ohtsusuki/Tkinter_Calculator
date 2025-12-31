import tkinter as tk
from tkinter import font
import math

class CircularButton(tk.Canvas):
    def __init__(self, parent, text, size, bg, fg, command, pressed_bg, font_size=22):
        super().__init__(parent, width=size, height=size, bg='#202124', highlightthickness=0)
        self.command = command
        self.bg_color = bg
        self.pressed_bg = pressed_bg
        self.text_color = fg
        self.size = size
        
        # Draw the circle and text
        pad = 2
        self.oval = self.create_oval(pad, pad, size-pad, size-pad, fill=self.bg_color, outline=self.bg_color)
        self.text_item = self.create_text(size/2, size/2, text=text, fill=self.text_color, font=('Roboto', font_size))
        
        # Bind click events to the canvas widget only
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.itemconfig(self.oval, fill=self.pressed_bg)

    def _on_release(self, event):
        self.itemconfig(self.oval, fill=self.bg_color)
        if 0 <= event.x <= self.size and 0 <= event.y <= self.size:
            if self.command:
                self.command()

class GoogleCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x700") 
        self.configure(bg="#202124")
        self.resizable(False, False)

        # --- Display Section ---
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display_label = tk.Label(self, textvariable=self.display_var, 
                                    font=('Roboto', 50), bg="#202124", fg="#e8eaed", 
                                    anchor='e', padx=20)
        self.display_label.pack(side=tk.TOP, fill=tk.X, pady=(80, 10))

        # --- Buttons Section ---
        self.buttons_frame = tk.Frame(self, bg="#202124")
        self.buttons_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=15, pady=10)
        
        for i in range(4):
            self.buttons_frame.columnconfigure(i, weight=1)

        self.current_expression = ""
        self.setup_buttons()

    def setup_buttons(self):
        # Layout (5 Rows x 4 Columns)
        layout = [
            # Row 0: Functions & Advanced
            ('AC', 0, 0, 'func'), ('π', 0, 1, 'func'), ('^', 0, 2, 'func'), ('÷', 0, 3, 'op'),
            
            # Row 1: Numbers
            ('7', 1, 0, 'num'),   ('8', 1, 1, 'num'),    ('9', 1, 2, 'num'),  ('×', 1, 3, 'op'),
            
            # Row 2: Numbers
            ('4', 2, 0, 'num'),   ('5', 2, 1, 'num'),    ('6', 2, 2, 'num'),  ('-', 2, 3, 'op'),
            
            # Row 3: Numbers
            ('1', 3, 0, 'num'),   ('2', 3, 1, 'num'),    ('3', 3, 2, 'num'),  ('+', 3, 3, 'op'),
            
            # Row 4: Zero, Dot, Backspace, Equals
            ('0', 4, 0, 'num'),   ('.', 4, 1, 'num'),    ('⌫', 4, 2, 'num'), ('=', 4, 3, 'eq'),
        ]

        for text, row, col, type_ in layout:
            self.create_button(text, row, col, type_)

    def create_button(self, text, row, col, type_):
        colors = {
            'num':  {'bg': "#3c4043", 'fg': "#e8eaed", 'p_bg': "#303134"},
            'op':   {'bg': "#303134", 'fg': "#8ab4f8", 'p_bg': "#3c4043"},
            'func': {'bg': "#303134", 'fg': "#a8c7fa", 'p_bg': "#3c4043"},
            'eq':   {'bg': "#8ab4f8", 'fg': "#202124", 'p_bg': "#669df6"}
        }
        
        c = colors[type_]
        # Uniform size for grid alignment
        size = 80 
        
        btn = CircularButton(self.buttons_frame, text, size, c['bg'], c['fg'], 
                             lambda: self.on_button_click(text), c['p_bg'])
        
        btn.grid(row=row, column=col, padx=5, pady=5)

    def on_button_click(self, text):
        if text == 'AC':
            self.current_expression = ""
        elif text == '⌫':
            self.current_expression = self.current_expression[:-1]
        elif text == '=':
            try:
                # Backend Logic
                eval_expr = self.current_expression
                eval_expr = eval_expr.replace('×', '*').replace('÷', '/')
                eval_expr = eval_expr.replace('^', '**')
                eval_expr = eval_expr.replace('π', 'math.pi')
                
                # Safe eval
                result = eval(eval_expr, {"__builtins__": None}, {"math": math})
                
                # Round to 4 decimal places
                if isinstance(result, float):
                     result = round(result, 4)
                     if result.is_integer():
                         self.current_expression = str(int(result))
                     else:
                         self.current_expression = str(result)
                else:
                    self.current_expression = str(result)
            except Exception:
                self.current_expression = "Error"
        else:
            # Prevent multiple decimals or operators if needed, but keeping it flexible for now
            if self.current_expression == "0" and text not in ['.', '×', '÷', '+', '-', '^']:
                self.current_expression = text
            elif self.current_expression == "Error":
                self.current_expression = text
            else:
                self.current_expression += text
            
        self.update_display()

    def update_display(self):
        txt = self.current_expression if self.current_expression else "0"
        self.display_var.set(txt)

if __name__ == "__main__":
    app = GoogleCalculator()
    app.mainloop()
