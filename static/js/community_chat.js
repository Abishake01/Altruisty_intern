let id_ref
document.addEventListener("DOMContentLoaded", function () {
    id_ref = document.getElementById('user').innerText
    console.log(id_ref)

});

async function search() {
    const searchTerm = document.getElementById('search-input').value
    console.log(searchTerm)
    const d = new FormData()
    d.append("query", searchTerm)
    d.append("uid", sessionStorage.getItem('user_id'))

    const url = `http://127.0.0.1:8000/search_community/${id_ref}/${searchTerm}`
    document.getElementById('search-input').value = ""
    window.location.href = url
}
function getFormattedTimestamp() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const milliseconds = String(now.getMilliseconds()).padStart(3, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;
}
async function edit(messageId) {
    const messageElement = document.getElementById(`mc${messageId}`);
    const currentMessage = messageElement.innerText;
    const newMessage = prompt("Enter new message", currentMessage);

    if (!newMessage || newMessage.trim() === "") {
        alert("Message cannot be empty!");
        return;
    }

    const url = "http://127.0.0.1:8000/edit_content/";
    try {
        const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify({ mess_id: messageId, nc: newMessage }),
            headers: { "Content-Type": "application/json" },
        });

        if (response.ok) {
            messageElement.innerText = newMessage;
            alert("Message updated successfully!");
        } else {
            const errorText = await response.text();
            alert(`Error: ${errorText}`);
        }
    } catch (err) {
        console.error("Error:", err);
        alert("An error occurred. Please try again.");
    }
}

function getFormattedTimestamp2() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const milliseconds = String(now.getMilliseconds()).padStart(3, '0');
    return `${year}${month}${day}_${hours}${minutes}${seconds}${milliseconds}`;
}

document.addEventListener("DOMContentLoaded", async () => {
    const chatWindow = document.getElementById("chat-window");
    const chatContents = document.getElementById("chat-window-contents");
    const composeBox = document.getElementById("compose-chat-box");
    const sendIcon = document.getElementById("sendicon");
    let currentCommunityId = null;
    let socket = null;

    // Community Tile Click

    console.log(sessionStorage.getItem('comm_id'))
    currentCommunityId = sessionStorage.getItem('comm_id')
    const url = `http://127.0.0.1:8000/community_data/${currentCommunityId}`;

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        const data = await response.json();

        chatWindow.style.visibility = "visible";
        document.getElementById("comm_title1").textContent = data.data[0]?.community_name || "Unnamed";
        document.getElementById("comm_creator").textContent = data.data[0]?.creator_id || "Unknown Creator";
        document.getElementById("commid").textContent = data.data[0]?.community_id || "Unknown";

        chatContents.innerHTML = "";
        if (data.messdata && data.messdata.length > 0) {
            renderMessages(data.messdata);
        } else {
            chatContents.innerHTML = "<p>No messages yet.</p>";
        }

        setupWebSocket(currentCommunityId);
    } catch (err) {
        console.error("Error fetching community data:", err);
    }



    function renderMessages(messages) {
        messages.forEach(msg => {
            const messageDiv = document.createElement("div");
            messageDiv.className = "chat-message-group";

            const isOwnMessage = msg.user_id === id_ref;
            const containerClass = isOwnMessage ? "chat-message-container" : "chat-message-container-receive";

            messageDiv.innerHTML = `
            <div class="${containerClass}">
                <div class="chat-messages">
                    <div class="chat-message-sender"style="color:rgba(221, 242, 71, 0.8)">${msg.user_id || "Unknown User"}
                        <span style="visibility:hidden">${msg.message_id}</span>
                        ${isOwnMessage && msg.content_type === 'text' ? `<i onclick="return edit('${msg.message_id}')" class="fas fa-ellipsis-v"></i>` : ""}
                    </div>

                    ${msg.content_type === "text"
                    ? `<span class="chat-message-content" id="mc${msg.message_id}" style="color:white;font-size:25px">
                            ${msg.messagecontent || ""}
                          </span><br/>`
                    : msg.media_content
                        ? `<img src="http://127.0.0.1:8000/media/${msg.media_content}" style="height:300px;width:auto" alt="Media"><br/>`
                        : "<p style='color:gray;'>Unsupported content type</p>"}
                    <span class="chat-message-time">${msg.sent_date || ""}</span>
                </div>
            </div>`;
            chatContents.appendChild(messageDiv);
        });
    }

    // WebSocket Setup
    function setupWebSocket(communityId) {
        if (socket) {
            socket.close();
        }

        socket = new WebSocket(`ws://127.0.0.1:8000/ws/community/${communityId}/`);

        socket.onopen = () => {
            console.log("WebSocket connection established");
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.content_type && data.user_id && data.messagecontent !== undefined) {
                renderMessages([data]);
            } else {
                console.warn("Unexpected message format:", data);
            }
        };

        socket.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        socket.onclose = (event) => {
            console.log("WebSocket connection closed:", event.reason || "Unknown reason");
        };
    }

    // Send Message
    sendIcon.addEventListener("click", async () => {
        const messageContent = composeBox.value.trim();
        if (!messageContent || !currentCommunityId) return;

        const commId = document.getElementById("commid").textContent;
        const url = "http://127.0.0.1:8000/community_chat/";
        const message_id = id_ref + commId + getFormattedTimestamp2();

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message_id: message_id,
                    chat: messageContent,
                    send_id: id_ref,
                    community_id: commId,
                    contenttype: "text",
                    sent_date: getFormattedTimestamp()
                }),
            });

            if (!response.ok) throw new Error(`Error: ${response.status}`);
            const result = await response.json();
            console.log("Message sent:", result);

            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
                    message_id: message_id,
                    chat_message: messageContent,
                    send_id: id_ref,
                    community_id: commId,
                    contenttype: "text",
                    sent_date: getFormattedTimestamp()
                }));
            } else {
                console.log("WebSocket not open, message not sent to other users.");
            }

            composeBox.value = "";
        } catch (err) {
            console.error("Error sending message:", err);
        }
    });

    // Edit Message

});

function navigate() {
    const comid = document.getElementById("commid").innerHTML;
    window.location.href = `http://127.0.0.1:8000/mediapost/${id_ref}/${comid}`;
}

function info() {
    const comid = document.getElementById("commid").innerHTML;
    window.location.href = `http://127.0.0.1:8000/community_info/${comid}`;
}

function edit2() {
    const pk = id_ref;
    const comid = document.getElementById("commid").innerHTML;
    window.location.href = `http://127.0.0.1:8000/view_media/${pk}/${comid}`;
}

function filterMediaMessages() {
    const chatMessages = document.querySelectorAll(".chat-message-group");
    chatMessages.forEach((message) => {
        const imgElement = message.querySelector("img");
        message.style.display = imgElement ? "flex" : "none";
    });
}

