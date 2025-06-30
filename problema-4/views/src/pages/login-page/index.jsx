import React from 'react'
import { useNavigate } from 'react-router-dom';
import './login-page.css';

const LoginPage = () => {
    const navigate = useNavigate();

    const handleLogin = (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const email = formData.get("email");
        const password = formData.get("password");
        console.log("Email:", email);
        console.log("Senha:", password);

        navigate("/home");
    }

    return (
        <div className="login-card">
            <h2 className="login-title">Faça o Login</h2>

            <form className="login-form" onSubmit={handleLogin}>
                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <div className="input-wrapper">
                        <input
                            type="email"
                            id="email"
                            name="email"
                            placeholder="exemplo@dominio.com"
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label htmlFor="password">Senha</label>
                    <div className="input-wrapper">
                        <input
                            type="password"
                            id="password"
                            name="password"
                            placeholder="••••••••"
                        />
                    </div>
                </div>

                <button
                    type="submit"
                >
                    Entrar
                </button>
            </form>
        </div>
    )
}

export default LoginPage