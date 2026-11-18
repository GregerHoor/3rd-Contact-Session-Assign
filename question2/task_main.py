import os
import json
import subprocess
import sys
import importlib

from to_do_list import ToDoList
from task import Task

def install_packages():
    package = ['psycopg', 'dotenv']
    for p in package:
        try:
            importlib.import_module(p)
            print(f'{p} is already installed')
        except ImportError:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', p])

def main():
    install_packages()
    
    to_do = ToDoList()
    task_title = None
    task_index = None
    option = None
    
    while True:
        to_do.create_tables()
        
        print("\n\nTo-Do List Menu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Edit Task")
        print("4. View Tasks")
        print("5. Complete Task")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            while True:
                title = input("\nEnter task title (enter 'back' to return to the main menu): ")
                if title.lower() == 'back':
                    break
                description = input("Enter task description (enter 'back' to return to the main menu): ")
                if description.lower() == 'back':
                    break
                task = Task(title, description, False)
                to_do.add_task(task.to_dict(), task)
                
                add_more = input("Do you want to ADD another task? (y/n): ")
                if add_more.lower() == 'n':
                    break
                elif add_more.lower() != 'y':
                    print("Invalid input. Returning to the main menu.")
                    break
        
        
        elif choice == '2':
            while True:
                all_tasks = to_do.view_tasks()
                while True:
                    option = input("\nDo you want to SELECT a task to REMOVE by title or index? (Enter 'title' or 'index') (Enter 'back' to return to the main menu): ").strip().lower()
                    
                    if option == 'title':
                        task_title = input("\nEnter the title of the task to REMOVE (enter 'back' to return to the main menu): ")
                        if task_title.lower() == 'back':
                            continue
                        break
                        
                    elif option == 'index':
                        task_index = int(input("\nEnter the index of the task to REMOVE (enter '00' to return to the main menu): "))
                        if task_index == 00:
                            continue
                        break
                    
                    elif option == 'back':
                        break
                    
                    else:
                        print("Invalid option. Please enter 'title' or 'index'.")
                
                if option != 'back' and option is not None:
                    task_to_remove = next((task for task in all_tasks if task.get('title') == task_title or task.get('id') == task_index), None)
                    if task_to_remove is not None:
                        to_do.remove_task(task_to_remove)
                        
                    else:
                        print(f'Task not found in the list.')
                    
                remv_more = input("Do you want to REMOVE another task? (y/n): ")
                if remv_more.lower() == 'n':
                    break
                elif remv_more.lower() != 'y':
                    print("Invalid input. Returning to the main menu.")
                    break
        
        
        elif choice == '3':
            while True:
                all_tasks =  to_do.view_tasks()
                
                new_title = None
                new_desc = None
                task_to_edit = None
                
                while True:
                    option = input("\nDo you want to SELECT a task to EDIT by title or index? (Enter 'title' or 'index') (Enter 'back' to return to the main menu): ").strip().lower()
                    if option == 'back':
                        break
                    
                    if option == 'title':
                        task_title = input("\nEnter the title of the task to EDIT (enter 'back' to return): ")
                        if task_title.lower() == 'back':
                            continue
                        break
                    
                    elif option == 'index':
                        task_index = int(input("\nEnter the index of the task to EDIT (enter '00' to return): "))
                        if task_index == 00:
                            continue    
                        break
                        
                    else:
                        print("Invalid option. Please enter 'title' or 'index'.")
                        continue
                
                if option != 'back' and option is not None:
                    task_to_edit = next((task for task in all_tasks if task.get('title') == task_title or task.get('id') == task_index), None)
                    
                    if task_to_edit is not None:
                        while True:
                            print("\nWhat are you interested in editing?")
                            print("1. Title")
                            print("2. Description")
                            print("3. Edit Both")
                            print("4. Exit")
                            more_opt = input("Enter your choice (1-4)")
                            if more_opt == '4':
                                break
                                                
                            if more_opt == '1':
                                new_title = input(f"Old Title: {task_to_edit.get('title')} \n Enter the new title: ")
                                break
                            elif more_opt == '2':
                                new_desc = input(f"Old Description: {task_to_edit.get('description')} \n Enter the new description: ")
                                break
                            elif more_opt == '3':
                                new_title = input(f"Old Title: {task_to_edit.get('title')} \n Enter the new title: ")
                                new_desc = input(f"Old Description: {task_to_edit.get('description')} \n Enter the new description: ")
                                break
                            else:
                                print(f"'{more_opt}' is an invalid reponse!") 
                                
                            to_do.edit_task(task_to_edit, new_title, new_desc)
                    else:
                        print(f'Task not found in the list.')
                            
                edit_more = input("Do you want to EDIT another task? (y/n): ")
                if edit_more.lower() == 'n':
                    break
                elif edit_more.lower() != 'y':
                    print("Invalid input. Returning to the main menu.")
                    break    
                           

        elif choice == '4':
            to_do.view_tasks()
        
        
        elif choice == '5':
            while True:
                all_tasks = to_do.view_tasks()
                
                while True:
                    option = input("\nDo you want to SELECT a task to COMPLETE by title or index? (Enter 'title' or 'index') (Enter 'back' to return to the main menu): ").strip().lower()
                                    
                    if option == 'title':
                        task_title = input("\nSELECT task by title (enter 'back' to return to the main menu): ")
                        if task_title.lower() == 'back':
                            continue
                        break
                    
                    elif option == 'index':
                        task_index = int(input("\nSELECT task by id (enter '00' to return to the main menu): "))
                        if task_index == 00:
                            continue
                        break
                    
                    elif option == 'back':
                        break
                    
                    else:
                        print("Invalid option. Please enter 'title' or 'index'.")
                
                if option != 'back' and option is not None:
                    task_to_complete = next((task for task in all_tasks if task.get('title') == task_title or task.get('id') == task_index), None)
                    if task_to_complete is not None:
                        to_do.complete_task(task_to_complete)
                        
                    else:
                        print(f'Task not found in the list.')
                    
                comp_more = input("Do you want to COMPLETE another task? (y/n): ")
                if comp_more.lower() == 'n':
                    break
                elif comp_more.lower() != 'y':
                    print("Invalid input. Returning to the main menu.")
                    break
                
                
        
        elif choice == '6':
            print("\nExiting the To-Do List application.")
            break
        
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main()