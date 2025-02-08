
function navigation() {
    const username = document.getElementById('username').value;
    const password = document.getElementById("password").value;
    let urlname = username +"-"+ password;
    window.location.href = `http://127.0.0.1:8000/verification_check/${urlname}`;
}