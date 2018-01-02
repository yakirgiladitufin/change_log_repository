#!/usr/bin/python3
# -*- coding: utf-8 -*-

import AutoDesktop
import dictionary_run
import tkinter
import os
import string
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
from tkinter.ttk import Frame, Label, Style

do_action = False
disable_unsupported = True
file = ""
script_name = ""
# top = tkinter.Tk()
# # Code to add widgets will go here...
# top.mainloop()

class Application(Frame):

    def quit(self):
        root.quit()
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     root.quit()

    def __init__(self, master=None):

        self.master = master
        self.line_start = 0
        self.line_end = 0
        self.object_cb_list = []

        self.search_func=IntVar(master) # find, click, coordinate
        self.rlb=IntVar(master) # right, left, double Search Obj
        self.rbv=IntVar(master) # L/R Click
        self.exists_clicked=IntVar(master)
        self.lb_condition_var = StringVar(master)

        self.btn_if_pressed = False
        self.btn_else_pressed = False


        s = tkinter.ttk.Style()
        # print(s.theme_names())
        s.theme_use("xpnative")

        def condition():

            return int(self.lb_condition_var.get())

        def create_menu_bar(master):
            # create a toplevel menu
            menubar = Menu(master)

            # create a pulldown menu, and add it to the menu bar
            filemenu = Menu(menubar, tearoff=0)
            filemenu.add_command(label="New Scenario", command=hello, accelerator="Ctrl+N")
            filemenu.add_command(label="Open", command=openfile, accelerator="Ctrl+O")
            filemenu.add_command(label="Save", command=save, accelerator="Ctrl+S")
            filemenu.add_command(label="Save As", command=save_as, accelerator="Ctrl+Shift+S")
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
            menubar.add_cascade(label="File", menu=filemenu)

            # create more pulldown menus
            # editmenu = Menu(menubar, tearoff=0)
            # editmenu.add_command(label="Cut", command=hello)
            # editmenu.add_command(label="Copy", command=hello)
            # editmenu.add_command(label="Paste", command=hello)
            # menubar.add_cascade(label="Edit", menu=editmenu)

            helpmenu = Menu(menubar, tearoff=0)
            helpmenu.add_command(label="About", command=hello)
            menubar.add_cascade(label="Help", menu=helpmenu)

            # root.bind("<Control-q>", self.quit)
            
            # display the menu
            root.config(menu=menubar)

        def save():

            global file
            actions_save = text_actions_list.get("1.0",END) #store the contents of the text widget in a str
            
            try:
                if not file:
                    save_as()
                else:                            #this try/except block checks to
                    with open(file, 'w') as outputFile:  #see if the str containing the output
                        outputFile.write(actions_save)         #file (self.f) exists, and we can write to it,
            except AttributeError:                     #and if it doesn't,
                save_as()  

        def save_as():

            global file
            actions_save = text_actions_list.get("1.0",END)
            try:
                file = filedialog.asksaveasfilename( defaultextension=".txt", filetypes = (("text file", "*.txt"), ("text", "*.txt")))
                with open(file, 'w') as outputFile:
                    outputFile.write(actions_save)
            except Exception as e:
                print(e)

        def openfile():
            global file
            contentfile = ""
            file = filedialog.askopenfilename( defaultextension=".txt", filetypes = (("text file", "*.txt"), ("text", "*.txt")))
            with open(file, 'r') as readfile:
                for line in readfile:
                    contentfile += line

            insert_to_actions_list(contentfile)

        def sleep():

            time_sleep = int(float(tf_sleep.get("1.0",END))) 
            insert_to_actions_list("sleep({})".format(time_sleep))
            if do_action:
                AutoDesktop.do_sleep(time_sleep)

        def get_path():
            path = filedialog.askopenfilename( filetypes = (("PNG file", "*.png"), ("PNG", "*.png")))
            tf_search_object.insert(INSERT, path)

        def move_mouse_com():
            x = tf_move_mouse_x.get("1.0",END)
            y = tf_move_mouse_y.get("1.0",END)

            if x[0] == '0':
                x=1
            if y[0] == '0':
                y=1

            speed = tf_move_mouse_speed.get("1.0",END)
            # x, y, speed = int(float(x)) ,int(float(y)), int(float(speed))

            insert_to_actions_list("move_mouse({},{},{})".format(x.strip(), y.strip(), speed.strip()))
            if do_action:
                AutoDesktop.move_mouse(int(float(x)) ,int(float(y)), int(float(speed))) 

        def get_search_object_name(path = ""):

            names_dir = path.split("/")
            for name_dir in names_dir:
                if ".png" in name_dir:
                    name = name_dir[:name_dir.index(".")]

            return name

        def add_cb_obj(text):

            self.object_cb_list.append(text)
            self.cb_obj['values'] = self.object_cb_list 

        def search_object_com():
            path = (tf_search_object.get("1.0",END)).strip()
            ## need to handle path empty
            attempts = (tf_search_attempts.get("1.0",END)).strip()
            sleep = (tf_search_sleep.get("1.0",END)).strip()

            obj_name = get_search_object_name(path)
            add_cb_obj(obj_name)

            search_func = self.search_func.get()

            if search_func == 0:
                search_func = 'find()'
                # obj_name += "_exists"
            if search_func == 1:
                search_func = 'click()'
                # obj_name += "_clicked"
            if search_func == 2: 
                search_func = 'coordinate()'


            insert_to_actions_list("search_object(\"{}\",{},{})\n{}\n{}".format(path, attempts, sleep, obj_name, search_func))
            if do_action:
                object_searched = AutoDesktop.UIElem(str(path))
                ######################### Need to be in Thread #########################
                exist = object_searched.find() 
                if not exist:
                    print("Cannot Find the " + path)
                else:
                    print("Found the " + path)
                    AutoDesktop.move_mouse(object_searched.x, object_searched.y , 1) 
                ######################### Need to be in Thread #########################


        def click():

            clicktype = self.rbv.get()
            clicks = int(tf_click_time.get("1.0",END))
            speed = int(tf_click_speed.get("1.0",END))

            if clicktype == 0: ## Right
                clicktype = 'Right'
            if clicktype == 1: ## Left
                clicktype = 'Single'

            insert_to_actions_list("click(\"{}\",{},{})".format(clicktype, clicks, speed))
            if do_action:
                AutoDesktop.mouse_click(click_type=clicktype, clicks=clicks, speed=speed)

        def typetext():

            text = (tf_typetext_text.get("1.0",END)).strip()
            speed = int(tf_click_speed.get("1.0",END))

            insert_to_actions_list("typetext(\"{}\",{})".format(text, speed))
            if do_action:
                AutoDesktop.keyboard_type(type_write=text, speed=speed)   

        def press_keyboard():

            pass      

        def insert_to_actions_list(text=""):
            text_actions_list.config(state=NORMAL)
            text_actions_list.insert(INSERT, '{}\n{}:'.format(text,condition()))
            text_actions_list.config(state=DISABLED)

        def clear_actions_list():
            text_actions_list.config(state=NORMAL)
            text_actions_list.delete('1.0', END)
            text_actions_list.insert(INSERT, "0:")
            text_actions_list.config(state=DISABLED)

        def hello():
            print ("hello!")

        def select(event):
            self.line_start = text_actions_list.index("@%s,%s linestart" % (event.x, event.y))
            self.line_end = text_actions_list.index("%s lineend +1c" % self.line_start ) # +1c (newline)
            text_actions_list.tag_remove("highlight", 1.0, "end")
            text_actions_list.tag_add("highlight", self.line_start, self.line_end)
            # text_actions_list.tag_configure("highlight", background="bisque")
            text_actions_list.tag_configure("highlight", background="#5DADE2")

        def remove_action():
            text_actions_list.config(state=NORMAL)
            text_actions_list.delete(self.line_start, self.line_end)
            text_actions_list.config(state=DISABLED)

        def search_func_disable_rld():

            rb_click_obj_R.config(state=DISABLED)
            rb_click_obj_L.config(state=DISABLED)
            rb_click_obj_D.config(state=DISABLED)

        def search_func_enable_rld():

            rb_click_obj_R.config(state=NORMAL)
            rb_click_obj_L.config(state=NORMAL)
            rb_click_obj_D.config(state=NORMAL)

        def OK():

            global file, script_name, rf_filename
            
            script_name = (rf_filename.get("1.0",END)).strip() ## not working
            print(script_name)

            if os.path.getsize(file) > 0:
                ##### put on thread #####
                dictionary_run.run(file, script_name)
            else: # is empty
                messagebox.showerror("Running Error", "Can\'t run empty scenario")

        def get_object_condition_name():

            obj_name = self.cb_obj.get().strip()

            if self.exists_clicked.get() == 0:
                obj_name = obj_name + "_exists"
            if self.exists_clicked.get() == 1:
                obj_name = obj_name + "_clicked"

            return obj_name

        def if_command():
            
            btn_else.config(state=NORMAL)
            btn_if.config(state=DISABLED)

            # self.btn_if_pressed = True

            obj_name = get_object_condition_name()

            cond = condition() + 1
            self.lb_condition_var.set(cond)
            
            insert_to_actions_list("if({})".format(obj_name))
            btn_finish_condition.config(state=NORMAL)
        

        def else_command():

            btn_if.config(state=NORMAL)
            btn_else.config(state=DISABLED)

            cond = condition() - 1
            self.lb_condition_var.set(cond)
            edit_line(last_lineindex())
            self.lb_condition_var.set(cond + 1)

            obj_name = get_object_condition_name()

            insert_to_actions_list("{}".format("else({})".format(obj_name)))
            # btn_else
            # tf_if_else
            # rb_exists
            # rb_clicked
            pass

        def last_lineindex():

            return text_actions_list.index("end-1c linestart")

        def edit_line(lineindex, text=""):

            text_actions_list.config(state=NORMAL)
            text_actions_list.delete(lineindex, END)
            insert_to_actions_list(text)
            text_actions_list.config(state=DISABLED)

        def finish_condition():

            cond = condition() - 1
            
            if cond >= 0:
                self.lb_condition_var.set(cond)

            btn_if.config(state=NORMAL)
            btn_else.config(state=DISABLED)

            edit_line(last_lineindex())

            if condition() == 0:
            	btn_finish_condition.config(state=DISABLED)

        def insert_filename_frame():

            global script_name, rf_filename 
            insert_filename = Tk()
            
            insert_filename.geometry("300x100")
            insert_filename.title("Script Name")

            Label(insert_filename, text="Scenario Script Name:").pack(side="top", fill='both', expand=True, padx=4, pady=4)
            entry_var = StringVar()
            rf_filename = Text(insert_filename, width=20,height=1)
            rf_filename.pack(side="top", fill='both', expand=True, padx=4, pady=4)
            Button(insert_filename, text='Cancel', command=insert_filename.destroy).pack(side="right", fill='both', expand=True, padx=4, pady=4)
            Button(insert_filename, text='OK', command=OK).pack(side="left", fill='both', expand=True, padx=4, pady=4)


        def run():
            save()
            insert_filename_frame()
            


        fm2 = Frame(master)
        create_menu_bar(master)

        ############ AutoDesktop ############
        autodesktop_frame = LabelFrame(fm2, labelanchor=N, text="AutoDesktop", font="Arial 25 bold italic")
        autodesktop_frame.grid(row=0, column=0, columnspan=2, sticky=E+W, ipady=5, pady=5, ipadx=10)

        ############ Scenarios Actions ############
        scenarios_actions = LabelFrame(fm2, text="Scenarios Actions", font="Arial 20 bold italic")
        scenarios_actions.grid(row=1, column=0, sticky=N+W,ipady=5, ipadx=10)

        ############ Actions List ############
        scenarios_list = LabelFrame(fm2, text="Scenarios List", font="Arial 20 bold italic")
        scenarios_list.grid(row=1, column=1, sticky=N+W, ipady=19, ipadx=10)

        ############ OS Actions ############
        os_actions = LabelFrame(scenarios_actions, text="OS", font="Arial 15 bold italic")
        os_actions.grid(row=0, column=0, sticky=N+W,pady=2, ipady=5, padx=9, ipadx=10)

        ############ Search Object Actions ############
        search_object_frame = LabelFrame(scenarios_actions, text="Search Object", font="Arial 15 bold italic")
        search_object_frame.grid(row=1, column=0,columnspan=10, sticky=N+W, pady=2, ipady=5, padx=9, ipadx=10)

        ############ UI Actions ############
        ui_actions = LabelFrame(scenarios_actions, text="UI", font="Arial 15 bold italic")
        ui_actions.grid(row=2, column=0,columnspan=10, sticky=N+W, pady=2, ipady=5, padx=9, ipadx=10)

        ############ Keyboard Actions ############
        keyboard_actions = LabelFrame(scenarios_actions, text="Keyboard", font="Arial 15 bold italic")
        keyboard_actions.grid(row=3, column=0,columnspan=10, sticky=N+W, pady=2, ipady=5, padx=9, ipadx=10)


        ## Top title btns
        save_photo = PhotoImage(file="GUI_img/save_btn_1.png")
        save_btn = ttk.Button(autodesktop_frame, image=save_photo, command=save) 
        save_btn.grid(row=0, column=0, padx=10, pady=2)
        save_btn.image = save_photo

        btn_new_scenario = ttk.Button(autodesktop_frame, width=15, text='New Scenario', command=sleep)
        btn_new_scenario.grid(row=0, column=1, padx=0, pady=2)

        btn_open_scenario = ttk.Button(autodesktop_frame, width=15, text='Open Scenarios', command=openfile)
        btn_open_scenario.grid(row=0, column=2, padx=10, pady=2)

        btn_show_all_scenarios = ttk.Button(autodesktop_frame, width=15, text='Show All Scenarios', command=sleep)
        btn_show_all_scenarios.grid(row=0, column=3, padx=0, pady=2)

        btn_self_coding = ttk.Button(autodesktop_frame, width=15, text='Self Coding', command=sleep)
        btn_self_coding.grid(row=0, column=4, padx=10, pady=2)

        ####### Sleep #######
        btn_sleep = ttk.Button(os_actions, width=15, text='Sleep', command=sleep)
        btn_sleep.grid(row=0, column=0,columnspan=2, padx=5, pady=2,sticky=W)
        Label(os_actions, text="Time:").grid(row=0, column=2, sticky=W, padx=2)
        tf_sleep = Text(os_actions, height=1, width=7)
        tf_sleep.grid(row=0, column=3, sticky=W)
        tf_sleep.insert(INSERT, "1")
        

        ####### IF/ELSE #######
        btn_if = ttk.Button(os_actions, width=6, text='If', command=if_command)
        btn_if.grid(row=1, column=0, pady=2)
        btn_else = ttk.Button(os_actions, width=6, text='Else', command=else_command)
        btn_else.grid(row=1, column=1, pady=2)
        btn_else.config(state=DISABLED)
        Label(os_actions, text="Object:").grid(row=1, column=2, sticky=W ,padx=2)

        btn_finish_condition = ttk.Button(os_actions, width=15, text='Finish Condition', command=finish_condition)
        btn_finish_condition.grid(row=2, column=0, columnspan=2 ,sticky=W, padx=5)
        btn_finish_condition.config(state=DISABLED)

        Label(os_actions, text="Condition:").grid(row=2, column=2, sticky=W, padx=2)
        self.lb_condition_var.set("0")
        lb_condition = Label(os_actions, textvariable = self.lb_condition_var).grid(row=2, column=3, sticky=W, padx=2)
        

        # self.box_value = StringVar()
        self.cb_obj = ttk.Combobox(os_actions, width=15)
        # self.box.current(0)
        self.cb_obj.grid(row=1, column=3, sticky=W)

        # tf_if_else = Text(os_actions, height=1, width=7)
        # tf_if_else.grid(row=1, column=3, sticky=W)
        # tf_if_else.insert(INSERT, "Name")

        rb_exists = Radiobutton(os_actions, width = 6, text="Exists", variable=self.exists_clicked, value=0)
        rb_clicked = Radiobutton(os_actions, width = 6, text="Clicked", variable=self.exists_clicked, value=1)
        rb_exists.grid(sticky=W, row=1, column=4)
        rb_clicked.grid(sticky=W ,row=1, column=5)

        ####### Search Object #######
        btn_search_object = ttk.Button(search_object_frame, width=15, text='Search Object', command=search_object_com)
        btn_search_object.grid(row=0, column=0, padx=5, pady=2, columnspan=2, sticky=W)

        # Path
        Label(search_object_frame, text="Path:").grid(row=1, column=0, sticky=W,padx=5)
        tf_search_object = Text(search_object_frame, height=1, width=8)
        tf_search_object.grid(row=1, column=1, sticky=W)

        # Browse
        btn_browse = ttk.Button(search_object_frame,width=3, text="...", command=get_path)  
        btn_browse.grid(row=1, column=2,columnspan=2, padx=5,sticky=W)

        rb_click_obj_R = Radiobutton(search_object_frame, width = 3, text="Left", variable=self.rlb, value=0)
        rb_click_obj_L = Radiobutton(search_object_frame, width = 5, text="Right", variable=self.rlb, value=1)
        rb_click_obj_D = Radiobutton(search_object_frame, width = 6, text="Double", variable=self.rlb, value=2)
        rb_click_obj_R.grid(sticky=W, row=1, column=3)
        rb_click_obj_L.grid(sticky=W ,row=1, column=4)
        rb_click_obj_D.grid(sticky=W ,row=1, column=5)
        search_func_disable_rld()

        # search attempts
        Label(search_object_frame,text="Attempts:").grid(row=2, column=0, sticky=W,padx=5)
        tf_search_attempts = Text(search_object_frame, height=1, width=8)
        tf_search_attempts.grid(row=2, column=1, sticky=W)
        tf_search_attempts.insert(INSERT, "3")

        # search sleep
        Label(search_object_frame, text="Sleep:").grid(row=2, column=2, sticky=W,padx=5)
        tf_search_sleep = Text(search_object_frame, height=1, width=8)
        tf_search_sleep.grid(row=2, column=3,columnspan=3, sticky=W)
        tf_search_sleep.insert(INSERT, "1")

        
        rb_click_find = Radiobutton(search_object_frame, text="Find", variable=self.search_func, value=0,command=search_func_disable_rld)
        rb_click_click = Radiobutton(search_object_frame, text="Click", variable=self.search_func, value=1,command=search_func_enable_rld)
        rb_click_getcoordinate = Radiobutton(search_object_frame, text="Coordinate", variable=self.search_func, value=2)
        rb_click_find.grid(sticky=W, row=0, column=2)
        rb_click_click.grid(sticky=W ,row=0, column=3)
        rb_click_getcoordinate.grid(sticky=W ,row=0, column=4, columnspan=2)

        ####### Move Mouse #######
        btn_move_mouse = ttk.Button(ui_actions, width = 15, text='Move Mouse', command=move_mouse_com)
        btn_move_mouse.grid(row=3, column=0, pady=2, padx=5)

        # Mouse X
        Label(ui_actions,text="X:").grid(row=3, column=1, sticky=W)
        tf_move_mouse_x = Text(ui_actions, height=1, width=7)
        tf_move_mouse_x.grid(row=3, column=2, sticky=W)
        tf_move_mouse_x.insert(INSERT, "1")

        # Mouse Y
        Label(ui_actions, text="Y:").grid(row=3, column=3, sticky=W, padx=5)
        tf_move_mouse_y = Text(ui_actions, height=1, width=7)
        tf_move_mouse_y.grid(row=3, column=4, sticky=W)
        tf_move_mouse_y.insert(INSERT, "1")

        # Mouse Speed
        Label(ui_actions, text="Speed:").grid(row=3, column=5, sticky=W, padx=5)
        tf_move_mouse_speed = Text(ui_actions, height=1, width=7)
        tf_move_mouse_speed.grid(row=3, column=6, sticky=W)
        tf_move_mouse_speed.insert(INSERT, "0")

        ####### Click #######
        btn_click = ttk.Button(ui_actions, width = 15, text='Click', command = click)
        btn_click.grid(row=4, column=0, pady=2)

        # Click Times
        Label(ui_actions, text="Times:").grid(row=4, column=1, ipadx=5)
        tf_click_time = Text(ui_actions, height=1, width=7)
        tf_click_time.insert(INSERT, "1")
        tf_click_time.grid(row=4, column=2, sticky=W)

        # Click Speed
        Label(ui_actions, text="Speed:").grid(row=4, column=3, sticky=W, padx=5)
        tf_click_speed = Text(ui_actions, height=1, width=7)
        tf_click_speed.insert(INSERT, "0")
        tf_click_speed.grid(row=4, column=4, sticky=W)

        rb_click_R = Radiobutton(ui_actions, width = 5, text="Left", variable=self.rbv, value=1)
        rb_click_L = Radiobutton(ui_actions, width = 5, text="Right", variable=self.rbv, value=0)
        rb_click_R.grid(sticky=E, row=4, column=5)
        rb_click_L.grid(sticky=W ,row=4, column=6)

        ####### Keyboard Actions Widgets ########
        ### Type Text ###
        btn_typetext = ttk.Button(keyboard_actions, width = 15, text='Type Text', command = typetext)
        btn_typetext.grid(row=0, column=0, pady=2, padx=5)

        # Type Text Times
        Label(keyboard_actions, text="Text:").grid(row=0, column=1)
        tf_typetext_text = Text(keyboard_actions, height=1, width=7)
        tf_typetext_text.insert(INSERT, "text")
        tf_typetext_text.grid(row=0, column=2, sticky=W)

        # Type Text Speed
        Label(keyboard_actions, text="Speed:").grid(row=0, column=3, sticky=W, padx=5)
        tf_typetext_speed = Text(keyboard_actions, height=1, width=7)
        tf_typetext_speed.insert(INSERT, "0")
        tf_typetext_speed.grid(row=0, column=4, sticky=W)

        ### Keyboard press ###
        btn_keypress = ttk.Button(keyboard_actions, width = 15, text='Keyboard Press', command = typetext)
        btn_keypress.grid(row=1, column=0, pady=2)

        var = 1
        cb_multipress = Checkbutton(keyboard_actions, text="MultiPress", variable=var)
        cb_multipress.grid(row=1, column=1, columnspan=2)


        
        ############ Action List ############        
        # text field
        text_actions_list = Text(master=scenarios_list, height=23, width=31)
        text_actions_list.grid(row=2, column=1,columnspan=20, pady=2 , padx=10)
        text_actions_list.insert(INSERT, "0:")

        scr = Scrollbar(scenarios_list, orient=VERTICAL, command=text_actions_list.yview)
        scr.grid(row=2, column=11, columnspan=15, sticky=N+S)
        
        text_actions_list.config(yscrollcommand=scr.set, font=('Arial', 10))
        text_actions_list.config(state=DISABLED)
        text_actions_list.bind("<Button 1>",select)

        # Clear Actions
        btn_clear_actions_list = ttk.Button(scenarios_list, width = 15, text='Clear Actions', command=clear_actions_list)
        btn_clear_actions_list.grid(row=3, column=2)

        # remove Action
        btn_remove_action = ttk.Button(scenarios_list, width = 15, text='Remove Action', command=remove_action)
        btn_remove_action.grid(row=3, column=1, padx=15,pady=5)


        ####### EXIT #######
        ttk.Button(fm2, width = 15, text='EXIT', command=self.quit).grid(row=4, column=0, pady=5)

        ####### RUN #######
        ttk.Button(fm2, width = 15, text='RUN', command=run).grid(row=4, column=1, pady=5)

        fm2.pack(anchor=CENTER, padx=10)
        root.protocol('WM_DELETE_WINDOW', self.quit)


        if disable_unsupported:
            rb_click_getcoordinate.config(state=DISABLED)
            btn_keypress.config(state=DISABLED)
            btn_new_scenario.config(state=DISABLED)
            btn_show_all_scenarios.config(state=DISABLED)
            btn_self_coding.config(state=DISABLED)
            cb_multipress.config(state=DISABLED)
            # btn_if.config(state=DISABLED)
            # btn_else.config(state=DISABLED)
            # rb_exists.config(state=DISABLED)
            # rb_clicked.config(state=DISABLED)



list_TF = []

root = Tk()
root.geometry("1100x720")
root.title("AutoDesktop Demo")
app = Application(root)
root.mainloop()
root.destroy()