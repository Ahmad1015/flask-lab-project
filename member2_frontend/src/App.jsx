import { useEffect, useMemo, useState } from 'react'
import './App.css'

const STORAGE_KEY = 'flask-lab-todos'

const filters = {
  all: () => true,
  active: (todo) => !todo.completed,
  completed: (todo) => todo.completed,
}

const createId = () =>
  typeof crypto !== 'undefined' && crypto.randomUUID
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(16).slice(2)}`

const getStoredTodos = () => {
  if (typeof window === 'undefined') {
    return []
  }

  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) {
      return []
    }

    const parsed = JSON.parse(raw)
    if (!Array.isArray(parsed)) {
      return []
    }

    return parsed
      .map((item) => ({
        id: item.id ?? createId(),
        text: typeof item.text === 'string' ? item.text : '',
        completed: Boolean(item.completed),
        createdAt: typeof item.createdAt === 'number' ? item.createdAt : Date.now(),
      }))
      .filter((todo) => todo.text.trim().length > 0)
  } catch (error) {
    console.warn('Failed to read todos from storage:', error)
    return []
  }
}

function App() {
  const [todos, setTodos] = useState(getStoredTodos)
  const [filter, setFilter] = useState('all')
  const [draft, setDraft] = useState('')
  const [theme, setTheme] = useState(() => {
    if (typeof window === 'undefined' || !window.matchMedia) {
      return 'light'
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light'
  })

  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-theme', theme)
    }
  }, [theme])

  useEffect(() => {
    if (typeof window === 'undefined') {
      return
    }

    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(todos))
  }, [todos])

  const filteredTodos = useMemo(
    () => todos.filter(filters[filter] ?? filters.all),
    [todos, filter],
  )

  const remainingCount = useMemo(
    () => todos.filter((todo) => !todo.completed).length,
    [todos],
  )

  const progress = useMemo(() => {
    if (todos.length === 0) {
      return 0
    }

    return Math.round(((todos.length - remainingCount) / todos.length) * 100)
  }, [todos.length, remainingCount])

  const handleSubmit = (event) => {
    event.preventDefault()
    const value = draft.trim()

    if (!value) {
      return
    }

    setTodos((current) => [
      {
        id: createId(),
        text: value,
        completed: false,
        createdAt: Date.now(),
      },
      ...current,
    ])
    setDraft('')
  }

  const handleToggle = (id) => {
    setTodos((current) =>
      current.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo,
      ),
    )
  }

  const handleDelete = (id) => {
    setTodos((current) => current.filter((todo) => todo.id !== id))
  }

  const handleClearCompleted = () => {
    setTodos((current) => current.filter((todo) => !todo.completed))
  }

  const completedCount = todos.length - remainingCount

  return (
    <div className="app-root">
      <div className="app-shell">
        <header className="app-header">
          <div>
            <p className="eyebrow">Task Flow</p>
            <h1>Plan the day, enjoy the momentum</h1>
            <p className="subtitle">
              Capture your todos, tick them off, and keep track of progress with
              a delightful motion experience.
            </p>
          </div>
          <button
            type="button"
            className="theme-toggle"
            onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
          >
            {theme === 'light' ? 'Switch to dark' : 'Switch to light'} mode
          </button>
        </header>

        <section className="progress-card" aria-live="polite">
          <div className="progress-bar">
            <span
              className="progress-track"
              aria-hidden="true"
              style={{ width: `${progress}%` }}
            />
          </div>
          <div className="progress-meta">
            <strong>{progress}% complete</strong>
            <span>
              {remainingCount} remaining · {completedCount} done
            </span>
          </div>
        </section>

        <form className="todo-form" onSubmit={handleSubmit}>
          <label className="todo-label" htmlFor="todo-input">
            Add a new task
            Ahmad changed this
          </label>
          <div className="todo-input-group">
            <input
              id="todo-input"
              name="todo"
              placeholder="Outline a plan, jot a reminder, or capture an idea"
              autoComplete="off"
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
            />
            <button type="submit" className="primary-action">
              Add task
            </button>
          </div>
        </form>

        <div className="todo-controls" role="toolbar" aria-label="Filters">
          <div className="filters">
            {Object.keys(filters).map((key) => (
              <button
                key={key}
                type="button"
                className={`filter-btn${filter === key ? ' is-active' : ''}`}
                onClick={() => setFilter(key)}
              >
                {key.charAt(0).toUpperCase() + key.slice(1)}
              </button>
            ))}
          </div>
          <button
            type="button"
            className="ghost-action"
            onClick={handleClearCompleted}
            disabled={completedCount === 0}
          >
            Clear completed
          </button>
        </div>

        <section className="todo-list" aria-live="polite">
          {filteredTodos.length === 0 ? (
            <p className="empty-state">
              {todos.length === 0
                ? 'No tasks yet. Add your first plan above to start the flow.'
                : 'Nothing to show here. Switch filters or add a fresh task.'}
            </p>
          ) : (
            <ul>
              {filteredTodos.map((todo, index) => (
                <li
                  key={todo.id}
                  className={`todo-item${todo.completed ? ' is-complete' : ''}`}
                  style={{ animationDelay: `${index * 60}ms` }}
                >
                  <label className="todo-checkbox">
                    <input
                      type="checkbox"
                      checked={todo.completed}
                      onChange={() => handleToggle(todo.id)}
                    />
                    <span aria-hidden="true" className="checkbox-visual" />
                    <span className="visually-hidden">
                      Mark {todo.completed ? 'incomplete' : 'complete'}
                    </span>
                  </label>
                  <div className="todo-content">
                    <p>{todo.text}</p>
                    <span>
                      Added {new Date(todo.createdAt).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                  </div>
                  <button
                    type="button"
                    className="delete-action"
                    onClick={() => handleDelete(todo.id)}
                    aria-label={`Delete ${todo.text}`}
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  )
}

export default App
