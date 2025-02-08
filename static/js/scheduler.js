
    function confirmDelete() {
        return confirm("Are you sure you want to delete this task?");
    }
    
    function openRescheduleModal(taskId) {
        document.querySelector('.modal').style.display = 'flex';
        document.querySelector('#taskId').value = taskId;
    }

    function closeRescheduleModal() {
        document.querySelector('.modal').style.display = 'none';
    }
