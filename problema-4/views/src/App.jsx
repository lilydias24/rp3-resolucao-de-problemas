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
<<<<<<< HEAD
import ProductCreation from "./pages/product-creation";
=======
import RegisterPage from "./pages/register-page";
import ProductCreation from "./pages/product-creation";
import ProtectedRoute from "./components/ProtectedRoute";
>>>>>>> eric-branch

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to= "/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/create-project" element={<ProductCreation />} />
        <Route path="/groq-chat" element={<GroqChat />} />
<<<<<<< HEAD
=======
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/home" element={
          <ProtectedRoute>
            <HomePage />
          </ProtectedRoute>
        } />
        <Route path="/create-project" element={
          <ProtectedRoute>
            <ProductCreation />
          </ProtectedRoute>
        } />
        <Route path="/groq-chat" element={
          <ProtectedRoute>
            <GroqChat />
          </ProtectedRoute>
        } />
>>>>>>> eric-branch
      </Routes>
    </Router>
  )
}

export default App
