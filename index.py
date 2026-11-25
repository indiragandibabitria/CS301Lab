import json  # Import built-in JSON module to handle reading and writing JSON files
import os  # Import OS module to check file system paths
import tkinter as tk  # Import Tkinter library for constructing the graphical user interface
from tkinter import messagebox  # Import messagebox dialogs for displaying alerts to the user

FILE_NAME = "tasks.json"  # Define constant for the JSON file storing task data


class TodoApp:  # Define main application class managing the To-Do app logic and UI
    def __init__(self, root):  # Constructor method initializing the application instance
        self.root = root  # Store reference to the main Tkinter window
        self.root.title("Simple To-Do App")  # Set title displayed on the application window frame
        self.root.geometry("450x600")  # Set initial width (450px) and height (600px) of window
        self.root.configure(bg="#081410")  # Set background color of the main window frame
        self.root.resizable(False, False)  # Disable window resizing along both width and height

        self.current_tab = "all"  # Initialize active view tab filter setting to 'all'
        self.tasks = self.load_tasks()  # Load saved tasks from JSON file upon initialization

        self.build_ui()  # Call method constructing layout and visual components
        self.render_tasks()  # Call method populating task list display

    def load_tasks(self):  # Helper method loading task data stored on disk
        if os.path.exists(FILE_NAME):  # Check if tasks storage file exists locally
            try:  # Attempt file read operations inside error handling block
                with open(FILE_NAME, "r") as file:  # Open JSON file in read mode
                    return json.load(file)  # Parse JSON content into Python list structure
            except json.JSONDecodeError:  # Handle empty or corrupted JSON file formats
                return []  # Return empty task list fallback if parsing fails
        return []  # Return empty list if task file does not exist yet

    def save_tasks(self):  # Helper method writing task list changes to disk
        with open(FILE_NAME, "w") as file:  # Open JSON file in overwrite mode
            json.dump(self.tasks, file, indent=2)  # Write tasks array formatted with 2 spaces indent

    def build_ui(self):  # Method assembling UI components and frame layouts
        # Title
        title_label = tk.Label(  # Instantiate label header element
            self.root, text="My Tasks", font=("Segoe UI", 22, "bold"),  # Set font properties and text
            fg="#34d399", bg="#081410"  # Set text color and background matching main frame
        )  # End label component definition
        title_label.pack(pady=(20, 2))  # Place header element with vertical spacing padding

        # Active item counter
        self.counter_label = tk.Label(  # Instantiate counter label displaying remaining active tasks
            self.root, text="0 active items left", font=("Segoe UI", 10),  # Set label default text and font
            fg="#6ee7b7", bg="#081410"  # Set text and background color schemes
        )  # End counter label component definition
        self.counter_label.pack(pady=(0, 15))  # Place counter label with bottom padding

        # Input Frame
        input_frame = tk.Frame(self.root, bg="#081410")  # Create sub-container frame holding task input controls
        input_frame.pack(fill="x", padx=25, pady=5)  # Expand frame horizontally with horizontal/vertical padding

        self.entry = tk.Entry(  # Instantiate text entry field for new tasks
            input_frame, font=("Segoe UI", 11), bg="#0b1411", fg="#e0f2fe",  # Set fonts and entry colors
            insertbackground="white", bd=1, relief="solid"  # Set cursor color, border width, and border style
        )  # End entry element configuration
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))  # Pack field stretching horizontally
        self.entry.bind("<Return>", lambda e: self.add_task())  # Bind Enter key press event to trigger task addition

        add_btn = tk.Button(  # Instantiate button triggering creation of new task entry
            input_frame, text="Add", font=("Segoe UI", 10, "bold"),  # Set button text label and bold font
            bg="#10b981", fg="#041611", activebackground="#059669",  # Set primary background/text and click states
            activeforeground="#ffffff", bd=0, relief="flat", command=self.add_task  # Remove borders and wire click event
        )  # End button element definition
        add_btn.pack(side="right", ipady=6, ipadx=15)  # Place button on right side with internal padding

        # Tabs Frame
        tabs_frame = tk.Frame(self.root, bg="#0b1411", bd=1, relief="solid")  # Container for filter tab navigation
        tabs_frame.pack(fill="x", padx=25, pady=15)  # Pack tabs bar full width with outer margins

        self.tab_all = tk.Button(  # Create navigation button filtering view to all items
            tabs_frame, text="All", font=("Segoe UI", 9, "bold"), fg="#10b981", bg="#122d23",  # Style active tab colors
            bd=0, relief="flat", command=lambda: self.switch_tab("all")  # Set click handler switching tab filter
        )  # End tab creation
        self.tab_all.pack(side="left", expand=True, fill="both", ipady=5)  # Layout tab equally across frame width

        self.tab_active = tk.Button(  # Create navigation button filtering view to incomplete items
            tabs_frame, text="Active", font=("Segoe UI", 9, "bold"), fg="#558574", bg="#0b1411",  # Style default inactive colors
            bd=0, relief="flat", command=lambda: self.switch_tab("active")  # Set click handler switching tab filter
        )  # End tab creation
        self.tab_active.pack(side="left", expand=True, fill="both", ipady=5)  # Layout tab equally across frame width

        self.tab_completed = tk.Button(  # Create navigation button filtering view to finished items
            tabs_frame, text="Completed", font=("Segoe UI", 9, "bold"), fg="#558574", bg="#0b1411",  # Style inactive state colors
            bd=0, relief="flat", command=lambda: self.switch_tab("completed")  # Set click handler switching tab filter
        )  # End tab creation
        self.tab_completed.pack(side="left", expand=True, fill="both", ipady=5)  # Layout tab equally across frame width

        # Listbox Frame
        list_frame = tk.Frame(self.root, bg="#081410")  # Container holding scrollable listbox area
        list_frame.pack(fill="both", expand=True, padx=25, pady=5)  # Allow container expansion in all directions

        self.listbox = tk.Listbox(  # Instantiate listbox widget rendering task list content
            list_frame, font=("Segoe UI", 11), bg="#0f1b17", fg="#cbd5e1",  # Set color theme and list font
            selectbackground="#10b981", selectforeground="#041611",  # Set highlight styling for user selections
            bd=1, relief="solid", highlightthickness=0, activestyle="none"  # Style borders and remove focus underline
        )  # End listbox widget declaration
        self.listbox.pack(side="left", fill="both", expand=True)  # Expand listbox widget across available space

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)  # Instantiate scrollbar for list
        scrollbar.pack(side="right", fill="y")  # Place scrollbar vertically along right border
        self.listbox.config(yscrollcommand=scrollbar.set)  # Sync listbox vertical scrolling with scrollbar handle

        self.listbox.bind("<Double-1>", lambda e: self.toggle_task())  # Bind double-click mouse action to toggle status

        # Action Buttons Frame
        action_frame = tk.Frame(self.root, bg="#081410")  # Container holding task manipulation buttons
        action_frame.pack(fill="x", padx=25, pady=(5, 15))  # Align frame across bottom margin area

        delete_btn = tk.Button(  # Instantiate button removing single selected item
            action_frame, text="Delete Selected", font=("Segoe UI", 9, "bold"),  # Set font and text label
            bg="#ef4444", fg="white", bd=0, relief="flat", command=self.delete_task  # Apply danger theme colors and handler
        )  # End delete button declaration
        delete_btn.pack(side="left", ipady=6, ipadx=10)  # Align button to left edge with internal padding

        clear_btn = tk.Button(  # Instantiate button removing all completed items
            action_frame, text="Clear Completed", font=("Segoe UI", 9, "bold"),  # Set font and text label
            bg="#0b1411", fg="#6ee7b7", bd=1, relief="solid", command=self.clear_completed  # Apply outline styling and handler
        )  # End clear button declaration
        clear_btn.pack(side="right", ipady=6, ipadx=10)  # Align button to right edge with internal padding

    def get_filtered_tasks(self):  # Helper method returning tasks matching current tab view state
        if self.current_tab == "active":  # Check if filter active tab is selected
            return [t for t in self.tasks if not t["completed"]]  # Return list containing incomplete items only
        elif self.current_tab == "completed":  # Check if filter completed tab is selected
            return [t for t in self.tasks if t["completed"]]  # Return list containing finished items only
        return self.tasks  # Default case returning entire task dataset

    def render_tasks(self):  # Update visual elements in listbox and status counters
        self.listbox.delete(0, tk.END)  # Clear all existing listbox entries
        filtered = self.get_filtered_tasks()  # Get subset of tasks corresponding to current tab view filter

        for task in filtered:  # Iterate over filtered task elements
            status = "✓ " if task["completed"] else "☐ "  # Choose visual checkbox symbol based on completion status
            self.listbox.insert(tk.END, f"  {status} {task['title']}")  # Insert formatted task string into listbox

        active_count = sum(1 for t in self.tasks if not t["completed"])  # Calculate number of remaining active tasks
        plural = "s" if active_count != 1 else ""  # Handle pluralization suffix for counter string formatting
        self.counter_label.config(text=f"{active_count} active item{plural} left")  # Update active item counter display

    def add_task(self):  # Logic method handling addition of new task items
        title = self.entry.get().strip()  # Retrieve input text field content and trim whitespace
        if title:  # Check that task title is non-empty
            new_task = {"id": len(self.tasks) + 1, "title": title, "completed": False}  # Build task dictionary object
            self.tasks.append(new_task)  # Append new task dictionary item into main list dataset
            self.save_tasks()  # Persist modified task list state to disk storage
            self.entry.delete(0, tk.END)  # Clear text entry input field
            self.render_tasks()  # Re-render list display to reflect additions

    def toggle_task(self):  # Logic method toggling completion status of highlighted task item
        try:  # Handle selection logic inside exception handler
            selected_idx = self.listbox.curselection()[0]  # Get index of currently selected entry in listbox
            filtered = self.get_filtered_tasks()  # Get tasks visible under current filter mode
            target_task = filtered[selected_idx]  # Locate target task object corresponding to selection

            for task in self.tasks:  # Search for matching item inside primary tasks array
                if task["id"] == target_task["id"]:  # Check for identifier match
                    task["completed"] = not task["completed"]  # Invert task completion boolean flag value
                    break  # Exit search loop upon matching item update

            self.save_tasks()  # Write updated status change to disk JSON file
            self.render_tasks()  # Re-render updated state to UI components
        except IndexError:  # Handle cases where user clicks listbox without selecting an item
            pass  # Do nothing on invalid click index

    def delete_task(self):  # Logic method removing selected task from dataset
        try:  # Handle delete operations inside error protection block
            selected_idx = self.listbox.curselection()[0]  # Retrieve index of item highlighted in UI listbox
            filtered = self.get_filtered_tasks()  # Fetch array of currently displayed elements
            target_task = filtered[selected_idx]  # Map selection index to target task object

            self.tasks = [t for t in self.tasks if t["id"] != target_task["id"]]  # Exclude selected item from tasks list
            self.save_tasks()  # Save remaining task entries to persistent storage
            self.render_tasks()  # Refresh user display to reflect removal
        except IndexError:  # Trigger error warning dialog if no element is selected during deletion attempt
            messagebox.showinfo("Select Task", "Please select a task from the list to delete.")  # Show warning dialog popup

    def clear_completed(self):  # Logic method removing all completed tasks from storage
        self.tasks = [t for t in self.tasks if not t["completed"]]  # Retain only incomplete task elements in list
        self.save_tasks()  # Persist filtered array changes to JSON file
        self.render_tasks()  # Update interface controls and display state

    def switch_tab(self, tab_name):  # UI method updating state when navigating filter tabs
        self.current_tab = tab_name  # Update current active filter variable state
        self.tab_all.config(bg="#0b1411", fg="#558574")  # Reset All tab button visual theme to inactive state
        self.tab_active.config(bg="#0b1411", fg="#558574")  # Reset Active tab button visual theme to inactive state
        self.tab_completed.config(bg="#0b1411", fg="#558574")  # Reset Completed tab button visual theme to inactive state

        if tab_name == "all":  # Highlight All tab if selected
            self.tab_all.config(bg="#122d23", fg="#10b981")  # Apply active styling highlight
        elif tab_name == "active":  # Highlight Active tab if selected
            self.tab_active.config(bg="#122d23", fg="#10b981")  # Apply active styling highlight
        elif tab_name == "completed":  # Highlight Completed tab if selected
            self.tab_completed.config(bg="#122d23", fg="#10b981")  # Apply active styling highlight

        self.render_tasks()  # Re-render task view according to newly selected tab filter


if __name__ == "__main__":  # Check if python file is executed as the primary main program
    root = tk.Tk()  # Instantiate main root window application context
    app = TodoApp(root)  # Instantiate To-Do application instance passing root window reference
    root.mainloop()  # Run Tkinter main event loop listening for user interaction