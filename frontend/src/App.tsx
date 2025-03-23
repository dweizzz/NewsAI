import { useState } from 'react'
import { getInsights, Insight } from './services/api'
import './App.css'

function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [insights, setInsights] = useState<Insight[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchTerm.trim()) return

    setLoading(true)
    setError(null)
    try {
      const results = await getInsights(searchTerm)
      setInsights(results)
    } catch (err) {
      setError('Failed to fetch insights. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>News AI Insights</h1>
      
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Enter a topic to search..."
          className="search-input"
        />
        <button type="submit" disabled={loading} className="search-button">
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      <div className="insights-container">
        {insights.map((insight, index) => (
          <div key={index} className="insight-card">
            <p className="insight-text">{insight.insight}</p>
            <div className="source-info">
              <a href={insight.source_link} target="_blank" rel="noopener noreferrer">
                {insight.source_title}
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
