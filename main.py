#below are all the modules i imported to make my code
import time
from tkinter import *
import tkinter as tk
from tkinter import ANCHOR, Frame, Menu
import customtkinter as ctk
import tkinter.font as font
from PIL import Image, ImageTk
import random
from multiprocessing.sharedctypes import Value
import os
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
from statistics import mean
#module below allows arguments in widget commands to be written easier
from functools import partial
print("started program")
import sys

#the line below sets the theme and appearance of the program from the config file
with open("config.txt", "r+") as f:
    file_lines = f.readlines()
    no_n = file_lines[0][:len(file_lines[0])-1]     #removes the "\n" in string
    theme = no_n
    no_n = file_lines[1][:len(file_lines[1])-1]
    appearance = no_n
    print(theme, appearance+":")


#default starting parameters
app = ctk.CTk()
app.title("Reaction Game")
app.attributes('-fullscreen',True)

ctk.set_appearance_mode(appearance)
ctk.set_default_color_theme(theme)
myFont_small = font.Font(family='8514oem', size=20)
myFont_big = font.Font(family='8514oem', size=50)

#these variables store the value for the dimensions of the host monitor's screen
rw = app.winfo_screenwidth()
rh = app.winfo_screenheight()

accel = False

average_time = []

#multiple functions - this function lets the program run multiple functions by calling one function only
def multi_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

#image edits
def image_edit(x, dir="images/race lights/", t=True):
    img = Image.open(dir+x+".png")
    if t:
        wid=round(0.17*rh)
        hei=round(0.17*rh)
        img = img.resize((wid,hei), Image.ANTIALIAS)    #resizing + antialiasing
        w, h = img.size    #cropping
        left = round(0.376*hei)                                           #creates a for loop which does this process to all images
        right = round(0.624*hei)
        upper = round(0.38*hei)
        lower = round(0.62*hei)
        img = img.crop([left, upper, right, lower])
    img = ImageTk.PhotoImage(img)
    return img

total_time = ""
#convert time
def time_convert(sec):
    global accel
    accel = False
    print("accel=False")
    global total_time
    mins = sec // 60
    sec = f'{(sec%60):>0.3f}'        #sec = round((sec % 60), 3)
    mins = mins % 60
    print("Time Lapsed = {0}s".format(sec))
    total_time = ("{0}".format(sec))
    data.taken.set(total_time)

    change_frame(test_frame, data_frame)
    return total_time

#highscores - this function saves the highscore to a text file
def highscore_entry(name, age, total):
    with open(("highscores.txt"),"a+") as f:
        if name == "":
            name = "anonymous"
        if age == "":
            age = 0
        
        entry= None
        entry ={"name":name, "age":int(age), "time":float(total)}
        print(name, age, total)
        f.write(str(entry)+"\n")   #the data is written as a dictionary in string formation.

#submit data
def submit():
    name=data.name_var.get()
    age=data.age_var.get()
    ttl_time = data.taken.get()      #this function formats the name and age submission.
    print("Name: " + name)
    print("Age: " + age)
    highscore_entry(name, age, ttl_time)
    data.name_var.set("")
    data.age_var.set("")
    change_frame(data_frame, menu_frame)

#reading highscores
def read_highscores():
    my_dicts = []
    try:
        with open("highscores.txt","r+") as f:
            pos = highscores.positions             #pos is a variable which is for each position of the labels
            var = highscores.vars                  #var is the variable which stores the time value for the labels
            data = f.readlines()
            for i in range(len(data)):
                data_line=data[i]
                data_line = data_line.strip()
                data_line = eval(data_line)
                my_dicts.append(data_line)

            sorted_dicts = sorted(my_dicts, key=lambda data_line: data_line['time'])
            #Print the sorted dictionaries
            l = 0
            try:
                converted = ""
                for d in sorted_dicts:
                    print(d)
                    for key in d:
                        if key == "name":
                            if l != 9:
                                converted += " "+str(l+1)+"| "+key + ": " + str(d[key][:10])+ "   \t\t"
                            else:
                                converted += str(l+1)+"| "+key + ": " + str(d[key])+ "   \t\t"
                        elif key == "time":
                            stuff = format(float(d[key]), '.3f')
                            converted += key + ": " + str(stuff)+ "\t\t"
                        elif key == "age":
                            converted += key + ": " + str(d[key])+ "   \t\t"
                            
                    var[l].set(converted)
                    l+=1
                    converted = ""
            except IndexError:
                pass
    except FileNotFoundError:
        with open("highscores.txt", "x") as f:
            pass

