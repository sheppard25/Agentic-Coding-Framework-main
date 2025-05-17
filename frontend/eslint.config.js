// @ts-check

import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import reactRecommended from 'eslint-plugin-react/configs/recommended.js';
import reactJsxRuntime from 'eslint-plugin-react/configs/jsx-runtime.js'; // For new JSX transform
// import reactHooks from 'eslint-plugin-react-hooks'; // If you use hooks plugin
// import globals from 'globals'; // For global variables

export default tseslint.config(
  {
    ignores: ["dist", "node_modules", "eslint.config.js"], // Folders/files to ignore
  },
  eslint.configs.recommended, // ESLint recommended rules
  ...tseslint.configs.recommended, // TypeScript recommended rules
  { // React specific settings
    files: ['**/*.{ts,tsx}'], // Apply only to TS/TSX files
    ...reactRecommended,
    ...reactJsxRuntime, // Use this if your React version supports the new JSX transform
    settings: {
      react: {
        version: 'detect', // Automatically detect React version
      },
    },
    languageOptions: {
      ...reactRecommended.languageOptions,
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
      // globals: { // Example if you need browser globals
      //   ...globals.browser,
      // },
    },
    rules: {
      // Add or override rules here
      // e.g., 'react/prop-types': 'off',
      // If using eslint-plugin-react-hooks:
      // 'react-hooks/rules-of-hooks': 'error',
      // 'react-hooks/exhaustive-deps': 'warn',
    },
  }
  // Add other configurations if needed (e.g., for Prettier integration, specific plugins)
);