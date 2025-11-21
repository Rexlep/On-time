import pytz
import customtkinter as ctk
import datetime
import time
import os
from PIL import Image, ImageTk
from listbox.CTkListbox import *
from datetime import datetime, date
from messagebox.CTkMessagebox import CTkMessagebox
from hover.hover import CreateToolTip

clock_shown = False
timer_shown = False
stop_watch_shown = False
start_image = None
timer_running = False
timer_paused = False
is_running = False
pause_time = None

remaining_time = 0
start_time = 0

today = date.today()
formatted_date_number = today.strftime("%m/%d/%y")

current_date = (datetime.now())
formatted_date = current_date.strftime("%A, %B %d, %Y")


# _____________________________________________________________functions_____________________________________________________________


def add_different_time():
    """This function add another time with listbox"""

    def show_value():
        selected_options = listbox.curselection()  # Get the indices of the selected options

        selected_times = []
        for index in selected_options:
            location = locations[index + 1]  # Adjust the index since it starts from 0
            current_time = datetime.now(pytz.timezone(location["timezone"])).strftime("%H:%M:%S")
            selected_times.append(f"{location['name']} Time: {current_time}")

        selected_times_str = "\n".join(selected_times)  # Concatenate the selected times as a string

        # Create a new label to display the selected times
        selected_times_label = ctk.CTkLabel(frame_main, text=selected_times_str, font=("Arial", 24))
        selected_times_label.pack(pady=10, padx=5)

        # Update the position of the time_label and selected_times_label
        time_label.pack(side='top', pady=10)
        selected_times_label.pack(side='top', pady=20)

    def kill_root():
        root_list_box.destroy()

    root_list_box = ctk.CTk()

    listbox = CTkListbox(root_list_box, command=show_value)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    btn_close = ctk.CTkButton(root_list_box, text='Close', font=('fonts/MonoLisa-Bold.ttf', 15), width=5,
                              fg_color='#696969',
                              corner_radius=8, hover_color='#707070', command=kill_root)
    btn_close.pack(side=ctk.BOTTOM, pady=10)

    CreateToolTip(btn_close, "Close")

    locations = {
        1: {"name": "Paris", "timezone": "Europe/Paris"},
        2: {"name": "Milan", "timezone": "Europe/Rome"}
    }

    def update_time():
        current_option_count = listbox.size()
        for index in locations:
            location = locations[index]
            current_time = datetime.now(pytz.timezone(location["timezone"])).strftime("%H:%M:%S")
            option_text = f"Option {index}"
            if index < current_option_count:
                listbox.delete(index)
            listbox.insert(index, f"{location['name']} Time: {current_time}")
        root_list_box.after(1000, update_time)

    update_time()

    root_list_box.mainloop()


def clock_labels():
    """This function pack or unpack clock elements"""
    global clock_shown, timer_shown, stop_watch_shown

    if not clock_shown:
        frame_btn_delete_add.pack(pady=10)
        btn_delete.pack(side='left', padx=10, pady=10)
        btn_add.pack(side='left', padx=10)
        frame_time_date.pack(pady=5)
        time_label.pack(pady=20)
        date_label.pack(side="left", padx=5)
        date_number_label.pack(side="left")
        frame_timer.pack_forget()
        frame_stop_watch.pack_forget()

        # Check if the stopwatch widget is already shown, and hide it if true
        if stop_watch_shown:
            frame_stop_watch.pack_forget()

        clock_shown = True
        timer_shown = False
        stop_watch_shown = False

    else:
        frame_btn_delete_add.pack_forget()
        btn_delete.pack_forget()
        btn_add.pack_forget()
        frame_time_date.pack_forget()
        time_label.pack_forget()
        date_label.pack_forget()
        date_number_label.pack_forget()

        clock_shown = False