#analysing data - this function sorts the highscores based on the time key in each dictionary
def analysis(choice):
    analyse.details.delete(0,END)
    my_dicts = []
    ages = []
    with open("highscores.txt","r+") as f:
        data = f.readlines()
        for i in range(len(data)):
            x=data[i]
            x = x.strip()
            x = eval(x)
            my_dicts.append(x)
        sorted_dicts = sorted(my_dicts, key=lambda x: x['time'])

    l = 0
    for d in sorted_dicts:
        space = "    "
        if d["age"] == int(choice):
            print(d["age"])
            try:
                converted = ""
                
                for key in d:
                    if key == "name":
                        if l <9:
                            
                            converted += " " + str(l+1)+"| "+key + ": " + str(d[key][:10].rjust(10))+ f"{space:>2}"
                        else:
                            converted += str(l+1)+"| "+key + ": " + str(d[key].rjust(10))+ f"{space:>2}"
                    elif key == "time":
                        stuff = format(float(d[key]), '.3f')
                        converted += key + ": " + str(stuff)+ f"{space:>2}"
                    elif key == "age":
                        converted += key + ": " + str(d[key])+ f"{space:>2}"
                
                l+=1
                analyse.details.insert(END, converted)
                converted = ""
            except IndexError:
                pass

#reset highscores
def reset():
    print("reset")
    # open both files
    with open("highscores.txt",'r') as firstfile, open("old_highscores.txt",'a') as secondfile:
        # read content from first file
        for line in firstfile:
                # append content to second file
                secondfile.write(line)
    with open("highscores.txt",'w') as f:
        pass
#colour change
def theme_change(choice):
    global theme, appearance
    ctk.set_default_color_theme(choice)
    with open("config.txt","r") as f:
        data = f.readlines()
    data[0]=choice+"\n"
    with open("config.txt", "w") as f:
        f.writelines(data)
    print(choice)
    os.startfile(sys.argv[0])
    sys.exit()

#appearance change
def appearance_change(choice):
    global theme, appearance
    ctk.set_appearance_mode(choice)
    with open("config.txt","r") as f:
        data = f.readlines()
    data[1]=choice+"\n"
    with open("config.txt", "w") as f:
        f.writelines(data)
    print(choice)

shuffle = True
stop = False
#light shuffle
def light_shuffle(lst, col, count=0):
    global stop
    if stop != True:
        num = len(lst)
        global shuffle
        light_green = image_edit("green")
        light_grey = image_edit("grey")
        light_blank = image_edit("default")
        light_red = image_edit("red") 
        if count != len(lst) and shuffle==True:
            light = lst[len(lst)-count-1]
            light.config(image = col)
            light.image = col
            app.after(1000, partial(light_shuffle, lst, light_grey, count+1))
            if count == len(lst)-1:
                shuffle=False
        elif shuffle==False:
            print(num-count, shuffle)
            if count==-1:
                shuffle=True
                light_shuffle(play.red_lights, light_grey, 0)
            else:
                light = lst[len(lst)-count-1]
                light.config(image = col)
                light.image = col
                app.after(1000, partial(light_shuffle, lst, light_red, count-1))
    else:
        return

#extinguished
def greyed():
    global start_time, accel
    light_grey = image_edit("grey")
    for i in range(len(test.red_lights)):
                    light=test.red_lights[i]
                    light.config(image = light_grey)
                    light.image = light_grey
    for i in range(len(test.mid_red_lights)):
        light=test.mid_red_lights[i]
        light.config(image = light_grey)
        light.image = light_grey
    print("lights extinguished")
    accel = True
    print("accel=True")
    start_time = time.time()
    print("time started")
    
