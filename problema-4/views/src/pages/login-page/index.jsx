import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { api } from '../../utils/api';
import './login-page.css';

function formatApiError(error) {
  if (error && Array.isArray(error.detail)) {
    return error.detail.map(
      (e) => `${e.loc?.join('.') || ''}: ${e.msg}`
    ).join('\n');
  }
  if (typeof error === 'string') return error;
  if (error && typeof error.detail === 'string') return error.detail;
  return 'Erro desconhecido';
}

const LoginPage = () => {
    const navigate = useNavigate();
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleLogin = async (event) => {
        event.preventDefault();
        setError('');
        setLoading(true);
        
        const formData = new FormData(event.target);
        const email = formData.get("email");
        const password = formData.get("password");

        try {
            const data = await api.login(email, password);
            
            // Armazena o token no localStorage
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('user_email', email);
            navigate("/home");
        } catch (err) {
            setError(err);
            console.error('Erro no login:', err);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="login-card">
            <h2 className="login-title">Faça o Login</h2>

            {error && (
                <div className="error">
                    {formatApiError(error)}
                </div>
            )}

            <form className="login-form" onSubmit={handleLogin}>
                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <div className="input-wrapper">
                        <input
                            type="email"
                            id="email"
                            name="email"
                            placeholder="exemplo@dominio.com"
                            required
                            disabled={loading}
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
                            required
                            disabled={loading}
                        />
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading ? 'Entrando...' : 'Entrar'}
                </button>

                <div className="register-link">
                    Não tem uma conta? <button type="button" onClick={() => navigate('/register')}>Crie uma conta</button>
                </div>
            </form>
        </div>
    )
}

export default LoginPage