document.addEventListener('DOMContentLoaded', function () {
    user_id=document.getElementById('user_id').innerHTML
    sessionStorage.setItem('user_id',  user_id);
});