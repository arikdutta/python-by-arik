import { useState, useRef, useEffect } from 'react'

const SUGGESTIONS = [
  'How do I write a strong resume summary?',
  'What are the most in-demand skills for software engineers in 2025?',
  'How should I prepare for a behavioral interview?',
  'Tips for negotiating a higher salary offer?',
]

export default function Chatbot() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (text) => {
    const userMessage = text || input.trim()
    if (!userMessage || loading) return

    const newMessages = [...messages, { role: 'user', content: userMessage }]
    setMessages(newMessages)
    setInput('')
    setLoading(true)

    const assistantIndex = newMessages.length
    setMessages((prev) => [...prev, { role: 'assistant', content: '' }])

    try {
      const res = await fetch('/api/chatbot/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      })

      const reader = res.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        const chunk = decoder.decode(value)
        setMessages((prev) =>
          prev.map((msg, i) =>
            i === assistantIndex ? { ...msg, content: msg.content + chunk } : msg
          )
        )
      }
    } catch (err) {
      setMessages((prev) =>
        prev.map((msg, i) =>
          i === assistantIndex ? { ...msg, content: 'Error: ' + err.message } : msg
        )
      )
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: 16 }}>
        <h2 className="card-title">Career Chatbot</h2>
        <p className="card-desc">
          Ask CareerCoach AI anything about resumes, interviews, salary negotiation, career transitions, and more.
        </p>
      </div>

      <div className="chat-container">
        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="chat-welcome">
              <div style={{ fontSize: 48, marginBottom: 16 }}>🤖</div>
              <h3>Hi! I'm CareerCoach AI</h3>
              <p style={{ marginBottom: 20 }}>Ask me anything about your career journey</p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center' }}>
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    className="btn-secondary"
                    onClick={() => sendMessage(s)}
                    style={{ fontSize: 13 }}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                <div className="message-avatar">
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-bubble">
                  {msg.content}
                  {loading && i === messages.length - 1 && msg.role === 'assistant' && !msg.content && (
                    <span className="streaming-cursor" />
                  )}
                </div>
              </div>
            ))
          )}
          {loading && messages[messages.length - 1]?.role === 'assistant' &&
            messages[messages.length - 1]?.content && (
              <div ref={messagesEndRef} />
            )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input-area">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about resume tips, interview prep, salary negotiation... (Enter to send)"
            rows={2}
            disabled={loading}
          />
          <button
            className="btn-send"
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading}
          >
            {loading ? <div className="spinner" /> : 'Send'}
          </button>
        </div>
      </div>

      {messages.length > 0 && (
        <div style={{ marginTop: 12, textAlign: 'right' }}>
          <button className="btn-secondary" onClick={() => setMessages([])}>
            Clear Chat
          </button>
        </div>
      )}
    </div>
  )
}
