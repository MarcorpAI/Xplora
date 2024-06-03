document.addEventListener("DOMContentLoaded", function () {
    const connectionForm = document.getElementById("connection-form");
    const queryInput = document.getElementById("query-input");
    const chatLog = document.getElementById("chat-log");
    const queryBtn = document.getElementById("query-btn");
    const uploadStatus = document.getElementById("upload-status");
    const csrfToken = document.querySelector("input[name=csrfmiddlewaretoken]").value;
  
    let showTimeout, hideTimeout;
  
    connectionForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const formData = new FormData(connectionForm);
        formData.append("csrfmiddlewaretoken", csrfToken);
  
        const fileUploadSpinner = document.getElementById("file-upload-spinner");
        fileUploadSpinner.style.display = "flex";
  
        fetch("http://127.0.0.1:8000/askpostgres/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": csrfToken,
            },
        })
        .then((response) => {
            fileUploadSpinner.style.display = "none";
            return response.json();
        })
        .then((data) => {
            clearTimeout(showTimeout);
            clearTimeout(hideTimeout);
  
            if (data.status === "success") {
                uploadStatus.innerHTML = "<p class='success'>Connection successful!</p>";
            } else {
                uploadStatus.innerHTML = "<p class='error'>Connection failed: " + data.message + "</p>";
            }
            uploadStatus.classList.add("show");
  
            showTimeout = setTimeout(() => {
                uploadStatus.classList.remove("show");
                uploadStatus.classList.add("fadeOut");
  
                hideTimeout = setTimeout(() => {
                    uploadStatus.classList.remove("fadeOut");
                    uploadStatus.innerHTML = "";
                }, 500);
            }, 3000);
        })
        .catch((error) => {
            fileUploadSpinner.style.display = "none";
            uploadStatus.innerHTML = "<p class='error'>Error connecting to database: " + error + "</p>";
        });
    });
  
    queryBtn.addEventListener("click", (event) => {
      event.preventDefault();
      const query = queryInput.value.trim();
  
      if (query){
        const formData = new FormData();
        formData.append("question", query);
        formData.append("csrfmiddlewaretoken", csrfToken);
  
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.textContent = query;
        chatLog.appendChild(userMessage)
  
        queryInput.value = "";
  
        const llmTypingSpinner = document.getElementById("llm-typing-spinner");
        llmTypingSpinner.style.display = 'flex';
  
        fetch("http://127.0.0.1:8000/querypost/",{
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": csrfToken
          },
        })
          .then((response) => {
            llmTypingSpinner.style.display = "none";
            if (response.ok) {
              return response.json();
            } else {
              throw new Error("Bad response from server");
            }
          })
          .then((data) => {
            if (data.status ==="success" && data.response) {
              const assistantMessage = document.createElement("div");
              assistantMessage.classList.add("assistant-message");
              assistantMessage.textContent = data.response;
              chatLog.appendChild(assistantMessage);
              chatLog.scrollTop = chatLog.scrollHeight;
            } else {
              const errorMessage = document.createElement("div");
              errorMessage.classList.add("assistant-message");
              errorMessage.textContent = "No answer found in the response.";
              chatLog.appendChild(errorMessage);
              chatLog.scrollTop = chatLog.scrollHeight; 
            }
          })
          .catch((error) => {
            llmTypingSpinner.style.display = "none";
            const errorMessage = document.createElement("div");
            errorMessage.classList.add("assistant-message");
            errorMessage.textContent = "Error processing query: " + error;
            chatLog.appendChild(errorMessage);
            chatLog.scrollTop = chatLog.scrollHeight;
          });
      } else {
  
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("assistant-message");
        errorMessage.textContent = "Please enter a question.";
        chatLog.appendChild(errorMessage);
        chatLog.scrollTop = chatLog.scrollHeight; 
  
      }
    });
  });