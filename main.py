import os
import subprocess

import customtkinter
from customtkinter import CTkLabel, CTkButton, CTkFrame, CTk

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = CTk()  # create CTk window like you do with the Tk window
app.title("NxtBSTweaker")
app.geometry("750x450")

# Configure the grid to make the main content frame expand
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Create the left sidebar frame
sidebar_frame = CTkFrame(master=app, width=200, corner_radius=0)
sidebar_frame.grid(row=0, column=0, sticky="ns")

# Add widgets to the sidebar
main_label = CTkLabel(master=sidebar_frame, text="BlueStacks 5", font=("Arial", 24), width=250)
main_label.pack(pady=(20, 5), padx=20)
mainbase_label = CTkLabel(master=sidebar_frame, text="                         - Engines")
mainbase_label.pack(pady=(0, 5), padx=20)

# Create the main content frame
main_content_frame = CTkFrame(master=app, corner_radius=0)
main_content_frame.grid(row=0, column=1, sticky="nsew")

# Add widgets to the main content area
main_label = CTkLabel(master=main_content_frame, text="NxtBSTweaker", font=("Arial", 24))
author_label = CTkLabel(master=main_content_frame, text="- Project By NXTGENCAT")
main_label.pack(pady=(20, 5), padx=20)
author_label.pack(pady=(0, 5), padx=20)

# Add Root and Unroot buttons initially hidden
unlock_button = CTkButton(master=main_content_frame, text="Unlock")
root_button = CTkButton(master=main_content_frame, text="Root")
unroot_button = CTkButton(master=main_content_frame, text="Unroot")
lock_button = CTkButton(master=main_content_frame, text="Lock")
output_label = CTkLabel(master=main_content_frame, text="")


# Function to display engine buttons
def display_engine_buttons(engine_names):
    for engine_name in engine_names:
        engine_button = CTkButton(master=sidebar_frame, text=engine_name,
                                  command=lambda name=engine_name: button_function(name))
        engine_button.pack(pady=10, padx=20)


def button_function(engine_name):
    # Update main content with the engine name
    main_label.configure(text=f"{engine_name} Actions")

    # Show Root and Unroot buttons
    unlock_button.configure(command=lambda: unlock_bluestacks(engine_name))
    root_button.configure(command=lambda: root_engine(engine_name))
    unroot_button.configure(command=lambda: unroot_engine(engine_name))
    lock_button.configure(command=lambda: lock_bluestacks(engine_name))

    unlock_button.pack(pady=10, padx=20)
    root_button.pack(pady=10, padx=20)
    unroot_button.pack(pady=10, padx=20)
    lock_button.pack(pady=10, padx=20)
    output_label.pack()

    lock_status(engine_name)


def get_engines():
    # Directory path
    directory = r'C:\ProgramData\BlueStacks_nxt\Engine'

    # List of prefixes to check for
    prefixes = ['Nougat64', 'Pie64', 'Rvc64']

    engines = []

    # Check if the directory exists
    if os.path.exists(directory):
        # Iterate through the directories in the specified path
        for dir_name in os.listdir(directory):
            # Check if the directory starts with any of the specified prefixes
            if any(dir_name.startswith(prefix) for prefix in prefixes):
                engines.append(dir_name)

    return engines


def lock_status(engine):
    # Define the file path
    file_path = r'C:\ProgramData\BlueStacks_nxt\bluestacks.conf'

    # Check if the file exists
    if os.path.exists(file_path):
        # Read the contents of the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Check if the lock status is present in the file
        root_status = False
        for line in lines:
            if f'bst.instance.{engine}.enable_root_access="1"' in line:
                root_status = True
                break

        # Print the lock status
        if root_status:
            logger(f"The engine '{engine}' is unlocked.")
        else:
            logger(f"The engine '{engine}' is locked.")
    else:
        logger("No BlueStacks config found.")


def lock_bluestacks(engine):
    file_path = r'C:\ProgramData\BlueStacks_nxt\bluestacks.conf'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if 'bst.feature.rooting="1"' in line:
                lines[i] = 'bst.feature.rooting="0"\n'  # Changed to 0

        with open(file_path, 'w') as file:
            file.writelines(lines)

        logger(f"The engine '{engine}' is locked successfully.")
    else:
        logger("No BlueStacks config found.")


