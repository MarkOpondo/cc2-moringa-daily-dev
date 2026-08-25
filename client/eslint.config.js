import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{js,jsx}'],
    extends: [
      js.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: { ecmaFeatures: { jsx: true } },
    },
    rules: {
      // This project doesn't use React Compiler yet, and this rule flags
      // the standard "fetch data in useEffect, setLoading around it"
      // pattern used throughout the app's pages — not an actual bug.
      // Revisit if/when the team adopts React Compiler.
      'react-hooks/set-state-in-effect': 'off',
    },
  },
])
