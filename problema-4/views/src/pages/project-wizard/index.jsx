import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './project-wizard.css';

const ProjectWizard = () => {
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [useDefaultPrompt, setUseDefaultPrompt] = useState(true);
  const [customPrompt, setCustomPrompt] = useState('');
  const [form, setForm] = useState({
    nome: '',
    descricao: '',
    personas: '',
    proposta: '',
    canais: ''
  });
  const [epics, setEpics] = useState('');
  const [userStories, setUserStories] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE_URL = 'http://localhost:8000/llm-project'; // Ajuste conforme seu backend

  const nextStep = () => {
    setError(null);
    setStep((s) => s + 1);
  };
  const prevStep = () => {
    setError(null);
    setStep((s) => s - 1);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const defaultFormValues = {
    nome: 'Sistema de Geração de Produtos com IA',
    descricao: 'Uma plataforma inovadora para Product Owners gerenciarem o ciclo de vida do produto, desde a concepção até o backlog detalhado, utilizando inteligência artificial (LLMs) para automatizar a geração de épicos, histórias de usuário e requisitos funcionais.',
    personas: 'Product Owner, Scrum Master, Desenvolvedor, Stakeholder, QA Tester',
    proposta: 'Resolve a dor de cabeça inicial dos Product Owners ao acelerar a criação de documentação ágil (épicos, histórias, requisitos) através de IA, garantindo alinhamento e reduzindo o tempo de ramp-up do projeto. Ajuda a padronizar a qualidade das especificações do produto.',
    canais: 'Web Application (Desktop & Mobile Responsive), REST API'
  };

  const handlePromptOption = (isDefault) => {
    setUseDefaultPrompt(isDefault);
    if (isDefault) {
      setForm(defaultFormValues); // Preenche o formulário com os valores padrão
    } else {
      setForm({ nome: '', descricao: '', personas: '', proposta: '', canais: '' });
      setCustomPrompt(''); // Limpa também o campo de prompt personalizado
    }
    nextStep();
  };

  const handleGenerateEpics = () => {
    console.log("handleGenerateEpics: Botão clicado!");
    const productInfo = `Nome: ${form.nome}. Descrição: ${form.descricao}. Personas: ${form.personas}. Proposta de Valor: ${form.proposta}. Canais: ${form.canais}.`;
    console.log("handleGenerateEpics: Dados do produto formatados:", productInfo);
    generateContent('generate-epics', { productInfo }, setEpics);
    console.log("handleGenerateEpics: Chamada para generateContent feita.");
  };

  const generateContent = async (endpoint, payload, setStateCallback) => {
    console.log(`generateContent: Chamando endpoint ${endpoint} com payload:`, payload);
    setLoading(true);
    setError(null);
    try {
      console.log(`generateContent: Enviando requisição para ${API_BASE_URL}/${endpoint}`);
      const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      console.log("generateContent: Resposta do fetch recebida:", response);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: response.statusText }));
        console.error(`generateContent: Resposta de erro da API: Status ${response.status}`, errorData);
        throw new Error(`Erro ${response.status}: ${errorData.error || response.statusText}`);
      }

      const data = await response.json();
      console.log("generateContent: Dados da resposta JSON recebidos:", data);
      setStateCallback(data.content);
      console.log("generateContent: Estado atualizado e avançando passo.");
      nextStep();
    } catch (err) {
      console.error(`generateContent: Erro no bloco catch:`, err);
      setError(`Falha ao gerar conteúdo: ${err.message}. Verifique a console do navegador e o terminal do servidor.`);
    } finally {
      setLoading(false);
      console.log("generateContent: Carregamento finalizado.");
    }
  };

  const handleGenerateUserStories = () => {
    console.log("handleGenerateUserStories: Botão clicado!");
    const productInfo = `Nome: ${form.nome}. Descrição: ${form.descricao}. Personas: ${form.personas}. Proposta de Valor: ${form.proposta}. Canais: ${form.canais}.`;
    console.log("handleGenerateUserStories: Dados do produto formatados:", productInfo);
    const epicsSummary = epics; // Resumo dos épicos gerados
    console.log("handleGenerateUserStories: Resumo dos épicos:", epicsSummary);

    generateContent('generate-user-stories', { productInfo, epicsSummary, userPromptAdjustment: customPrompt }, setUserStories);
    console.log("handleGenerateUserStories: Chamada para generateContent feita.");
  };

  const handleGoBackToHome = () => {
    navigate('/home'); // Navega de volta para a rota da HomePage
  };

  return (
    <div className="wizard-container">
      {error && <div className="error-message">{error}</div>}
      {loading && (
        <div className="loading-overlay">
          <p>Carregando...</p>
        </div>
      )}

      {step === 1 && (
        <div className="wizard-step">
          <h2>Configurar Geração LLM</h2>
          <p>Deseja utilizar um prompt pré-definido para a LLM, ou prefere personalizá-lo?</p>
          <div className="button-group">
            <button onClick={handleGoBackToHome} disabled={loading} className="btn-secondary">
              Voltar para Home
            </button>
            <button onClick={() => handlePromptOption(true)} disabled={loading}>
              Sim, usar padrão
            </button>
            <button onClick={() => handlePromptOption(false)} disabled={loading}>
              Não, quero personalizar
            </button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="wizard-step">
          <h2>Informações do Produto</h2>
          <input
            name="nome"
            placeholder="Nome do produto (ex: Plataforma de Gestão de Projetos Ágeis)"
            value={form.nome}
            onChange={handleChange}
            disabled={loading}
          />
          <textarea
            name="descricao"
            placeholder="Descrição detalhada do produto (ex: Uma plataforma para Product Owners gerenciarem o ciclo de vida do produto do conceito ao backlog, utilizando IA para auxiliar na geração de épicos e histórias de usuário.)"
            value={form.descricao}
            onChange={handleChange}
            disabled={loading}
            rows="5"
          />
          <input
            name="personas"
            placeholder="Personas envolvidas (ex: Product Owner, Scrum Master, Desenvolvedor, Stakeholder)"
            value={form.personas}
            onChange={handleChange}
            disabled={loading}
          />
          <textarea
            name="proposta"
            placeholder="Proposta de valor (problema que o produto resolve: ex: A dificuldade de Product Owners em iniciar projetos, criar épicos e gerar histórias de usuário de forma eficiente e alinhada, resultando em retrabalho e atrasos.)"
            value={form.proposta}
            onChange={handleChange}
            disabled={loading}
            rows="3"
          />
          <input
            name="canais"
            placeholder="Canais/Plataformas (ex: Web, Mobile App)"
            value={form.canais}
            onChange={handleChange}
            disabled={loading}
          />
          <div className="button-group">
            <button onClick={prevStep} disabled={loading}>Voltar</button>
            <button onClick={nextStep} disabled={loading || !form.nome || !form.descricao}>Avançar</button>
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="wizard-step">
          <h2>Geração de Épicos</h2>
          {!useDefaultPrompt && (
            <div className="prompt-customization">
              <label htmlFor="customPrompt">Ajuste o prompt para a geração de épicos:</label>
              <textarea
                id="customPrompt"
                value={customPrompt}
                onChange={(e) => setCustomPrompt(e.target.value)}
                placeholder="Ex: Foque mais em funcionalidades de relatórios para o Product Owner."
                rows="3"
                disabled={loading}
              />
            </div>
          )}
          <p>{useDefaultPrompt ? 'Clique para gerar épicos com base nas informações do produto usando o modelo padrão.' : 'Com seu prompt personalizado, a LLM gerará os épicos para o produto.'}</p>
          <div className="button-group">
            <button onClick={prevStep} disabled={loading}>Voltar</button>
            <button onClick={handleGenerateEpics} disabled={loading}>
              {loading ? 'Gerando Épicos...' : 'Gerar Épicos com LLM'}
            </button>
          </div>
        </div>
      )}

      {step === 4 && (
        <div className="wizard-step">
          <h2>Revisar Épicos</h2>
          <p>Edite os épicos gerados abaixo se desejar fazer ajustes.</p>

          <div className="epic-list-scroll">
            {epics.split(/\n\s*\n/).map((epic, index) => (
              <div key={index} className="epic-card">
                <textarea
                  value={epic.trim()}
                  onChange={(e) => {
                    const updatedEpics = [...epics.split(/\n\s*\n/)];
                    updatedEpics[index] = e.target.value;
                    setEpics(updatedEpics.join('\n\n'));
                  }}
                  rows={4}
                />
              </div>
            ))}
          </div>

          <div className="button-group">
            <button onClick={prevStep} disabled={loading}>Voltar</button>
            <button onClick={handleGenerateUserStories} disabled={loading || !epics}>
              {loading ? 'Gerando Histórias...' : 'Gerar Histórias de Usuário'}
            </button>
          </div>
        </div>
      )}

      {step === 5 && (
        <div className="wizard-step">
          <h2>Histórias de Usuário</h2>
          <p>Histórias de usuário geradas! Revise e edite abaixo para ajustar detalhes de negócio.</p>
          <textarea
            value={userStories}
            onChange={(e) => setUserStories(e.target.value)}
            rows="10"
            disabled={loading}
          />
          <div className="button-group">
            <button onClick={prevStep} disabled={loading}>Voltar</button>
            <button disabled={loading}>Salvar e Gerar Requisitos</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectWizard;