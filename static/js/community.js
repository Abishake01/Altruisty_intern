user_ref = sessionStorage.getItem('user_id')

console.log(sessionStorage.getItem('user_id'))
function navigate() {
    window.location.href = `http://127.0.0.1:8000/community_list/${user_ref}`
}
function getFormattedTimestamp2() {
    const now = new Date();

    // Get date components
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(now.getDate()).padStart(2, '0');

    // Get time components
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const milliseconds = String(now.getMilliseconds()).padStart(3, '0');

    // Combine into the desired format
    return `${year}${month}${day}_${hours}${minutes}${seconds}${milliseconds}`;
}
async function savepost() {
    const caption = document.getElementById('postcaption').value;

    const fileInput = document.getElementById('postfile');
    const file = fileInput.files[0];

    // Replace these placeholders with actual values in your backend or JavaScript
    const userid = user_ref;
    const url = "http://127.0.0.1:8000/generalpostupload/"; // Replace with the actual URL for saving the post
    const pm = "PM"
    let post_id = pm + userid + getFormattedTimestamp2();

    if (!file) {
        alert("File is not selected");
        return;
    }

    const formd = new FormData();
    formd.append('post_id', post_id);
    formd.append('caption', caption);
    formd.append('file', file);
    formd.append('userid', userid);

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formd,
        });

        if (response.ok) {
            const newdata = await response.json();
            console.log(newdata);

            alert("Successfully posted");
            window.location.href = `http://127.0.0.1:8000/community_home/`
        } else {
            console.error('Error in response:', response.statusText);
            alert("Error in your upload, try again");
            window.location.href = `http://127.0.0.1:8000/community_home/`
        }
    } catch (err) {
        console.log("Error:", err);
        alert("Error in your upload, try again");
        window.location.href = `http://127.0.0.1:8000/community_home/`
    }
}
function navigatetochat(commid) {
    sessionStorage.setItem('comm_id', commid)
    
    window.location.href = `http://127.0.0.1:8000/community_list/`


}

function search_user() {
    text = document.getElementById("search").value;
    window.location.href = `http://127.0.0.1:8000/find_user/${text}`

}
async function edit(messageId) {
    // Get the current message


    // Prepare the data
    const formData = new FormData();
    formData.append("community_id", messageId);
    formData.append("uid", sessionStorage.getItem('user_id'));

    // Send the data to the server
    const url = "http://127.0.0.1:8000/add_member/";
    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData,
        });

        // Handle response
        if (response.ok) {
            // Update the message in the DOM
            alert("Added to community");
        } else {
            const errorText = await response.text();
            alert(`Error: ${errorText}`);
        }
    } catch (err) {
        console.error("Error:", err);
        alert("An error occurred. Please try again.");
    }
}
async function search() {
    const searchTerm = document.getElementById('search-input').value
    console.log(searchTerm)
    const d = new FormData()
    d.append("query", searchTerm)
    d.append("uid", sessionStorage.getItem('user_id'))
    const url = `http://127.0.0.1:8000/search_community/${user_ref}/${searchTerm}`
    document.getElementById('search-input').value = ""
    window.location.href = url
}

async function search() {
    const searchTerm = document.getElementById('search-input').value
    console.log(searchTerm)
    const d = new FormData()
    d.append("query", searchTerm)
    d.append("uid", sessionStorage.getItem('user_id'))
    const url = `http://127.0.0.1:8000/search_community/${user_ref}/${searchTerm}`
    document.getElementById('search-input').value = ""
    window.location.href = url
}
async function findcomm(data) {

    const d = new FormData()
    d.append("query", data)
    d.append("uid", sessionStorage.getItem('user_id'))
    const url = `http://127.0.0.1:8000/search_community/${user_ref}/${searchTerm}`
    document.getElementById('search-input').value = ""
    window.location.href = url
}

