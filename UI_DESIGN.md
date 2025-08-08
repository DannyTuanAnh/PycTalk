# PycTalk Modern Login UI - Visual Design

## UI Layout (400x500px)

```
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                              🌈 GRADIENT BACKGROUND                                             ║
║                            (Blue #667eea → Purple #764ba2)                                     ║
║                                                                                                 ║
║    ╔═════════════════════════════════════════════════════════════════════════════════════╗    ║
║    ║                        💎 GLASSMORPHISM CARD                                          ║    ║
║    ║                   (White 95% opacity + shadow)                                       ║    ║
║    ║                                                                                       ║    ║
║    ║                            🎯 PycTalk                                                 ║    ║
║    ║                      (32px, Bold, #2D3436)                                           ║    ║
║    ║                                                                                       ║    ║
║    ║                  Đăng nhập vào tài khoản của bạn                                     ║    ║
║    ║                     (14px, #636E72)                                                  ║    ║
║    ║                                                                                       ║    ║
║    ║    Tên đăng nhập                                                                     ║    ║
║    ║    ┌─────────────────────────────────────────────────────────────────────────┐     ║    ║
║    ║    │  Nhập tên đăng nhập...                          │     ║    ║
║    ║    │  (Border: #E0E0E0 → #6C5CE7 on focus)                                   │     ║    ║
║    ║    └─────────────────────────────────────────────────────────────────────────┘     ║    ║
║    ║                                                                                       ║    ║
║    ║    Mật khẩu                                                                          ║    ║
║    ║    ┌─────────────────────────────────────────────────────────────────────────┐     ║    ║
║    ║    │  ●●●●●●●●●●●                                                             │     ║    ║
║    ║    │  (Hidden password input)                                                │     ║    ║
║    ║    └─────────────────────────────────────────────────────────────────────────┘     ║    ║
║    ║                                                                                       ║    ║
║    ║    ☐ Ghi nhớ đăng nhập                                                              ║    ║
║    ║    (Custom checkbox with checkmark SVG)                                             ║    ║
║    ║                                                                                       ║    ║
║    ║    ┌─────────────────────────────────────────────────────────────────────────┐     ║    ║
║    ║    │                      🚀 Đăng Nhập                                       │     ║    ║
║    ║    │         (Gradient: #6C5CE7 → #A29BFE, hover effect)                    │     ║    ║
║    ║    └─────────────────────────────────────────────────────────────────────────┘     ║    ║
║    ║                                                                                       ║    ║
║    ║                              Quên mật khẩu?                                          ║    ║
║    ║                          (Link color: #6C5CE7)                                      ║    ║
║    ║                                                                                       ║    ║
║    ║              Chưa có tài khoản?    Đăng ký ngay                                     ║    ║
║    ║                                   (Bold link)                                       ║    ║
║    ╚═════════════════════════════════════════════════════════════════════════════════════╝    ║
║                                                                                                 ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
```

## Color Palette

### Primary Gradient
- **Start**: #667eea (Light Blue)
- **End**: #764ba2 (Purple)

### UI Elements
- **Card Background**: rgba(255, 255, 255, 0.95)
- **Primary Text**: #2D3436 (Dark Gray)
- **Secondary Text**: #636E72 (Medium Gray)
- **Accent Color**: #6C5CE7 (Purple)
- **Input Border**: #E0E0E0 → #6C5CE7 (focus)
- **Button Gradient**: #6C5CE7 → #A29BFE

## Interactive States

### Input Fields
- **Default**: Light gray border (#E0E0E0)
- **Hover**: Medium gray border (#A8A8A8)
- **Focus**: Purple border (#6C5CE7) with glow effect
- **Active**: White background, dark text

### Login Button
- **Default**: Purple gradient with rounded corners
- **Hover**: Darker purple gradient
- **Pressed**: Even darker gradient
- **Loading**: "Đang đăng nhập..." text

### Checkbox
- **Unchecked**: White with gray border
- **Checked**: Purple background with white checkmark SVG

## Typography
- **Title**: 32px, Bold, Dark gray
- **Subtitle**: 14px, Regular, Medium gray
- **Labels**: 13px, Semi-bold, Dark gray
- **Inputs**: 14px, Regular, Dark gray
- **Button**: 16px, Bold, White
- **Links**: 13px, Regular/Bold, Purple

## Animations & Effects
- **Card**: Drop shadow with 20px blur, 5px offset
- **Inputs**: Smooth border color transitions
- **Button**: Hover and press state transitions
- **Links**: Underline on hover

## Responsive Design
- **Fixed Size**: 400x500px (optimal for login)
- **Centered**: Auto-centered on screen
- **Scalable**: All elements use relative sizing
- **Accessible**: High contrast ratios and clear focus states

This modern design follows current UI/UX trends with glassmorphism, gradients, and smooth animations while maintaining professional appearance and usability.