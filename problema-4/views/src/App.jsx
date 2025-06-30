import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from "react-router-dom";
import HomePage from "./pages/home-page";
import GroqChat from "./pages/groq-chat";
import LoginPage from "./pages/login-page";
import ProjectWizard from "./pages/project-wizard";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to= "/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/create-project" element={<ProjectWizard />} />
        <Route path="/groq-chat" element={<GroqChat />} />
      </Routes>
    </Router>
  )
}

export default App
