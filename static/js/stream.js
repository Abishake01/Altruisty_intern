const APP_ID = "5be627cf59014fd2b76efbaa7eb0760a";
const TOKEN = sessionStorage.getItem("token");
const CHANNEL = sessionStorage.getItem("room");
let UID = Number(sessionStorage.getItem("UID"));

console.log("Stream.js connected!!");
console.log("Channel:", CHANNEL);
console.log("UID:", UID);
console.log("Token:", TOKEN);

const client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });

let localTrack = [];
let remoteUser = {};

let handleUserJoined = async (user, mediaType) => {
  console.log("User joined:", user.uid, "Media type:", mediaType);

  remoteUser[user.uid] = user;

  await client.subscribe(user, mediaType);

  if (mediaType === "video") {
    // Check if a container already exists for this user and remove it if it does
    let player = document.getElementById(`user-container-${user.uid}`);
    if (player != null) {
      player.remove();
    }

    try {
      // Fetch user details
      let member = await getMember(user);

      // Create a new video container
      player = `
              <div class="video-container" id="user-container-${user.uid}">
                  <div class="video-player" id="user-${user.uid}"></div>
                  <div class="username-wrapper">
                      <span class="user-name">${member.name}</span>
                  </div>
              </div>`;

      const videoStreams = document.getElementById("video-streams");
      if (videoStreams) {
        videoStreams.insertAdjacentHTML("beforeend", player);
        console.log(`Video container added for user ${user.uid}`);
      } else {
        console.error(`Video streams container not found`);
      }

      // Play the video track
      if (user.videoTrack) {
        user.videoTrack.play(`user-${user.uid}`);
        console.log(`Playing video for user ${user.uid}`);
      } else {
        console.error(`No video track found for user ${user.uid}`);
      }
    } catch (err) {
      console.error(`Error handling video for user ${user.uid}:`, err);
    }
  }

  if (user.audioTrack) {
    user.audioTrack.play();
    console.log("Its working");
  } else {
    console.log("here is the problem");
  }
  if (mediaType === "audio") {
    user.audioTrack.play();
  }
};

let handleUserLeft = async (user) => {
  delete remoteUser[user.uid];
  document.getElementById(`user-container-${user.uid}`).remove();
};

let leaveAndRemoveLocalStream = async () => {
  for (let i = 0; i < localTrack.length > i; i++) {
    localTrack[i].stop();
    localTrack[i].close();
  }
  await client.leave();
  window.open("/", "_self");
};

let toggleCamera = async (e) => {
  const videoElement = document.getElementById(`user-${UID}`);
  const placeholderElement = document.getElementById(
    `video-placeholder-${UID}`
  );
  const name = document.querySelector(".username-wrapper");

  console.log("Looking for video element:", videoElement);
  console.log("Looking for placeholder element:", placeholderElement);

  if (localTrack[1].muted) {
    await localTrack[1].setMuted(false);
    videoElement.style.display = "block";
    name.style.display = "block";
    if (placeholderElement) {
      placeholderElement.style.display = "none";
    } else {
      console.log(`Couldn't find placeholder element for UID: ${UID}`);
    }
    localTrack[1].play(`user-${UID}`); // Ensure the camera feed resumes playing
    e.target.style.backgroundColor = "#fff";
  } else {
    await localTrack[1].setMuted(true);
    videoElement.style.display = "none";
    name.style.display = "none";
    if (placeholderElement) {
      placeholderElement.style.display = "block";
    } else {
      console.log(`Couldn't find placeholder element for UID: ${UID}`);
    }
    e.target.style.backgroundColor = "rgb(255, 80, 80, 1)";
  }
};

let toggleMic = async (e) => {
  if (localTrack[0].muted) {
    await localTrack[0].setMuted(false);
    e.target.style.backgroundColor = "#fff";
  } else {
    await localTrack[0].setMuted(true);
    e.target.style.backgroundColor = "rgb(255, 80, 80, 1)";
  }
};

let screenTrack = null;
let screenSharingActive = false;

let toggleScreenSharing = async (e) => {
  const userVideoElement = document.getElementById(`user-${UID}`);
  const videoContainer = userVideoElement.closest(".video-container"); // Find the container
  let screenDiv = document.getElementById("screen-share");
  let screenShareElement;

  if (!screenDiv) {
    // Create the screen-sharing container and video element if they don't exist
    screenDiv = document.createElement("div");
    screenDiv.id = "screen-share";
    screenDiv.style.position = "relative";
    screenDiv.style.width = "100%";
    screenDiv.style.height = "100%";
    screenDiv.style.display = "none"; // Initially hidden

    screenShareElement = document.createElement("video");
    screenShareElement.autoplay = true;
    screenShareElement.style.position = "absolute";
    screenShareElement.style.top = "0";
    screenShareElement.style.left = "0";
    screenShareElement.style.width = "100%";
    screenShareElement.style.height = "100%";

    screenDiv.appendChild(screenShareElement);
    videoContainer.appendChild(screenDiv); // Add it to the container
  } else {
    screenShareElement = screenDiv.querySelector("video");
  }

  if (!screenSharingActive) {
    try {
      // Start screen sharing
      const screenStream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
        audio: false, // Include audio if required
      });

      screenTrack = screenStream.getVideoTracks()[0];

      // Hide user's video and show the screen-sharing container
      userVideoElement.style.display = "none";
      screenDiv.style.display = "block"; // Show the screen-sharing container
      screenShareElement.srcObject = screenStream;

      // Replace the video track with the screen-sharing track in the Agora client
      const videoSender = client
        .getSenders()
        .find((sender) => sender.track.kind === "video");
      if (videoSender) {
        await videoSender.replaceTrack(screenTrack);
      }

      // Handle screen-sharing stop
      screenTrack.onended = () => {
        stopScreenSharing(e);
      };

      screenSharingActive = true;
      e.target.style.backgroundColor = "rgb(255, 80, 80, 1)";
    } catch (err) {
      console.error("Error during screen sharing:", err.message);
      // alert("Screen sharing failed. Please try again.");
    }
  } else {
    screenDiv.style.display = "none";
    stopScreenSharing(e);
  }
};

