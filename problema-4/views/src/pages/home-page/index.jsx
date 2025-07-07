import React from 'react';
import { useNavigate } from 'react-router-dom'; // Importe useNavigate
import './home-page.css';

const HomePage = () => {
  const navigate = useNavigate(); // Inicialize o hook de navegação

  const projetos = [
    { id: 1, nome: "App de Educação Financeira", status: "aguardando geração de histórias" },
    { id: 2, nome: "Plataforma de Mentoria", status: "histórias já geradas" }
  ];

  // Função para navegar para a página de criação de projeto
  const handleCreateNewProject = () => {
    navigate('/create-project'); // Navega para a rota do ProjectWizard
  };

  return (
    <div className="home-container">
        <h1 className="title">Projetos Pendentes</h1>

        <div className="project-list">
          {projetos.map((projeto) => (
            <div key={projeto.id} className="project-card">
              <div>
                <h3>{projeto.nome}</h3>
                <p>{projeto.status}</p>
              </div>
              <button className="btn-black">Continuar</button>
            </div>
          ))}
        </div>

        <button className="btn-blue" onClick={handleCreateNewProject}> {/* Chama a função de navegação */}
          Iniciar novo projeto
        </button>
    </div>
  );
};

export default HomePage;