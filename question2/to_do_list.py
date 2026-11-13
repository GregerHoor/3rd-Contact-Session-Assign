from task import *

import os
import json
import psycopg
from psycopg.types.json import Jsonb
from psycopg.rows import dict_row

from dotenv import load_dotenv

# Please adopt use of your postgres db private dets
load_dotenv(r"C:\Users\USER\PostgreSQL.env")

class ToDoList:
    def __init__(self):
        self.conn = psycopg.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
        )

        self.cur = self.conn.cursor(row_factory=dict_row)
        
    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(25) NOT NULL,
                description VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            );
        """)
        
        self.conn.commit()
        
    def table_is_empty(self):
        self.cur.execute("SELECT COUNT(*) FROM tasks")
        
        return self.cur.fetchone().get('total') == 0

    def add_task(self, task_as_dict, task):
        if task and not self.existing_tasks(task_as_dict):
            self.cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (task.title, task.description))
            self.conn.commit()
            print(f'\n"{task}" \nadded to the list.')
        else:
            print(f"Adding Failed, {task.title} already exists, please try another title")
        

    def existing_tasks(self, task):
        exists = None
        if task and not self.table_is_empty():
            self.cur.execute("SELECT * FROM tasks WHERE title = %s", (task.get('title'),))
            exists = self.cur.fetchone()
            if not exists:
                print(f"\nNo match found")
                
        elif self.table_is_empty():
            print(f"\nTable is empty")
                
        elif task==None:
            print(f"\nNo task to check, try again")
            
        return exists
        

    def remove_task(self, task):
        if task and self.existing_tasks(task):
            task_title = task.get('title')
            self.cur.execute("DELETE FROM tasks WHERE title = %s", (task_title,))
            print(f'\nTask "{task_title}" has been removed.')

        else:
            print(f"\nTask removal went wrong!")
            
        self.conn.commit()
        

    def edit_task(self, task, new_title, new_description):
        if task and self.existing_tasks(task):
            task_id = task.get('id')
            if new_title is not None:
                self.cur.execute("UPDATE tasks SET title = %s WHERE id = %s", (new_title, task_id))
                print(f'\nTask "title" updated.')
            if new_description is not None:
                self.cur.execute("UPDATE tasks SET description =  %s WHERE id = %s", (new_description, task_id))
                print(f'\nTask "decription" updated.')
            
        else:
            print("\nTask update went wrong!")
        self.conn.commit()
        

    def complete_task(self, task):
        if task is not None and self.existing_tasks(task):
            task_id = task.get('id')
            self.cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (True, task_id))
            print(f'\nTask has been saved as completed.')
            
        else:
            print("\nTask update went wrong!")
        self.conn.commit()
            

    def view_tasks(self):
        if self.table_is_empty():
            print("\nNo tasks in the list.")
        else:
            print("\nTasks in the list:")
            self.cur.execute("SELECT * FROM tasks")
            tasks = self.cur.fetchall()
            for t in tasks:
                id = t.get("id")
                title = t.get("title")
                desc = t.get("description")
                comp = t.get("completed")
                
                tp = Task(title, desc, comp)
                print(f'\nID: {id}\n{tp}')
            return tasks
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()