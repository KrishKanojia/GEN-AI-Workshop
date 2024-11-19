from tkinter import *
import tkinter as tk
from tkinter import messagebox

count = 1

def add_student():
    global count
    name = name_input.get()
    class_data = class_input.get()
    marks = marks_input.get()
    if name and class_data and marks:
        my_list.insert(tk.END, f"{count}. {name}, {class_data}, {marks}")

        name_input.delete(0, tk.END)
        class_input.delete(0, tk.END)
        marks_input.delete(0, tk.END)
        count += 1
    else:
        messagebox.showerror("Error", "Input field Empty")


def open_new_window(selected_item, index):
    new_window = tk.Toplevel(root)  # Create a new top-level window
    new_window.title("Selected Record")
    data_list = selected_item.split(",")

    edit_email = tk.Label(new_window, text="Name")
    edit_email.pack()
    edit_email_input = Entry(new_window, width=50)
    edit_email_input.insert(tk.END, data_list[0])
    edit_email_input.pack()
    

    edit_email = tk.Label(new_window, text=f"Class")
    edit_email.pack()
    edit_class_input = Entry(new_window, width=50)
    edit_class_input.insert(tk.END, data_list[1])
    edit_class_input.pack()


    edit_email = tk.Label(new_window, text=f"Marks")
    edit_email.pack()
    edit_marks_input = Entry(new_window, width=50)
    edit_marks_input.insert(tk.END, data_list[2])
    edit_marks_input.pack()

    

    # Create a Frame to hold the buttons
    button_frame = tk.Frame(new_window)
    button_frame.pack(pady=20)  # Add padding around the frame if needed

    # Add Update button to the frame
    update_button = tk.Button(
        button_frame,
        text="Update",
        command=lambda: update_record(index, edit_email_input.get(), edit_class_input.get(), edit_marks_input.get(), new_window)
    )
    update_button.pack(side="left", padx=5)  # Pack vertically with padding

    # Add Close button to the frame
    close_button = tk.Button(
        button_frame,
        text="Close",
        command=new_window.destroy
    )
    close_button.pack(side="left", padx=5)  # Pack vertically with padding


def update_record(index, name, class_data, marks, top_window):
    my_list.delete(index)
    my_list.insert(index, f"{index+1}. {name}, {class_data}, {marks}")
    top_window.destroy()

def update_student():
    selected_item = my_list.get(tk.ACTIVE)
    selected_student  = my_list.curselection()
    print("Selected student ", selected_student)
    if not selected_student:
        messagebox.showerror("Error","Item not selected")
    else:
        print("Active Data:", selected_item)
        open_new_window(selected_item.split(".")[1], selected_student[0])


    # if name and class_data and marks:
        # selected_student  = my_list.curselection()
        
    
    #     if selected_student:
    #         index = selected_student[0]
            # selected_item = my_list.get(index)
            # my_list.delete(index)
            # my_list.insert(index, f"{index+1}. {name}, {class_data}, {marks}")

def delete_student():
    selected_student  = my_list.curselection()
    if not selected_student:
        messagebox.showerror("Error", "Select student data")
    else:
        my_list.delete(selected_student[0])


root = Tk()
root.title("CRUD App")

root.geometry("500x600")
root.configure(background='#0096DC')
name = tk.Label(root, text="Name:")
name.pack(pady=10)

name_input = tk.Entry(root, width=50)
name_input.pack(ipady=5)

temp_class = tk.Label(root, text="Class:")
temp_class.pack(pady=10)

class_input = tk.Entry(root, width=50)
class_input.pack(ipady=5)

marks = tk.Label(root, text="Marks:")
marks.pack(pady=10)

marks_input = tk.Entry(root, width=50)
marks_input.pack(ipady=5)


btn_frame = tk.Frame(root,bg="#0096DC")
btn_frame.pack(pady=10)


add_btn = tk.Button(btn_frame, text='Add Student', command=add_student, fg='white', bg='#00509E')
add_btn.pack(side='left', padx=5)

update_btn = tk.Button(btn_frame, text='Update Student', command=update_student, fg='white', bg='#00509E')
update_btn.pack(side='left', padx=5)

delete_btn = tk.Button(btn_frame, text='Delete Student', command=delete_student, fg='white', bg='#00509E')
delete_btn.pack(side='left', padx=5)

my_list = tk.Listbox(root, width=50)
my_list.pack(ipady=5)
root.mainloop()