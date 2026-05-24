# OctoFit Tracker — Frontend Requirements

## Project Context

OctoFit Tracker is a fitness tracking web application built for Mergington High School. The frontend is a single-page application (SPA) that communicates with the backend REST API to display users, teams, activities, workouts, and a leaderboard.

---

## Architecture Overview

- **Pattern:** Single-page application (SPA), decoupled from the backend.
- **Frontend server port:** `3000`
- **Backend API port:** `8000`
- **API communication:** HTTP `fetch()` calls from each component to backend REST endpoints.
- **Routing:** Client-side routing (no page reloads between views).
- **Styling:** Bootstrap 5 utility classes combined with custom CSS in `App.css`.

---

## Technology Stack (as implemented)

| Component          | Technology                    |
|--------------------|-------------------------------|
| Language           | JavaScript (JSX)              |
| UI framework       | React 19.2.6                  |
| Routing            | react-router-dom 7.15.1       |
| CSS framework      | Bootstrap 5.3.8               |
| Build tooling      | react-scripts 5.0.1 (Create React App) |
| Testing library    | @testing-library/react 16.3.2, @testing-library/jest-dom 6.9.1, @testing-library/user-event 13.5.0, @testing-library/dom 10.4.1 |
| Performance        | web-vitals 2.1.4              |

---

## Directory Structure

```
octofit-tracker/
└── frontend/
    ├── package.json
    ├── public/
    │   ├── index.html
    │   ├── favicon.ico
    │   ├── logo192.png
    │   ├── logo512.png
    │   ├── manifest.json
    │   └── robots.txt
    └── src/
        ├── index.js
        ├── index.css
        ├── App.js
        ├── App.css
        ├── App.test.js
        ├── logo.svg
        ├── reportWebVitals.js
        ├── setupTests.js
        └── components/
            ├── Activities.js
            ├── Leaderboard.js
            ├── Teams.js
            ├── Users.js
            └── Workouts.js
```

---

## npm Dependencies (package.json)

```json
{
  "bootstrap": "^5.3.8",
  "react": "^19.2.6",
  "react-dom": "^19.2.6",
  "react-router-dom": "^7.15.1",
  "react-scripts": "5.0.1",
  "web-vitals": "^2.1.4",
  "@testing-library/dom": "^10.4.1",
  "@testing-library/jest-dom": "^6.9.1",
  "@testing-library/react": "^16.3.2",
  "@testing-library/user-event": "^13.5.0"
}
```

### npm Scripts

| Script          | Command                   |
|-----------------|---------------------------|
| `npm start`     | `react-scripts start`     |
| `npm run build` | `react-scripts build`     |
| `npm test`      | `react-scripts test`      |
| `npm run eject` | `react-scripts eject`     |

---

## Entry Point

**`src/index.js`**

- Imports Bootstrap CSS globally: `import 'bootstrap/dist/css/bootstrap.min.css'`
- Imports custom CSS: `import './index.css'`
- Renders `<App />` inside `React.StrictMode` into the DOM element with id `root`.
- Calls `reportWebVitals()` for performance measurement.

---

## App Component (`src/App.js`)

### Responsibilities

- Wraps the entire application in a `<Router>` (react-router-dom).
- Renders the top navigation bar.
- Defines all client-side routes.
- Renders a landing/home page at `/`.

### Navigation Bar

- Full-width Bootstrap navbar (`navbar-expand-lg`, `navbar-dark`, `bg-dark`).
- Brand logo: `logo192.png` from `public/`, displayed with class `App-logo` (spinning animation).
- Brand text: `OctoFit Tracker`
- Collapsible hamburger menu for smaller screens.
- Navigation links:

| Label       | Route          |
|-------------|----------------|
| Activities  | `/activities`  |
| Leaderboard | `/leaderboard` |
| Teams       | `/teams`       |
| Users       | `/users`       |
| Workouts    | `/workouts`    |

### Routes