def timer_labels():
    """This function pack or unpack timer elements"""
    global timer_shown, clock_shown, stop_watch_shown

    if not timer_shown:
        frame_timer.pack(pady=10)
        frame_entry.pack(padx=10, pady=30)
        entry_h.pack(side=ctk.LEFT, padx=10)
        entry_m.pack(side=ctk.LEFT, padx=10)
        entry_s.pack(side=ctk.LEFT, padx=10, pady=15)
        timer_label.pack(padx=50, pady=20)
        frame_timer_btn.pack(pady=10)
        btn_reset.pack(side=ctk.LEFT, padx=10)
        btn_start.pack(side=ctk.LEFT, padx=10, pady=10)

        frame_time_date.pack_forget()
        frame_btn_delete_add.pack_forget()
        frame_stop_watch.pack_forget()

        timer_shown = True
        clock_shown = False
        stop_watch_shown = False

    else:
        frame_timer.pack_forget()
        frame_entry.pack_forget()
        entry_h.pack_forget()
        entry_m.pack_forget()
        entry_s.pack_forget()
        timer_label.pack_forget()
        frame_timer_btn.pack_forget()
        btn_reset.pack_forget()
        btn_start.pack_forget()

        timer_shown = False


def stop_watch_labels():
    """This function pack or unpack stopwatch elements"""
    global stop_watch_shown, clock_shown, timer_shown

    if not stop_watch_shown:
        frame_stop_watch.pack(pady=10)
        frame_timer.pack_forget()
        frame_time_date.pack_forget()
        frame_btn_delete_add.pack_forget()
        stopwatch_label.pack(padx=18, pady=50)
        label.pack()
        frame_btn_stopwatch.pack(pady=30)
        btn_reset_stopwatch.pack(side="left", padx=10)
        btn_start_stopwatch.pack(side="left", padx=10)
        btn_flag_stopwatch.pack(side="left", padx=10, pady=10)

        stop_watch_shown = True
        clock_shown = False
        timer_shown = False

    else:
        frame_stop_watch.pack_forget()
        stopwatch_label.pack_forget()
        label.pack_forget()
        frame_btn_stopwatch.pack_forget()
        btn_start_stopwatch.pack_forget()
        btn_reset_stopwatch.pack_forget()
        btn_flag_stopwatch.pack_forget()

        stop_watch_shown = False


def update_time():
    """This function is for the main time"""
    tehran_tz = pytz.timezone('Asia/Tehran')
    current_time = datetime.now(tehran_tz).strftime("%H:%M:%S")

    time_label.configure(text=current_time)
    time_label.after(1000, update_time)


def validate_time():
    """Validates the entered time values"""
    try:
        hours = entry_h.get()
        minutes = entry_m.get()
        seconds = entry_s.get()

        if not hours or not minutes or not seconds:
            raise ValueError("Please enter values for all fields")

        if hours == "00" and minutes == "00" and seconds == "00":
            raise ValueError("Please enter a non-zero value for at least one field")

        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        if hours < 0 or hours > 23:
            raise ValueError("Please enter a valid number between 0 and 23 for hours")
        if minutes < 0 or minutes > 59:
            raise ValueError("Please enter a valid number between 0 and 59 for minutes")
        if seconds < 0 or seconds > 59:
            raise ValueError("Please enter a valid number between 0 and 59 for seconds")
        else:
            toggle_timer()
            return True

    except ValueError as e:
        CTkMessagebox(title="Error", message=str(e), icon="cancel")


def reset_timer():
    global remaining_time, start_image
    """Resets the timer elements"""

    timer_label.configure(text="00:00:00")
    remaining_time = 0
    btn_start.configure(image=img_start)


def toggle_timer():
    """Toggles the timer start/stop state and updates the button image"""
    global start_image

    if start_image is None:
        start_image = img_start

    if start_image == img_start:
        start_image = img_stop
    else:
        start_image = img_start

    btn_start.configure(image=start_image)


def start_timer():
    """Start the timer if values are True"""
    global timer_running, timer_paused, remaining_time, start_image

    # If the timer is not running and the time values are valid, start it
    if not timer_running and validate_time():
        try:
            hours = int(entry_h.get())
            minutes = int(entry_m.get())
            seconds = int(entry_s.get())

            remaining_time = hours * 3600 + minutes * 60 + seconds
            timer_running = True
            timer_paused = False
            countdown()
            toggle_timer()

        except ValueError:
            timer_label.configure(text="Invalid input")

    elif timer_running and not timer_paused:
        timer_paused = True

    elif timer_running and timer_paused:
        timer_paused = False
        countdown()  # Resume countdown when timer is resumed

    # Update the start button image based on the timer state
    if timer_running and not timer_paused:
        btn_start.configure(image=img_stop)
    else:
        btn_start.configure(image=img_start)


