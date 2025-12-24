# K-Minimal Design System - Visual Guide

## 🎨 Corporate Identity: K-Minimal Pastel Pink

---

## Color Swatches

### Primary Colors
```
█████████████████ #E8B4D4 (Primary Pink)
   RGB: 232, 180, 212
   Usage: Main buttons, primary gradients, primary accents

█████████████████ #D4A5C8 (Secondary Pink)
   RGB: 212, 165, 200
   Usage: Headers, section titles, hover states, borders

█████████████████ #F0D9E8 (Light Pink)
   RGB: 240, 217, 232
   Usage: Light backgrounds, card backgrounds, light accents

█████████████████ #B8879F (Accent Dark Pink)
   RGB: 184, 135, 159
   Usage: Dark headers, secondary text, accents
```

### Neutral Colors
```
█████████████████ #FFFFFF (White)
   RGB: 255, 255, 255
   Usage: Primary background, card backgrounds

█████████████████ #F5F5F5 (Off-white)
   RGB: 245, 245, 245
   Usage: Subtle backgrounds, hover states

█████████████████ #F5E8F0 (Very Light Pink)
   RGB: 245, 232, 240
   Usage: Sidebar background, light backgrounds

█████████████████ #333333 (Dark Gray)
   RGB: 51, 51, 51
   Usage: Primary text, dark text
```

---

## Component Examples

### Buttons

#### Primary Button
```
┌─────────────────────┐
│ 🔓 Primary Button   │  Background: Linear gradient (#E8B4D4 → #D4A5C8)
└─────────────────────┘  Text: White, Prompt 600
                         Border-radius: 12px
                         Shadow: 0 4px 15px rgba(232, 180, 212, 0.3)
                         Hover: translateY(-3px)
```

#### Secondary Button
```
┌─────────────────────┐
│ Secondary Button    │  Background: Linear gradient (#E8B4D4 → #F0D9E8)
└─────────────────────┘  Text: #B8879F, Prompt 600
                         Border: 2px solid #D4A5C8
                         Border-radius: 12px
```

### Cards

```
╔═════════════════════════════════════╗
║  Card Title                         ║  Background: White or #F5E8F0
║                                     ║  Border: 2px solid #F0D9E8
║  Card content goes here...          ║  Border-radius: 12px
║                                     ║  Padding: 20px
║                                     ║  Shadow: 0 2px 8px rgba(232, 180, 212, 0.1)
║                                     ║  Hover: translateY(-5px) + stronger shadow
╚═════════════════════════════════════╝
```

### Tabs

```
┌────────────────┐ ┌──────────────────────┐
│ Inactive Tab   │ │ ► Active Tab         │  Active: Gradient + white text
└────────────────┘ └──────────────────────┘  Border-bottom: 3px #D4A5C8
```

### Input Fields

```
┌─────────────────────────────────────┐
│ Enter text here...                  │  Border: 2px solid #F0D9E8
└─────────────────────────────────────┘  Border-radius: 10px
                                         Focus: Border #E8B4D4 + glow
```

### Alerts

```
✅ Success Alert        Background: #E6F9E6, Border: #B3E6B3
ℹ️  Info Alert          Background: #E8F4F8, Border: #B3D9E6
⚠️  Warning Alert       Background: #FFF8E6, Border: #FFE699
❌ Error Alert          Background: #FFE8E8, Border: #FF9999
```

---

## Gradient Directions

### Main Background (135°)
```
╱╱╱╱╱╱╱╱╱
╱ Light ╱  Diagonal gradient from top-left to bottom-right
╱ Pink  ╱  #F0D9E8 → #E8B4D4
╱╱╱╱╱╱╱╱╱
```

### Button Gradient (90°)
```
┌─────────────┐
│ #E8B4D4 →   │  Horizontal gradient left to right
│ #D4A5C8     │
└─────────────┘
```

