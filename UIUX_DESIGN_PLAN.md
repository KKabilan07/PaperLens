# PaperLens - Complete UI/UX Design Plan

## Executive Summary
This document outlines a modern, professional design system for PaperLens with a clean landing page, intuitive authentication flow, and a productive chat/paper management interface.

---

## Part 1: Design Philosophy & Goals

### Core Principles
- **Clean & Minimal**: Avoid clutter, focus on content
- **Research-Focused**: Design for academics and researchers
- **Consistent**: Unified component system across all pages
- **Accessible**: WCAG 2.1 AA compliance
- **Responsive**: Works seamlessly on desktop, tablet, mobile

### Target Audience
- Graduate students & researchers
- Academic professionals
- Industry R&D teams
- All skill levels (intuitive enough for non-tech users)

---

## Part 2: Complete Route Structure & Navigation Map

### Routes Overview
```
/
├── /login                    (Authentication Page)
├── /auth/callback           (OAuth Redirect Handler)
├── /chat                    (Main Chat Interface)
├── /chat/:paperId          (Paper-Specific Chat - Optional Enhancement)
├── /dashboard              (Optional: Future Enhancement)
└── (redirect logic)
```

### Navigation Flow
```
Landing (Hero) → Get Started Button
         ↓
/login (Auth Page)
  ├─ OAuth (Google/GitHub) → /auth/callback → /chat
  └─ Email/Password (Login/Sign Up)
                              ↓
                        /chat (Main Interface)
                          ├─ Upload Paper
                          ├─ Select Paper from Sidebar
                          ├─ Chat with Paper
                          └─ View History
```

---

## Part 3: Page-by-Page Design Specifications

### 3.1 LANDING PAGE (Hero Section) - ✅ YES

**Status**: Already Implemented
**Location**: Shown when user is not authenticated
**Design**: Full-screen gradient hero

#### Layout Structure
```
┌─────────────────────────────────────────┐
│                                         │
│         Landing/Hero Page               │
│     ┌──────────────────────────┐       │
│     │                          │       │
│     │  PaperLens              │       │
│     │  Your AI Research        │       │
│     │  Assistant              │       │
│     │                          │       │
│     │  [Get Started Button]    │       │
│     │                          │       │
│     └──────────────────────────┘       │
│                                         │
└─────────────────────────────────────────┘
```

#### Components
- **Logo/Icon** (Top optional): Small PaperLens icon or simplified mark
- **Headline**: "PaperLens"
- **Subheading**: "Your AI-Powered Research Assistant"
- **Description**: 2-3 lines about value proposition
- **CTA Button**: "Get Started" (White text on gradient)
- **Optional**: Floating icons representing features (optional for visual appeal)

#### Styling
- **Background**: Gradient `135deg, #667eea 0%, #764ba2 100%` (Purple/Blue)
- **Height**: 100vh (Full viewport)
- **Text**: White, centered, readable
- **Animation**: Subtle fade-in on load (optional)

#### Content Example
```
🔬 PaperLens

Your AI-Powered Research Assistant

Upload research papers and let AI help you extract 
insights, find connections, and accelerate your workflow.

[Get Started →]
```

---

### 3.2 AUTHENTICATION PAGE - /login

**Design Approach**: Single-Page with Form Modal/Card
**Two States**: Initial (Hero-like) & Auth Form

#### Option A: Split Layout (RECOMMENDED FOR DESKTOP)

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  ┌──────────────────┐    ┌──────────────────────────┐ │
│  │   Left Side      │    │   Right Side (Form)      │ │
│  │   Content        │    │                          │ │
│  │                  │    │  ┌────────────────────┐  │ │
│  │  ┌──────────┐    │    │  │ Login / Sign Up    │  │ │
│  │  │ Logo     │    │    │  │                    │  │ │
│  │  └──────────┘    │    │  │ Email              │  │ │
│  │                  │    │  │ [text input]       │  │ │
│  │  PaperLens       │    │  │                    │  │ │
│  │                  │    │  │ Password           │  │ │
│  │  Transform your  │    │  │ [password input]   │  │ │
│  │  research with   │    │  │                    │  │ │
│  │  AI              │    │  │ [Login Button]     │  │ │
│  │                  │    │  │                    │  │ │
│  │  • Upload PDFs   │    │  │ Or continue with:  │  │ │
│  │  • Ask Questions │    │  │ [Google] [GitHub]  │  │ │
│  │  • Get Answers   │    │  │                    │  │ │
│  │                  │    │  │ No account?        │  │ │
│  │  Beautiful UI    │    │  │ Sign Up →          │  │ │
│  │  Instant Results │    │  │                    │  │ │
│  │                  │    │  └────────────────────┘  │ │
│  └──────────────────┘    └──────────────────────────┘ │
│                                                        │
└────────────────────────────────────────────────────────┘
```

#### Left Side Content (50% width on desktop)
```
Styling:
- Background: Gradient (same purple/blue as hero)
- Text: White
- Padding: 40-60px
- Display: Flex, center

