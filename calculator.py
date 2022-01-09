import tkinter as tk
from tkinter import font
from tkinter.constants import W

#Colours
darkgray = "#212529"
gray = "#212529"
red = "#fe413c"
lightred = "#eb8872"
yellow = "#fdba2a"
lightgray = "#f3f3fa"
white = "#ffffff"

#Font
arial_default = ("Arial", 20)
arial_sm = ("Arial" , 16)
arial_md = ("Arial" , 24 , "bold")
arial_lg = ("Arial" , 40 , "bold")

class calc:
    def __init__(self):
        #Window Settitngs
        self.window = tk.Tk()
        self.window.geometry("400x700")
        self.window.resizable(0,0)
        self.window.title("Calculator")

        self.totalExpression = ""
        self.currentExpression = ""

        self.display_frame = self.drawDisplay()

        self.total_label, self.label = self.drawLabels()
        
        self.digits ={
            7:(1,1),8:(1,2),9:(1,3),
            4:(2,1),5:(2,2),6:(2,3),
            1:(3,1),2:(3,2),3:(3,3),
            0:(4,2),".":(4,1)
        }

        self.operations = {"/": "\u00f7", "*":"\u00D7", "-":"-", "+":"+"}

        self.buttons_frame = self.drawButtons()
        
        self.buttons_frame.rowconfigure(0, weight=1)


        for x in range(1,5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.drawDigitButtons()
        self.drawOpButtons()
        self.drawEqualButton()
        self.drawClearButton()
        self.drawSquareButton()
        self.drawRootButton()
        self.keybinds()

    def keybinds(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add(digit))
        
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.appendOp(operator))

    def drawDisplay(self):
        frame = tk.Frame(self.window,height = 200, bg=gray)
        frame.pack(expand=True, fill="both")
        return frame

    def drawButtons(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def drawDigitButtons(self):
        for digit,grid in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=gray, foreground=white, font=arial_md, borderwidth=0, command=lambda x=digit: self.add(x))
            button.grid(row=grid[0], column=grid[1], sticky=tk.NSEW)

    def appendOp(self, operator):
        self.currentExpression += operator
        self.totalExpression += self.currentExpression
        self.currentExpression = ""
        self.updateTotal()
        self.updateLabel()

    def drawOpButtons(self):
        i=0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=red,fg=white, font=arial_default, borderwidth=0, command=lambda x=operator: self.appendOp(x))
            button.grid(row=i,column=4,sticky=tk.NSEW)
            i+=1

    def square(self):
        self.currentExpression = str(eval(f"{self.currentExpression}**2"))
        self.updateLabel()

    def drawSquareButton(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=red,fg=white, font=arial_default, borderwidth=0, command=self.square)
        button.grid(row=0,column=2, sticky=tk.NSEW)

    def root(self):
        self.currentExpression = str(eval(f"{self.currentExpression}**0.5"))
        self.updateLabel()

    def drawRootButton(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=red,fg=white, font=arial_default, borderwidth=0, command=self.root)
        button.grid(row=0,column=3, sticky=tk.NSEW)

    def clear(self):
        self.currentExpression = ""
        self.totalExpression = ""
        self.updateLabel()
        self.updateTotal()

    def drawClearButton(self):
        button = tk.Button(self.buttons_frame, text="C", bg=yellow,fg=white, font=arial_default, borderwidth=0, command=self.clear)
        button.grid(row=0,column=1, sticky=tk.NSEW)

    def evaluate(self):
        self.totalExpression += self.currentExpression
        self.updateTotal()

        try:
            self.currentExpression = str(eval(self.totalExpression))
            self.totalExpression = ""
        except Exception as e:
            self.currentExpression = "Math Error"
        finally:
            self.updateLabel()

    def drawEqualButton(self):
        button = tk.Button(self.buttons_frame, text="=", bg=lightred,fg=white, font=arial_default, borderwidth=0, command=self.evaluate)
        button.grid(row=4,column=3, columnspan=2, sticky=tk.NSEW)

    def drawLabels(self):
        totalLabel = tk.Label(self.display_frame, text=self.totalExpression, anchor=tk.E, bg=gray,  fg=lightgray,padx=24, font=arial_sm)
        totalLabel.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.currentExpression, anchor=tk.E, bg=gray,  fg=lightgray,padx=24, font=arial_lg)
        label.pack(expand=True, fill="both")

        return totalLabel, label

    def add(self, value):
        self.currentExpression += str(value)
        self.updateLabel()
        

    def updateTotal(self):
        expression = self.totalExpression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)
    
    def updateLabel(self):
        self.label.config(text=self.currentExpression[:11])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calculator = calc()
    calculator.run()