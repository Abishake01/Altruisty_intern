
        let socket;
        document.addEventListener("DOMContentLoaded", () => {
            const communityId = "{{comm_id}}"; // Replace with dynamic community ID
            socket = new WebSocket(`ws://127.0.0.1:8000/ws/community/${communityId}/`);

            socket.onopen = () => {
                console.log("WebSocket connection established.");
            };

            socket.onerror = (error) => {
                console.error("WebSocket error:", error);
            };

            socket.onclose = (event) => {
                console.log("WebSocket connection closed:", event.reason || "Unknown reason");
            };
        });

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
            const mediatype = document.getElementById('mediatype').value;
            const fileInput = document.getElementById('postfile');
            const file = fileInput.files[0];

            // Replace these placeholders with actual values in your backend or JavaScript
            const userid = "{{userid}}";
            const commid = "{{comm_id}}";
            const url = "{% url 'community:mediapostupload' %}"; // Replace with the actual URL for saving the post
            let message_id = userid + commid + getFormattedTimestamp2();

            if (!file) {
                alert("File is not selected");
                return;
            }

            const formd = new FormData();
            formd.append('message_id', message_id);
            formd.append('caption', caption);
            formd.append('mediatype', mediatype);
            formd.append('file', file);
            formd.append('userid', userid);
            formd.append('commid', commid);

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    body: formd,
                });

                if (response.ok) {
                    const newdata = await response.json();
                    console.log(newdata);

                    // Notify WebSocket about the new post
                    if (socket && socket.readyState === WebSocket.OPEN) {
                        socket.send(JSON.stringify({
                            message_id: newdata.message_id, // Assuming this is returned by the server
                            chat_message: "", // No text message for media
                            send_id: userid,
                            community_id: commid,
                            contenttype: "Image",
                            media_content: newdata.file_path, // Assuming file_path is returned
                            media_caption: caption,
                            sent_date: newdata.sent_date
                        }));
                    }

                    alert("Successfully posted");
                } else {
                    console.error('Error in response:', response.statusText);
                    alert("Error in your upload, try again");
                }
            } catch (err) {
                console.log("Error:", err);
                alert("Error in your upload, try again");
            }
        }
    