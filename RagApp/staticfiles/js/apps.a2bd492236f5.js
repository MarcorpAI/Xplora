document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-input");
    const uploadBtn = document.getElementById("upload-btn");
    const uploadStatus = document.getElementById("upload-status");
    const queryInput = document.getElementById("query-input");
    const queryBtn = document.getElementById("query-btn");
    const chatLog = document.getElementById("chat-log");
    const name = document.getElementById("fileName");
    const chatBox = document.getElementById("chatLayer");
    const fileUploadBox = document.getElementById("file-upload-box");
    const loaderBubbles = document.querySelector(".loaderBubbles");
  
    let csrftokenmiddlewaretoken = document.querySelector("input[type=hidden]");
    const csrfToken = csrftokenmiddlewaretoken ? csrftokenmiddlewaretoken.value : null;
    console.log(csrfToken);
    let showTimeout, hideTimeout;
  
    function showLoader() {
      loaderBubbles.style.display = 'flex';
      chatLog.appendChild(loaderBubbles);
    }
  
    function hideLoader() {
      loaderBubbles.style.display = 'none';
      if (loaderBubbles.parentNode === chatLog) {
        chatLog.removeChild(loaderBubbles);
      }
    }
  
  
    function getUserFriendlyFileType(mimeType) {
      const mimeTypeMap = {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX",
        "application/pdf": "PDF Document",
        "image/jpeg": "JPEG Image",
        "image/png": "PNG Image",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "XLSX",
        "application/vnd.ms-excel": "XLS",
        "text/plain": "TXT",
        "application/zip": "ZIP",
        "application/x-compress": "ZIP",
        "application/x-zip-compressed": "ZIP",
        "multipart/x-zip": "ZIP",
      };
  
      return mimeTypeMap[mimeType] || "Unknown File Type";
    }
  
    //  uploadBtn.addEventListener("click", () => {
  
    // if file is selected run this script
    fileInput.addEventListener("change", () => {
      //   const file = fileInput.files[0];
      //   console.log(file);
      // });
  
  
      const file = fileInput.files[0];
  
      // if file is not selected
      if (!file) {
        uploadStatus.innerHTML = "<p class='error'>Please select a file to upload.</p>";
        uploadStatus.classList.add("show");
  
        showTimeout = setTimeout(() => {
          uploadStatus.classList.remove("show");
          uploadStatus.classList.add("fadeOut");
  
          hideTimeout = setTimeout(() => {
            uploadStatus.classList.remove("fadeOut");
            uploadStatus.innerHTML = "";
          }, 500);
        }, 3000);
  
        return;
      }
  
      fileUploadBox.style.display = "flex";
      var uploadFileName = document.querySelector(".upload-file-name");
      var uploadFiletype = document.querySelector(".prompt-upload-file-type");
      var fileLoader = document.querySelector(".loaderSmall");
      var fileUploadIcon = document.querySelector(".prompt-upload-icon-icon");
  
  
      chatBox.style.display = "none";
      fileLoader.style.display = "block";
      fileUploadIcon.style.display = "none";
  
  
      uploadFileName.innerHTML = file.name;
      uploadFiletype.innerHTML = getUserFriendlyFileType(file.type);
  
      console.log(file);
  
      if (file) {
        const formData = new FormData();
        formData.append("file_content", file);
  
        const fileUploadSpinner = document.getElementById("file-upload-spinner");
        var buttonText = document.querySelector(".btn-text");
        fileUploadSpinner.style.display = "flex";
        buttonText.style.display = "none";
  
        fetch("http://127.0.0.1:8000/chatwfile/", {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": csrfToken,
          },
        })
          .then((response) => {
            fileUploadSpinner.style.display = "none";
            buttonText.style.display = "block";
  
            if (response.ok) {
              clearTimeout(showTimeout);
              clearTimeout(hideTimeout);
  
              uploadStatus.innerHTML = "<p class='success'>File uploaded successfully!</p>";
              fileLoader.style.display = "none";
              fileUploadIcon.style.display = "flex";
              uploadStatus.classList.add("show");
  
              showTimeout = setTimeout(() => {
                uploadStatus.classList.remove("show");
                uploadStatus.classList.add("fadeOut");
  
                hideTimeout = setTimeout(() => {
                  uploadStatus.classList.remove("fadeOut");
                  uploadStatus.innerHTML = "";
                }, 500);
              }, 3000);
            } else {
              clearTimeout(showTimeout);
              clearTimeout(hideTimeout);
  
              uploadStatus.innerHTML = "<p class='error'>Error uploading file.</p>";
              uploadStatus.classList.add("show");
  
              fileLoader.style.display = 'none';
              fileUploadIcon.style.display = 'block';
  
              showTimeout = setTimeout(() => {
                uploadStatus.classList.remove("show");
                uploadStatus.classList.add("fadeOut");
  
                hideTimeout = setTimeout(() => {
                  uploadStatus.classList.remove("fadeOut");
                  uploadStatus.innerHTML = "";
                }, 500);
              }, 3000);
            }
          })
          .catch((error) => {
            uploadStatus.innerHTML = "<p class='error'>Error uploading file: " + error + "</p>";
            uploadStatus.classList.add("show");
  
            showTimeout = setTimeout(() => {
              uploadStatus.classList.remove("show");
              uploadStatus.classList.add("fadeOut");
  
              hideTimeout = setTimeout(() => {
                uploadStatus.classList.remove("fadeOut");
                uploadStatus.innerHTML = "";
              }, 500);
            }, 3000);
          });
      } else {
        clearTimeout(showTimeout);
        clearTimeout(hideTimeout);
  
        uploadStatus.innerHTML = "<p class='error'>Please select a file to upload.</p>";
        uploadStatus.classList.add("show");
  
        showTimeout = setTimeout(() => {
          uploadStatus.classList.remove("show");
          uploadStatus.classList.add("fadeOut");
  
          hideTimeout = setTimeout(() => {
            uploadStatus.classList.remove("fadeOut");
            uploadStatus.innerHTML = "";
          }, 500);
        }, 3000);
      }
    });
  
    queryBtn.addEventListener("click", () => {
      const query = queryInput.value.trim();
      const file = fileInput.files[0];
  
      // if file is not selected
      if (!file) {
        uploadStatus.innerHTML = "<p class='error'>Please select a file to upload.</p>";
        uploadStatus.classList.add("show");
  
        showTimeout = setTimeout(() => {
          uploadStatus.classList.remove("show");
          uploadStatus.classList.add("fadeOut");
  
          hideTimeout = setTimeout(() => {
            uploadStatus.classList.remove("fadeOut");
            uploadStatus.innerHTML = "";
          }, 500);
        }, 3000);
  
        return;
      }
  
      // if query is not entered
      if (!query) {
        uploadStatus.innerHTML = "<p class='error'>Please enter a message.</p>";
        uploadStatus.classList.add("show");
  
        showTimeout = setTimeout(() => {
          uploadStatus.classList.remove("show");
          uploadStatus.classList.add("fadeOut");
  
          hideTimeout = setTimeout(() => {
            uploadStatus.classList.remove("fadeOut");
            uploadStatus.innerHTML = "";
          }, 500);
        }, 3000);
  
        return;
      }
  
      if (query && file) {
  
        showLoader();
  
        const formData = new FormData();
        formData.append("file_content", file);
        formData.append("question", query);
  
        const userMessage = document.createElement("div");
        userMessage.classList.add("user-message");
        userMessage.textContent = query;
        chatLog.appendChild(userMessage);
        queryInput.value = ""; // Clear the message box after sending
  
  
        fetch("http://127.0.0.1:8000/queryfile_view/", {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": csrfToken,
          },
        })
          .then((response) => {
            // llmTypingSpinner.style.display = "none";
            if (response.ok) {
              return response.json();
            } else {
              throw new Error("Bad response from server");
            }
          })
          .then((data) => {
            hideLoader();
            if (data.answer && data.answer.result) {
              const assistantMessage = document.createElement("div");
              assistantMessage.classList.add("assistant-message");
              assistantMessage.textContent = data.answer.result;
  
              chatLog.appendChild(assistantMessage);
            } else {
              const errorMessage = document.createElement("div");
              errorMessage.classList.add("assistant-message");
              errorMessage.textContent = "No answer found in the response.";
              chatLog.appendChild(errorMessage);
              chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom of the chat log
            }
          })
          .catch((error) => {
            hideLoader();
            // llmTypingSpinner.style.display = "none";
            const errorMessage = document.createElement("div");
            errorMessage.classList.add("assistant-message");
            errorMessage.textContent = "Error processing query: " + error;
            chatLog.appendChild(errorMessage);
            chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom of the chat log
          });
      } else {
  
        // display message
        uploadStatus.innerHTML = "<p class='error'>Please enter a message.</p>";
        uploadStatus.classList.add("show");
  
        showTimeout = setTimeout(() => {
          uploadStatus.classList.remove("show");
          uploadStatus.classList.add("fadeOut");
  
          hideTimeout = setTimeout(() => {
            uploadStatus.classList.remove("fadeOut");
            uploadStatus.innerHTML = "";
          }, 500);
        }, 3000);
  
      }
    });
  });