| Path           | Component Rendered                                    |
|----------------|-------------------------------------------------------|
| `/activities`  | `<Activities />`                                      |
| `/leaderboard` | `<Leaderboard />`                                     |
| `/teams`       | `<Teams />`                                           |
| `/users`       | `<Users />`                                           |
| `/workouts`    | `<Workouts />`                                        |
| `/`            | Welcome message, tagline, and "Get Started" button linking to `/activities` |

### Home Page Content (at `/`)

- Heading: `Welcome to OctoFit Tracker!`
- Paragraph: `Track your fitness, join teams, and compete on the leaderboard!`
- Button: `Get Started` — links to `/activities`

---

## API URL Resolution (all components)

Each component reads the `REACT_APP_CODESPACE_NAME` environment variable to determine the correct backend API base URL:

```js
const codespace = process.env.REACT_APP_CODESPACE_NAME;
const endpoint = codespace
  ? `https://${codespace}-8000.app.github.dev/api/<resource>/`
  : 'http://localhost:8000/api/<resource>/';
```

If `REACT_APP_CODESPACE_NAME` is set (GitHub Codespaces), the public Codespace URL is used. Otherwise, `localhost:8000` is used.

---

## Components

All components follow the same data-fetching pattern:

1. Declare state with `useState([])`.
2. Use `useEffect` to `fetch()` from the backend endpoint on mount.
3. Accept either `data.results` or `data` as the array (handles both paginated and non-paginated responses).
4. Log fetched data and endpoint to the console.
5. Render a Bootstrap card with a card header (title + action button) and a card body containing a Bootstrap table.

---

### Activities (`src/components/Activities.js`)

- **Endpoint:** `/api/activities/`
- **State:** `activities` (array)
- **Card Header:** Title `Activities`, Button `Add Activity` (`.btn-success`)
- **Table Columns:** `Name`, `Description`
- **Rendered fields per row:** `activity.name`, `activity.description`

---

### Leaderboard (`src/components/Leaderboard.js`)

- **Endpoint:** `/api/leaderboard/`
- **State:** `leaderboard` (array)
- **Card Header:** Title `Leaderboard`, Button `Refresh` (`.btn-info`)
- **Table Columns:** `User`, `Score`
- **Rendered fields per row:** `entry.user`, `entry.score`

---

### Teams (`src/components/Teams.js`)

- **Endpoint:** `/api/teams/`
- **State:** `teams` (array)
- **Card Header:** Title `Teams`, Button `Create Team` (`.btn-primary`)
- **Table Columns:** `Name`, `Members`
- **Rendered fields per row:** `team.name`, `team.members.join(', ')` (if `members` exists)

---

### Users (`src/components/Users.js`)

- **Endpoint:** `/api/users/`
- **State:** `users` (array)
- **Card Header:** Title `Users`, Button `Invite User` (`.btn-secondary`)
- **Table Columns:** `Username`, `Email`
- **Rendered fields per row:** `user.username`, `user.email`

---

### Workouts (`src/components/Workouts.js`)

- **Endpoint:** `/api/workouts/`
- **State:** `workouts` (array)
- **Card Header:** Title `Workouts`, Button `Add Workout` (`.btn-warning`)
- **Table Columns:** `Name`, `Duration`
- **Rendered fields per row:** `workout.name`, `workout.duration`

---

## Styling (`src/App.css`)

All custom styles are in `src/App.css`, applied globally alongside Bootstrap.

### Body

- Background: `linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%)`
- Minimum height: `100vh`
- Text color: `#22223b`

### Navbar

- Background: `linear-gradient(90deg, #3a86ff 0%, #8338ec 100%)` (overrides Bootstrap)
- Box shadow: `0 2px 8px rgba(51, 51, 153, 0.08)`
- Nav links and brand: color `#fff`, font-weight `600`, letter-spacing `1px`
- Active/focused nav link: color `#ffd60a`
- Brand logo height: `36px`, margin-right: `10px`

### Cards