def unlock_bluestacks(engine):
    file_path = r'C:\ProgramData\BlueStacks_nxt\bluestacks.conf'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if 'bst.feature.rooting="0"' in line:
                lines[i] = 'bst.feature.rooting="1"\n'  # Changed to 0
            if f'bst.instance.{engine}.enable_root_access="0"' in line:
                lines[i] = f'bst.instance.{engine}.enable_root_access="1"\n'  # Changed to 0

        with open(file_path, 'w') as file:
            file.writelines(lines)

        print(f"The engine '{engine}' is unlocked successfully.")
        output_label.configure(text=f"The engine '{engine}' is unlocked successfully.")
    else:
        print("No BlueStacks config found.")
        output_label.configure(text="No BlueStacks config found.")


def check_root_status(engine):
    directory = rf'C:\ProgramData\BlueStacks_nxt\Engine\{engine}'
    files_to_check = ['Android.bstk.in', f'{engine}.bstk']

    rooted = False

    for filename in files_to_check:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            print(f"Checking file: {file_path}")  # Debugging print
            lines = file.readlines()
            for i, line in enumerate(lines):
                if 'location="fastboot.vdi"' in line or 'location="Root.vhd"' in line:
                    if 'type="Normal"' in line:
                        rooted = True
                    break

    if rooted:
        print(f"The engine '{engine}' is rooted.")
        output_label.configure(text=f"The engine '{engine}' is rooted.")
    else:
        print(f"The engine '{engine}' is not rooted.")
        output_label.configure(text=f"The engine '{engine}' is not rooted.")


def root_engine(engine):
    directory = rf'C:\ProgramData\BlueStacks_nxt\Engine\{engine}'
    print("Processing files..")  # Print file path for debugging

    # Function to modify files
    def modify_files(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Perform replacements
        for i, line in enumerate(lines):
            if 'location="fastboot.vdi"' in line or 'location="Root.vhd"' in line:
                lines[i] = line.replace('type="Readonly"', 'type="Normal"')

        with open(file_path, 'w') as file:
            file.writelines(lines)

    # Files to be modified
    files_to_modify = ['Android.bstk.in', f'{engine}.bstk']

    # Iterate through files in the directory
    for filename in files_to_modify:
        file_path = os.path.join(directory, filename)
        modify_files(file_path)
    print(f"{engine} is Rooted.")  # Print file path for debugging
    output_label.configure(text=f"{engine} is Rooted.")


def unroot_engine(engine):
    directory = rf'C:\ProgramData\BlueStacks_nxt\Engine\{engine}'
    file_path = r'C:\ProgramData\BlueStacks_nxt\bluestacks.conf'

    print("Processing files..")  # Print file path for debugging

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if f'bst.instance.{engine}.enable_root_access="1"' in line:
                lines[i] = f'bst.instance.{engine}.enable_root_access="0"\n'  # Changed to 0

        with open(file_path, 'w') as file:
            file.writelines(lines)
    else:
        print("No BlueStacks config found.")
        output_label.configure(text="No BlueStacks config found.")

    # Function to modify files
    def modify_files(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Perform replacements
        for i, line in enumerate(lines):
            if 'location="fastboot.vdi"' in line or 'location="Root.vhd"' in line:
                lines[i] = line.replace('type="Normal"', 'type="Readonly"')

        with open(file_path, 'w') as file:
            file.writelines(lines)

    # Files to be modified
    files_to_modify = ['Android.bstk.in', f'{engine}.bstk']

    # Iterate through files in the directory
    for filename in files_to_modify:
        file_path = os.path.join(directory, filename)
        modify_files(file_path)
    logger(f"{engine} is UnRooted.")


def get_instances():
    file_path = r'C:\ProgramData\BlueStacks_nxt\bluestacks.conf'

    if os.path.exists(file_path):
        instance_names = set()

        with open(file_path, 'r') as file:
            for line in file:
                if 'bst.instance.Nougat64' in line:
                    instance_names.add('Nougat64')
                elif 'bst.instance.Pie64' in line:
                    instance_names.add('Pie64')
                elif 'bst.instance.Rvc64' in line:
                    instance_names.add('Rvc64')

        return instance_names
    else:
        print("No BlueStacks config found.")
        return set()


def logger(text):
    print(text)  # Print file path for debugging
    output_label.configure(text=text)


# Get engine names using the function
engine_names = get_engines()

# Display engine buttons
display_engine_buttons(engine_names)

app.mainloop()
