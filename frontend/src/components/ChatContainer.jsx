import React from 'react';
import MessageList from './MessageList';
import InputBox from './InputBox';

function ChatContainer({ messages, isLoading, error, onSendMessage }) {
  return (
    <div className="flex-1 flex flex-col overflow-hidden relative">
      {/* Error Banner */}
      {error && (
        <div className="bg-red-100 text-red-700 p-3 text-sm text-center font-medium shadow-sm">
          {error}
        </div>
      )}
      
      {/* Message List Area */}
      <div className="flex-1 overflow-y-auto">
        <MessageList messages={messages} isLoading={isLoading} />
      </div>

      {/* Input Area */}
      <div className="shrink-0 p-4 bg-white border-t border-slate-100">
        <InputBox onSendMessage={onSendMessage} isLoading={isLoading} />
        
        {/* Disclaimer per PRD */}
        <p className="text-center text-xs text-slate-400 mt-3 px-2">
          This chatbot is an AI and not a substitute for professional mental health help. 
          If you're in crisis, please seek immediate professional support.
        </p>
      </div>
    </div>
  );
}

export default ChatContainer;
