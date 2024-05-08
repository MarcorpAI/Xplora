

const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const chatHistory = document.querySelector('.chat-history');

sendButton.addEventListener('click', () => {
  const message = messageInput.value.trim();
  if (message) {
    // Simulate sending a message (replace with logic to interact with your backend if needed)
    addMessage('You', message);
    addMessage('AI', 'Processing...'); 
    messageInput.value = '';
  }
});

function addMessage(sender, message) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.innerHTML = <b>${sender}</b>; {message};
  chatHistory.appendChild(messageElement);
  chatHistory.scrollTo({ top: chatHistory.scrollHeight, behavior: 'smooth' });
}





