# Facets_ClickUp
**Create python scripts**

**create a account on clickup:**
Manually sign up for an account 
**Create List and Task**
Manually created two list named blue and green in clickup
Added 3 - 4 tasks with different names and description to both the lists
**Python Scripts**
Used The personal ClickUP api token to interact with the clickup account 
created a function create task parameters passed are list name , task name , task description
for making a new task in the desired list made use of "requests" module to make an api call 
**Function to updat the task due date**
Loop through the tasks in the list and update their due date to tommorrow 
**Function to get the task information like name, id , description , due date and save them in the csv file 
Fetch all the task ids ferom both the list blue and green and saved the relevenat task details in details.csv file using csv module 
**Function for Checking the due dates every 30 Minutes**
used the 'time' module to set up a script that runs every 30 minutes. this function will check all the tasks in both the lists and if the task doesnt have a due date then it will add a comment "please add due date". Used the clickUp api to add the comments to the task 


