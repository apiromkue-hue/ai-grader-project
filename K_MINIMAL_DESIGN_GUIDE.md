# K-Minimal Design System Implementation
## Corporate Identity: Pastel Pink Theme

### 📋 Overview
The AI Project Grader system has been updated with the **K-Minimal design system** featuring a sophisticated **pastel pink color palette** and **Prompt font** for a modern, elegant user interface.

---

## 🎨 Color Palette

### K-Minimal Primary Colors
| Color Name | Hex Code | RGB | Usage |
|----------|----------|-----|-------|
| **Primary Pink** | `#E8B4D4` | rgb(232, 180, 212) | Main buttons, gradients, accents |
| **Secondary Pink** | `#D4A5C8` | rgb(212, 165, 200) | Headers, titles, hover states |
| **Light Pink** | `#F0D9E8` | rgb(240, 217, 232) | Backgrounds, light accents |
| **Accent Pink** | `#B8879F` | rgb(184, 135, 159) | Dark headers, secondary text |

### Neutral Colors
| Color Name | Hex Code | RGB | Usage |
|----------|----------|-----|-------|
| **Off-White** | `#F5F5F5` | rgb(245, 245, 245) | Subtle backgrounds |
| **White** | `#FFFFFF` | rgb(255, 255, 255) | Primary background |
| **Dark Gray** | `#333333` | rgb(51, 51, 51) | Primary text |

---

## 🔤 Typography

### Font Family: Prompt
- **Font**: [Prompt](https://fonts.google.com/specimen/Prompt) from Google Fonts
- **Import**: `<link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">`
- **Weight Variants Used**:
  - 300 (Light) - Subtle text
  - 400 (Regular) - Body text
  - 500 (Medium) - Emphasis
  - 600 (SemiBold) - Headers, buttons
  - 700 (Bold) - Main titles

### Typography Hierarchy
- **H1 (Main Title)**: Color: `#B8879F`, Weight: 600, Font-family: Prompt
- **H2/H3 (Section Headers)**: Color: `#D4A5C8`, Weight: 600, Font-family: Prompt
- **Body Text**: Color: `#333333`, Weight: 400, Font-family: Prompt

---

## 🖼️ UI Components Styling

### Buttons
```css
Background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%)
Color: white
Border-radius: 12px
Padding: 12px 24px
Box-shadow: 0 4px 15px rgba(232, 180, 212, 0.3)
Hover: transform: translateY(-3px)
```

### Cards & Containers
```css
Background: white or #F5E8F0
Border: 2px solid #F0D9E8
Border-radius: 12px
Box-shadow: 0 2px 8px rgba(232, 180, 212, 0.1)
Hover: transform: translateY(-5px), stronger shadow
```

### Tabs
```css
Inactive: Color: #B8879F
Active: Background gradient (#E8B4D4 → #D4A5C8), Color: white
Border-bottom: 3px solid #D4A5C8
```

### Input Fields
```css
Border: 2px solid #F0D9E8
Border-radius: 10px
Padding: 10px 15px
Focus: Border-color: #E8B4D4, Shadow: 0 0 10px rgba(232, 180, 212, 0.4)
```

### Alerts & Messages
```css
Success: Background: #E6F9E6, Border: #B3E6B3
Info: Background: #E8F4F8, Border: #B3D9E6
Warning: Background: #FFF8E6, Border: #FFE699
Error: Background: #FFE8E8, Border: #FF9999
Border-radius: 12px
```

---

## 🎨 Background Gradients

### Main Background
```css
background: linear-gradient(135deg, #F0D9E8 0%, #E8B4D4 100%)
```

### Sidebar Background
```css
background: linear-gradient(180deg, #FFFFFF 0%, #F5E8F0 100%)
border-right: 2px solid #E8B4D4
```

### Button Gradients
```css
Primary: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%)
Secondary: linear-gradient(90deg, #E8B4D4 0%, #F0D9E8 100%)
Divider: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%)
```

---

## 📱 PWA Theme Colors

### manifest.json
```json
{
  "theme_color": "#E8B4D4",
  "background_color": "#FFFFFF"
}
```

### Icons
- **Primary Icon Background**: `#E8B4D4`
- **Secondary Icon Background**: `#D4A5C8`
- **Tertiary Icon Background**: `#F0D9E8`

---

## 🔄 Transitions & Animations

### Button Interactions
```css
transition: all 0.3s ease
hover: transform: translateY(-3px)
active: transform: translateY(-1px)
```

### Card Hover Effects
```css
transition: all 0.3s ease
hover: transform: translateY(-5px)
    box-shadow: 0 8px 25px rgba(212, 165, 200, 0.3)
```

### Tab Transitions
```css
transition: all 0.3s ease
hover: background-color: rgba(232, 180, 212, 0.15)
    color: #D4A5C8
```

---

## 📊 Design Specifications Summary

| Element | Primary Color | Secondary Color | Accent Color |
|---------|---------------|-----------------|--------------|
| Main Buttons | #E8B4D4 | #D4A5C8 | - |
| Headers/Titles | #D4A5C8 | #B8879F | - |
| Backgrounds | #F0D9E8 | #FFFFFF | #F5E8F0 |
| Borders | #F0D9E8 | #E8B4D4 | - |
| Hover Effects | #E8B4D4 | #D4A5C8 | rgba shades |

---

## 🌍 Implementation Files Updated

1. **student_view.py**
   - Integrated Google Fonts (Prompt)
   - Updated all CSS styling with K-Minimal colors
   - Updated login page theme
   - Applied theme to all UI components

2. **manifest.json**
   - Updated theme_color to `#E8B4D4`
   - Updated icon backgrounds with K-Minimal palette
   - Updated screenshot backgrounds

---

## ✨ Visual Features

- **Gradient Backgrounds**: Smooth 135° diagonal gradients
- **Rounded Corners**: 10-15px border radius for modern look
- **Soft Shadows**: Subtle shadows with pink-tinted rgba colors
- **Smooth Transitions**: 0.3s ease for all interactive elements
- **Hover Effects**: Upward translate (3px) on hover
- **Focus States**: Visible focus with shadow and border color change

---

## 🎯 Design Goals Achieved

✅ **Cohesive Branding**: Unified K-Minimal pastel pink aesthetic
✅ **Professional Appearance**: Elegant, modern design system
✅ **Accessibility**: Good contrast ratios maintained
✅ **Responsive Design**: Works across all device sizes
✅ **User Experience**: Smooth animations and clear interactions
✅ **Font Integration**: Prompt font for Thai language support

---

## 📝 Notes

- All colors have been carefully chosen to work together harmoniously
- The pastel pink palette is calming and professional
- Prompt font supports Thai language beautifully
- The design system is consistent across desktop and mobile views
- PWA manifest includes K-Minimal colors for app installation

---

**Last Updated**: December 14, 2025
**Design System**: K-Minimal with Pastel Pink Palette
**Typography**: Prompt Font (Google Fonts)
