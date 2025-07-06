import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../utils/api';
import './register-page.css';

const RegisterPage = () => {
    const navigate = useNavigate();
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleRegister = async (event) => {
        event.preventDefault();
        setError('');
        setLoading(true);
        
        const formData = new FormData(event.target);
        const email = formData.get("email");
        const name = formData.get("name");
        const password = formData.get("password");
        const confirmPassword = formData.get("confirmPassword");

        if (password !== confirmPassword) {
            setError('As senhas não coincidem');
            setLoading(false);
            return;
        }

        try {
            await api.register({
                email,
                name,
                password
            });
            
            // Redireciona para login após registro bem-sucedido
            navigate("/login");
        } catch (err) {
            setError(err.message || 'Erro no registro');
            console.error('Erro no registro:', err);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="register-card">
            <h2 className="register-title">Criar Conta</h2>

            {error && <div className="error-message">{error}</div>}

            <form className="register-form" onSubmit={handleRegister}>
                <div className="form-group">
                    <label htmlFor="name">Nome Completo</label>
                    <div className="input-wrapper">
                        <input
                            type="text"
                            id="name"
                            name="name"
                            placeholder="Seu nome completo"
                            required
                            disabled={loading}
                        />
                    </div>
                </div>

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
                            minLength={6}
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label htmlFor="confirmPassword">Confirmar Senha</label>
                    <div className="input-wrapper">
                        <input
                            type="password"
                            id="confirmPassword"
                            name="confirmPassword"
                            placeholder="••••••••"
                            required
                            disabled={loading}
                            minLength={6}
                        />
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading ? 'Criando conta...' : 'Criar Conta'}
                </button>

                <div className="login-link">
                    Já tem uma conta? <button type="button" onClick={() => navigate('/login')}>Faça login</button>
                </div>
            </form>
        </div>
    );
};

export default RegisterPage; 