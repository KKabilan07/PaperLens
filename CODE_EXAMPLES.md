# PaperLens - Code Examples & Quick Start Guide

## Quick Start: Get Designer Setup Done in 1 Hour

### Step 1: Install Icons (2 minutes)
```bash
cd FrontEnd
npm install lucide-react
```

### Step 2: Create Design Variables File
**File**: `FrontEnd/src/styles/variables.css`

Copy-paste this:

```css
:root {
  /* PRIMARY COLORS */
  --color-primary: #667eea;
  --color-primary-dark: #764ba2;
  --color-primary-light: #f3f0ff;
  
  /* SEMANTIC COLORS */
  --color-success: #27ae60;
  --color-error: #e74c3c;
  --color-warning: #f39c12;
  --color-info: #3498db;
  
  /* TEXT COLORS */
  --color-text-primary: #2d2d2d;
  --color-text-secondary: #555555;
  --color-text-light: #999999;
  --color-text-muted: #b0b0b0;
  
  /* BACKGROUND COLORS */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f8f8f8;
  --color-bg-tertiary: #f0f0f0;
  --color-bg-light: #f5f5f5;
  
  /* BORDER COLORS */
  --color-border: #e0e0e0;
  --color-border-light: #f0f0f0;
  
  /* TYPOGRAPHY */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  --font-family-mono: 'Monaco', 'Courier New', monospace;
  
  /* FONT SIZES */
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
  --font-size-xl: 20px;
  --font-size-2xl: 24px;
  --font-size-3xl: 32px;
  
  /* FONT WEIGHTS */
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  
  /* LINE HEIGHTS */
  --line-height-tight: 1.2;
  --line-height-snug: 1.375;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;
  --line-height-loose: 2;
  
  /* SPACING */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  
  /* BORDER RADIUS */
  --radius-none: 0;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-2xl: 20px;
  --radius-full: 9999px;
  
  /* SHADOWS */
  --shadow-none: none;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  
  /* TRANSITIONS */
  --transition-fast: 150ms ease-in-out;
  --transition-normal: 300ms ease-in-out;
  --transition-slow: 500ms ease-in-out;
  
  /* Z-INDEX */
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
}

/* Dark mode support (optional future enhancement) */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: #1a1a1a;
    --color-bg-secondary: #2d2d2d;
    --color-text-primary: #f5f5f5;
    --color-text-secondary: #d0d0d0;
  }
}
```

### Step 3: Update Global Styles
**File**: `FrontEnd/src/index.css`

Replace with:

```css
/* Import design variables */
@import './styles/variables.css';

/* CSS Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
}

body {
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
  color: var(--color-text-primary);
  background-color: var(--color-bg-primary);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#root {
  width: 100%;
  height: 100%;
}

/* Typography Defaults */
h1 {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(--spacing-md);
}

h2 {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-snug);
  margin-bottom: var(--spacing-md);
}

h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-snug);
  margin-bottom: var(--spacing-sm);
}

p {
  margin-bottom: var(--spacing-md);
}

a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

/* Input Reset */
input, textarea, select {
  font-family: inherit;
  font-size: inherit;
}

button {
  font-family: inherit;
  cursor: pointer;
}

/* Remove default focus styles */
*:focus {
  outline: none;
}

/* Scrollbar Styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--color-bg-secondary);
}

::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: var(--radius-md);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-text-light);
}
```

---

## Component Examples

### 1. Reusable Button Component
**File**: `FrontEnd/src/Components/Common/Button.jsx`

```jsx
import React from 'react'
import './Button.css'

const Button = ({
  children,
  variant = 'primary', // primary, secondary, ghost, danger
  size = 'md', // sm, md, lg
  fullWidth = false,
  disabled = false,
  loading = false,
  onClick,
  className = '',
  type = 'button',
  ...props
}) => {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={`
        btn
        btn-${variant}
        btn-${size}
        ${fullWidth ? 'btn-full' : ''}
        ${loading ? 'btn-loading' : ''}
        ${className}
      `}
      {...props}
    >
      {loading ? (
        <span className="btn-spinner">
          ⚙️ {/* Or use lucide: <Loader className="spinner" /> */}
        </span>
      ) : (
        children
      )}
    </button>
  )
}

export default Button
```

**File**: `FrontEnd/src/Components/Common/Button.css`