race_end = False
pre_race = 1
#race sequence - this function initiates and controls the sequence of the lights turning green/grey/red
def race_sequence(lst1, lst2, count=0):
    global race_end, pre_race, accel
    accel = False
    print("accel=False")
    light_green = image_edit("green")
    light_grey = image_edit("grey")
    light_blank = image_edit("default")
    light_red = image_edit("red")
    if race_end != True:
        if pre_race == 1:
            print("pre_race = 1")
            for i in range(len(test.red_lights)):
                light=test.red_lights[i]
                light.config(image = light_red)
                light.image = light_red
            for i in range(len(test.mid_red_lights)):
                light=test.mid_red_lights[i]
                light.config(image = light_red)
                light.image = light_red
            for i in range(len(test.green_lights)):
                light=test.green_lights[i]
                light.config(image = light_green)
                light.image = light_green
            pre_race = 2
            app.after(500, partial(race_sequence, lst1, lst2))

        elif pre_race == 2:
            print("pre_race = 3")
            for i in range(len(test.red_lights)):
                    light=test.red_lights[i]
                    light.config(image = light_grey)
                    light.image = light_grey
            for i in range(len(test.mid_red_lights)):
                light=test.mid_red_lights[i]
                light.config(image = light_grey)
                light.image = light_grey
            for i in range(len(test.green_lights)):
                light=test.green_lights[i]
                light.config(image = light_grey)
                light.image = light_grey
            pre_race = 3
            app.after(0000, partial(race_sequence, lst1, lst2))

        elif pre_race==3:
            if count != len(lst1):
                light = lst1[len(lst1)-count-1]
                y = lst2[len(lst2)-count-1]
                light.config(image = light_red)
                y.config(image = light_red)
                light.image = light_red
                y.image = light_red
                if count != len(lst1):
                    app.after(1000, partial(race_sequence, lst1, lst2, count+1))
            else:                                       #MAKE RACE LIGHTS EXTINGUISH
                rand = round(random.uniform(0.2, 3.0), 3)*1000
                #image change
                app.after(int(rand), greyed)
                record_time(True)
                
                return

    else:
        print("ended")
        return


#change frame
def change_frame(x, y):    #x is the previous frame, y is the frame which is going to be called
    global stop, shuffle, race_end, pre_race
    x.forget()
    y.pack(fill='both', expand=1)
    stop = True
    for i in range(len(play.red_lights)):
            light=play.red_lights[i]
            light.config(image = light_red)
            light.image = light_red
    if y == play_frame:
        stop = False
        shuffle = True
        for i in range(len(play.red_lights)):
            light=play.red_lights[i]
            light.config(image = light_red)
            light.image = light_red
        light_shuffle(play.red_lights, light_grey, 0)

    elif y == test_frame:
        Stop = True
        pre_race=1
        race_end=False
        race_sequence(test.red_lights, test.mid_red_lights)
    elif y == analyse_frame:
        analysis(choice=0)
        analyse.options.set("Select Age")
    elif y == settings_frame:
        with open("config.txt", "r+") as f:
            data = f.readlines()
            e = data[0][:len(data[0])-1]
            Settings.themes.set(e)   
            r = data[1][:len(data[1])-1]
            Settings.appearances.set(r)
            print(e, r)
        
    return

num = 3
average_time = []
#record time
def record_time(recording=True):
    global start_time, race_end, accel, num, average_time

    if recording != True:
        end_time = time.time()
        print("time ended")
        
        try:
            time_lapsed = end_time - start_time
            if accel == False:
                print("cannot press button before lights go out")
                race_end=True
                average_time=[]
                num=3
                change_frame(test_frame, fail_frame)
            else:
                if num > 0:
                    average_time.append(time_lapsed)
                    print(average_time)
                    num -=1
                    change_frame(test_frame, test_frame)
                    print(num)
                elif num == 0:
                    num = 3
                    print("back to num = 3")
                    average_time.append(time_lapsed)
                    print(average_time)
                    time_lapsed = mean(average_time)
                    print(time_lapsed)
                    time_lapsed = round(time_lapsed, 3)
                    time_convert(time_lapsed)
                    average_time=[]
            
        except NameError or UnboundLocalError:   
            print("cannot press button before lights go out, Error")
            race_end=True
            average_time=[]
            num=3
            change_frame(test_frame, fail_frame)    #CREATE PART WHERE IF REACT BUTTON PRESSED BEFORE LIGHTS EXTINGUISH; THE TEST FAILS
        return
    return

#frames
launch_game_frame = ctk.CTkFrame(app)
menu_frame = ctk.CTkFrame(app)
settings_frame = ctk.CTkFrame(app)
highscores_frame = ctk.CTkFrame(app)
about_frame = ctk.CTkFrame(app)
analyse_frame = ctk.CTkFrame(app)
play_frame = ctk.CTkFrame(app)
test_frame = ctk.CTkFrame(app)
fail_frame = ctk.CTkFrame(app)
data_frame = ctk.CTkFrame(app)

