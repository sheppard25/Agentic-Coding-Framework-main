// @ts-check

import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import reactRecommended from 'eslint-plugin-react/configs/recommended.js';
import reactJsxRuntime from 'eslint-plugin-react/configs/jsx-runtime.js';
import reactHooks from 'eslint-plugin-react-hooks';
import eslintConfigPrettier from 'eslint-config-prettier';

export default tseslint.config(
  {
    // Global ignores
    ignores: [
      "dist/",
      "node_modules/",
      // "eslint.config.js", // REMOVE THIS LINE
      "vite.config.ts",
      // If you have .js files you don't want linted by TS-ESLint, consider ignoring them
      // For example: "**/*.js"
    ],
  },

  // 1. Base ESLint recommended rules (for general JavaScript)
  eslint.configs.recommended,

  // 2. TypeScript type-aware linting configuration
  // This spread includes the TypeScript parser, plugin, and recommended type-checked rules.
  // It applies to .ts, .tsx, .mts, .cts files.
  ...tseslint.configs.recommendedTypeChecked,
  // This separate config object provides the necessary parserOptions for type-aware linting.
  {
    languageOptions: {
      parserOptions: {
        project: true, // Crucial for type-aware rules
        tsconfigRootDir: import.meta.dirname, // Assumes tsconfig.json is in 'frontend/'
      },
    },
    // You can add/override specific type-aware rules here if needed
    // rules: {
    //   '@typescript-eslint/no-floating-promises': 'error',
    // },
  },

  // 3. React specific settings
  {
    files: ['src/**/*.{ts,tsx}'], // Apply React rules primarily to files in src/
    ...reactRecommended, // Base React recommended rules
    ...reactJsxRuntime, // For the new JSX transform
    settings: {
      react: {
        version: 'detect', // Automatically detect React version
      },
    },
    rules: {
      'react/prop-types': 'off', // Often turned off in TypeScript projects
      // Add any other React specific rule overrides here
    },
  },

  // 4. React Hooks plugin configuration
  {
    files: ['src/**/*.{ts,tsx}'], // Apply to the same files as React settings
    plugins: {
      'react-hooks': reactHooks,
    },
    rules: {
      ...reactHooks.configs.recommended.rules, // Recommended rules for React Hooks
    },
  },

  // 5. Prettier configuration (must be the last one to override other formatting rules)
  eslintConfigPrettier
);