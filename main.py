import requests
import json
import csv
import threading
import time

from datetime import datetime
api_key = 'pk_67495744_LC7K593DGDWSW6B6S4VGY3TYDE7HGQWU' #personal api key
blue_list_id = '900201884096' #blue list id
green_list_id= '900201884095' # green list id
headers = {
    'Authorization': api_key
}
# This function helps to create the task parameters passed is list name , task name , task description
def create_task(list_name,task_name,task_description):
    id = ''
    if list_name == 'blue':
        id = blue_list_id
    elif list_name == 'green':
        id = green_list_id
    else:
        print("list not found")
    print(id)
    # body o create task api
    task_data = {
        'name': task_name,
        'description': task_description
    }
    response = requests.post(f'https://api.clickup.com/api/v2/list/{id}/task', json=task_data, headers=headers)
    if response.status_code == 200:
        print("Task added successfully.{response.status_code}")
    else:
        print("Failed to add task.")


#Function to update date
def update_task_due_date(list_name,due_date):
    id = ''
    if list_name == 'blue':
        id = blue_list_id
    elif list_name == 'green':
        id = green_list_id
    else:
        print("list not found")
    response = requests.get(f'https://api.clickup.com/api/v2/list/{id}/task', headers=headers)
    data = json.loads(response.text) #converting to json format
    print(data['tasks'])
    task_list = data['tasks']
    task_ids = [] # empty list for task ids
    for i in range(len(task_list)): #iterating over the task ids
        task_ids.append(task_list[i]['id']) # append the id the task_list
    print(task_ids)
    #converting passed due date of format dd:mm:yyyy to miliseconds according to unix echo
    date_str = due_date
    date_obj = datetime.strptime(date_str, '%d:%m:%Y')
    timestamp_ms = int(date_obj.timestamp() * 1000)
    #body of update due date api
    task_data = {
        'due_date': timestamp_ms
    }

    for j in task_ids:
        res = requests.put(f'https://api.clickup.com/api/v2/task/{j}', data=task_data,headers=headers)
        if res.status_code == 200:
            print(f"Task updated successfully.{response.status_code}")
        else:
            print("Failed to add task.")

    return
# update_task_due_date('blue','13:09:2023')
# function for  get task details and save to csv file
def get_task_detail():
    tasks_list = []
    response = requests.get(f'https://api.clickup.com/api/v2/list/{blue_list_id}/task', headers=headers)
    response1 = requests.get(f'https://api.clickup.com/api/v2/list/{green_list_id}/task', headers=headers)
    data = json.loads(response.text)
    task_list = data['tasks']
    for i in range(len(task_list)):
        #temporary dictonary to store the details
        temp_dict = {
            'id' : task_list[i]['id'],
            'name': task_list[i]['name'],
            'description' : task_list[i]['description'],
            'due_date' : task_list[i]['due_date']
        }
        tasks_list.append(temp_dict)
        # converting to json format
    data1 = json.loads(response1.text)
    task_list1 = data1['tasks']
    # get the details of green list
    for i in range(len(task_list1)):
        temp_dict1 = {
            'id': task_list1[i]['id'],
            'name': task_list1[i]['name'],
            'description': task_list1[i]['description'],
            'due_date': task_list1[i]['due_date']
        }
        tasks_list.append(temp_dict1)
    print(tasks_list)
    # writing the data to the csv file
    csv_file = 'details.csv'
    with open(csv_file, mode='w', newline='') as file:
        fieldnames = tasks_list[0].keys()
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks_list)

#get_task_detail()
# function to check due date and comment. Comment Please add due date if due date is not set
def check_due_date():
    tasks_list = []
    response = requests.get(f'https://api.clickup.com/api/v2/list/{blue_list_id}/task', headers=headers)
    response1 = requests.get(f'https://api.clickup.com/api/v2/list/{green_list_id}/task', headers=headers)
    data = json.loads(response.text)
    task_list = data['tasks']
    for i in range(len(task_list)):
        temp_dict = {
            'id': task_list[i]['id'],
            'due_date': task_list[i]['due_date']
        }
        tasks_list.append(temp_dict)
    data1 = json.loads(response1.text)
    task_list1 = data1['tasks']
    for i in range(len(task_list1)):
        temp_dict1 = {
            'id': task_list1[i]['id'],
            'due_date': task_list1[i]['due_date']
        }
        tasks_list.append(temp_dict1)
    task_data = {
        'comment_text': 'Please add due date',
        'notify_all': True
    }
    for j in tasks_list:
        if j['due_date'] == None:
            response = requests.post(f'https://api.clickup.com/api/v2/task/{j["id"]}/comment', json=task_data, headers=headers)

#check_due_date()
interval = 30 * 60
# function to check every 30 min whether a task has a due date
def run_task():
    while True:
        check_due_date()
        time.sleep(interval)
task_thread = threading.Thread(target=run_task)
task_thread.start()
# Keep the main function running in background
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    task_thread.join()










