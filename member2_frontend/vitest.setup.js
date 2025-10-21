import { webcrypto } from 'node:crypto'
import '@testing-library/jest-dom/vitest'

if (!globalThis.crypto) {
	globalThis.crypto = webcrypto
}

if (typeof window !== 'undefined' && !window.matchMedia) {
	window.matchMedia = (query) => ({
		matches: query.includes('dark'),
		media: query,
		onchange: null,
		addEventListener: () => undefined,
		removeEventListener: () => undefined,
		addListener: () => undefined,
		removeListener: () => undefined,
		dispatchEvent: () => false,
	})
}
