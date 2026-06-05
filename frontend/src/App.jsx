import { useState } from 'react'
import './App.css'

function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [darkMode, setDarkMode] = useState(true)

  const predict = async () => {
    if (!text.trim()) {
      console.log('[Frontend] Empty input, skipping')
      return
    }
    console.log('[Frontend] Sending prediction request:', text)
    setLoading(true)
    setResult(null)
    try {
      const url = '/predict'
      console.log('[Frontend] POST', url)
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })
      console.log('[Frontend] Response status:', res.status, res.statusText)
      const data = await res.json()
      console.log('[Frontend] Response data:', data)
      setResult(data)
    } catch (err) {
      console.error('[Frontend] Fetch error:', err.message)
      setResult({ emotion: 'error', confidence: 0, emoji: '❌', color: '#ff4444' })
    }
    setLoading(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      predict()
    }
  }

  const examples = [
    'I feel so happy and excited today!',
    'This makes me really angry and frustrated',
    'I am feeling sad and lonely right now',
    'Wow, that was absolutely unexpected!',
    'I am so grateful for everything I have',
  ]

  return (
    <div className={`app ${darkMode ? 'dark' : 'light'}`}>
      <div className="bg-effects">
        <div className="gradient-orb orb-1" />
        <div className="gradient-orb orb-2" />
        <div className="gradient-orb orb-3" />
      </div>

      <header>
        <div className="logo">
          <span className="logo-icon">🎭</span>
          <div>
            <h1>EmotionSense</h1>
            <p className="subtitle">AI-Powered Emotion Detector</p>
          </div>
        </div>
        <button
          className="theme-toggle"
          onClick={() => setDarkMode(!darkMode)}
          title="Toggle theme"
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </header>

      <main>
        <div className="card input-card">
          <label className="input-label">
            What are you feeling? Type your thoughts below...
          </label>
          <div className="input-wrapper">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="e.g., I feel absolutely amazing about my new project..."
              rows={4}
              maxLength={500}
            />
            <span className="char-count">{text.length}/500</span>
          </div>
          <button
            className="predict-btn"
            onClick={predict}
            disabled={loading || !text.trim()}
          >
            {loading ? (
              <span className="loading-spinner" />
            ) : (
              'Analyze Emotion'
            )}
          </button>

          <div className="examples">
            <span className="examples-label">Try:</span>
            {examples.map((ex, i) => (
              <button
                key={i}
                className="example-chip"
                onClick={() => setText(ex)}
              >
                {ex.slice(0, 35)}...
              </button>
            ))}
          </div>
        </div>

        {loading && (
          <div className="card result-card loading-card">
            <div className="skeleton emotion-skeleton" />
            <div className="skeleton text-skeleton" />
            <div className="skeleton bar-skeleton" />
          </div>
        )}

        {result && !loading && (
          <div className="card result-card" style={{ '--accent': result.color }}>
            <div className="result-header">
              <div className="emotion-display">
                <span className="emotion-emoji">{result.emoji}</span>
                <span className="emotion-name" style={{ color: result.color }}>
                  {result.emotion}
                </span>
              </div>
              <div className="confidence-ring">
                <svg viewBox="0 0 36 36">
                  <path
                    className="ring-bg"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className="ring-fill"
                    stroke={result.color}
                    strokeDasharray={`${(result.confidence * 100).toFixed(0)}, 100`}
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <text x="18" y="20.5" className="ring-text">
                    {(result.confidence * 100).toFixed(0)}%
                  </text>
                </svg>
              </div>
            </div>

            <div className="probabilities">
              <h3>All Emotions</h3>
              {result.probabilities.map((p) => (
                <div key={p.emotion} className="prob-bar">
                  <span className="prob-label">{p.emotion}</span>
                  <div className="prob-track">
                    <div
                      className="prob-fill"
                      style={{
                        width: `${(p.probability * 100).toFixed(0)}%`,
                        backgroundColor: p.emotion === result.emotion ? result.color : undefined,
                      }}
                    />
                  </div>
                  <span className="prob-value">
                    {(p.probability * 100).toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>

            <div className="input-text-display">
              <span className="quote-mark">"</span>
              {result.text}
              <span className="quote-mark">"</span>
            </div>
          </div>
        )}
      </main>

      <footer>
        <p>Model Accuracy: <strong>86.3%</strong> • Logistic Regression + TF-IDF</p>
      </footer>
    </div>
  )
}

export default App