#images
light_red = image_edit("red")
light_green = image_edit("green")
light_grey = image_edit("grey")
light_blank = image_edit("default")

background = "#2a2d2e"

#*************************#BUTTONS REQUIRE 20 SYMBOLS. if you cannot use letters, use spaces to fill in to make 20 digits, symbols...#

#launch_game_frame - done
class launch_game:
    launch_game_button = ctk.CTkButton(launch_game_frame, text="Press to Run Test", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, launch_game_frame, menu_frame))
    launch_game_button.place(anchor=tk.CENTER, relx=0.5, rely=0.7, width=425)
    logo = ctk.CTkLabel(launch_game_frame, text="F1", fg="#FF0000", text_font=font.Font(family='8514oem', size=50)).place(anchor=tk.CENTER, relx=0.5,rely=0.1, width=500)
    launch_game_title = ctk.CTkLabel(launch_game_frame, text="Reaction Test", text_font=font.Font(family='8514oem', size=50), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.5, rely=0.2)

#highscores_frame - done
class highscores:
    back_button = ctk.CTkButton(highscores_frame, text="Back", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, highscores_frame, menu_frame))
    back_button.place(anchor=tk.E, relx=0.95, rely=0.8, width=425)
    analyse_button = ctk.CTkButton(highscores_frame, text="Analyse", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, highscores_frame, analyse_frame))
    analyse_button.place(anchor=tk.W, relx=0.05, rely=0.8, width=425)
    highscores_title = ctk.CTkLabel(highscores_frame, text = "Highscores", text_font=font.Font(family='8514oem', size=50))
    highscores_title.place(anchor=tk.CENTER, relx= 0.5, rely=0.1)
    inf = ctk.CTkLabel(highscores_frame, text = "If the area below is blank, there are no highscores set yet.", text_font=font.Font(family='8514oem', size=15))
    inf.place(anchor=tk.CENTER, relx=0.5, rely=0.15)
    var1 = tk.StringVar()
    var2 = tk.StringVar()
    var3 = tk.StringVar()
    var4 = tk.StringVar()
    var5 = tk.StringVar()
    var6 = tk.StringVar()
    var7 = tk.StringVar()
    var8 = tk.StringVar()
    var9 = tk.StringVar()
    var10 = tk.StringVar()
    pos1 = ctk.CTkLabel(highscores_frame, textvariable=var1, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.25)
    pos2 = ctk.CTkLabel(highscores_frame, textvariable=var2, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.3)
    pos3 = ctk.CTkLabel(highscores_frame, textvariable=var3, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.35)
    pos4 = ctk.CTkLabel(highscores_frame, textvariable=var4, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.4)
    pos5 = ctk.CTkLabel(highscores_frame, textvariable=var5, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.45)
    pos6 = ctk.CTkLabel(highscores_frame, textvariable=var6, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.5)
    pos7 = ctk.CTkLabel(highscores_frame, textvariable=var7, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.55)
    pos8 = ctk.CTkLabel(highscores_frame, textvariable=var8, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.6)
    pos9 = ctk.CTkLabel(highscores_frame, textvariable=var9, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.65)
    pos10 = ctk.CTkLabel(highscores_frame, textvariable=var10, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.W, relx= 0.05, rely=0.7)
    positions = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, pos10]
    vars = [var1, var2, var3, var4, var5, var6, var7, var8, var9, var10]

#fail_frame - done
class fail:
    play_title = ctk.CTkLabel(fail_frame, text="Test Failed", text_font=font.Font(family='8514oem', size=50), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.5, rely=0.2)
    back_button = ctk.CTkButton(fail_frame, text="Back", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, fail_frame, menu_frame)).place(anchor=tk.CENTER, relx=0.5, rely=0.7, width=425)
    info = ctk.CTkLabel(fail_frame, text="Reason: You pressed \"React!\" button before all the lights become grey.", text_font=font.Font(family='8514oem', size=20), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.5, rely=0.5)

