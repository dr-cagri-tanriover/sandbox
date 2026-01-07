
from tkinter import *
from tkinter import filedialog
from mypackages import tkint_gui_const as gc  # constants for the GUI application
from mypackages import patent101_app as pa  # constants for the GUI application


# Good tkinter ref: https://levelup.gitconnected.com/10-interesting-python-tkinter-programs-with-code-df52174993e1
# https://datatofish.com/entry-box-tkinter/

def p101_application():
    #gui = Tk()  # instantiate the gui handler

    p101Obj = pa.p101_class()  # initialize GUI

    p101Obj.gui.mainloop()  # run the GUI application

def basic_gui():

    def working_dir_button_callback():
        selected_dir = filedialog.askdirectory()
        label1.config(text="cwd = " + selected_dir, font=('helvetica', 10, 'bold'))

    def exec_button_callback():
        print(f"Option selected = {dd1_variable.get()}")

    gui = Tk()  # instantiate the gui handler
    #gui.attributes('-fullscreen', True)  # make main window full-screen
    gui.minsize(width=gui.winfo_screenwidth(), height=gui.winfo_screenheight())

    gui.title(gc.TITLE_STRING)
    gui.iconbitmap(gc.TITLE_ICON_FILE)

    mainCanvas = Canvas(gui)  # create canvas for widget placement
    #mainCanvas = Canvas(gui, width=gc.CANVAS_DIM['w'], height=gc.CANVAS_DIM['h'])  # create canvas for widget placement
    mainCanvas.pack(fill=BOTH, expand=True)  # configure canvas to occupy the whole main window

    textBox1 = Entry(gui)  # Text entry box 1
    mainCanvas.create_window(gc.TXTBOX1_POS['x'], gc.TXTBOX1_POS['y'], window=textBox1)  # specify x,y location of text box 1 in canvas

    label1 = Label(gui, text=" ")  # clears off text first
    mainCanvas.create_window(gc.LABEL1_POS['x'], gc.LABEL1_POS['y'], window=label1)

    working_dir_button = Button(gui, text="~Select Working Directory~", command=working_dir_button_callback)
    mainCanvas.create_window(gc.WORKING_DIR_BUTTON_POS['x'], gc.WORKING_DIR_BUTTON_POS['y'], window=working_dir_button)  # specify x,y location of button 1 in canvas

    dd1_variable = StringVar(gui)
    dd1_variable.set(gc.DROPDOWN1_OPTIONS_LIST[0])  # default selected value
    dropdown1 = OptionMenu(gui, dd1_variable, *gc.DROPDOWN1_OPTIONS_LIST)
    mainCanvas.create_window(gc.DROPDOWN1_POS['x'], gc.DROPDOWN1_POS['y'], window=dropdown1)  # specify x,y location of button 1 in canvas

    exec_button = Button(gui, text="~RUN~", command=exec_button_callback)
    mainCanvas.create_window(gc.EXEC_BUTTON_POS['x'], gc.EXEC_BUTTON_POS['y'], window=exec_button)  # specify x,y location of button 1 in canvas

    gui.mainloop()