```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-fast);
  cursor: pointer;
  white-space: nowrap;
}

/* Sizes */
.btn-sm {
  padding: 6px 12px;
  font-size: var(--font-size-xs);
}

.btn-md {
  padding: 10px 16px;
  font-size: var(--font-size-sm);
}

.btn-lg {
  padding: 12px 24px;
  font-size: var(--font-size-base);
}

/* Variants */
.btn-primary {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-secondary {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-bg-tertiary);
  border-color: var(--color-primary);
}

.btn-ghost {
  background: transparent;
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
}

.btn-ghost:hover:not(:disabled) {
  background: var(--color-primary-light);
}

.btn-danger {
  background: var(--color-error);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  opacity: 0.9;
}

/* Full width */
.btn-full {
  width: 100%;
}

/* Disabled */
.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading */
.btn-loading {
  position: relative;
}

.btn-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
```

### 2. Reusable Input Component
**File**: `FrontEnd/src/Components/Common/Input.jsx`

```jsx
import React, { useState } from 'react'
import { Eye, EyeOff } from 'lucide-react'
import './Input.css'

const Input = ({
  type = 'text',
  label,
  placeholder,
  value,
  onChange,
  error,
  success,
  disabled = false,
  required = false,
  className = '',
  helperText,
  ...props
}) => {
  const [showPassword, setShowPassword] = useState(false)

  const inputType =
    type === 'password' && showPassword ? 'text' : type

  return (
    <div className={`input-wrapper ${className}`}>
      {label && (
        <label className={`input-label ${required ? 'required' : ''}`}>
          {label}
        </label>
      )}
      <div className="input-container">
        <input
          type={inputType}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          disabled={disabled}
          className={`
            input
            ${error ? 'input-error' : ''}
            ${success ? 'input-success' : ''}
            ${disabled ? 'input-disabled' : ''}
          `}
          {...props}
        />
        {type === 'password' && (
          <button
            type="button"
            className="input-toggle-password"
            onClick={() => setShowPassword(!showPassword)}
            tabIndex="-1"
          >
            {showPassword ? (
              <EyeOff size={20} />
            ) : (
              <Eye size={20} />
            )}
          </button>
        )}
        {success && <span className="input-icon-success">✓</span>}
        {error && <span className="input-icon-error">!</span>}
      </div>
      {error && <p className="input-error-text">{error}</p>}
      {helperText && !error && (
        <p className="input-helper-text">{helperText}</p>
      )}
    </div>
  )
}

export default Input
```

**File**: `FrontEnd/src/Components/Common/Input.css`

```css
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}

.input-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
}

.input-label.required::after {
  content: ' *';
  color: var(--color-error);
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-family: inherit;
  transition: all var(--transition-fast);
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
}

.input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input:disabled {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-muted);
  cursor: not-allowed;
  opacity: 0.6;
}

.input-error {
  border-color: var(--color-error);
}

.input-error:focus {
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.input-success {
  border-color: var(--color-success);
}

.input-success:focus {
  box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1);
}

.input-toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: var(--color-text-light);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  transition: color var(--transition-fast);
}

.input-toggle-password:hover {
  color: var(--color-text-secondary);
}

.input-icon-success,
.input-icon-error {
  position: absolute;
  right: 12px;
  font-size: var(--font-size-lg);
}

.input-icon-success {
  color: var(--color-success);
}

.input-icon-error {
  color: var(--color-error);
}

.input-error-text {
  font-size: var(--font-size-xs);
  color: var(--color-error);
  margin: 0;
}

.input-helper-text {
  font-size: var(--font-size-xs);
  color: var(--color-text-light);
  margin: 0;
}
```

### 3. Provider Badge Component
**File**: `FrontEnd/src/Components/Common/ProviderBadge.jsx`

```jsx
import React from 'react'
import './ProviderBadge.css'

const ProviderBadge = ({ provider }) => {
  const getProviderColor = (provider) => {
    const providers = {
      'GPT-4': { bg: '#00a67e', text: 'white' },
      'Claude': { bg: '#9d8189', text: 'white' },
      'LLaMA': { bg: '#ffc107', text: 'black' },
      'Gemini': { bg: '#1f2937', text: 'white' },
    }
    return providers[provider] || { bg: '#667eea', text: 'white' }
  }

  const colors = getProviderColor(provider)

  return (
    <span
      className="provider-badge"
      style={{
        backgroundColor: colors.bg,
        color: colors.text,
      }}
    >
      {provider}
    </span>
  )
}

export default ProviderBadge
```

**File**: `FrontEnd/src/Components/Common/ProviderBadge.css`

```css
.provider-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-medium);
  white-space: nowrap;
}
```

---

## Updated Layout CSS

### Enhanced Main.css (Chat Layout)
**File**: `FrontEnd/src/Components/Main/Main.css`