let stopScreenSharing = async (e) => {
  const userVideoElement = document.getElementById(`user-${UID}`);
  const screenDiv = document.getElementById("screen-share");

  if (screenTrack) {
    // Replace the screen-sharing track with the user's video track in the Agora client
    const videoSender = client
      .getSenders()
      .find((sender) => sender.track.kind === "video");
    if (videoSender) {
      await videoSender.replaceTrack(localTrack[1]); // Revert to the user's original video track
    }

    // Hide the screen-sharing container and show the user's video
    if (screenDiv) {
      screenDiv.style.display = "none"; // Hide the container
      const screenShareElement = screenDiv.querySelector("video");
      if (screenShareElement) {
        screenShareElement.srcObject = null; // Clear the stream
      }
    }
    userVideoElement.style.display = "block";
    await localTrack[1].setMuted(false);
    localTrack[1].play(`user-${UID}`);

    // Stop the screen-sharing track
    screenTrack.stop();
    screenTrack = null;

    screenSharingActive = false;
    e.target.style.backgroundColor = "#fff"; // Reset the button color
  }
};

let joinAndDisplayLocalStream = async () => {
  let userDetailsResponse = await fetch("/get_user_details/");
  let userDetails = await userDetailsResponse.json();

  if (userDetails.error) {
    console.error("Error fetching user details:", userDetails.error);
    return;
  }

  // Use the fetched username and user_id
  const { username, user_id } = userDetails;

  document.getElementById("room-name").innerText = CHANNEL;

  client.on("user-published", handleUserJoined);
  client.on("user-left", handleUserLeft);

  await client.join(APP_ID, CHANNEL, TOKEN, UID);
  localTrack = await AgoraRTC.createMicrophoneAndCameraTracks();
  let player = `<div class="video-container" id="user-container-${UID}">
      <div class="video-player" id="user-${UID}"></div>
      <div class="card-item" id="video-placeholder-${UID}" style="display: none;">
        <img src="${staticImagePath}" alt="User placeholder" class="card-image" />
        <h4 style="position: absolute; top: 10px; left: 10px; margin: 0; padding: 10px; font-weight: normal; color: white;">${username}</h4>
      </div>
      <div class="username-wrapper"><span class="user-name">${username}</span></div>
    </div>`;
  const videoStream = document.getElementById("video-streams");
  videoStream.insertAdjacentHTML("beforeend", player);
  const videoElement = document.getElementById(`user-${UID}`);
  console.log("Local video track created:", localTrack[1]);
  if (videoElement) {
    console.log("Local video track created:", localTrack[1]);
    localTrack[1].play(videoElement); // Pass the video element directly
  } else {
    console.error("Video container not found.");
  }
  console.log("Local video track created:", localTrack[1]);

  await client.publish([localTrack[0], localTrack[1]]);
  await createMember(username);
};

//storing the user details in the db
let createMember = async (username) => {
  try {
    console.log("USERNAME: ", username);

    // Send request to create member
    let response = await fetch("/create_member/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: username, room_name: CHANNEL, UID: UID }),
    });

    if (!response.ok) {
      throw new Error(`Failed to create member: ${response.statusText}`);
    }

    let member = await response.json();

    // Check if the response contains the expected data
    if (!member || !member.name) {
      throw new Error(
        "Failed to create member. Name not returned in response."
      );
    }

    return member;
  } catch (error) {
    console.error("Error creating member:", error.message);
  }
};

let getMember = async (user) => {
  try {
    let response = await fetch(
      `/get_member/?UID=${user.uid}&room_name=${CHANNEL}`
    );

    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }

    let member = await response.json();

    if (!member.name) {
      throw new Error("Member name not found in the response");
    }

    return member;
  } catch (error) {
    console.error("Error fetching member:", error.message);

    return null;
  }
};

let deleteMember = async () => {
  // Fetch user details
  let userDetailsResponse = await fetch("/get_user_details/");
  let userDetails = await userDetailsResponse.json();

  if (userDetails.error) {
    console.error("Error fetching user details:", userDetails.error);
    return;
  }

  const { username } = userDetails; // Extract the username

  // Send request to delete member
  let response = await fetch("/delete_member/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name: username, room_name: CHANNEL, UID: UID }),
  });

  let member = await response.json();
  return member;
};

window.addEventListener("beforeunload", deleteMember);

joinAndDisplayLocalStream();

document
  .getElementById("leave-btn")
  .addEventListener("click", leaveAndRemoveLocalStream);
document.getElementById("camera-btn").addEventListener("click", toggleCamera);
document.getElementById("mic-btn").addEventListener("click", toggleMic);
document
  .getElementById("screen")
  .addEventListener("click", toggleScreenSharing);
