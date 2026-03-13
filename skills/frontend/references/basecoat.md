# Basecoat UI Setup

Use this when you want shadcn-style components without depending on React.

## Install Package

```bash
npm install basecoat-css
```

## Import Basecoat in CSS

Add Basecoat after Tailwind in your main stylesheet:

```css
@import 'tailwindcss';
@import 'basecoat-css';
@import './theme.css';
```

The `theme.css` import is optional, but it matches the Basecoat recommendation
when you want a shadcn-compatible semantic theme file.

## `theme.css`

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 47.4% 11.2%;
  --card: 0 0% 100%;
  --card-foreground: 222.2 47.4% 11.2%;
  --popover: 0 0% 100%;
  --popover-foreground: 222.2 47.4% 11.2%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --accent: 199 89% 48%;
  --accent-foreground: 210 40% 98%;
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 221.2 83.2% 53.3%;
  --radius: 0.9rem;
}

.dark {
  --background: 222.2 47.4% 6%;
  --foreground: 210 40% 98%;
  --card: 222.2 47.4% 8%;
  --card-foreground: 210 40% 98%;
  --popover: 222.2 47.4% 8%;
  --popover-foreground: 210 40% 98%;
  --primary: 212.7 97% 62%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --secondary: 217.2 32.6% 17.5%;
  --secondary-foreground: 210 40% 98%;
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  --accent: 187 85% 53%;
  --accent-foreground: 222.2 47.4% 11.2%;
  --destructive: 0 72% 51%;
  --destructive-foreground: 210 40% 98%;
  --border: 217.2 32.6% 17.5%;
  --input: 217.2 32.6% 17.5%;
  --ring: 212.7 97% 62%;
}
```

## Optional JavaScript

If your project is ESM-aware, import all components:

```js
import 'basecoat-css/all'
```

Or import only the pieces you need:

```js
import 'basecoat-css/basecoat'
import 'basecoat-css/popover'
import 'basecoat-css/tabs'
```

Without a build tool, Basecoat also supports a static-file flow by copying JS
files from `node_modules/basecoat-css/dist/js`.

## Jinja or Nunjucks Macros

For more complex server-rendered components:

```bash
npx basecoat-cli add dialog
```

That fits Jinja or Nunjucks projects that want reusable component macros.
