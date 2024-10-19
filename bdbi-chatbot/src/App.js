import React, { useState } from 'react';
import './App.css';
import axios from 'axios'

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [inputImage, setInputImage] = useState(null);

  const handleTextChange = (e) => {
    setInputText(e.target.value);
  };

  const handleImageChange = (e) => {
    setInputImage(e.target.files[0]);
  };

  const handleSend = async () => {
    if (inputText) {
      // Handle text input
      const userMessage = { type: 'text', content: inputText };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      // Simulate a text API call
      const apiResponse = await callTextAPI(inputText);
      const botMessage = { type: 'text', content: apiResponse };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } else if (inputImage) {
      // Handle image input
      const userMessage = { type: 'image', content: URL.createObjectURL(inputImage) };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      // Simulate an image API call
      const apiResponse = await callImageAPI(inputImage);
      const botMessage = { type: 'text', content: apiResponse };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    }

    // Clear input fields
    setInputText('');
    setInputImage(null);
  };

  // Simulate API call for text
  const callTextAPI = async (text) => {
    try {
      const response = await axios.post('https://api.imgur.com/3/upload', { text });
      return response.data; // Assuming the API returns a useful response
    } catch (error) {
      console.error(error);
      return 'Error calling the API';
    }
  };

  // Simulate API call for images
  const callImageAPI = async (image) => {
    const formData = new FormData();
    formData.append('image', image);
  
    try {
      const response = await axios.post('https://api.imgur.com/3/upload', formData, {
        headers: {
          Authorization: '7a993eec3ef364a',
        },
      });
      return response.data.data.link; // Assuming the API returns an image link
    } catch (error) {
      console.error(error);
      return 'Error calling the API';
    }
  };

  return (
    <div className="App">
      <div className="chat-box">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={msg.type === 'text' ? 'message' : 'image-message'}>
              {msg.type === 'text' ? (
                <p>{msg.content}</p>
              ) : (
                <img src={msg.content} alt="User Upload" width="100" />
              )}
            </div>
          ))}
        </div>
        <div className="input-section">
          <input
            type="text"
            placeholder="Type your message"
            value={inputText}
            onChange={handleTextChange}
            disabled={inputImage !== null} // Disable text input when image is selected
          />
          <input
            type="file"
            onChange={handleImageChange}
            accept="image/*"
            disabled={inputText !== ''} // Disable file input when text is present
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
