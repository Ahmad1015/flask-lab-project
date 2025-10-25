import { beforeEach, describe, expect, test } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../App.jsx'

beforeEach(() => {
  window.localStorage.clear()
})

describe('App todo flow', () => {
  test('renders hero copy and empty state', () => {
    render(<App />)

    expect(
      screen.getByRole('heading', { name: /plan the day, enjoy the momentum/i }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(
        /no tasks yet\. add your first plan above to start the flow\./i,
      ),
    ).toBeInTheDocument()
  })

  test('allows adding todos and updates progress indicators', async () => {
    const user = userEvent.setup()
    render(<App />)

    const input = screen.getByPlaceholderText(
      /outline a plan, jot a reminder, or capture an idea/i,
    )
    const submitButton = screen.getByRole('button', { name: /add task/i })

    await user.type(input, 'Write API docs')
    await user.click(submitButton)

    const todo = await screen.findByText('Write API docs')
    expect(todo).toBeInTheDocument()
    expect(
      screen.getByText(/1 remaining · 0 done/i, { selector: '.progress-meta span' }),
    ).toBeInTheDocument()
  })

  test('completes todos and filters by status', async () => {
    const user = userEvent.setup()
    render(<App />)

    const input = screen.getByPlaceholderText(
      /outline a plan, jot a reminder, or capture an idea/i,
    )
    const submitButton = screen.getByRole('button', { name: /add task/i })

    await user.type(input, 'Fix styling bug')
    await user.click(submitButton)

    const checkbox = screen.getByRole('checkbox', { name: /mark complete/i })
    await user.click(checkbox)

    expect(checkbox).toBeChecked()
    expect(
      screen.getByText(/0 remaining · 1 done/i, { selector: '.progress-meta span' }),
    ).toBeInTheDocument()

  await user.click(screen.getByRole('button', { name: /^Completed$/i }))
    expect(screen.getByText('Fix styling bug')).toBeInTheDocument()

  await user.click(screen.getByRole('button', { name: /^Active$/i }))
    expect(
      screen.getByText(
        /nothing to show here\. switch filters or add a fresh task\./i,
      ),
    ).toBeInTheDocument()

  await user.click(screen.getByRole('button', { name: /^All$/i }))
    expect(screen.getByText('Fix styling bug')).toBeInTheDocument()
  })
})
