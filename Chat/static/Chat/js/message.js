// Let us open a web socket
var ws = new WebSocket("ws://" + window.location.host + "/chat/");

// Web Socket is connected
ws.onopen = function () {
  console.log("WebSocket connection established...");
};

// Handle WebSocket errors
ws.onerror = function (error) {
  console.error("WebSocket error:", error);
};

// Handle WebSocket close
ws.onclose = function (event) {
  console.log("WebSocket connection closed:", event);
};

// Handle WebSocket Receive
ws.onmessage = function(evt) {
    var receiver = JSON.parse(document.getElementById('receiver').textContent);
    var received_msg = evt.data;

    if (typeof received_msg === 'string') {
        // Add the received message to the chat messages
        addMessageToChatReceiver(receiver, received_msg);
    } else {
        addImageToChatReceiver(receiver, received_msg);
    }
};

// Setup the variables from the template
var sender_id = JSON.parse(document.getElementById('sender_id').textContent);
var receiver_id = JSON.parse(document.getElementById('receiver_id').textContent);
var receiver = JSON.parse(document.getElementById('receiver').textContent);

function addMessageToChatReceiver(receiver, message) {
    var chatMessages = document.getElementById("chatMessages");
    // Parse the JSON string into a JavaScript object
    var jsonData = JSON.parse(message);
    var receiver_id_pk = receiver_id;
    
    if (jsonData.sender_id != receiver_id_pk) {
        // Initialize the toast
        var notificationToastEl = document.getElementById('notificationToast');
        var notificationToast = new bootstrap.Toast(notificationToastEl);
        // Set the content for the notification
        document.getElementById('notification').innerHTML = jsonData.text;
        document.getElementById('notification_receive').innerHTML = jsonData.receive_name;
        // Show the toast
        notificationToast.show();
        return;
    }

    // Create a new message element
    var newMessage = document.createElement("div");
    newMessage.className = "alert alert-primary message-left";
    newMessage.setAttribute("role", "alert");
    newMessage.textContent = receiver + ": " + jsonData.text;
    
    // Append the new message element to the chat messages
    chatMessages.insertBefore(newMessage, chatMessages.firstChild);
}



// Function which triggers when the message is sent
document.getElementById("messageForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent default form submission

    var messageInput = document.getElementById("messageInput");
    var message = messageInput.value.trim(); // Get the trimmed value from the input field

    // Check if message is empty
    if (message === "") {
        // If message is empty, do not submit the form
        return;
    }

    // Send data to the server via WebSocket
    var messageObject = {
        // Your message content
        receive_id: receiver_id,
        sender_id: sender_id,
        text: message,
        receive_name: receiver,
    };

    // Convert the message object to a JSON string
    var jsonMessage = JSON.stringify(messageObject);
    ws.send(jsonMessage);

    // Clear the input field after sending
    messageInput.value = "";

    // Add the sent message to the chat messages
    addMessageToChat("You", message);
});

function addMessageToChat(sender, message) {
    var chatMessages = document.getElementById("chatMessages");

    // Create a new message element
    var messageElement = document.createElement("div");
    messageElement.className = "alert alert-secondary message-right";
    messageElement.setAttribute("role", "alert");
    messageElement.textContent = sender + ": " + message;

    // Append the new message element to the chat messages
    chatMessages.insertBefore(messageElement, chatMessages.firstChild);
}

// Function which triggers when the image is sent
document.getElementById("imageInput").addEventListener("change", function(event) {
    var file = event.target.files[0]; // Get the selected file
    console.log(file);
    if (file) {
        // Set WebSocket binaryType to "blob" to handle binary data
        ws.binaryType = "blob";

        // Convert the user ID to bytes
        var userIdBytes = new TextEncoder().encode(receiver_id + `:`);

        // Concatenate user ID bytes and file data bytes
        var combinedData = new Uint8Array(userIdBytes.length + file.size);
        combinedData.set(userIdBytes);

        var fileReader = new FileReader();
        fileReader.onload = function(event) {
            combinedData.set(
                new Uint8Array(event.target.result),
                userIdBytes.length
            );
            ws.send(combinedData);
        };
        fileReader.readAsArrayBuffer(file);

        // Add the sent message to the chat messages
        addImageToChat("You", file);
    }
});

function addImageToChat(sender, message) {
    var chatMessages = document.getElementById("chatMessages");
    console.log("wfrd", message);
    // Create a new image element
    var img = new Image();

    // Create a blob URL from the received blob
    var blobUrl = URL.createObjectURL(message);

    // Set the src attribute of the image element to the blob URL
    img.src = blobUrl;

    // Set the height and width of the image
    img.height = 100; // Set the desired height (in pixels)
    img.width = 100; // Set the desired width (in pixels)
    // Create a new message element
    var messageElement = document.createElement("div");
    messageElement.className = "alert alert-secondary message-right";
    messageElement.setAttribute("role", "alert");
    messageElement.textContent = sender + ": ";

    // Append the image element to the message element
    messageElement.appendChild(img);

    // Append the new message element to the chat messages
    chatMessages.insertBefore(messageElement, chatMessages.firstChild);
}

function addImageToChatReceiver(receiver, received_msg) {
    var chatMessages = document.getElementById("chatMessages");

    // Create a new image element
    var img = new Image();

    // Create a blob URL from the received blob
    var blobUrl = URL.createObjectURL(received_msg);

    // Set the src attribute of the image element to the blob URL
    img.src = blobUrl;

    // Set the height and width of the image
    img.height = 100; // Set the desired height (in pixels)
    img.width = 100; // Set the desired width (in pixels)

    // Create a new message element
    var tt = document.createElement("div");
    tt.className = "alert alert-primary message-left";
    tt.setAttribute("role", "alert");
    tt.textContent = receiver + ": ";

    // Append the image element to the message element
    tt.appendChild(img);

    // Append the new message element to the chat messages
    chatMessages.insertBefore(tt, chatMessages.firstChild);
}