Content:
- Logo/Icon (larger)
- Headline: "PaperLens"
- Tagline: "Your AI Research Assistant"
- 3-4 Feature bullets with small icons:
  ✓ Upload PDF research papers
  ✓ Ask questions in natural language
  ✓ Get AI-powered insights from sources
  ✓ Understand complex topics faster
```

#### Right Side Form (50% width on desktop)
```
White background with subtle shadow
Card-like appearance with padding: 40px

Elements (Top to Bottom):
1. "Login to PaperLens" / "Create Account" (Tab toggle)
2. Email Input Field
   - Label: "Email Address"
   - Placeholder: "you@example.com"
   - Validation on blur

3. Password Input Field
   - Label: "Password"
   - Show/Hide toggle icon
   - Min 8 characters

4. [For Sign Up] Confirm Password
   - Label: "Confirm Password"
   - Match validation

5. [For Sign Up] Full Name (optional)
   - Label: "Full Name (Optional)"
   - Placeholder: "John Doe"

6. Forgot Password Link (Login mode only)
   - "Forgot password?" → Password reset flow

7. Login/Sign Up Button
   - Full width
   - Gradient background (same as hero)
   - Hover: Slight lift, shadow increase

8. Divider: "Or continue with"

9. OAuth Buttons (Side by side)
   - Google OAuth
   - GitHub OAuth
   - Icons + labels
   - Full width stack on mobile

10. Toggle Link
    - "Don't have account? Sign Up"
    - "Already have account? Login"
```

#### Responsive Behavior

**Desktop (1024px+)**:
- 50/50 split layout
- Both sides visible together
- Card height matches content

**Tablet (768px - 1023px)**:
- 60% form / 40% content
- Content icons smaller
- Reduced padding

**Mobile (< 768px)**:
- Full width form
- Left side content slides under (collapsed)
- Or: Left content becomes header above form
- Form padding: 20px
- Single column everything

#### Form Validation & States
```
Email Input States:
✓ Default: Empty with placeholder
✓ Focus: Blue border, subtle shadow
✓ Valid: Green checkmark icon
✓ Invalid: Red border + error message
✓ Disabled: Gray, not clickable

Password Input States:
✓ Default: Empty with dots/asterisks
✓ Show/Hide: Toggle eye icon
✓ Focus: Blue border
✓ Strength indicator (optional):
  - Weak (Red)
  - Medium (Orange)
  - Strong (Green)

Button States:
✓ Default: Gradient, cursor pointer
✓ Hover: Lifted (transform: translateY(-2px))
✓ Loading: Spinner, disabled
✓ Error: Red background, shake animation
✓ Success: Green checkmark
```

#### Typography for Login Page
```CSS
Title: "Login / Sign Up"
- Font Size: 28px
- Weight: 600
- Color: #2d2d2d

Label: "Email Address"
- Font Size: 14px
- Weight: 500
- Color: #555555

Input Placeholder
- Font Size: 14px
- Color: #999999

Error Message
- Font Size: 12px
- Color: #e74c3c
- Margin Top: 4px