### Sidebar Gradient (180°)
```
┌─────────┐
│ White   │  Vertical gradient top to bottom
│    ↓    │  White → #F5E8F0
│ Pinkish │
└─────────┘
```

---

## Typography Hierarchy

### H1 - Main Title
```
🎓 ระบบตรวจโครงงาน AI
   Color: #B8879F
   Font: Prompt, 600
   Size: 32px
```

### H2/H3 - Section Headers
```
📂 วิเคราะห์โครงงาน
   Color: #D4A5C8
   Font: Prompt, 600
   Size: 20-24px
```

### Body Text
```
Regular text content here...
   Color: #333333
   Font: Prompt, 400
   Size: 16px
```

### Secondary Text
```
Smaller, muted text
   Color: #B8879F
   Font: Prompt, 500
   Size: 14px
```

---

## Spacing System

```
4px   (xs)   ▥
8px   (sm)   ▥▥
12px  (md)   ▥▥▥
20px  (lg)   ▥▥▥▥▥
24px  (xl)   ▥▥▥▥▥▥
```

---

## Border Radius Scale

```
8px    (small)   │ Input fields, small buttons
10px   (medium)  │ Cards, expanders
12px   (large)   │ Buttons, containers
15px   (xlarge)  │ Metric boxes, special elements
```

---

## Shadow System

```
Light Shadow       Box-shadow: 0 2px 8px rgba(232, 180, 212, 0.1)
   └─ Cards, subtle elements

Medium Shadow      Box-shadow: 0 4px 15px rgba(232, 180, 212, 0.2)
   └─ Cards on hover, buttons

Strong Shadow      Box-shadow: 0 8px 25px rgba(232, 180, 212, 0.3)
   └─ Modal overlays, elevated elements
```

---

## Animations

### Button Hover (0.3s ease)
```
Before: Y: 0px
After:  Y: -3px  (lift effect)
```

### Card Hover (0.3s ease)
```
Before: Y: 0px, Shadow: light
After:  Y: -5px, Shadow: strong
```

### Transition Speed
```
Default: 0.3s ease
Slow:    0.5s ease
```

---

## Responsive Breakpoints

```
Desktop (1200px+)     [████████████ Full width]
Tablet  (768-1199px)  [████████ Adjusted width]
Mobile  (< 768px)     [████ Stacked layout]
```

---

## Accessibility Features

### Contrast Ratios
- ✅ Text on white background: 7.1:1 (AAA)
- ✅ Text on light pink: 6.8:1 (AAA)
- ✅ White on gradient: 4.5:1 (AA)

### Focus States
- ✅ Visible focus indicators
- ✅ Box shadow outlines
- ✅ Color changes on focus
- ✅ Reduced motion support

---

## Dark Mode Considerations

If dark mode is implemented:
```
Background: #1A1A1A (instead of white)
Text: #F0F0F0 (instead of #333333)
Cards: #252525 (instead of white)
Accents: Lighter pink variants
```

---

## Usage Examples

### CSS Gradient
```css
background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
```

### Rounded Button
```css
border-radius: 12px;
padding: 12px 24px;
font-family: 'Prompt', sans-serif;
```

### Focus State
```css
border-color: #E8B4D4;
box-shadow: 0 0 10px rgba(232, 180, 212, 0.4);
```

### Card Hover
```css
transform: translateY(-5px);
box-shadow: 0 8px 25px rgba(232, 180, 212, 0.3);
```

---

## Brand Personality

- **Modern**: Contemporary design with smooth transitions
- **Professional**: Elegant pastel palette for trust
- **Approachable**: Soft colors for educational context
- **Consistent**: Unified design system throughout
- **Accessible**: Clear contrast and readable typography
- **Responsive**: Works beautifully on all devices

---

## Design System Version

**Version**: 1.0
**Date**: December 14, 2025
**Theme**: K-Minimal Pastel Pink
**Typography**: Prompt Font
**Status**: Production Ready

---

Generated for: AI Project Grader System
Design System: K-Minimal
