# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
# create the user and password from the user.txt file, with the information in the user_data 
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        ''' 'r' = Add a new user to the user.txt file'''
        reg_completed = False #create a loop to complete the registration
        while reg_completed == False:
            # - Request input of a new username
            new_username = input("New Username: ")

            # - Request input of a new password
            new_password = input("New Password: ")

            # - Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

            # check if the user already exists
            if new_username in username_password:
                choice = input("User already registered. Do you want to register a new user? (Y/N): ").lower()
                # allow user to try again
                if choice == "y":
                    continue
                # go to main menu
                else:
                    reg_completed = True

            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password and new_username not in username_password:
                    # - If password is equal to confirmed password, they are the same, add them to the user.txt file,
                print("New user added")
                username_password[new_username] = new_password

                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
                    reg_completed = True

            # - Otherwise you present a relevant message.
            else:
                print("Passwords do no match")

    elif menu == 'a':
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No",
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")


    elif menu == 'va':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)
            


    elif menu == 'vm':
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        # Summarize the tasks
        for index, task in enumerate(task_list):
            if task['username'] == curr_user:
                print(f"Task: {index} - Title: {task['title']} | Description: {task['description']} | Completed: {task['completed']} ")
        # ask the user to select one task to see
                choice_task = int(input("which task do you want to see (if do you want to go back to main menu type -1): "))
        if curr_user not in task['username']: 
            print("User don't have any task")
            choice_task = -1
            continue
        if choice_task == -1:
            continue
        else:
            disp_str = f"Task: \t\t {task_list[choice_task]['title']}\n"
            disp_str += f"Assigned to: \t {task_list[choice_task]['username']}\n"
            disp_str += f"Date Assigned: \t {task_list[choice_task]['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {task_list[choice_task]['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {task_list[choice_task]['description']}\n"
            print(disp_str)
            # ask the user if they want to edit or mark as completed
            task_edit = input("Do you wish to mark this task as completed (type completed) or edit (type edit) or go to main menu(type menu): ").lower()
            if task_edit == "menu":
                continue
            elif task_edit == "completed":
                # change the task to completed
                if task_list[choice_task]['completed'] is True:
                    print("Task already completed.")
                    continue
                else:
                    task_list[choice_task]['completed'] = True
                    print(task_list[choice_task]['completed'])
            elif task_edit == "edit":
                # check if the task is already completed
                if task_list[choice_task]['completed'] is True:
                    print("Task already completed, not possible to edit!")
                    continue
                else:
                    choice_edit = input("Edit the user (type user) or due date (type date) or return to main menu(type menu): ").lower()
                    if choice_edit == "menu":
                        continue
                    elif choice_edit == "user":
                        # change the person assigned to the task
                        new_user = input("To whom do you want to assign the task: ")
                        if new_user not in username_password.keys():
                            print("User does not exist. Please enter a valid username")
                            continue
                        else:
                            task_list[choice_task]['username'] = new_user
                            print(task_list[choice_task]['username'])
                    elif choice_edit == "date":
                        # change the date due of the task
                        while True:
                            try:
                                new_date = input("When it the new due date: YYYY-MM-DD: ")
                                due_date = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                                task_list[choice_task]['due_date'] = due_date
                                print(task_list[choice_task]['due_date'])
                                break

                            except ValueError:
                                print("Invalid datetime format. Please use the format specified")

                        # new_date = input("When it the new due date: YYYY-MM-DD: ")
                        # due_date = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                        # task_list[choice_task]['due_date'] = due_date
                        # print(task_list[choice_task]['due_date'])
            # edit the file with the new information
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No",
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
                print("Task successfully edited.")
            

    elif menu == 'gr':
        # if not existent the task_overview.txt, create one
        if not os.path.exists("task_overview.txt"):
            with open("task_overview.txt", "w") as default_file:
                # i.e: total tasks generated = 0; completed tasks = 0; uncompleted tasks = 0; overdue uncompleted = 0; % incomplete = 0; % overdue = 0
                default_file.write("0;0;0;0;0%;0%")

        task_generated = 0
        task_completed = 0
        task_uncompleted = 0
        overdue_uncompleted = 0
        today = datetime.today()

        print_report = False
        for t in task_list:
            if curr_user not in t['username']: 
                print_report == False
                continue
            else:
                print_report == True
            task_generated += 1
            if t['completed'] == True:
                task_completed += 1
            else:
                task_uncompleted += 1
                if t['due_date'] < today:
                    overdue_uncompleted += 1

        if print_report == True:
            print("_________________________________________________________")
            print(f"Total Tasks Generated:             {task_generated}")
            print(f"Total Tasks Completed:             {task_completed}")
            print(f"Total Tasks Uncompleted:           {task_uncompleted}")
            print(f"Total Tasks Overdue:               {overdue_uncompleted}")
            percent_incomplete = 100*task_uncompleted/task_generated
            print(f"Percent of Total Tasks Incomplete: {percent_incomplete}%")
            percent_overdue = 100*overdue_uncompleted/task_generated
            print(f"Percent of Total Tasks Overdue:    {percent_overdue}%")
            print("_________________________________________________________")

            with open("task_overview.txt", 'w') as task_overview_file:
                task_overview_file.write(f"{task_generated};{task_completed};{task_uncompleted};{overdue_uncompleted};{percent_incomplete}%;{percent_overdue}%")
                print("\nFile updated")

        # create the user_overview.txt if not existent
        if not os.path.exists("user_overview.txt"):
            with open("user_overview.txt", "w") as default_file:
                # default_file.write("")
                pass

        num_users = len(username_password.keys())
        total_task = task_generated
        user_overview = []
        # create a list of data to produce user report
        if curr_user not in task_list: 
            print("User don't have any task")
            continue
        for curr_user in username_password:
            user_dict = {
                "username" : user,
                "total_tasks": 0,
                "tasks_complete": 0,
                "tasks_incomplete": 0,
                "tasks_overdue": 0,
            }

            for t in task_list:
                if t["username"] == user:
                    user_dict["total_tasks"] += 1
                    if t["completed"] == True:
                        user_dict["tasks_complete"] += 1
                    elif t["completed"] == False:
                        user_dict["tasks_incomplete"] += 1
                    elif t["due_date"] < today:
                        user_dict["tasks_overdue"] += 1
            user_overview.append(user_dict)
        print(user_overview)

        # Printing the report
        for user in username_password:
            print("_________________________________________________")
            print(f"USER: {user}")
            for u in user_overview:
                if u["username"] == user:
                    print(f"Total number of tasks:          {u['total_tasks']} ")
                    p_task = u["total_tasks"] * 100 / total_task
                    print(f"Percentage of tasks assigned:   {p_task} %")
                    p_comp = u["tasks_complete"] * 100 / u["total_tasks"]
                    print(f"Percentage of tasks completed:  {p_comp} %")
                    p_incomp = u["tasks_incomplete"] * 100 / u["total_tasks"]
                    print(f"Percentage of tasks incomplete: {p_incomp} %")
                    p_due = u["tasks_overdue"] * 100 / u["total_tasks"]
                    print(f"Percentage of tasks incomplete: {p_due} %")
                    print("_________________________________________________")

        with open("user_overview.txt", 'w') as task_overview_file:
            task_overview_file.write(f"Total users: {num_users}; Total Tasks: {total_task}; {user_overview} ")
            print("\nFile updated")
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")