- Border radius: `1rem`
- Box shadow: `0 4px 24px rgba(51, 51, 153, 0.08)`
- Background: `#fff`
- Card header: `linear-gradient(90deg, #f72585 0%, #7209b7 100%)`, text white, top corners rounded `1rem`
- Card title: color `#3a86ff`, font-weight `700`

### Headings (h1–h5)

- Color: `#3a86ff`
- Font-weight: `700`

### Buttons

All action buttons use rounded style (`border-radius: 2rem`), font-weight `600`, letter-spacing `1px`.

| Class          | Background Gradient                          | Text color  |
|----------------|----------------------------------------------|-------------|
| `.btn-primary` | `#3a86ff` → `#8338ec`                        | white       |
| `.btn-success` | `#06d6a0` → `#1b9aaa`                        | white       |
| `.btn-info`    | `#00b4d8` → `#48cae4`                        | white       |
| `.btn-warning` | `#ffd60a` → `#ff8800`                        | `#22223b`   |
| `.btn-secondary`| `#adb5bd` → `#495057`                       | white       |

### Links

- Default color: `#7209b7`, underlined, transition `0.2s`
- Hover color: `#f72585`

### Tables

- Background: `#f8fafc`
- Border radius: `0.5rem`
- Header (`th`): background `#3a86ff`, text white, font-weight `600`
- Odd rows (striped): background `#e0e7ff`
- Hover row: background `#ffd6e0`

### Logo Animation (`.App-logo`)

- Height: `40px`
- Margin-right: `10px`
- Spinning animation: `App-logo-spin`, infinite, `20s`, linear
- Keyframes: rotate from `0deg` to `360deg`

---

## Public Assets

| File             | Purpose                                                |
|------------------|--------------------------------------------------------|
| `favicon.ico`    | Browser tab icon                                       |
| `logo192.png`    | App logo (used in navbar, PWA metadata)               |
| `logo512.png`    | Large app logo (PWA metadata)                         |
| `index.html`     | HTML shell; mounts React at `<div id="root">`         |
| `manifest.json`  | PWA manifest: short name `React App`, name `Create React App Sample`, theme `#000000`, background `#ffffff` |
| `robots.txt`     | Allows all crawlers (`User-agent: *`, `Disallow:`)    |

---

## Functional Requirements

1. The frontend must render five distinct views: Activities, Leaderboard, Teams, Users, and Workouts.
2. Navigation between views must use client-side routing without full page reloads.
3. Each view must fetch its data from the corresponding backend REST API endpoint on mount.
4. The API endpoint URL must be dynamically resolved using the `REACT_APP_CODESPACE_NAME` environment variable.
5. Each view must display its data in a Bootstrap table with appropriate columns.
6. Each view must include a card header with the view title and a contextual action button.
7. The navbar must display the OctoFit Tracker logo (`logo192.png`) on the left, spinning.
8. The navbar must collapse into a hamburger menu on smaller screens.
9. The home page at `/` must display a welcome message and a "Get Started" button linking to `/activities`.
10. Bootstrap CSS must be imported globally and applied across all components.
11. Each component must log the fetched data and the endpoint URL to the browser console.
12. The app must handle both paginated (`data.results`) and non-paginated (`data`) API responses.

---

## Non-Functional Requirements

1. The frontend runs on port `3000`.
2. React StrictMode is enabled in development.
3. Custom styles in `App.css` override Bootstrap defaults for navbar, cards, buttons, tables, headings, and links.
4. The app logo has a continuous spinning animation (20s, linear, infinite).
5. The app uses a favicon (`favicon.ico`) for the browser tab.
6. A PWA manifest (`manifest.json`) is present with app name, icons, theme color, and background color.
7. The `REACT_APP_CODESPACE_NAME` environment variable controls the backend URL — no hardcoded production URL.
8. ESLint is configured with `react-app` and `react-app/jest` extends.
9. The browserslist targets: production (`>0.2%`, not dead, not op_mini all); development (last 1 chrome/firefox/safari version).
