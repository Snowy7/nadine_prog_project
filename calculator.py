from tkinter import *
import game as solitaire_main

pass_key = "1234"

# Initialize the main window
me = Tk()
me.geometry("354x460")
me.title("CALCULATOR")
me.config(background='Dark gray')

# Label
melabel = Label(me, text="CALCULATOR", bg='White', font=("Times", 30, 'bold'))
melabel.pack(side=TOP)

# StringVar to hold the current input
textin = StringVar()
operator = ""

# Function to handle button clicks (number and operator buttons)
def clickbut(number):
    global operator
    operator = operator + str(number)  # Append the button click value to the operator string
    textin.set(operator)

# Function to calculate the result of the expression
def equlbut():
    global operator
    try:
        # check if the input is the password
        if operator == pass_key:
            textin.set("Correct Password")
            solitaire_main.main()
            return
        
        # Evaluate the expression and display the result
        result = str(eval(operator))
        textin.set(result)
        operator = result  # After calculation, the result can be used for further calculations
    except Exception as e:
        textin.set("Error")  # If there is an error in the expression, show "Error"
        print(e)
        operator = ""

# Function to clear the input
def clrbut():
    textin.set('')
    global operator
    operator = ""

# Entry widget to display the input/output
metext = Entry(me, font=("Courier New", 12, 'bold'), textvar=textin, width=25, bd=5, bg='powder blue')
metext.pack()

# Button definitions
button_data = [
    ('1', 10, 100), ('2', 75, 100), ('3', 140, 100), ('+', 205, 100),
    ('4', 10, 170), ('5', 75, 170), ('6', 140, 170), ('-', 205, 170),
    ('7', 10, 240), ('8', 75, 240), ('9', 140, 240), ('*', 205, 240),
    ('0', 10, 310), ('.', 75, 310), ('=', 140, 310), ('/', 205, 310),
    ('CE', 270, 100, 119),  # Clear button, customized width
]

# Create buttons using the data
for button in button_data:
    if len(button) == 3:
        # Regular buttons (with text, x, y)
        text, x, y = button
        if text == "=":
            btn = Button(me, padx=14, pady=14, bd=4, bg='white', text=text, font=("Courier New", 16, 'bold'), command=equlbut)
        else:
            btn = Button(me, padx=14, pady=14, bd=4, bg='white', text=text, font=("Courier New", 16, 'bold'),
                         command=lambda t=text: clickbut(t))
        btn.place(x=x, y=y)
    elif len(button) == 4:
        # Custom buttons (like CE with a different size)
        text, x, y, height = button
        btn = Button(me, padx=14, pady=height, bd=4, bg='white', text=text, font=("Courier New", 16, 'bold'), command=clrbut)
        btn.place(x=x, y=y)

# Start the Tkinter main loop
me.mainloop()