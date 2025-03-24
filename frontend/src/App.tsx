import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { getInsights, Insight } from './services/api'
import { authEvents } from './services/authEvents'
import Login from './components/Login'
import Register from './components/Register'
import './App.css'

// Define a Tab type to manage our tabs system
interface Tab {
  id: string;
  searchTerm: string;
  insights: Insight[];
  loading: boolean;
  error: string | null;
}

function App() {
  const [searchTerm, setSearchTerm] = useState('')
  const [savedSearches, setSavedSearches] = useState<string[]>([])
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // New state for managing tabs
  const [tabs, setTabs] = useState<Tab[]>([])
  const [activeTabId, setActiveTabId] = useState<string | null>(null)

  // Check if user is already authenticated
  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      setIsAuthenticated(true)
    }

    // Listen for authentication events
    const unsubscribeLogin = authEvents.onLogin(() => {
      console.log('Auth event: login');
      setIsAuthenticated(true);
    });

    const unsubscribeLogout = authEvents.onLogout(() => {
      console.log('Auth event: logout');
      setIsAuthenticated(false);
    });

    // Cleanup event listeners
    return () => {
      unsubscribeLogin();
      unsubscribeLogout();
    };
  }, [])

  // For debugging - log auth state changes
  useEffect(() => {
    console.log('Authentication state changed:', isAuthenticated);
  }, [isAuthenticated]);

  // Load saved searches from localStorage on initial render
  useEffect(() => {
    if (isAuthenticated) {
      const saved = localStorage.getItem('savedSearches')
      if (saved) {
        setSavedSearches(JSON.parse(saved))
      }
    }
  }, [isAuthenticated])

  // Save searches to localStorage whenever they change
  useEffect(() => {
    if (isAuthenticated) {
      localStorage.setItem('savedSearches', JSON.stringify(savedSearches))
    }
  }, [savedSearches, isAuthenticated])

  // Function to generate a unique ID for tabs
  const generateTabId = () => {
    return Date.now().toString()
  }

  // Get the active tab
  const getActiveTab = () => {
    return tabs.find(tab => tab.id === activeTabId) || null
  }

  const handleLogout = () => {
    // Clear auth state
    setIsAuthenticated(false)
    // Remove token
    localStorage.removeItem('token')
    // Emit logout event
    authEvents.emitLogout()
    // Clear user data
    setSavedSearches([])
    setTabs([])
    setActiveTabId(null)
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!searchTerm.trim()) return

    // Create a new tab with this search term
    const newTabId = generateTabId()
    const newTab: Tab = {
      id: newTabId,
      searchTerm: searchTerm,
      insights: [],
      loading: true,
      error: null
    }

    // Add new tab and set it as active
    setTabs([...tabs, newTab])
    setActiveTabId(newTabId)

    // Add to saved searches if it's not already there
    if (!savedSearches.includes(searchTerm)) {
      setSavedSearches([...savedSearches, searchTerm])
    }

    // Clear the search input
    setSearchTerm('')

    // Fetch results
    try {
      const results = await getInsights(newTab.searchTerm)

      // Update the tab with results
      setTabs(prevTabs =>
        prevTabs.map(tab =>
          tab.id === newTabId
            ? { ...tab, insights: results, loading: false }
            : tab
        )
      )
    } catch (err) {
      // Update the tab with error
      setTabs(prevTabs =>
        prevTabs.map(tab =>
          tab.id === newTabId
            ? { ...tab, error: 'Failed to fetch insights. Please try again.', loading: false }
            : tab
        )
      )
      console.error(err)
    }
  }

  const handleSavedSearchClick = async (term: string) => {
    // Check if we already have a tab with this search term
    const existingTab = tabs.find(tab => tab.searchTerm === term)

    if (existingTab) {
      // If tab exists, just activate it
      setActiveTabId(existingTab.id)
      return
    }

    // Otherwise create a new tab for this saved search
    const newTabId = generateTabId()
    const newTab: Tab = {
      id: newTabId,
      searchTerm: term,
      insights: [],
      loading: true,
      error: null
    }

    // Add new tab and set it as active
    setTabs([...tabs, newTab])
    setActiveTabId(newTabId)

    // Fetch results
    try {
      const results = await getInsights(term)

      // Update the tab with results
      setTabs(prevTabs =>
        prevTabs.map(tab =>
          tab.id === newTabId
            ? { ...tab, insights: results, loading: false }
            : tab
        )
      )
    } catch (err) {
      // Update the tab with error
      setTabs(prevTabs =>
        prevTabs.map(tab =>
          tab.id === newTabId
            ? { ...tab, error: 'Failed to fetch insights. Please try again.', loading: false }
            : tab
        )
      )
      console.error(err)
    }
  }

  const handleRemoveSavedSearch = (term: string, e: React.MouseEvent) => {
    e.stopPropagation() // Prevent triggering the parent click handler
    setSavedSearches(savedSearches.filter(search => search !== term))
  }

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  const handleTabClick = (tabId: string) => {
    setActiveTabId(tabId)
  }

  const handleCloseTab = (tabId: string, e: React.MouseEvent) => {
    e.stopPropagation() // Prevent tab activation when closing

    // Remove the tab
    const newTabs = tabs.filter(tab => tab.id !== tabId)
    setTabs(newTabs)

    // If we're closing the active tab, activate another tab if available
    if (tabId === activeTabId && newTabs.length > 0) {
      setActiveTabId(newTabs[newTabs.length - 1].id)
    } else if (newTabs.length === 0) {
      setActiveTabId(null)
    }
  }

  // Get the currently active tab
  const activeTab = getActiveTab()

  // Main application UI component
  const MainApp = () => (
    <div className="app-container">
      <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h2>Saved Searches</h2>
          <button
            className="toggle-sidebar-button"
            onClick={toggleSidebar}
            aria-label={sidebarOpen ? "Close sidebar" : "Open sidebar"}
          >
            {sidebarOpen ? '←' : '→'}
          </button>
        </div>

        <div className="saved-searches-list">
          {savedSearches.length === 0 ? (
            <p className="no-saved-searches">No saved searches yet</p>
          ) : (
            savedSearches.map((term, index) => (
              <div
                key={index}
                className="saved-search-item"
                onClick={() => handleSavedSearchClick(term)}
              >
                <span>{term}</span>
                <button
                  className="remove-search-button"
                  onClick={(e) => handleRemoveSavedSearch(term, e)}
                  aria-label={`Remove ${term} from saved searches`}
                >
                  ×
                </button>
              </div>
            ))
          )}
        </div>

        {/* New search form at the bottom of sidebar */}
        <form onSubmit={handleSearch} className="sidebar-search-form">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search for insights..."
            className="sidebar-search-input"
          />
        </form>
      </div>

      <div className="main-content">
        <div className="header-container">
          <h1>News AI Insights</h1>
          <button className="logout-button" onClick={handleLogout}>
            Log Out
          </button>
        </div>

        <div className="scrollable-content">
          {/* Tab navigation system */}
          {tabs.length > 0 && (
            <div className="tabs-container">
              <div className="tabs-header">
                {tabs.map(tab => (
                  <button
                    key={tab.id}
                    className={`tab ${activeTabId === tab.id ? 'active' : ''}`}
                    onClick={() => handleTabClick(tab.id)}
                  >
                    {tab.searchTerm}
                    <span
                      className="tab-close"
                      onClick={(e) => handleCloseTab(tab.id, e)}
                    >
                      ×
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Display the active tab's content */}
          {activeTab ? (
            <div className="tab-content">
              {activeTab.loading ? (
                <div className="loading">Loading insights for "{activeTab.searchTerm}"...</div>
              ) : activeTab.error ? (
                <div className="error">{activeTab.error}</div>
              ) : (
                <div className="insights-container">
                  {activeTab.insights.length === 0 ? (
                    <div className="no-results">
                      No insights found for "{activeTab.searchTerm}"
                    </div>
                  ) : (
                    activeTab.insights.map((insight, index) => (
                      <div key={index} className="insight-card">
                        <p className="insight-text">{insight.insight}</p>
                        <div className="source-info">
                          <a href={insight.source_link} target="_blank" rel="noopener noreferrer">
                            {insight.source_title}
                          </a>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="no-active-tab">
              <p>Search for a topic using the sidebar to see insights</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <Router>
      <div className="app-root">
        <Routes>
          <Route path="/login" element={
            isAuthenticated ? <Navigate to="/" replace /> : <Login />
          } />
          <Route path="/register" element={
            isAuthenticated ? <Navigate to="/" replace /> : <Register />
          } />
          <Route path="/" element={
            isAuthenticated ? <MainApp /> : <Navigate to="/login" replace />
          } />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;