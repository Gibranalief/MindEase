import React, { useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';

function MessageList({ messages, isLoading }) {
  const bottomRef = useRef(null);

  // Auto-scroll to bottom smoothly
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex flex-col gap-4 p-4 lg:p-6">
      {messages.map((msg, index) => (
        <MessageBubble key={index} message={msg} />
      ))}
      
      {/* Loading Indicator */}
      {isLoading && (
        <div className="self-start flex items-center bg-teal-50 border border-teal-100 px-4 py-3 rounded-2xl rounded-tl-sm shadow-sm max-w-[85%]">
          <div className="flex space-x-1.5 items-center justify-center py-1">
            <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
            <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
            <div className="w-2 h-2 bg-teal-400 rounded-full animate-bounce"></div>
          </div>
        </div>
      )}

      {/* Invisible element to scroll to */}
      <div ref={bottomRef} />
    </div>
  );
}

export default MessageList;
