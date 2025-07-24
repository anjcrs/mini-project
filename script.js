// Task management system
let tasks = [];
let currentFilter = 'all';

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    loadTasks();
    renderTasks();
    updateTaskCount();
    
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('dateInput').value = today;
    
    // Add Enter key support for task input
    document.getElementById('taskInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTask();
        }
    });
});

// Add new task
function addTask() {
    const taskInput = document.getElementById('taskInput');
    const dateInput = document.getElementById('dateInput');
    
    const taskName = taskInput.value.trim();
    const dueDate = dateInput.value;
    
    if (!taskName) {
        showNotification('Please enter a task name!', 'error');
        return;
    }
    
    if (!dueDate) {
        showNotification('Please select a due date!', 'error');
        return;
    }
    
    const newTask = {
        id: Date.now(),
        name: taskName,
        dueDate: dueDate,
        completed: false,
        createdAt: new Date().toISOString()
    };
    
    tasks.unshift(newTask); // Add to beginning for newest first
    saveTasks();
    renderTasks();
    updateTaskCount();
    
    // Clear inputs
    taskInput.value = '';
    dateInput.value = new Date().toISOString().split('T')[0];
    
    showNotification('Task added successfully! ✨', 'success');
}

// Toggle task completion
function toggleTask(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        saveTasks();
        renderTasks();
        updateTaskCount();
        
        const message = task.completed ? 'Task completed! 🎉' : 'Task marked as pending! 📝';
        showNotification(message, 'success');
    }
}

// Delete task
function deleteTask(id) {
    const taskElement = document.querySelector(`[data-id="${id}"]`);
    
    if (taskElement) {
        taskElement.classList.add('task-exit');
        
        setTimeout(() => {
            tasks = tasks.filter(t => t.id !== id);
            saveTasks();
            renderTasks();
            updateTaskCount();
            showNotification('Task deleted! 🗑️', 'success');
        }, 400);
    }
}

// Filter tasks
function filterTasks(filter) {
    currentFilter = filter;
    
    // Update active filter button
    document.querySelectorAll('.btn-secondary').forEach(btn => {
        btn.style.opacity = '0.7';
        btn.style.transform = 'scale(1)';
    });
    
    event.target.style.opacity = '1';
    event.target.style.transform = 'scale(1.05)';
    
    renderTasks();
}

// Render tasks to DOM
function renderTasks() {
    const tasksList = document.getElementById('tasksList');
    let filteredTasks = [];
    
    switch (currentFilter) {
        case 'completed':
            filteredTasks = tasks.filter(t => t.completed);
            break;
        case 'pending':
            filteredTasks = tasks.filter(t => !t.completed);
            break;
        default:
            filteredTasks = tasks;
    }
    
    if (filteredTasks.length === 0) {
        tasksList.innerHTML = `
            <div class="empty-state">
                <div class="empty-pixel-art"></div>
                <p>${currentFilter === 'all' ? 'NO TASKS YET!' : `NO ${currentFilter.toUpperCase()} TASKS!`}</p>
                <p style="font-size: 6px; margin-top: 10px;">
                    ${currentFilter === 'all' ? 'Add your first task above' : `Switch to "ALL" to see other tasks`}
                </p>
            </div>
        `;
        return;
    }
    
    tasksList.innerHTML = filteredTasks.map(task => {
        const dueDate = new Date(task.dueDate);
        const today = new Date();
        const isOverdue = dueDate < today && !task.completed;
        
        return `
            <div class="task-item ${task.completed ? 'completed' : ''} task-enter" data-id="${task.id}">
                <div class="task-content">
                    <div class="task-info">
                        <div class="task-name ${task.completed ? 'completed' : ''}">${task.name}</div>
                        <div class="task-date" style="color: ${isOverdue ? '#FF6B6B' : 'var(--dark-text)'}">
                            📅 ${formatDate(task.dueDate)} ${isOverdue ? '(OVERDUE!)' : ''}
                        </div>
                    </div>
                    <div class="task-actions">
                        <button class="btn btn-secondary" onclick="toggleTask(${task.id})">
                            ${task.completed ? 'UNDO' : 'DONE'}
                        </button>
                        <button class="btn btn-danger" onclick="deleteTask(${task.id})">
                            DELETE
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Update task counter
function updateTaskCount() {
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(t => t.completed).length;
    const pendingTasks = totalTasks - completedTasks;
    
    const taskCountElement = document.getElementById('taskCount');
    
    let countText = '';
    switch (currentFilter) {
        case 'completed':
            countText = `${completedTasks} COMPLETED`;
            break;
        case 'pending':
            countText = `${pendingTasks} PENDING`;
            break;
        default:
            countText = `${totalTasks} TOTAL TASKS`;
    }
    
    taskCountElement.textContent = countText;
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    };
    return date.toLocaleDateString('en-US', options);
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    // Hide notification after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Save tasks to localStorage (in a real environment)
// For demo purposes, we'll use a simple array in memory
function saveTasks() {
    // In a real browser environment, you would use:
    // localStorage.setItem('pixelTasks', JSON.stringify(tasks));
    
    // For this demo, tasks are stored in memory only
    console.log('Tasks saved:', tasks);
}

// Load tasks from localStorage (in a real environment)
function loadTasks() {
    // In a real browser environment, you would use:
    // const savedTasks = localStorage.getItem('pixelTasks');
    // if (savedTasks) {
    //     tasks = JSON.parse(savedTasks);
    // }
    
    // For this demo, we'll start with sample tasks
    if (tasks.length === 0) {
        tasks = [
            {
                id: 1,
                name: "Complete the pixel art todo app",
                dueDate: new Date().toISOString().split('T')[0],
                completed: false,
                createdAt: new Date().toISOString()
            },
            {
                id: 2,
                name: "Learn more JavaScript animations",
                dueDate: new Date(Date.now() + 86400000).toISOString().split('T')[0], // Tomorrow
                completed: true,
                createdAt: new Date().toISOString()
            }
        ];
    }
}