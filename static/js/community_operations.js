async function unfollow(messageId) {
    // Get the current message

    console.log(messageId)
    // Prepare the data
    const formData = new FormData();
    formData.append("to_id", messageId);
    formData.append("uid", sessionStorage.getItem('user_id'));

    // Send the data to the server
    const url = "http://127.0.0.1:8000/unfollow_user/";
    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData,
        });

        // Handle response
        if (response.ok) {
            // Update the message in the DOM
            alert(`unfollowing the user,${messageId}`);
        } else {
            const errorText = await response.text();
            alert(`Error: ${errorText}`);
        }
    } catch (err) {
        console.error("Error:", err);
        alert("An error occurred. Please try again.");
    }
}

async function leavecomm(messageId) {
    // Get the current message

    console.log(messageId)
    // Prepare the data
    const formData = new FormData();
    formData.append("community_id", messageId);
    formData.append("uid", sessionStorage.getItem('user_id'));

    // Send the data to the server
    const url = "http://127.0.0.1:8000/exitcommunity/";
    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData,
        });

        // Handle response
        if (response.ok) {
            // Update the message in the DOM
            alert(`successfully removed from the group`);
        } else {
            const errorText = await response.text();
            alert(`Error: ${errorText}`);
        }
    } catch (err) {
        console.error("Error:", err);
        alert("An error occurred. Please try again.");
    }
}

async function join(messageId) {
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

async function follownewuser(messageId) {
    // Get the current message

    console.log(messageId)
    // Prepare the data
    const formData = new FormData();
    formData.append("to_id", messageId);
    formData.append("uid", sessionStorage.getItem('user_id'));

    // Send the data to the server
    const url = "http://127.0.0.1:8000/follow_user/";
    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData,
        });

        // Handle response
        if (response.ok) {
            // Update the message in the DOM
            alert(`following the user,${messageId}`);
        } else {
            const errorText = await response.text();
            alert(`Error: ${errorText}`);
        }
    } catch (err) {
        console.error("Error:", err);
        alert("An error occurred. Please try again.");
    }
}