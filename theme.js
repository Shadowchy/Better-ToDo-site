document.addEventListener('DOMContentLoaded', function () {
    // Theme Switcher Logic
    const themeToggleButtons = document.querySelectorAll('.theme-switcher a');

    themeToggleButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const theme = this.dataset.theme;
            document.body.className = theme;

            // Store the selected theme in localStorage
            localStorage.setItem('theme', theme);

            // Send an AJAX request to update the theme on the server
            fetch(`/theme/${theme}`);
        });
    });

    // Apply the theme stored in localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.body.className = savedTheme;
    }

    // Edit Task Modal Logic
    const editButtons = document.querySelectorAll('.edit-task');
    const editModal = document.getElementById('editModal');
    const editForm = document.getElementById('editTaskForm');
    const editTaskInput = document.getElementById('editTaskInput');
    const editTaskIdInput = document.getElementById('editTaskId');
    const closeModalButton = document.querySelector('.modal .close');

    editButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const taskId = this.dataset.taskId;
            const taskContent = this.dataset.task;
            editTaskInput.value = taskContent;
            editTaskIdInput.value = taskId;
            editModal.style.display = 'block';
        });
    });

    closeModalButton.addEventListener('click', function () {
        editModal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target == editModal) {
            editModal.style.display = 'none';
        }
    });
});