```css
@import '../../styles/variables.css';

.main-container-full {
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: var(--color-bg-primary);
}

.sidebar-papers {
  width: 280px;
  background-color: var(--color-bg-secondary);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-sm);
}

.sidebar-scroll {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
}

.paper-item {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  background: var(--color-bg-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid var(--color-border);
}

.paper-item:hover {
  background: white;
  box-shadow: var(--shadow-sm);
}

.paper-item.active {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  border-color: transparent;
}

.paper-name {
  font-weight: var(--font-weight-medium);
  margin-bottom: var(--spacing-xs);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.paper-meta {
  font-size: var(--font-size-xs);
  opacity: 0.7;
}

.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.chat-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.chat-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-primary);
}

.chat-meta {
  font-size: var(--font-size-xs);
  color: var(--color-text-light);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.message {
  display: flex;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
  word-wrap: break-word;
}

.message.user .message-content {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
}

.message.bot .message-content {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border-left: 3px solid var(--color-primary);
}

.message.bot .sources {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-sm);
}

.source-tag {
  display: inline-block;
  padding: 4px 8px;
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-xs);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.source-tag:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.chat-input-area {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  background: white;
  display: flex;
  gap: var(--spacing-sm);
  align-items: flex-end;
}

.chat-input-wrapper {
  flex: 1;
  display: flex;
  gap: var(--spacing-sm);
  align-items: flex-end;
}

.chat-input {
  flex: 1;
  padding: 10px 12px;
  min-height: 40px;
  max-height: 120px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-family: inherit;
  font-size: var(--font-size-sm);
  resize: none;
  transition: border-color var(--transition-fast);
}

.chat-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.chat-send-btn {
  padding: 10px 16px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-lg);
  transition: all var(--transition-fast);
}

.chat-send-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.chat-send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--color-text-light);
}

.empty-state-icon {
  font-size: 48px;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.empty-state-text {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-container-full {
    flex-direction: column;
  }

  .sidebar-papers {
    width: 100%;
    height: auto;
    max-height: 200px;
    border-right: none;
    border-bottom: 1px solid var(--color-border);
  }

  .message-content {
    max-width: 85%;
  }

  .chat-input-area {
    flex-direction: column;
  }

  .chat-input {
    width: 100%;
  }

  .chat-send-btn {
    width: 100%;
  }
}
```

---

## Optional: Dark Mode Support

Add this file to support dark mode:

**File**: `FrontEnd/src/styles/dark-mode.css`

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: #1a1a1a;
    --color-bg-secondary: #2d2d2d;
    --color-bg-tertiary: #383838;
    --color-bg-light: #404040;
    
    --color-text-primary: #f5f5f5;
    --color-text-secondary: #d0d0d0;
    --color-text-light: #989898;
    
    --color-border: #404040;
  }

  .message.bot .message-content {
    background: var(--color-bg-secondary);
  }

  .chat-area {
    background: var(--color-bg-primary);
  }
}
```

---

## Installation Steps (Copy-Paste Ready)

### 1. Copy variables file content above
```bash
# Create the file
touch FrontEnd/src/styles/variables.css
# Then paste the variables.css content
```

### 2. Update index.css
```bash
# Backup first
cp FrontEnd/src/index.css FrontEnd/src/index.css.backup
# Then replace with content above
```

### 3. Create Button component
```bash
mkdir -p FrontEnd/src/Components/Common
# Create Button.jsx and Button.css with content above
```

### 4. Create Input component
```bash
# Create Input.jsx and Input.css with content above
```

### 5. Update Main.css
```bash
# Backup first
cp FrontEnd/src/Components/Main/Main.css FrontEnd/src/Components/Main/Main.css.backup
# Then replace with enhanced version above
```

---

## Usage Examples

### Using Button Component
```jsx
import Button from '../Components/Common/Button'

<Button variant="primary" size="md">
  Login
</Button>

<Button variant="secondary" fullWidth>
  Sign Up
</Button>

<Button variant="ghost" loading>
  Uploading...
</Button>
```

### Using Input Component
```jsx
import Input from '../Components/Common/Input'
import { useState } from 'react'

function MyForm() {
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')

  const handleEmail = (e) => {
    setEmail(e.target.value)
    // Clear error on change
    if (error) setError('')
  }

  return (
    <Input
      type="email"
      label="Email Address"
      placeholder="you@example.com"
      value={email}
      onChange={handleEmail}
      error={error}
      helperText="We'll never share your email"
    />
  )
}
```

### Using Provider Badge
```jsx
import ProviderBadge from '../Components/Common/ProviderBadge'

<div>
  <p>Response from <ProviderBadge provider="GPT-4" /></p>
</div>
```

---

## Next Steps

1. ✅ Copy the `variables.css` content into your project
2. ✅ Update `index.css` with global styles
3. ✅ Create the Button and Input components
4. ✅ Update `Main.css` with the new version
5. ✅ Test components in your pages
6. ✅ Install lucide-react for icons
7. ✅ Refine LoginPage with split layout
8. ✅ Add responsive queries

You now have a solid foundation for a professional PaperLens UI!