def countdown():
    """Start the timer countdown"""
    global remaining_time, timer_running, timer_paused

    if remaining_time > 0 and not timer_paused:
        hours = remaining_time // 3600
        minutes = (remaining_time % 3600) // 60
        seconds = remaining_time % 60

        timer_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        remaining_time -= 1
        timer_label.after(1000, countdown)
    elif remaining_time <= 0:
        timer_running = False
        reset_timer()


def start_stopwatch():
    """Start the stopwatch"""
    global is_running, start_time, pause_time

    if not is_running:
        is_running = True
        if pause_time is None:
            start_time = time.time()
        else:
            start_time = time.time() - (pause_time / 1000)
        update_stopwatch()
        btn_start_stopwatch.configure(image=img_stop)
    else:
        is_running = False
        pause_time = round((time.time() - start_time) * 1000)
        btn_start_stopwatch.configure(image=img_start)


def update_stopwatch():
    """Update the stopwatch every second"""
    if is_running:
        elapsed_time = round((time.time() - start_time) * 1000)
    else:
        elapsed_time = pause_time

    # Compute hours, minutes, seconds, and milliseconds
    if elapsed_time is not None:
        hours = elapsed_time // 3600000
        minutes = (elapsed_time % 3600000) // 60000
        seconds = (elapsed_time % 60000) // 1000
        milliseconds = elapsed_time % 1000

        # Update the label with the elapsed time
        stopwatch_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}")

    # Schedule the next update after 1 millisecond
    stopwatch_label.after(1, update_stopwatch)


def reset_stopwatch():
    """Reset the number of stopwatch"""
    global is_running, start_time, pause_time
    is_running = False
    start_time = None
    pause_time = None
    stopwatch_label.configure(text="00:00:00:000")
    label.configure(text="00:00:00:000")
    btn_start_stopwatch.configure(image=img_start)


def add_stopwatch_label():
    """Add label with text of started stopwatch"""
    global is_running
    if is_running:
        elapsed_time = round((time.time() - start_time) * 1000)

        hours = elapsed_time // 3600000
        minutes = (elapsed_time % 3600000) // 60000
        seconds = (elapsed_time % 60000) // 1000
        milliseconds = elapsed_time % 1000

        label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}", font=("Arial", 20))
    else:
        CTkMessagebox(title="Error", message="Please start the stopwatch first", icon="cancel")


# _____________________________________________________images___________________________________________________________

img_clock = ctk.CTkImage(Image.open("icons/clock.png"), size=(30, 30))
img_timer = ctk.CTkImage(Image.open("icons/_timer.png"), size=(28, 28))
img_stop_watch = ctk.CTkImage(Image.open("icons/stopwatch.png"), size=(30, 30))
img_add = ctk.CTkImage(Image.open("icons/add.png"), size=(30, 30))
img_delete = ctk.CTkImage(Image.open("icons/delete.png"), size=(30, 30))
img_start = ctk.CTkImage(Image.open("icons/start.png"), size=(30, 30))
img_stop = ctk.CTkImage(Image.open("icons/stop.png"), size=(30, 30))
img_reset = ctk.CTkImage(Image.open("icons/reset.png"), size=(30, 30))

# _____________________________________________________ui_____________________________________________________________

main_window = ctk.CTk()
main_window.title("On Time")
main_window.geometry('800x500')

icon_path = ImageTk.PhotoImage(file=(os.path.join("icons/O.ico")))
main_window.wm_iconbitmap()
main_window.iconphoto(False, icon_path)


frame_main = ctk.CTkFrame(master=main_window)
frame_main.pack(fill='both', expand=True)

frame_timer = ctk.CTkFrame(master=frame_main, corner_radius=15)

frame_timer_btn = ctk.CTkFrame(master=frame_timer, corner_radius=15)

frame_entry = ctk.CTkFrame(master=frame_timer, corner_radius=15)

frame_stop_watch = ctk.CTkFrame(master=frame_main, corner_radius=15)

frame_btn = ctk.CTkFrame(master=frame_main, corner_radius=15)
frame_btn.pack(pady=10)

frame_btn_delete_add = ctk.CTkFrame(master=frame_main, corner_radius=15)

frame_time_date = ctk.CTkFrame(master=frame_main, fg_color='#2B2B2B')

frame_btn_stopwatch = ctk.CTkFrame(master=frame_stop_watch, fg_color='#2B2B2B', corner_radius=15)

frame_list_box = ctk.CTkFrame(master=frame_main, corner_radius=15)

# ------------------------------------clock-elements--------------------------------------------------------------------

