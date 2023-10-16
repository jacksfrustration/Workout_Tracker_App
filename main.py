from tkinter import *
from tkinter import messagebox
import json
from datetime import datetime
import calendar as cal

cur_row=1
count=1


def display_act():
    '''makes a string of all activities within a specific date. uses messagebox to display each day as it is iterated through'''
    try:
        with open("saved_data.json","r")as file:
            data=json.load(file)
    except json.decoder.JSONDecodeError:
        data={}
        messagebox.showerror(title="Ooooops",message=f"There is no saved data to display")
    finally:
        data_str=""
        for key in data:
            for i,act in enumerate(data[key]['activity']):
                data_str+=f"On {key} you did {data[key]['activity'][i].lower()} for {data[key]['unit'][i]} minutes.\n"
            messagebox.showinfo(title=f"{key} Workout Information",message=f"{data_str}")
            data_str=""



def all_dates_current_month():
    '''generates a list of all days inside the current month and returns it.
    The dates are presented in a spcific format ("day name","date","month" and  "year")'''
    year, month, *_ = datetime.today().timetuple()
    dates = [dt.strftime('%a %d %B %Y') for dt in cal.Calendar().itermonthdates(year, month) if dt.month == month]
    return dates

def add_col():
    '''generates a column of entries and labels
    names of each entry and label are created dynamically
    and each widget has a location added. Tkinter "rows" are incremented so each time this function is called
    the next column of widgets gets generated below the previous'''
    global cur_row,count,updated_list
    cur_row+=1

    globals()[f'day_lbl{count}'] = Label(text="On")
    globals()[f"day_lbl{count}"].grid(row=cur_row, column=0)
    globals()[f"day_value_inside{count}"] = StringVar(window, value=day_value_inside0.get())
    globals()[f"day_opt{count}"] = OptionMenu(window, globals()[f"day_value_inside{count}"], updated_list[0], updated_list[1], updated_list[2], updated_list[3], updated_list[4])
    globals()[f"day_opt{count}"].grid(row=cur_row, column=1)

    globals()[f'lbl{count}']=Label(text="I did")
    globals()[f"lbl{count}"].grid(row=cur_row,column=2)
    globals()[f"act_value_inside{count}"]=StringVar(window,value="Aerobics")
    globals()[f"act_opt{count}"]=OptionMenu(window,globals()[f"act_value_inside{count}"],"Aerobics","Cycling","Running","Swimming","Walking")
    globals()[f"act_opt{count}"].grid(row=cur_row,column=3)
    globals()[f"unit_lbl{count}"]=Label(text="for: ")
    globals()[f"unit_lbl{count}"].grid(row=cur_row,column=4)

    globals()[f"unit_ent{count}"]=Entry()
    globals()[f"unit_ent{count}"].grid(row=cur_row,column=5)
    globals()[f"min_lbl{count}"]=Label(text="minutes")
    globals()[f"min_lbl{count}"].grid(row=cur_row,column=6)
    count+=1

def reg_act():
    '''saves dates of workout, activities and duration in a dictionary setting and later saves these in a json file'''
    global count
    try:
        with open("saved_data.json","r")as file:
            saved_data=json.load(file)
    except FileNotFoundError:
        saved_data={}
        with open("saved_data.json","w") as file:
            json.dump(saved_data,file)
    except json.decoder.JSONDecodeError:
        saved_data={}
    finally:

        for i in range(0,count):
            day=globals()[f"day_value_inside{i}"].get()
            activity=globals()[f"act_value_inside{i}"].get().title()
            try:
                unit=round(float(globals()[f"unit_ent{i}"].get()))
            except ValueError:
                messagebox.showerror(title="Oooops", message="You have not entered duration information")
            else:
                if messagebox.askokcancel(title=f"{day} Workout Information",
                                          message=f"Activity: {activity} for {unit} minutes.\nSave this activity?"):
                    if day in saved_data:
                        saved_data[day]["activity"].append(activity)
                        saved_data[day]["unit"].append(unit)
                    else:

                        new_data = {day: {"activity": [activity], "unit": [unit]}}
                        saved_data.update(new_data)
            with open("saved_data.json", "w") as file:
                json.dump(saved_data, file, indent=4)





updated_list=[]
dates_list=all_dates_current_month()

#make a list of the 3 past and 3 upcoming days
for i,dat in enumerate(dates_list):
    if dat==datetime.today().strftime('%a %d %B %Y'):
        updated_list.append(dates_list[i-3])
        updated_list.append(dates_list[i-2])
        updated_list.append(dates_list[i-1])
        updated_list.append(dates_list[i])
        updated_list.append(dates_list[i+1])
        updated_list.append(dates_list[i+2])
        updated_list.append(dates_list[i+3])


window=Tk()
pic_file=PhotoImage(file="workout.png")
canvas=Canvas(width=480,height=270)
canvas.grid(row=0,column=1,columnspan=8)
pic=canvas.create_image(240,135,image=pic_file)

day_lbl0=Label(text="On ")
day_lbl0.grid(row=1  ,column=0)
day_value_inside0=StringVar(window,value="Choose a date")
day_opt0=OptionMenu(window,day_value_inside0, updated_list[0], updated_list[1], updated_list[2], updated_list[3], updated_list[4], updated_list[5], updated_list[6])
day_opt0.grid(row=1  ,column=1)
activity_lbl=Label(text="i did ")
activity_lbl.grid(row=1  ,column=2)
act_value_inside0=StringVar(window,value="Choose a workout")

act_opt0=OptionMenu(window,act_value_inside0,"Aerobics","Cycling","Running","Swimming","Walking")
act_opt0.grid(row=1  ,column=3)
unit_lbl=Label(text="for: ")
unit_lbl.grid(row= 1,column=4)
minutes_lbl=Label(text="minutes")
minutes_lbl.grid(row=1,column=6)
unit_ent0=Entry()
unit_ent0.grid(row=1,column=5)
gen_row_but=Button(text="Add entry",command=add_col)
gen_row_but.grid(row=1,column=7)
reg_but=Button(text="Register activities",command=reg_act)
reg_but.grid(row=1,column=8)
display_but=Button(text="Display Saved Activities",command=display_act)
display_but.grid(row=1,column=9)

window.mainloop()