Helper Text
- Font Size: 12px
- Color: #7f8c8d
```

---

### 3.3 MAIN CHAT INTERFACE - /chat

**Layout**: Two-Column (Sidebar + Main Chat Area)
**Status**: Partially implemented, needs refinement

#### Full Layout Structure

```
┌──────────────────────────────────────────────────────────────┐
│                        TOP NAVBAR                            │
│  Logo  |  User Info  |  Settings  |  Notifications  Logout   │
├──────────────────────────────────────────────────────────────┤
│         │                                                     │
│  PAPERS │                                                     │
│  SIDEBAR│                    MAIN CHAT AREA                  │
│         │                                                     │
│         │   [Paper Title]                                    │
│  Recent │                                                     │
│  Papers │   ┌─────────────────────────────────────────────┐  │
│         │   │                                             │  │
│  • Paper│   │                                             │  │
│    1    │   │            Message History                  │  │
│         │   │            (Auto-scrolling)                 │  │
│  • Paper│   │                                             │  │
│    2    │   │  User: "What is..."    [Timestamp]          │  │
│         │   │  Bot: "Based on the paper..." [Provider]    │  │
│         │   │  Sources: [Citation 1] [Citation 2]         │  │
│         │   │                                             │  │
│  Upload │   │  User: "Can you explain..."                 │  │
│  PDF    │   │  Bot: "..." [Sources]                       │  │
│  Button │   │                                             │  │
│         │   └─────────────────────────────────────────────┘  │
│         │   ┌─────────────────────────────────────────────┐  │
│         │   │ [Input] Ask a question... [Send Button]     │  │
│         │   └─────────────────────────────────────────────┘  │
│         │                                                     │
└──────────────────────────────────────────────────────────────┘
```

#### 3.3.1 TOP NAVBAR

**Height**: 60-70px
**Background**: White with bottom border (subtle shadow)
**Sticky**: Yes (stays on top on scroll)

**Left Section**:
- Logo icon (20x20px) + "PaperLens" text
- Font: 20px, weight 600

**Center Section** (Optional):
- Current view indicator
- Example: "📄 Analyzing 'ResearchPaper.pdf'"

**Right Section**:
1. Search icon (future feature)
2. Settings icon → Dropdown menu
3. User avatar (circular, 40x40px)
4. User name or email
5. Logout button (text or icon)

#### 3.3.2 LEFT SIDEBAR (Papers/Documents Panel)

**Width**: 
- Desktop: 280px
- Tablet: 250px
- Mobile: 100% (full width, expandable as drawer)

**Background**: Off-white/Light gray (#f8f8f8)
**Border**: Right border (1px, #e0e0e0)

**Top Section** (40% height):
```
┌─────────────────────────┐
│ [Menu Icon] [+] New Chat│ (50px)
├─────────────────────────┤
│                         │
│ 📄 Active Paper Name    │ (selected: blue bg)
│   (Currently selected)  │
│                         │
│ 📄 Paper 2 Name         │
│   (Hover: light gray)   │
│                         │
│ 📄 Paper 3 Name         │
│   (Right-click → menu)  │
│                         │
│ See All Papers »        │ (link)
│                         │
└─────────────────────────┘
```

**Features**:
- Each paper item: 50px height
- Hover state: Light background (#f0f0f0)
- Selected state: Blue background + white text
- Right-click context menu:
  - View Details
  - Rename
  - Delete
  - Download
- Scroll area for many papers

**Bottom Section** (60% height):
```
┌─────────────────────────┐
│ Upload PDF              │
│ [Upload Button]         │ (Full width, centered)
│                         │
├─────────────────────────┤
│ QUICK ACTIONS           │
│ ⓘ Help                  │
│ ⏱ Activity              │
│ ⚙  Settings             │
│ ⭐️ Favorites            │
│                         │
└─────────────────────────┘
```

**Upload Button Styling**:
- Background: Gradient (purple)
- Color: White
- Border: 2px dashed if empty
- Hover: Lift effect
- Click: File picker dialog

#### 3.3.3 MAIN CHAT AREA (70% on desktop)

**Background**: Clean white (#ffffff)
**Padding**: 20-30px

**Header (Within Chat Area)**:
```
┌─────────────────────────────────────────────┐
│ 📄 ResearchPaper.pdf                        │
│ Uploaded: 2024-04-10 | 12 pages | 2.4 MB   │
│ Status: ✓ Indexed and ready                 │
└─────────────────────────────────────────────┘
```

**Message Timeline Area**:
- Max-width: 800px (centered in chat area)
- Auto-scrolls to latest message
- Padding: 20px vertical between messages

**Message Styles**:

User Message:
```
┌─────────────────────────────────────────┐
│ ► User Message (Right-aligned)          │
│ "What are the key findings?"            │
│                                         │
│ Today, 2:35 PM                          │
└─────────────────────────────────────────┘
  Background: Light blue (#e3f2fd)
  Text: #333
  Border-radius: 12px
  Padding: 12px 16px
  Margin: 0 0 16px auto
  Max-width: 70%
```

Bot Message:
```
┌─────────────────────────────────────────┐
│ ◀ AI Assistant Response                 │
│ "Based on the paper, the key findings   │
│  are..."                                │
│                                         │
│ Provided by: GPT-4 | Sources: 3         │
│ [Source 1] [Source 2] [Source 3] [+]    │
│                                         │
│ Today, 2:36 PM                          │
└─────────────────────────────────────────┘
  Background: #f5f5f5 or white with border
  Text: #333
  Border-radius: 12px
  Padding: 12px 16px
  Margin: 0 0 16px 0
  Max-width: 80%
```

**Provider Badge**:
- Style: Small pill
- Content: "GPT-4" or "Claude" or "LLaMA"
- Position: Below response
- Background: Light color (provider-specific)
- Font Size: 12px

**Sources Display**:
- Style: Inline tags below response
- Format: "[Page X: Quote...]"
- Click: Shows full context from PDF
- Hover: Underline, cursor pointer

**Message States**:
- Sending: Spinner animation
- Sent: Checkmark
- Failed: Red icon + retry button
- Edited: "Edited" label

**Input Area (Bottom)**:
```
┌─────────────────────────────────────────┐
│ [Text Input Field]                [Send]│
│ "Ask a question about this paper..." ► │
└─────────────────────────────────────────┘

Position: Fixed at bottom or inside scrolling area
Background: White
Border: 1px #ddd, top shadow
Input Area:
  - Padding: 12px
  - Auto-expand (up to 150px height)
  - Placeholder: "Ask a question..."
  - Font: 16px
Send Button:
  - Small arrow icon or "Send"
  - Background: #667eea
  - Hover: Darker shade
  - Disabled: Gray when input empty
```

**Loading States**:
```
When AI is responding:
"Analyzing paper... ⚙️ (animated)"
"Generating response..." (with spinner)
```

**Error Messages**:
```
Position: In chat area, full-width banner
Style: Red background (#ffebee)
Content: "⚠️  Failed to send. Try Again?"
Dismiss: Auto-dismiss after 5 seconds or click X
```

#### 3.3.4 RESPONSIVE BEHAVIOR

**Desktop (1024px+)**:
- Sidebar: 280px (collapsible)
- Chat area: Remaining space
- Both visible simultaneously

**Tablet (768px - 1024px)**:
- Sidebar: 240px (smaller)
- Chat area: Remaining space
- Menu collapsed by default

**Mobile (< 768px)**:
- Sidebar: Full-screen drawer (hamburger menu toggle)
- Chat area: Full width
- Sidebar slides in from left
- Message input: Sticky at bottom
- Adjust padding and font sizes

---

## Part 4: Color Scheme & Typography

### Color Palette

**Primary Colors**:
```
Primary Gradient: #667eea → #764ba2 (Purple/Blue)
Primary Button: #667eea
Primary Accent: #764ba2

Secondary Colors:
Success Green: #27ae60
Error Red: #e74c3c
Warning Orange: #f39c12
Info Blue: #3498db

Neutral Grays:
Dark Text: #2d2d2d
Medium Text: #555555
Light Text: #999999
Light Background: #f8f8f8
Border Color: #e0e0e0
White: #ffffff
```

### Typography System

**Font Family**: 
```
Primary: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
Code: 'Monaco', 'Courier New', monospace
Fallback: -apple-system, BlinkMacSystemFont, sans-serif
```

**Font Sizes**:
```
H1 (Page Title): 32-40px
H2 (Section): 24-28px
H3 (Subsection): 18-20px
Body Large: 16px
Body Regular: 14px
Body Small: 12px
Label: 12-13px
```

**Font Weights**:
```
Headings: 600-700
Labels: 500
Body: 400
Light: 300
```

**Line Heights**:
```
Headings: 1.2-1.3
Body: 1.5-1.6
Labels: 1.4
```

---

## Part 5: Required Assets & Images

### Images to Download/Create

#### 1. **Icons Set** (Recommended: Font Awesome or Heroicons)

Essential Icons:
- Menu (hamburger) - 24x24
- Plus (new chat) - 24x24
- Upload - 24x24
- Send/Arrow - 20x20
- Settings - 24x24
- Help - 24x24
- Activity - 24x24
- Star/Favorite - 24x24
- Trash/Delete - 20x20
- Download - 20x20
- Check/Checkmark - 16x16
- Spinner/Loading (animated) - 24x24
- Eye (show password) - 20x20
- Google Logo - 20x20
- GitHub Logo - 20x20

**Recommended Source**: 
- Font Awesome (free tier): https://fontawesome.com/
- Heroicons: https://heroicons.com/ (excellent for modern UI)
- Lucide Icons: https://lucide.dev/ (lightweight, beautiful)

#### 2. **Brand Assets**

Logo Options:
- Option A: Simple text "PaperLens" with icon
- Option B: Abstract document/magnifying glass icon
- Option C: Layered paper illustration

Suggested Design:
```
Icon Concept:
  📄 (Paper) + 🔍 (Lens/Search) combined
  Or: Minimalist document with highlighted section
  Size: 32x32px for navbar, 64x64px for login page
```

**Action**: You can:
1. Use existing generic icons (fast)
2. Create your own in Figma (design tool)
3. Commission from Fiverr/99designs ($50-300)
4. Use AI tools like DALL-E or Midjourney

#### 3. **Background Images** (Optional but Recommended)

Landing Page:
- Subtle gradient (already done: purple/blue)
- Optional: Add abstract shapes/paper illustrations
- Recommended resource: undraw.co or freepik.com

Login Page:
- Left side could have subtle background pattern
- Paper texture or abstract shapes
- Keep it subtle (not distracting)

Chat Page:
- Clean white background (already good)
- Optional: Subtle pattern in sidebar background

**Recommended Sources**:
- Unsplash: https://unsplash.com/ (free, high quality)
- Freepik: https://freepik.com/ (free tier available)
- Undraw: https://undraw.co/ (free illustrations)
- Pexels: https://pexels.com/ (free images)

#### 4. **OAuth Provider Icons**

- Google OAuth button: 24x24px (official)
- GitHub OAuth button: 24x24px (official)
- Download from official brand guidelines:
  - Google: developers.google.com
  - GitHub: github.com/logos

#### 5. **Avatars**

User Avatar:
- Circular 40x40px for navbar
- Generate using service like:
  - Gravatar (uses email)
  - DiceBear: https://www.dicebear.com/
  - Letters avatar (initials in colored circle)

**Recommendation**: Use initials avatar (simplest, no additional assets)

---

## Part 6: Component Library Architecture

### Reusable Components to Create

```
/Components
├── /Common
│   ├── Button.jsx (Primary, Secondary, Tertiary variants)
│   ├── Input.jsx (Text, Password, Email with validation)
│   ├── Select.jsx (Dropdown)
│   ├── Modal.jsx (Dialog/Popup)
│   ├── Tabs.jsx (Tab switching)
│   ├── Badge.jsx (Pills/Tags)
│   ├── Toast.jsx (Notifications)
│   ├── Spinner.jsx (Loading state)
│   └── Card.jsx (Reusable card container)
│
├── /Layout
│   ├── Navbar.jsx
│   ├── Sidebar.jsx (Papers list)
│   ├── MainContainer.jsx
│   └── Footer.jsx (optional)
│
├── /Chat
│   ├── ChatMessage.jsx (User/Bot message)
│   ├── MessageList.jsx (Thread of messages)
│   ├── ChatInput.jsx (Input area with send)
│   ├── SourceCitation.jsx (Source display)
│   └── ProviderBadge.jsx
│
├── /Paper
│   ├── PaperCard.jsx
│   ├── PaperUpload.jsx
│   ├── PaperMetadata.jsx
│   └── PaperList.jsx
│
├── /Auth
│   ├── LoginForm.jsx
│   ├── SignUpForm.jsx
│   └── OAuth.jsx
│
└── /Styles
    ├── colors.css
    ├── typography.css
    ├── spacing.css
    ├── animations.css
    └── variables.css
```

---

## Part 7: Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [x] Landing page (already done)
- [x] Login page structure (partially done)
- [ ] Refine login page design
- [ ] Create color/typography system (CSS variables)
- [ ] Build common button & input components

### Phase 2: Chat Interface (Weeks 2-3)
- [ ] Refine top navbar
- [ ] Enhance papers sidebar styling
- [ ] Improve message display styling
- [ ] Add loading states & animations
- [ ] Responsive design for tablet/mobile

### Phase 3: Polish (Week 4)
- [ ] Add icons (use Font Awesome or Heroicons)
- [ ] Micro-interactions & animations
- [ ] Dark mode toggle (optional)
- [ ] Performance optimization
- [ ] Accessibility audit

### Phase 4: Testing & Launch (Week 5)
- [ ] Cross-browser testing
- [ ] Mobile device testing
- [ ] Lighthouse audit
- [ ] User feedback & iterations

---

## Part 8: Specific Recommendations for Your Project

### DO:
1. ✅ **Keep the hero section** - Great for marketing
2. ✅ **Use split-layout for login** - Professional, modern, user-friendly
3. ✅ **Add icons to paper sidebar** - Visual indicators help UX
4. ✅ **Implement loading states** - Users need feedback
5. ✅ **Make it responsive** - Test on mobile

### DON'T:
1. ❌ Don't add too many images (slows load)
2. ❌ Don't use more than 2-3 accent colors (confusing)
3. ❌ Don't make login complicated (keep it simple)
4. ❌ Don't forget dark mode accessibility (test contrast)
5. ❌ Don't ignore mobile users (majority may use mobile)

### Quick Assets Checklist

**Free Assets You Can Get Today**:
- [ ] Icons (from Heroicons or Font Awesome)
- [ ] User avatars (DiceBear API, no download needed)
- [ ] Background pattern (undraw.co)
- [ ] OAuth logos (official sources)

**Optional Assets** (Nice to have):
- [ ] Custom branding/logo design ($100-500)
- [ ] Subtle background illustrations ($50-200)
- [ ] Professional photography (if needed for marketing)

---

## Part 9: Design System Tokens (CSS Variables)

```css
/* Colors */
--color-primary: #667eea;
--color-primary-dark: #764ba2;
--color-success: #27ae60;
--color-error: #e74c3c;
--color-warning: #f39c12;
--color-text-dark: #2d2d2d;
--color-text-light: #999999;
--color-bg-light: #f8f8f8;
--color-border: #e0e0e0;

/* Typography */
--font-primary: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
--font-code: 'Monaco', 'Courier New', monospace;
--font-size-body: 14px;
--font-size-heading: 24px;
--font-weight-regular: 400;
--font-weight-bold: 600;

/* Spacing */
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;

/* Shadows */
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.1);
--shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);

