import React from 'react';

function MessageBubble({ message }) {
  const isUser = message.sender === 'user';
  
  // Safety banner logic
  const showSafetyBanner = message.label === 'suicidal' && message.confidence > 0.6;

  return (
    <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'} max-w-full`}>
      <div 
        className={`px-4 py-3 rounded-2xl shadow-sm text-[15px] leading-relaxed max-w-[85%]
          ${isUser 
            ? 'bg-teal-600 text-white rounded-tr-sm' 
            : 'bg-teal-50 text-slate-800 border border-teal-100 rounded-tl-sm'
          }
        `}
      >
        <p className="whitespace-pre-wrap">{message.text}</p>
      </div>

      {/* Safety Banner */}
      {!isUser && showSafetyBanner && (
        <div className="mt-2 bg-amber-50 border border-amber-200 text-amber-800 p-3 rounded-xl max-w-[85%] text-sm shadow-sm">
          <p className="font-semibold flex items-center gap-2 mb-1">
            <span className="text-lg">🫂</span> You're not alone
          </p>
          <p className="opacity-90">
            If you're feeling overwhelmed, help is available right now. Please consider reaching out to a crisis line or professional.
          </p>
        </div>
      )}
    </div>
  );
}

export default MessageBubble;
