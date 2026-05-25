import { useState } from 'react';
import ChatContainer from './components/ChatContainer';

// Ganti dari http://127.0.0.1:8000/chat
const API_URL = "https://gibby227-mindease.hf.space/chat";

function App() {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm here to listen. How are you feeling today?", sender: "bot", label: "general", confidence: 1.0 }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    
    const userMsg = { text, sender: "user" };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) throw new Error("API response error");

      const data = await response.json();
      
      const botMsg = {
        text: data.response,
        sender: "bot",
        label: data.label,
        confidence: data.confidence,
      };
      
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white shadow-xl rounded-2xl overflow-hidden flex flex-col h-[85vh]">
        {/* Header */}
        <div className="bg-teal-600 text-white p-4 text-center shrink-0">
          <h1 className="text-xl font-semibold tracking-wide">MindEase</h1>
          <p className="text-teal-100 text-sm">A safe space to talk</p>
        </div>
        
        {/* Chat Area */}
        <ChatContainer 
          messages={messages} 
          isLoading={isLoading} 
          error={error} 
          onSendMessage={sendMessage} 
        />
      </div>
    </div>
  );
}

export default App;
