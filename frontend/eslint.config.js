// @ts-check

import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import reactRecommended from 'eslint-plugin-react/configs/recommended.js';
import reactJsxRuntime from 'eslint-plugin-react/configs/jsx-runtime.js';
import reactHooks from 'eslint-plugin-react-hooks';
import eslintConfigPrettier from 'eslint-config-prettier'; // To disable ESLint rules that conflict with Prettier
// import globals from 'globals'; // Uncomment if you need to define global variables

export default tseslint.config(
  {
    ignores: ["dist", "node_modules", "eslint.config.js", "vite.config.ts"], // Added vite.config.ts
  },
  eslint.configs.recommended, // ESLint's built-in recommended rules
  ...tseslint.configs.recommendedTypeChecked, // TypeScript specific rules (type-aware)
  // OR for non-type-aware: ...tseslint.configs.recommended,
  { // React specific settings
    files: ['**/*.{ts,tsx}'],
    ...reactRecommended,
    ...reactJsxRuntime,
    languageOptions: {
      ...reactRecommended.languageOptions,
      parserOptions: {
        project: true, // Enable type-aware linting
        tsconfigRootDir: import.meta.dirname, // Or your frontend project root
      },
      // globals: { // Example for browser globals
      //   ...globals.browser,
      // },
    },
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      // Your specific React rules or overrides
      'react/prop-types': 'off', // Often not needed with TypeScript
    },
  },
  { // Configuration for React Hooks plugin
    files: ['**/*.{ts,tsx}'],
    plugins: {
      'react-hooks': reactHooks,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
    },
  },
  { // Configuration for React Refresh plugin (optional, Vite handles much of this)
    files: ['**/*.{ts,tsx}'],
    plugins: {
      // 'react-refresh': eslintPluginReactRefresh (if you installed and imported it)
    },
    rules: {
      // 'react-refresh/only-export-components': 'warn', // Example rule
    }
  },
  eslintConfigPrettier // This should be last to override other configs
);