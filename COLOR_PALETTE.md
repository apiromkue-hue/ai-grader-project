# K-Minimal Color Palette Quick Reference

## Hex Color Codes

### Primary Colors (Pastel Pink Tones)
- **#E8B4D4** - Primary Pink (Main buttons, gradients)
- **#D4A5C8** - Secondary Pink (Headers, hover states)
- **#F0D9E8** - Light Pink (Backgrounds, light accents)
- **#B8879F** - Accent Dark Pink (Dark headers, secondary text)

### Neutral Colors
- **#FFFFFF** - White (Primary background)
- **#F5F5F5** - Off-white (Subtle backgrounds)
- **#F5E8F0** - Very Light Pink (Sidebar background)
- **#333333** - Dark Gray (Primary text)

## CSS Usage Examples

### Button (Primary)
```css
background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
color: white;
border-radius: 12px;
box-shadow: 0 4px 15px rgba(232, 180, 212, 0.3);
```

### Button (Secondary)
```css
background: linear-gradient(90deg, #E8B4D4 0%, #F0D9E8 100%);
color: #B8879F;
border: 2px solid #D4A5C8;
border-radius: 12px;
```

### Card/Container
```css
background: white;
border: 2px solid #F0D9E8;
border-radius: 12px;
box-shadow: 0 2px 8px rgba(232, 180, 212, 0.1);
```

### Header Text
```css
color: #D4A5C8;
font-family: 'Prompt', sans-serif;
font-weight: 600;
```

### Main Title
```css
color: #B8879F;
font-family: 'Prompt', sans-serif;
font-weight: 600;
```

### Input Field (Focus)
```css
border-color: #E8B4D4;
box-shadow: 0 0 10px rgba(232, 180, 212, 0.4);
```

### Tab (Active)
```css
background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
color: white;
border-bottom: 3px solid #D4A5C8;
```

### Divider/Border
```css
background: linear-gradient(90deg, #E8B4D4 0%, #D4A5C8 100%);
height: 2px;
```

### Background Gradient
```css
background: linear-gradient(135deg, #F0D9E8 0%, #E8B4D4 100%);
```

### Alert (Info)
```css
background-color: #E8F4F8;
color: #1A4D5C;
border-color: #B3D9E6;
border-radius: 12px;
```

## Color Harmony Notes

- **Pastel Pink** is the dominant color family
- All colors maintain good contrast for accessibility
- The gradient from light (#F0D9E8) to dark (#B8879F) provides visual hierarchy
- Neutral white (#FFFFFF) ensures text readability
- Shadows use pink-tinted rgba for cohesion

## Typography

- **Font**: Prompt (Google Fonts)
- **Import**: `https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap`

## Gradient Directions

- **Buttons**: 90° (left to right)
- **Main Background**: 135° (diagonal)
- **Sidebar**: 180° (top to bottom)

---

Generated: December 14, 2025
Design System: K-Minimal
