
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

function Reassign(taskId) {
    document.querySelector('.modal1').style.display = 'flex';
    document.querySelector('#taskId1').value = taskId;
}

function history(taskId) {
 window.location.href = `http://127.0.0.1:8000/history/${taskId}`
    
}

function closeReassignModal() {
    document.querySelector('.modal1').style.display = 'none';
}