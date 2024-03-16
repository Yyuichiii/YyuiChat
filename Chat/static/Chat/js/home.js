// Let us open a web socket
var ws= new WebSocket('ws://'+ window.location.host+'/chat/');
console.log(ws)
  
    // Web Socket is connected
    ws.onopen = function() {
        console.log("WebSocket connection established.");
        };

    // Handle WebSocket errors
    ws.onerror = function(error) {
        console.error("WebSocket error:", error);
        };        
         
    // Handle WebSocket close
    ws.onclose = function(event) {
        console.log("WebSocket connection closed:", event);
    };
   
    //Handle WebSocket Receive
    ws.onmessage = function (evt) { 
        var received_msg = evt.data;
    
        console.log(received_msg)

        // Parse the JSON string into a JavaScript object
        var jsonData = JSON.parse(received_msg);

    

        // Initialize the toast
        var notificationToastEl = document.getElementById('notificationToast');
        var notificationToast = new bootstrap.Toast(notificationToastEl);

        // Set the content for the notification
        document.getElementById('notification').innerHTML = jsonData.text;
        document.getElementById('notification_receive').innerHTML = jsonData.receive_name;

        // Show the toast
        notificationToast.show();

        // Reload the page after 2 seconds
        setTimeout(function() {
            location.reload();
            }, 2000); // 2000 milliseconds = 2 seconds
  };
