import os
from queue import Queue

# =====================================
# PROJECT CLASS (OOP)
# =====================================

class Project:
    def __init__(self, id_num, title, size, priority):
        self.id_num = id_num
        self.title = title
        self.size = size
        self.priority = priority

    def __str__(self):
        return f"{self.id_num}|{self.title}|{self.size}|{self.priority}"


# =====================================
# FILES
# =====================================

PROJECT_FILE = "project.txt"
COMPLETED_FILE = "completed.txt"

schedule_queue = Queue()


# =====================================
# PRIORITY NAME
# =====================================

def priority_name(priority):
    priorities = {
        1: "Urgent",
        2: "High",
        3: "Medium",
        4: "Low",
        5: "Can Wait"
    }

    return priorities.get(priority, "Unknown")


# =====================================
# LOAD PROJECTS
# =====================================

def load_projects():

    projects = []

    if not os.path.exists(PROJECT_FILE):
        return projects

    with open(PROJECT_FILE, "r") as file:

        for line in file:

            data = line.strip().split("|")

            if len(data) == 4:

                projects.append(
                    Project(
                        int(data[0]),
                        data[1],
                        int(data[2]),
                        int(data[3])
                    )
                )

    return projects


# =====================================
# INPUT PROJECT
# =====================================

def add_project():

    try:

        print("\n================================")
        print("PRIORITY GUIDE")
        print("================================")
        print("1 - Urgent")
        print("2 - High Priority")
        print("3 - Medium Priority")
        print("4 - Low Priority")
        print("5 - Can Be Delayed")

        id_num = int(input("\nEnter Project ID: "))
        title = input("Enter Project Title: ")
        size = int(input("Enter Number of Pages: "))

        priority = int(
            input("Enter Priority (1-5): ")
        )

        for p in load_projects():
            if p.id_num == id_num:
                print("Project ID already exists.")
                return

        if size <= 0:
            print("Number of pages must be greater than 0.")
            return

        if priority < 1 or priority > 5:
            print("Priority must be between 1 and 5.")
            return

        project = Project(
            id_num,
            title,
            size,
            priority
        )

        with open(PROJECT_FILE, "a") as file:
            file.write(str(project) + "\n")

        print("\nProject saved successfully!")

    except ValueError:
        print("Invalid input. Enter valid numeric values.")


# =====================================
# VIEW ONE PROJECT
# =====================================

def view_one_project():

    try:

        search_id = int(
            input("Enter Project ID: ")
        )

        projects = load_projects()

        found = False

        for project in projects:

            if project.id_num == search_id:

                print("\nPROJECT FOUND")
                print("-------------------------")
                print("ID:", project.id_num)
                print("Title:", project.title)
                print("Pages:", project.size)
                print(
                    "Priority:",
                    priority_name(project.priority)
                )

                found = True
                break

        if not found:
            print("Project not found.")

    except ValueError:
        print("Invalid ID.")


# =====================================
# VIEW ALL PROJECTS
# =====================================

def view_all_projects():

    projects = load_projects()

    if not projects:
        print("No projects found.")
        return

    print("\nALL PROJECTS")
    print("---------------------------------------------------")

    for project in projects:

        print(
            f"ID: {project.id_num} | "
            f"Title: {project.title} | "
            f"Pages: {project.size} | "
            f"Priority: {priority_name(project.priority)}"
        )


# =====================================
# VIEW COMPLETED PROJECTS
# =====================================

def view_completed_projects():

    if not os.path.exists(COMPLETED_FILE):
        print("No completed projects.")
        return

    with open(COMPLETED_FILE, "r") as file:

        content = file.read()

        if content:
            print("\nCOMPLETED PROJECTS")
            print("-------------------------")
            for line in content.strip().splitlines():
                d=line.split("|")
                if len(d)==4:
                    print(f"ID: {d[0]} | Title: {d[1]} | Pages: {d[2]} | Priority: {priority_name(int(d[3]))}")

        else:
            print("No completed projects.")


# =====================================
# CREATE SCHEDULE
# =====================================

def create_schedule():

    global schedule_queue

    projects = load_projects()

    if not projects:
        print("No projects available.")
        return

    # Priority then Size
    projects.sort(
        key=lambda x: (
            x.priority,
            x.size
        )
    )

    schedule_queue = Queue()

    for project in projects:
        schedule_queue.put(project)

    print("\nSchedule created successfully!")

    display_schedule()


# =====================================
# DISPLAY SCHEDULE
# =====================================

def display_schedule():

    global schedule_queue

    if schedule_queue.empty():
        print("Schedule not created yet.")
        return

    print("\nCURRENT SCHEDULE")
    print("---------------------------------------------------")

    temp = list(schedule_queue.queue)

    for project in temp:

        print(
            f"ID: {project.id_num} | "
            f"Title: {project.title} | "
            f"Priority: {priority_name(project.priority)} | "
            f"Pages: {project.size}"
        )


# =====================================
# GET PROJECT
# =====================================

def get_project():

    global schedule_queue

    if schedule_queue.empty():
        print("Schedule is empty. Create schedule first.")
        return

    print("\nCURRENT QUEUE")
    print("--------------------------")

    display_schedule()

    project = schedule_queue.get()

    print(
        f"\nProject {project.id_num} "
        f"({project.title}) "
        f"removed from queue."
    )

    with open(COMPLETED_FILE, "a") as file:
        file.write(str(project) + "\n")

    print("\nProject moved to Completed Projects.")

    print("\nUPDATED QUEUE")
    print("--------------------------")

    display_schedule()


# =====================================
# VIEW MENU
# =====================================

def view_menu():

    while True:

        print("\nVIEW PROJECTS")
        print("1. One Project")
        print("2. Completed Projects")
        print("3. All Projects")
        print("4. Back")

        choice = input("Enter Choice: ")

        if choice == "1":
            view_one_project()

        elif choice == "2":
            view_completed_projects()

        elif choice == "3":
            view_all_projects()

        elif choice == "4":
            break

        else:
            print("Invalid choice.")


# =====================================
# SCHEDULE MENU
# =====================================

def schedule_menu():

    while True:

        print("\nSCHEDULE PROJECTS")
        print("1. Create Schedule")
        print("2. View Updated Schedule")
        print("3. Back")

        choice = input("Enter Choice: ")

        if choice == "1":
            create_schedule()

        elif choice == "2":
            display_schedule()

        elif choice == "3":
            break

        else:
            print("Invalid choice.")


# =====================================
# MAIN MENU
# =====================================

def main():

    while True:

        print("\n====================================")
        print("COPY TYPING PROJECT SCHEDULER")
        print("====================================")

        print("1. Input Project Details")
        print("2. View Projects")
        print("3. Schedule Projects")
        print("4. Get a Project")
        print("5. Exit")

        choice = input("\nEnter Choice: ")

        if choice == "1":
            add_project()

        elif choice == "2":
            view_menu()

        elif choice == "3":
            schedule_menu()

        elif choice == "4":
            get_project()

        elif choice == "5":
            print("\nProgram terminated.")
            break

        else:
            print("Invalid choice.")


# =====================================
# RUN PROGRAM
# =====================================

main()