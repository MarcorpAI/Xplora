document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("file-input");
  const uploadBtn = document.getElementById("upload-btn");
  const uploadStatus = document.getElementById("upload-status");
  const queryInput = document.getElementById("query-input");
  const queryBtn = document.getElementById("query-btn");
  const chatLog = document.getElementById("chat-log");
  const name = document.getElementById("fileName");
  let csrftokenmiddlewaretoken = document.querySelector("input[type=hidden]");
  const csrfToken = csrftokenmiddlewaretoken ? csrftokenmiddlewaretoken.value : null;
  console.log(csrfToken);

  uploadBtn.addEventListener("click", () => {
    const file_name = name;
    const file = fileInput.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("file_content", file);


      const fileUploadSpinner = document.getElementById("file-upload-spinner");
      fileUploadSpinner.style.display = "flex";


      fetch("http://127.0.0.1:8000/uploadxlsx_view/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrfToken,
        },
      })
        .then((response) => {

          fileUploadSpinner.style.display = "none";

          if (response.ok) {
            uploadStatus.textContent = "File uploaded successfully!";
          } else {
            uploadStatus.textContent = "Error uploading file.";
          }
        })
        .catch((error) => {

          fileUploadSpinner.style.display = "none";
          uploadStatus.textContent = "Error uploading file: " + error;
        });
    } else {
      uploadStatus.textContent = "Please select a file to upload.";
    }
  });

  queryBtn.addEventListener("click", () => {
    const query = queryInput.value.trim();
    const file = fileInput.files[0];
    if (query && file) {
      const formData = new FormData();
      formData.append("file_content", file);
      formData.append("question", query);

      const userMessage = document.createElement("div");
      userMessage.classList.add("user-message");
      userMessage.textContent = query;
      chatLog.appendChild(userMessage);
      queryInput.value = ""; // Clear the message box after sending

      const llmTypingSpinner = document.getElementById("llm-typing-spinner");
      llmTypingSpinner.style.display = "flex";

      fetch("http://127.0.0.1:8000/queryxlsx_view/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrfToken,
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
          if (data.answer && data.answer.result) {
            const assistantMessage = document.createElement("div");
            assistantMessage.classList.add("assistant-message");
            assistantMessage.textContent = data.answer.result;
            chatLog.appendChild(assistantMessage);
            chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom of the chat log
          } else {
            const errorMessage = document.createElement("div");
            errorMessage.classList.add("assistant-message");
            errorMessage.textContent = "No answer found in the response.";
            chatLog.appendChild(errorMessage);
            chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom of the chat log
          }
        })
        .catch((error) => {

          llmTypingSpinner.style.display = "none";
          const errorMessage = document.createElement("div");
          errorMessage.classList.add("assistant-message");
          errorMessage.textContent = "Error processing query: " + error;
          chatLog.appendChild(errorMessage);
          chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom of the chat log
        });
    } else {
      const errorMessage = document.createElement("div");
      errorMessage.classList.add("assistant-message");
      errorMessage.textContent = "Please enter a question.";
      chatLog.appendChild(errorMessage);
      chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom of the chat log
    }
  });
});