document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file-input");
    const uploadBtn = document.getElementById("upload-btn");
    const uploadStatus = document.getElementById("upload-status");
    const queryInput = document.getElementById("query-input");
    const queryBtn = document.getElementById("query-btn");
    const output = document.getElementById("output");
    const name = document.getElementById("fileName");
    // const csrftoken = getCookie('csrftoken')
    let csrftokenmiddlewaretoken = document.querySelector("input[type=hidden]");
    const csrfToken = csrftokenmiddlewaretoken ? csrftokenmiddlewaretoken.value : null;
    console.log(csrfToken);
  
    uploadBtn.addEventListener("click", () => {
      const file_name = name;
      const file = fileInput.files[0];
      if (file) {
        const formData = new FormData();
        formData.append("file_content", file);
        // formData.append('file_name', file_name).value;
        fetch("http://127.0.0.1:8000/HS/uploaddocx_view/", {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": csrfToken,
          },
        })
          .then((response) => {
            if (response.ok) {
              uploadStatus.textContent = "File uploaded successfully!";
            } else {
              uploadStatus.textContent = "Error uploading file.";
            }
          })
          .catch((error) => {
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
  
        fetch("http://127.0.0.1:8000/HS/querydocx_view/", {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": csrfToken,
          },
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error("Bad response from server");
            }
          })
          .then((data) => {

            if (data.answer && data.answer.result) {
                output.textContent = data.answer.result;
            } else {
                output.textContent = "No answer found in the response.";
            }
            // output.textContent = data.answer;
          })
          .catch((error) => {
            output.textContent = "Error processing query: " + error;
          });
      } else {
        output.textContent = "Please enter a question.";
      }
    });
  });
  
