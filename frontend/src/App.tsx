/**
 * =============================================================================
 * Word Guess Deluxe - Frontend (User Adapter)
 * =============================================================================
 * This component is the entry point for the user interface.
 * It communicates with the Backend (API) to manage game state.
 * Uses: React, Tailwind CSS for design, Axios for HTTP requests,
 * and Canvas Confetti for visual effects.
 * =============================================================================
 */

import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import { 
  Trophy, 
  Gamepad2, 
  RotateCcw, 
  Lightbulb, 
  Keyboard, 
  Info,
  BarChart3,
  XCircle,
  CheckCircle2
} from 'lucide-react'
import confetti from 'canvas-confetti'

// Base URL for Backend API
const API_URL = 'http://localhost:8000'

// Interface matching the Backend domain model
interface GameState {
  secret_word: string
  guessed_word: string
  guesses_left: number
  used_letters: string[]
  score: number
  correct_guesses: number
  wrong_guesses: number
  hints_used: number
  game_over: boolean
  won: boolean
  theme: string
}

function App() {
  // Local state to manage game session
  const [gameId, setGameId] = useState<string | null>(null)
  const [state, setState] = useState<GameState | null>(null)
  const [themes, setThemes] = useState<string[]>([])
  const [selectedTheme, setSelectedTheme] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showThemeSelector, setShowThemeSelector] = useState(true)

  // Fetch available themes on load
  useEffect(() => {
    const fetchThemes = async () => {
      try {
        const response = await axios.get(`${API_URL}/themes`)
        setThemes(response.data)
      } catch (err) {
        console.error("Error loading themes:", err)
      }
    }
    fetchThemes()
  }, [])

  /**
   * Requests the backend to start a new game.
   * useCallback is used to memoize the function and avoid unnecessary re-renders.
   */
  const startNewGame = useCallback(async (theme?: string) => {
    setLoading(true)
    setError(null)
    setShowThemeSelector(false)
    try {
      const response = await axios.post(`${API_URL}/game/new`, {
        theme: theme || selectedTheme
      })
      setGameId(response.data.game_id)
      setState(response.data.state)
    } catch (err) {
      setError('Could not connect to the backend server. Make sure the backend is running on port 8000.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [selectedTheme])

  /**
   * Sends a letter to the backend to process the guess.
   */
  const makeGuess = async (letter: string) => {
    // Preventive frontend validations
    if (!gameId || !state || state.game_over || state.used_letters.includes(letter)) return

    try {
      const response = await axios.post(`${API_URL}/game/guess`, {
        game_id: gameId,
        letter: letter
      })
      const newState = response.data
      setState(newState)
      
      // Confetti effect if player wins
      if (newState.game_over && newState.won) {
        confetti({
          particleCount: 150,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#6366f1', '#ec4899', '#f59e0b']
        })
      }
    } catch (err) {
      console.error('Error making guess:', err)
    }
  }

  /**
   * Requests a hint (reveal letter) from the backend.
   */
  const useHint = async () => {
    if (!gameId || !state || state.game_over) return

    try {
      const response = await axios.post(`${API_URL}/game/hint`, {
        game_id: gameId
      })
      setState(response.data)
    } catch (err) {
      console.error('Error requesting hint:', err)
    }
  }

  /**
   * Support for physical keyboard: allows playing by typing directly.
   */
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const key = e.key.toUpperCase()
      // Only process letters A to Z
      if (/^[A-Z]$/.test(key)) {
        makeGuess(key)
      } else if (key === '?') {
        useHint()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [gameId, state])

  // Theme selection screen
  if (showThemeSelector) {
    return (
      <div className="min-h-screen bg-[#0f172a] flex flex-col items-center justify-center p-4">
        <div className="bg-[#1e293b] p-10 rounded-[40px] border border-white/5 text-center max-w-2xl shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-indigo-500 via-pink-500 to-amber-500" />
          
          <Gamepad2 className="w-16 h-16 text-[#6366f1] mx-auto mb-6" />
          <h1 className="text-4xl font-black text-white mb-2 tracking-tighter">WORD GUESS <span className="text-[#6366f1]">DELUXE</span></h1>
          <p className="text-gray-400 mb-10 font-medium">Choose a theme to start your adventure</p>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-10">
            {themes.map(theme => (
              <button
                key={theme}
                onClick={() => {
                  setSelectedTheme(theme)
                  startNewGame(theme)
                }}
                className="group relative p-6 bg-white/5 hover:bg-[#6366f1] rounded-3xl border border-white/10 transition-all duration-300 text-left overflow-hidden"
              >
                <div className="absolute -right-4 -bottom-4 opacity-10 group-hover:scale-150 transition-transform duration-500">
                  <Trophy className="w-24 h-24" />
                </div>
                <span className="block text-xs font-black uppercase tracking-[0.2em] text-indigo-400 group-hover:text-indigo-200 mb-1">Theme</span>
                <span className="block text-xl font-black text-white">{theme}</span>
              </button>
            ))}
            
            <button
              onClick={() => startNewGame()}
              className="group relative p-6 bg-gradient-to-br from-pink-600 to-pink-400 rounded-3xl text-left overflow-hidden shadow-lg shadow-pink-500/20 hover:scale-[1.02] transition-all"
            >
              <div className="absolute -right-4 -bottom-4 opacity-20 group-hover:rotate-12 transition-transform duration-500">
                <RotateCcw className="w-24 h-24" />
              </div>
              <span className="block text-xs font-black uppercase tracking-[0.2em] text-pink-100 mb-1">Random</span>
              <span className="block text-xl font-black text-white">SURPRISE ME!</span>
            </button>
          </div>
          
          <p className="text-[10px] text-gray-500 font-black uppercase tracking-widest">Code in Place 2026 • Final Project</p>
        </div>
      </div>
    )
  }

  // Error view if API connection fails
  if (error) {
    return (
      <div className="min-h-screen bg-[#0f172a] flex flex-col items-center justify-center p-4">
        <div className="bg-[#1e293b] p-8 rounded-2xl border-2 border-red-500 text-center max-w-md shadow-2xl">
          <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-white mb-2">Connection Error!</h1>
          <p className="text-gray-400 mb-6">{error}</p>
          <button 
            onClick={() => startNewGame()}
            className="bg-[#6366f1] hover:bg-[#4f46e5] text-white px-8 py-3 rounded-xl font-bold transition-all shadow-lg shadow-indigo-500/20"
          >
            RETRY CONNECTION
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0f172a] text-white font-sans selection:bg-indigo-500/30">
      {/* Top Bar / Header */}
      <header className="max-w-4xl mx-auto pt-8 px-4 flex justify-between items-center">
        <div className="flex items-center gap-3 group">
          <button 
            onClick={() => setShowThemeSelector(true)}
            className="bg-[#6366f1] p-2 rounded-xl group-hover:rotate-12 transition-transform duration-300"
          >
            <Gamepad2 className="w-8 h-8 text-white" />
          </button>
          <div>
            <h1 className="text-2xl font-black tracking-tighter sm:text-3xl">
              WORD GUESS <span className="text-[#6366f1]">DELUXE</span>
            </h1>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-black uppercase tracking-widest text-indigo-400">Theme:</span>
              <span className="text-[10px] font-black uppercase tracking-widest text-white">{state?.theme}</span>
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="bg-[#1e293b] px-4 py-2 rounded-xl border border-white/5 flex items-center gap-2 shadow-inner">
            <Trophy className="w-5 h-5 text-amber-500" />
            <span className="font-black text-xl text-amber-500">{state?.score || 0}</span>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: The Game */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* Secret Word Display */}
            <div className="bg-[#1e293b] p-12 rounded-3xl border border-white/5 flex flex-col items-center justify-center shadow-2xl relative overflow-hidden min-h-[300px]">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-pink-500 to-amber-500 opacity-50" />
              
              <div className="flex flex-wrap justify-center gap-3">
                {state?.guessed_word.split('').map((char, i) => (
                  <div 
                    key={i}
                    className={`w-12 h-16 sm:w-16 sm:h-20 flex items-center justify-center text-3xl sm:text-4xl font-black rounded-2xl border-b-4 transition-all duration-300 ${
                      char !== '-' 
                        ? 'bg-[#6366f1] border-indigo-700 text-white scale-105 rotate-2' 
                        : 'bg-white/5 border-white/10 text-transparent'
                    }`}
                  >
                    {char !== '-' ? char : ''}
                  </div>
                ))}
              </div>

              {/* End Game Messages */}
              {state?.game_over && (
                <div className={`mt-10 px-8 py-4 rounded-2xl font-black text-xl flex items-center gap-3 animate-bounce shadow-xl ${
                  state.won 
                    ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                    : 'bg-red-500/20 text-red-400 border border-red-500/30'
                }`}>
                  {state.won ? (
                    <><CheckCircle2 className="w-8 h-8" /> MASTERFUL VICTORY!</>
                  ) : (
                    <><XCircle className="w-8 h-8" /> GAME OVER!</>
                  )}
                </div>
              )}
            </div>

            {/* Interactive Virtual Keyboard */}
            <div className="bg-[#1e293b]/50 p-6 rounded-3xl border border-white/5 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-6 text-gray-400">
                <Keyboard className="w-4 h-4" />
                <span className="text-xs font-black uppercase tracking-widest opacity-60">Touch Control / Keyboard</span>
              </div>
              <div className="flex flex-wrap justify-center gap-2">
                {"QWERTYUIOPASDFGHJKLZXCVBNM".split('').map(letter => {
                  const isUsed = state?.used_letters.includes(letter)
                  const isCorrect = isUsed && state?.secret_word.includes(letter)
                  const isWrong = isUsed && !state?.secret_word.includes(letter)

                  return (
                    <button
                      key={letter}
                      disabled={isUsed || state?.game_over || loading}
                      onClick={() => makeGuess(letter)}
                      className={`w-10 h-12 sm:w-12 sm:h-14 rounded-xl font-black text-lg transition-all duration-200 ${
                        isCorrect 
                          ? 'bg-green-500 text-white shadow-lg shadow-green-500/20 scale-95' 
                          : isWrong 
                            ? 'bg-red-500/10 text-red-500 border border-red-500/30 opacity-40'
                            : 'bg-white/10 hover:bg-white/20 text-white hover:scale-110'
                      } ${isUsed ? 'cursor-not-allowed' : 'active:scale-90'}`}
                    >
                      {letter}
                    </button>
                  )
                })}
              </div>
            </div>
          </div>

          {/* Right Column: Statistics and Hints */}
          <div className="space-y-6">
            
            {/* Status and Lives Card */}
            <div className="bg-[#1e293b] p-6 rounded-3xl border border-white/5 space-y-6 shadow-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-[#6366f1]">
                  <Info className="w-5 h-5" />
                  <h2 className="font-black text-sm uppercase tracking-wider">Session</h2>
                </div>
                <div className="px-3 py-1 bg-white/5 rounded-full text-[10px] font-mono text-gray-500">
                  {gameId?.slice(0, 8)}
                </div>
              </div>

              <div className="space-y-5">
                <div className="space-y-2">
                  <div className="flex justify-between text-xs font-bold text-gray-400 uppercase tracking-tighter">
                    <span>Available Lives</span>
                    <span className={state?.guesses_left && state.guesses_left <= 2 ? 'text-red-500 animate-pulse' : ''}>
                      {state?.guesses_left} / 8
                    </span>
                  </div>
                  <div className="flex gap-1.5 h-3">
                    {[...Array(8)].map((_, i) => (
                      <div 
                        key={i} 
                        className={`flex-1 rounded-full transition-all duration-700 ${
                          i < (state?.guesses_left || 0) 
                            ? 'bg-gradient-to-t from-pink-600 to-pink-400' 
                            : 'bg-white/5'
                        }`} 
                      />
                    ))}
                  </div>
                </div>

                <div className="p-4 bg-white/5 rounded-2xl border border-white/5 space-y-4">
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-gray-400 font-bold uppercase text-[10px]">Hints Used</span>
                    <span className="font-black text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded-lg">{state?.hints_used || 0}</span>
                  </div>
                  <button
                    disabled={state?.game_over || (state?.score || 0) < 10}
                    onClick={useHint}
                    className="w-full py-3 bg-amber-500/10 hover:bg-amber-500/20 text-amber-500 rounded-xl text-xs font-black flex items-center justify-center gap-2 transition-all disabled:opacity-20 disabled:grayscale"
                  >
                    <Lightbulb className="w-4 h-4" />
                    REVEAL LETTER (-10 PTS)
                  </button>
                </div>
              </div>
            </div>

            {/* Statistics Card */}
            <div className="bg-[#1e293b] p-6 rounded-3xl border border-white/5 space-y-5 shadow-xl">
              <div className="flex items-center gap-2 text-pink-500">
                <BarChart3 className="w-5 h-5" />
                <h2 className="font-black text-sm uppercase tracking-wider">Performance</h2>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-green-500/5 rounded-2xl border border-green-500/10 text-center">
                  <div className="text-[10px] text-green-500/60 uppercase font-black mb-1">Correct</div>
                  <div className="text-2xl font-black text-green-400">{state?.correct_guesses || 0}</div>
                </div>
                <div className="p-4 bg-red-500/5 rounded-2xl border border-red-500/10 text-center">
                  <div className="text-[10px] text-red-500/60 uppercase font-black mb-1">Wrong</div>
                  <div className="text-2xl font-black text-red-400">{state?.wrong_guesses || 0}</div>
                </div>
              </div>
            </div>

            {/* Primary Action Button */}
            <button
              onClick={() => setShowThemeSelector(true)}
              className="w-full py-5 bg-[#6366f1] hover:bg-[#4f46e5] text-white rounded-3xl font-black text-xl flex items-center justify-center gap-3 shadow-2xl shadow-indigo-500/40 transition-all hover:scale-[1.02] active:scale-95"
            >
              <RotateCcw className="w-6 h-6" />
              NEW THEME
            </button>
            
            {/* Word revelation on loss */}
            {state?.game_over && !state.won && (
              <div className="p-5 bg-red-500/10 border-2 border-red-500/20 rounded-3xl text-center animate-in fade-in zoom-in duration-500">
                <div className="text-[10px] text-red-400 uppercase font-black tracking-[0.2em] mb-2 opacity-60">The hidden word was</div>
                <div className="text-3xl font-black text-red-500 tracking-[0.3em]">{state.secret_word}</div>
              </div>
            )}
          </div>

        </div>
      </main>

      <footer className="text-center py-12 text-gray-600 text-[10px] font-black uppercase tracking-[0.3em]">
        <p>Word Guess Deluxe - Final Project <span className="text-[#6366f1]">Code in Place 2026</span></p>
      </footer>
    </div>
  )
}

export default App
