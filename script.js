// Initialize default array of task objects containing id, title, and completion status
let tasks = [
    { id: 1, title: "study", completed: false },
    { id: 2, title: "futsal", completed: false }
];

// Set default active tab filter state to 'all'
let currentTab = 'all';

// Attach event listener to execute renderTasks once the HTML document finishes loading
document.addEventListener("DOMContentLoaded", renderTasks);

// Main function responsible for rendering tasks to the DOM
function renderTasks() {
    // Get reference to the task list unordered element
    const taskList = document.getElementById("taskList");
    // Clear all existing HTML content inside the task list container
    taskList.innerHTML = "";

    // Initialize variable to hold list of filtered tasks defaulting to all tasks
    let filteredTasks = tasks;
    // Check if current tab filter is set to active items
    if (currentTab === 'active') {
        // Filter tasks array to keep only incomplete items
        filteredTasks = tasks.filter(t => !t.completed);
    // Check if current tab filter is set to completed items
    } else if (currentTab === 'completed') {
        // Filter tasks array to keep only completed items
        filteredTasks = tasks.filter(t => t.completed);
    }

    // Loop through each task object in the filtered tasks array
    filteredTasks.forEach(task => {
        // Create a new list item element for the task
        const li = document.createElement("li");
        // Add 'completed' class to list item if task status is completed
        if (task.completed) li.classList.add("completed");

        // Set the internal HTML structure for the list item element
        li.innerHTML = `
            <div class="task-left" onclick="toggleTask(${task.id})">
                <span class="custom-checkbox"></span>
                <span class="task-text">${escapeHtml(task.title)}</span>
            </div>
            <button class="delete-btn" onclick="deleteTask(${task.id})">&times;</button>
        `;
        // Append constructed list item element into task list DOM element
        taskList.appendChild(li);
    });

    // Count total number of incomplete active tasks
    const activeCount = tasks.filter(t => !t.completed).length;
    // Update counter display text with correct pluralization handling
    document.getElementById("itemCount").textContent = `${activeCount} active item${activeCount !== 1 ? 's' : ''} left`;
}

// Function to create and add a new task item
function addTask() {
    // Get reference to the task input field element
    const input = document.getElementById("taskInput");
    // Retrieve input field value and trim leading/trailing whitespace
    const title = input.value.trim();

    // Verify that the trimmed input string is not empty
    if (title !== "") {
        // Construct new task object with timestamp ID, input title, and false completion status
        const newTask = {
            id: Date.now(),
            title: title,
            completed: false
        };
        // Add newly created task object to tasks array
        tasks.push(newTask);
        // Clear input text field after addition
        input.value = "";
        // Re-render task list display
        renderTasks();
    }
}

// Keydown event handler function checking for Enter key press
function handleKeyPress(event) {
    // Check if key pressed matches the Enter key
    if (event.key === "Enter") {
        // Trigger addTask function on Enter key press
        addTask();
    }
}

// Function toggling completed status of a task by ID
function toggleTask(id) {
    // Return new tasks array with target task's completed flag inverted
    tasks = tasks.map(task => 
        task.id === id ? { ...task, completed: !task.completed } : task
    );
    // Re-render task list with updated state
    renderTasks();
}

// Function deleting a single task item matching specified ID
function deleteTask(id) {
    // Filter out target task object from tasks array by ID
    tasks = tasks.filter(task => task.id !== id);
    // Re-render task list display
    renderTasks();
}

// Function switching active tab navigation and applying filter state
function switchTab(tabName) {
    // Store newly selected tab filter name
    currentTab = tabName;
    // Remove 'active' class from all tab navigation elements
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    // Add 'active' class to newly selected tab element
    document.getElementById(`tab-${tabName}`).classList.add('active');
    // Re-render task list according to selected tab filter
    renderTasks();
}

// Function removing all completed tasks from storage array
function clearCompleted() {
    // Retain only incomplete task elements inside tasks array
    tasks = tasks.filter(t => !t.completed);
    // Re-render task list display
    renderTasks();
}

// Helper function converting HTML special characters into safe HTML entities
function escapeHtml(text) {
    // Return sanitized text string replacing HTML unsafe characters
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}