btn_clock = ctk.CTkButton(frame_btn, image=img_clock, text='', font=('Arial', 15), width=5, fg_color='#696969',
                          corner_radius=8, hover_color='#707070', command=clock_labels)
btn_clock.pack(side='left', padx=10)

btn_timer = ctk.CTkButton(frame_btn, image=img_timer, text='', font=('Arial', 15), width=5, fg_color='#696969',
                          corner_radius=8, hover_color='#707070', command=timer_labels)
btn_timer.pack(side='left', padx=10)

btn_stop_watch = ctk.CTkButton(frame_btn, image=img_stop_watch, text='', font=('Arial', 15), width=5,
                               fg_color='#696969',
                               corner_radius=8, hover_color='#707070', command=stop_watch_labels)
btn_stop_watch.pack(side='left', padx=10, pady=10)

time_label = ctk.CTkLabel(frame_time_date, font=("Ubuntu Bold", 120, 'bold'))
date_label = ctk.CTkLabel(frame_time_date, text=f'{formatted_date}  -', font=("Arial", 14))
date_number_label = ctk.CTkLabel(frame_time_date, text=formatted_date_number)

btn_add = ctk.CTkButton(frame_btn_delete_add, image=img_add, text='', font=('Arial', 15), width=5, fg_color='#696969',
                        corner_radius=8, hover_color='#707070', command=add_different_time)

btn_delete = ctk.CTkButton(frame_btn_delete_add, image=img_delete, text='', font=('Arial', 15), width=5,
                           fg_color='#696969',
                           corner_radius=8, hover_color='#707070')

# ------------------------------------timer-elements--------------------------------------------------------------------

hour = ctk.StringVar()
minute = ctk.StringVar()
second = ctk.StringVar()

hour.set("00")
minute.set("00")
second.set("00")

entry_h = ctk.CTkEntry(frame_entry, textvariable=hour, width=30)
entry_m = ctk.CTkEntry(frame_entry, textvariable=minute, width=30)
entry_s = ctk.CTkEntry(frame_entry, textvariable=second, width=30)

timer_label = ctk.CTkLabel(frame_timer, text='00:00:00', font=("Arial", 60))

label = ctk.CTkLabel(frame_stop_watch, text="", font=("Arial", 30))

btn_start = ctk.CTkButton(frame_timer_btn, image=img_start, text='', font=('Arial', 15), width=5, fg_color='#696969',
                          corner_radius=8, hover_color='#707070', command=start_timer)

btn_reset = ctk.CTkButton(frame_timer_btn, image=img_reset, text='', font=('Arial', 15), width=5, fg_color='#696969',
                          corner_radius=8, hover_color='#707070', command=reset_timer)

# ------------------------------------stopwatch-elements----------------------------------------------------------------

stopwatch_label = ctk.CTkLabel(frame_stop_watch, text="00:00:00:000", font=("Arial", 60))

listbox = CTkListbox(frame_list_box, height=10, font=("fonts/MonoLisa-Bold.ttf", 15))

btn_reset_stopwatch = ctk.CTkButton(frame_btn_stopwatch, image=img_reset, text='', font=('Arial', 15), width=5,
                                    fg_color='#696969', corner_radius=8, hover_color='#707070', command=reset_stopwatch)

btn_start_stopwatch = ctk.CTkButton(frame_btn_stopwatch, image=img_start, text='', font=('Arial', 15), width=5,
                                    fg_color='#696969', corner_radius=8, hover_color='#707070', command=start_stopwatch)

btn_flag_stopwatch = ctk.CTkButton(frame_btn_stopwatch, image=img_add, text='', font=('Arial', 15), width=5,
                                   fg_color='#696969', corner_radius=8, hover_color='#707070', command=add_stopwatch_label)

CreateToolTip(btn_clock, 'Clock')
CreateToolTip(btn_timer, 'Timer')
CreateToolTip(btn_stop_watch, 'Stop Watch')
CreateToolTip(btn_add, 'Add time')
CreateToolTip(btn_delete, 'Delete added times')
CreateToolTip(btn_start, 'Start')
CreateToolTip(btn_reset, 'Reset')
CreateToolTip(btn_reset_stopwatch, 'Reset')
CreateToolTip(btn_start_stopwatch, 'Start')
CreateToolTip(btn_flag_stopwatch, 'Flag')

update_time()

main_window.mainloop()
print("END of the code")