# +-----------------------------------------------------------------------+
# |                     Author : Prashant Bhandari                        |
# |                    ============================                       |
# +-----------------------------------------------------------------------+
# | Simple script to fetch and display Todo items from a REST API         |
# | using the jsonplaceholder.typicode.com endpoint.                      |
# |                                                                       |
# | This script fetches a specified number of Todo items and displays     |
# | them in a tabular format with columns for User ID, ID, Title, and     |
# | Completion status.                                                    |
# |                                                                       |
# | It utilizes the requests library for making HTTP requests, time for   |
# | adding delays, and the TermMeter class for displaying |a progress bar |
# | while fetching the Todo items.                                        |
# +-----------------------------------------------------------------------+

import requests
import time
from termmeter.term_meter import TermMeter

API_URL = 'https://jsonplaceholder.typicode.com/todos/'

def fetch_todos(num_todos):
    todos = []
    # Initialize TermMeter for tracking progress
    processing_meter = TermMeter("Fetching Todos", num_todos, 20, eta=True, benchmark=True)
    processing_meter.start()
    for i in range(1, num_todos + 1):
        response = requests.get(API_URL + str(i))
        if response.status_code == 200:
            todos.append(response.json())
            # Update progress after each todo is fetched
            processing_meter.update(i)
            # Print progress information
        else:
            print(f"Failed to fetch Todo : {i}")
        time.sleep(0.1)  # Simulate delay
    return todos

def display_todos(todos):
    print("+-" + "-"*10 + "-+-" + "-"*10 + "-+-" + "-"*50 + "-+-" + "-"*10 + "-+")
    print("| {:^10} | {:^10} | {:^50} | {:^10} |".format("User ID", "ID", "Title", "Completed"))
    print("+-" + "-"*10 + "-+-" + "-"*10 + "-+-" + "-"*50 + "-+-" + "-"*10 + "-+")
    for todo in todos:
        print("| {:^10} | {:^10} | {:<50} | {:^10} |".format(todo['userId'], todo['id'], todo['title'][:50], str(todo['completed'])))
    print("+-" + "-"*10 + "-+-" + "-"*10 + "-+-" + "-"*50 + "-+-" + "-"*10 + "-+")

if __name__ == "__main__":
    # Number of todos to fetch
    num_todos = 10
    # Fetch todos from the API
    todos = fetch_todos(num_todos)
    display_todos(todos)