#play_frame - done
class play:
    logo = ctk.CTkLabel(play_frame, text="F1", fg="#FF0000", text_font=font.Font(family='8514oem', size=50)).place(anchor=tk.CENTER, relx=0.5,rely=0.1, width=500)
    play_title = ctk.CTkLabel(play_frame, text="Reaction Test", text_font=font.Font(family='8514oem', size=50), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.5, rely=0.2)
    start_button = ctk.CTkButton(play_frame, text="Start Test", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, play_frame, test_frame)).place(anchor=tk.CENTER, relx=0.5, rely=0.7, width=425)
    back_button = ctk.CTkButton(play_frame, text="Back", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, play_frame, menu_frame)).place(anchor=tk.CENTER, relx=0.5, rely=0.85, width=425)
    info = ctk.CTkLabel(play_frame, text="After starting the test, when all the lights become grey, click the button \"React!\".\nThe test will repeat 4 times, meaning that your highscore is your average reaction time.", text_font=font.Font(family='8514oem', size=20), fg="#FFFFFF", bg="#2a2d2e")
    info.place(anchor=tk.CENTER, relx=0.5, rely=0.8)

    light_red = image_edit("red")
    light_green = image_edit("green")
    light_grey = image_edit("grey")
    light_blank = image_edit("default")
    #top green
    lbl_green1 = tk.Label(play_frame, image = light_green, borderwidth=0, bg=background)
    lbl_green1.place(anchor=tk.CENTER, x=0.450*rw, y=0.374*rh)
    lbl_green2 = tk.Label(play_frame, image = light_green, borderwidth=0, bg=background)
    lbl_green2.place(anchor=tk.CENTER, x=0.475*rw, y=0.374*rh)
    lbl_green3 = tk.Label(play_frame, image = light_green, borderwidth=0, bg=background)
    lbl_green3.place(anchor=tk.CENTER, x=0.500*rw, y=0.374*rh)
    lbl_green4 = tk.Label(play_frame, image = light_green, borderwidth=0, bg=background)
    lbl_green4.place(anchor=tk.CENTER, x=0.525*rw, y=0.374*rh)
    lbl_green5 = tk.Label(play_frame, image = light_green, borderwidth=0, bg=background)
    lbl_green5.place(anchor=tk.CENTER, x=0.550*rw, y=0.374*rh)
    #middle grey
    lbl_grey1 = tk.Label(play_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey1.place(anchor=tk.CENTER, x=0.450*rw, y=0.416*rh)
    lbl_grey2 = tk.Label(play_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey2.place(anchor=tk.CENTER, x=0.475*rw, y=0.416*rh)
    lbl_grey3 = tk.Label(play_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey3.place(anchor=tk.CENTER, x=0.500*rw, y=0.416*rh)
    lbl_grey4 = tk.Label(play_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey4.place(anchor=tk.CENTER, x=0.525*rw, y=0.416*rh)
    lbl_grey5 = tk.Label(play_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey5.place(anchor=tk.CENTER, x=0.550*rw, y=0.416*rh)
    #middle red
    lbl_red12 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red12.place(anchor=tk.CENTER, x=0.450*rw, y=0.458*rh)
    lbl_red22 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red22.place(anchor=tk.CENTER, x=0.475*rw, y=0.458*rh)
    lbl_red32 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red32.place(anchor=tk.CENTER, x=0.500*rw, y=0.458*rh)
    lbl_red42 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red42.place(anchor=tk.CENTER, x=0.525*rw, y=0.458*rh)
    lbl_red52 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red52.place(anchor=tk.CENTER, x=0.550*rw, y=0.458*rh)
    #lowest red
    lbl_red1 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red1.place(anchor=tk.CENTER, x=0.450*rw, y=0.5*rh)
    lbl_red2 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red2.place(anchor=tk.CENTER, x=0.475*rw, y=0.5*rh)
    lbl_red3 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red3.place(anchor=tk.CENTER, x=0.500*rw, y=0.5*rh)   
    lbl_red4 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red4.place(anchor=tk.CENTER, x=0.525*rw, y=0.5*rh)  
    lbl_red5 = tk.Label(play_frame, image = light_red, borderwidth=0, bg=background)
    lbl_red5.place(anchor=tk.CENTER, x=0.550*rw, y=0.5*rh)
    green_lights = [lbl_green1, lbl_green2, lbl_green3, lbl_green4, lbl_green5]
    grey_lights = [lbl_grey1, lbl_grey2, lbl_grey3, lbl_grey4, lbl_grey5]
    red_lights = [lbl_red1, lbl_red2, lbl_red3, lbl_red4, lbl_red5]
    mid_red_lights = [lbl_red12, lbl_red22, lbl_red32, lbl_red42, lbl_red52]

#data_frame - done
class data:
    taken = tk.StringVar()
    taken.set("")
    data_title = ctk.CTkLabel(data_frame, text="Highscore Entry", text_font=font.Font(family='8514oem', size=50), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.5, rely=0.2)

    name_var = tk.StringVar()
    name_label = ctk.CTkLabel(data_frame, text="Enter Name: ", text_font=font.Font(family='8514oem', size=20), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.2, rely=0.4)
    name_entry = ctk.CTkEntry(data_frame, textvariable=name_var, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.CENTER, relx=0.2, rely=0.45, width=425)
    
    age_var = tk.StringVar()
    age_label = ctk.CTkLabel(data_frame, text="Enter Age(Int): ", text_font=font.Font(family='8514oem', size=20), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.8, rely=0.4)
    age_entry = ctk.CTkEntry(data_frame, textvariable=age_var, text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.CENTER, relx=0.8, rely=0.45, width=425)

    time_taken = ctk.CTkLabel(data_frame, textvariable=taken, text_font=font.Font(family='8514oem', size=20), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.5, rely=0.5)
    submit_button = ctk.CTkButton(data_frame, text="Submit", text_font=font.Font(family='8514oem', size=20), command=partial(submit)).place(anchor=tk.CENTER, relx=0.5, rely=0.8, width=425)
    cancel_button = ctk.CTkButton(data_frame, text="Cancel", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, data_frame, menu_frame)).place(anchor=tk.CENTER, relx=0.5, rely=0.9, width=425)

#test_frame - done
class test:
    logo = ctk.CTkLabel(test_frame, text="F1", fg="#FF0000", text_font=font.Font(family='8514oem', size=50)).place(anchor=tk.CENTER, relx=0.5,rely=0.1, width=500)
    play_title = ctk.CTkLabel(test_frame, text="Reaction Test", text_font=font.Font(family='8514oem', size=50), fg="#FFFFFF", bg="#2a2d2e").place(anchor=tk.CENTER, relx=0.5, rely=0.2)
    react_button = ctk.CTkButton(test_frame, text="React!", text_font=font.Font(family='8514oem', size=20), command=partial(record_time, False))
    react_button.place(anchor=tk.CENTER, relx=0.5, rely=0.7, width=425)

    light_red = image_edit("red")
    light_green = image_edit("green")
    light_grey = image_edit("grey")
    light_blank = image_edit("default")
    #top green
    lbl_green1 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_green1.place(anchor=tk.CENTER, x=0.450*rw, y=0.374*rh)
    lbl_green2 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_green2.place(anchor=tk.CENTER, x=0.475*rw, y=0.374*rh)
    lbl_green3 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_green3.place(anchor=tk.CENTER, x=0.500*rw, y=0.374*rh)
    lbl_green4 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_green4.place(anchor=tk.CENTER, x=0.525*rw, y=0.374*rh)
    lbl_green5 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_green5.place(anchor=tk.CENTER, x=0.550*rw, y=0.374*rh)
    #middle grey
    lbl_grey1 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey1.place(anchor=tk.CENTER, x=0.450*rw, y=0.416*rh)
    lbl_grey2 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey2.place(anchor=tk.CENTER, x=0.475*rw, y=0.416*rh)
    lbl_grey3 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey3.place(anchor=tk.CENTER, x=0.500*rw, y=0.416*rh)
    lbl_grey4 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey4.place(anchor=tk.CENTER, x=0.525*rw, y=0.416*rh)
    lbl_grey5 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_grey5.place(anchor=tk.CENTER, x=0.550*rw, y=0.416*rh)
    #middle red
    lbl_red12 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red12.place(anchor=tk.CENTER, x=0.450*rw, y=0.458*rh)
    lbl_red22 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red22.place(anchor=tk.CENTER, x=0.475*rw, y=0.458*rh)
    lbl_red32 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red32.place(anchor=tk.CENTER, x=0.500*rw, y=0.458*rh)
    lbl_red42 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red42.place(anchor=tk.CENTER, x=0.525*rw, y=0.458*rh)
    lbl_red52 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red52.place(anchor=tk.CENTER, x=0.550*rw, y=0.458*rh)
    #lowest red
    lbl_red1 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red1.place(anchor=tk.CENTER, x=0.450*rw, y=0.5*rh)
    lbl_red2 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red2.place(anchor=tk.CENTER, x=0.475*rw, y=0.5*rh)
    lbl_red3 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red3.place(anchor=tk.CENTER, x=0.500*rw, y=0.5*rh)   
    lbl_red4 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red4.place(anchor=tk.CENTER, x=0.525*rw, y=0.5*rh)  
    lbl_red5 = tk.Label(test_frame, image = light_grey, borderwidth=0, bg=background)
    lbl_red5.place(anchor=tk.CENTER, x=0.550*rw, y=0.5*rh)
    green_lights = [lbl_green1, lbl_green2, lbl_green3, lbl_green4, lbl_green5]
    grey_lights = [lbl_grey1, lbl_grey2, lbl_grey3, lbl_grey4, lbl_grey5]
    red_lights = [lbl_red1, lbl_red2, lbl_red3, lbl_red4, lbl_red5]
    mid_red_lights = [lbl_red12, lbl_red22, lbl_red32, lbl_red42, lbl_red52]

#analyse_frame - done
class analyse:
    back_button = ctk.CTkButton(analyse_frame, text="Back", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, analyse_frame, highscores_frame))
    back_button.place(anchor=tk.W, relx=0.05, rely=0.8, width=425)
    analyse_title = ctk.CTkLabel(analyse_frame, text = "Analysis", text_font=font.Font(family='8514oem', size=50))
    analyse_title.place(anchor=tk.CENTER, relx= 0.5, rely=0.1)

    details = tk.Listbox(analyse_frame, font = font.Font(family='8514oem', size=20),activestyle="none", relief="flat", bg="#2a2d2e", bd=2, fg="white", selectmode=tk.EXTENDED, highlightthickness=0)
    details.place(anchor=tk.N, relx=0.3, rely=0.2, width=rw/2.5)   
    yscrollbar = ctk.CTkScrollbar(analyse_frame, bg="#2a2d2e", border_spacing=0, command=details.yview, corner_radius=2)
    yscrollbar.place(anchor=tk.N, relx=0.51, rely=0.2, height=details.winfo_height())
    details.config(yscrollcommand=yscrollbar.set)
    xscrollbar = ctk.CTkScrollbar(analyse_frame, orientation="horizontal", bg="#2a2d2e", border_spacing=0, command=details.xview, corner_radius=2)
    xscrollbar.place(anchor=tk.N, relx=0.3, rely=0.6, width=details.winfo_width())
    details.config(xscrollcommand=xscrollbar.set)

    info = ctk.CTkLabel(analyse_frame, text = "Select Age (12 - 18)", text_font=font.Font(family='8514oem', size=20)).place(anchor=tk.E, relx=0.79, rely=0.2)
    
    options = ctk.CTkComboBox(analyse_frame, values=["12", "13", "14", "15", "16", "17", "18"], text_font=font.Font(family='8514oem'), command=analysis)
    options.place(anchor=tk.E, relx=0.75, rely=0.25)

#settings_frame - done
class Settings:
    back_button = ctk.CTkButton(settings_frame, text="Back", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, settings_frame, menu_frame))
    back_button.place(anchor=tk.W, relx=0.05, rely=0.8, width=425)
    highscores_title = ctk.CTkLabel(settings_frame, text = "Settings", text_font=font.Font(family='8514oem', size=50))
    highscores_title.place(anchor=tk.CENTER, relx= 0.5, rely=0.1)

    reset = ctk.CTkButton(settings_frame, text="Reset Highscores", text_font=font.Font(family='8514oem', size=15), command=partial(reset))
    reset.place(anchor=tk.CENTER, relx=0.5, rely=0.8, width=215)
    reset_info =  ctk.CTkLabel(settings_frame, text = "|Creates a new highscores file, old file is still preserved in directory|", text_font=font.Font(family='8514oem', size=15))
    reset_info.place(anchor=tk.CENTER, relx= 0.5, rely=0.85)
    
    theme_info =  ctk.CTkLabel(settings_frame, text = "Theme", text_font=font.Font(family='8514oem', size=20))
    theme_info.place(anchor=tk.CENTER, relx= 0.5, rely=0.25)
    themes = ctk.CTkComboBox(settings_frame, values=["blue", "green", "dark-blue", "sweetkind"], text_font=font.Font(family='8514oem'), command=theme_change)
    themes.place(anchor=tk.CENTER, relx= 0.5, rely=0.3)

    appearance_info =  ctk.CTkLabel(settings_frame, text = "Appearance", text_font=font.Font(family='8514oem', size=20))
    appearance_info.place(anchor=tk.CENTER, relx= 0.5, rely=0.45)
    appearances = ctk.CTkComboBox(settings_frame, values=["system", "light", "dark"], text_font=font.Font(family='8514oem'), command=appearance_change)
    appearances.place(anchor=tk.CENTER, relx= 0.5, rely=0.5)

#about_frame - done
class about:
    about_title = ctk.CTkLabel(about_frame, text = "About", text_font=font.Font(family='8514oem', size=50))
    about_title.place(anchor=tk.CENTER, relx= 0.5, rely=0.1)
    back_button = ctk.CTkButton(about_frame, text="Back", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, about_frame, menu_frame))
    back_button.place(anchor=tk.CENTER, relx=0.5, rely=0.9, width=425)
    made_by = ctk.CTkLabel(about_frame, text = "Created By Aneesh Modi, 2022", text_font=font.Font(family='8514oem', size=20))
    made_by.place(anchor=tk.CENTER, relx= 0.5, rely=0.15)
    variation = ctk.CTkLabel(about_frame, text = "The race light sequence which initiates the race is a slight variation\nfor those who dont understand the official race light sequence.", text_font=font.Font(family='8514oem', size=20))
    variation.place(anchor=tk.CENTER, relx= 0.5, rely=0.21)
    how = ctk.CTkLabel(about_frame, text = "How To Play", text_font=font.Font(family='8514oem', size=30))
    how.place(anchor=tk.CENTER, relx= 0.5, rely=0.3)
    how_to_play = ctk.CTkLabel(about_frame, text = "After running the game, click on the button which says \"play\".\nClick the button which says \"start test\".\nWhen all the race lights on screen are grey, click the button which says \"React!\".\n Follow the rest of the steps on screen to record your reaction time.\n\n\nDon't forget that the test repeats itself 4 times to\nrecord your AVERAGE reaction time as your highscore.", text_font=font.Font(family='8514oem', size=20))
    how_to_play.place(anchor=tk.CENTER, relx= 0.5, rely=0.5)

#menu_frame - done
class menu:
    game_name_label = ctk.CTkLabel(menu_frame, text="Reaction Test", text_font=font.Font(family='8514oem', size=50)).place(anchor=tk.CENTER, relx=0.5,rely=0.2)
    playgame_menu_button = ctk.CTkButton(menu_frame, text="Play", text_font=font.Font(family='8514oem', size=20), command=multi_funcs(partial(change_frame, menu_frame, play_frame))) #, partial(light_shuffle, play.red_lights), partial(light_shuffle, play.mid_red_lights)
    playgame_menu_button.place(anchor=tk.CENTER, relx=0.5, rely=0.7, width=425)
    highscores_menu_button = ctk.CTkButton(menu_frame, text="Highscores", text_font=font.Font(family='8514oem', size=20), command=multi_funcs(partial(read_highscores), partial(change_frame, menu_frame, highscores_frame)))
    highscores_menu_button.place(anchor=tk.E, relx=0.95, rely=0.8, width=425)
    settings_menu_button = ctk.CTkButton(menu_frame, text="Settings", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, menu_frame, settings_frame))
    settings_menu_button.place(anchor=tk.W, relx=0.05, rely=0.8, width=425)
    quit_menu_button = ctk.CTkButton(menu_frame, text="Quit", text_font=font.Font(family='8514oem', size=20), command=quit)
    quit_menu_button.place(anchor=tk.CENTER, relx=0.5, rely=0.8, width=425)
    about_button = ctk.CTkButton(menu_frame, text="About", text_font=font.Font(family='8514oem', size=20), command=partial(change_frame, menu_frame, about_frame))
    about_button.place(anchor=tk.CENTER, relx=0.5, rely=0.9, width=425)
    logo = ctk.CTkLabel(menu_frame, text="F1", fg="#FF0000", text_font=font.Font(family='8514oem', size=50)).place(anchor=tk.CENTER, relx=0.5,rely=0.1)

#start of app
launch_game_frame.pack(fill='both', expand=1)

app.mainloop()