/* Borders */
--border-radius-sm: 4px;
--border-radius-md: 8px;
--border-radius-lg: 12px;
--border-radius-full: 9999px;

/* Transitions */
--transition-fast: 0.2s ease-in-out;
--transition-normal: 0.3s ease-in-out;
```

---

## Part 10: Summary & Next Steps

### Your Current State ✅
- Hero landing page: Done
- Basic login page: Done
- Chat interface: Functional but needs styling

### Immediate Next Steps (Priority Order):
1. **Create CSS Variables file** (colors, spacing, typography)
2. **Download icons** (Heroicons set recommended)
3. **Refine login page** (split layout, better styling)
4. **Enhance chat UI** (better message styling, badges, citations)
5. **Add responsive design** (test on mobile, tablet)
6. **Implement micro-interactions** (smooth transitions, hover effects)

### Files to Create/Modify:
```
FrontEnd/src/
├── styles/
│   ├── variables.css       (NEW - Design tokens)
│   ├── colors.css          (NEW)
│   ├── typography.css      (NEW)
│   └── animations.css      (NEW)
│
├── pages/
│   ├── LoginPage.jsx       (REFINE)
│   └── LoginPage.css       (REFINE)
│
├── Components/
│   ├── Main/Main.jsx       (REFINE)
│   ├── Main/Main.css       (ENHANCE)
│   ├── Sidebar/Sidebar.jsx (ENHANCE)
│   └── Navbar/Navbar.jsx   (NEW - Add top navbar)
│
└── Components/Common/
    ├── Button.jsx          (NEW)
    ├── Input.jsx           (NEW)
    ├── Card.jsx            (NEW)
    └── Badge.jsx           (NEW)
```

---

## Conclusion

This plan provides a complete blueprint for transforming PaperLens into a polished, professional application. The design philosophy balances aesthetics with functionality, prioritizing user experience for researchers and academics.

The split-screen login, two-column chat layout, and comprehensive component system will create a cohesive, modern application that stands out in the research tool space.

**Estimated time to implement**: 2-3 weeks of consistent development.
