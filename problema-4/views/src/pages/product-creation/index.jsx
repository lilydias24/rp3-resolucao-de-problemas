import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import TextField from '@mui/material/TextField';

import './product-creation.css';

const ProductCreation = () => {
  const navigate = useNavigate();
  const API_BASE_URL = 'http://localhost:8000/llm-project';

  // Nomes dos Steps ao invés de apenas números
  const STEP_NAMES = {
    CONFIG_LLM: 'configLLM',
    INFO_PRODUTO: 'infoProduto',
    ALERTA_VAZIO: 'alertaVazio',
    REVISAR_EPICOS: 'revisarEpicos',
    REVISAR_HISTORIAS_USUARIO: 'revisarHistoriasUsuario',
    REVISAR_REQUISITOS: 'revisarRequisitos'
  };
  const [step, setStep] = useState(STEP_NAMES.CONFIG_LLM);

  const [useDefaultPrompt, setUseDefaultPrompt] = useState(true);
  const [customPrompt, setCustomPrompt] = useState('');
  const [form, setForm] = useState({
    nome: '',
    descricao: '',
    personas: '',
    proposta: '',
    canais: ''
  });
  const defaultForm = {
    nome: 'Sistema de Geração de Produtos com IA',
    descricao: 'Uma plataforma inovadora para Product Owners gerenciarem o ciclo de vida do produto, desde a concepção até o backlog detalhado, utilizando inteligência artificial (LLMs) para automatizar a geração de épicos, histórias de usuário e requisitos funcionais.',
    personas: 'Product Owner, Scrum Master, Desenvolvedor, Stakeholder, QA Tester',
    proposta: 'Resolve a dor de cabeça inicial dos Product Owners ao acelerar a criação de documentação ágil (épicos, histórias, requisitos) através de IA, garantindo alinhamento e reduzindo o tempo de ramp-up do projeto. Ajuda a padronizar a qualidade das especificações do produto.',
    canais: 'Web Application (Desktop & Mobile Responsive), REST API'
  };
  const [epics, setEpics] = useState('');
  const [userStories, setUserStories] = useState('');
  const [requirements, setRequirements] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [emptyFields, setEmptyFields] = useState([]);
  const [isForm2Valid, setIsForm2Valid] = useState(false);

  useEffect(() => {
    if (form.nome.trim() !== '' && form.descricao.trim() !== '') {
      setIsForm2Valid(true);
    } else {
      setIsForm2Valid(false);
    }
  }, [form.nome, form.descricao]);

  const checkEmptyFields = () => {
    const fields = ['nome', 'descricao', 'personas', 'proposta', 'canais'];
    const currentEmptyFields = fields.filter(field => !form[field]);
    return currentEmptyFields;
  };

  const goToStep = (stepName) => {
    setError(null);
    setStep(stepName);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handlePromptOption = (isDefault) => {
    setUseDefaultPrompt(isDefault);
    if (isDefault) {
      setForm(defaultForm);
    } else {
      setForm({ nome: '', descricao: '', personas: '', proposta: '', canais: '' });
      setCustomPrompt('');
    }
    goToStep(STEP_NAMES.INFO_PRODUTO);
  };

  const handleAdvanceFromProductInfo = () => {
    const missingFields = checkEmptyFields();
    setEmptyFields(missingFields);

    if (missingFields.length > 0) {
      goToStep(STEP_NAMES.ALERTA_VAZIO);
    } else {
      handleGenerateEpics();
    }
  };

  const generateContent = async (endpoint, payload, setStateCallback, nextStepOnSucess) => {
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
      goToStep(nextStepOnSucess);
    } catch (err) {
      console.error(`generateContent: Erro no bloco catch:`, err);
      setError(`Falha ao gerar conteúdo: ${err.message}. Verifique a console do navegador e o terminal do servidor.`);
    } finally {
      setLoading(false);
      console.log("generateContent: Carregamento finalizado.");
    }
  };

  const handleGenerateEpics = () => {
    console.log("handleGenerateEpics: Botão clicado!");
    const productInfo = `Nome: ${form.nome}. Descrição: ${form.descricao}. Personas: ${form.personas}. Proposta de Valor: ${form.proposta}. Canais: ${form.canais}.`;
    console.log("handleGenerateEpics: Dados do produto formatados:", productInfo);
    generateContent(
      'generate-epics',
      { productInfo, userPromptAdjustment: customPrompt },
      setEpics,
      STEP_NAMES.REVISAR_EPICOS
    );
    console.log("handleGenerateEpics: Chamada para generateContent feita.");
  };

  const handleGenerateUserStories = () => {
    console.log("handleGenerateUserStories: Botão clicado!");
    const productInfo = `Nome: ${form.nome}. Descrição: ${form.descricao}. Personas: ${form.personas}. Proposta de Valor: ${form.proposta}. Canais: ${form.canais}.`;
    console.log("handleGenerateUserStories: Dados do produto formatados:", productInfo);
    const epicsSummary = epics;
    console.log("handleGenerateUserStories: Resumo dos épicos:", epicsSummary);
    generateContent(
      'generate-user-stories',
      { productInfo, epicsSummary, userPromptAdjustment: customPrompt }, setUserStories,
      STEP_NAMES.REVISAR_HISTORIAS_USUARIO);
    console.log("handleGenerateUserStories: Chamada para generateContent feita.");
  };

  const handleGenerateRequirements = () => {
    console.log("handleGenerateRequirements: Botão clicado!");
    const productInfo = `Nome: ${form.nome}. Descrição: ${form.descricao}. Personas: ${form.personas}. Proposta de Valor: ${form.proposta}. Canais: ${form.canais}.`;
    const userStoriesText = userStories;
    console.log("handleGenerateRequirements: Gerando com base nas histórias:", userStoriesText);

    generateContent(
      'generate-requirements',
      { userStories: userStoriesText, productInfo, userPromptAdjustment: customPrompt },
      setRequirements,
      STEP_NAMES.REVISAR_REQUISITOS
    );
  };

  const handleGoBackToHome = () => {
    navigate('/home');
  };

  const handleRequirementChange = (index, field, value) => {
    const updatedRequirements = [...requirements];
    updatedRequirements[index] = {
      ...updatedRequirements[index],
      [field]: value
    };
    setRequirements(updatedRequirements);
  };

  return (
    <div className="product-container">
      {error && <div className="error-message">{error}</div>}
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner"></div>
          <p>Carregando...</p>
        </div>
      )}

      {step === STEP_NAMES.CONFIG_LLM && (
        <div className="product-step">
          <h2>Configurar Geração LLM</h2>
          <p>Deseja utilizar um prompt pré-definido para a LLM, ou prefere personalizá-lo?</p>
          <div className="button-group">
            <button onClick={handleGoBackToHome} disabled={loading} className="btn-secondary">
              Cancelar
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

      {step === STEP_NAMES.INFO_PRODUTO && (
        <div className="product-step">
          <h2>Informações do Produto</h2>
          <TextField
            name="nome"
            label="Título do Produto"
            value={form.nome}
            onChange={handleChange}
            disabled={loading}
            multiline
            required
            error={!form.nome && !isForm2Valid}
          />
          <TextField
            name="descricao"
            label="Descrição do Produto"
            value={form.descricao}
            onChange={handleChange}
            disabled={loading}
            multiline
            required
            error={!form.descricao && !isForm2Valid}
          />
          <TextField
            name="personas"
            label="Personas Envolvidas"
            value={form.personas}
            onChange={handleChange}
            disabled={loading}
          />
          <TextField
            name="proposta"
            label="Problema que o Produto Resolve"
            value={form.proposta}
            onChange={handleChange}
            disabled={loading}
            multiline
          />
          <TextField
            name="canais"
            label="Canais/Plataformas"
            value={form.canais}
            onChange={handleChange}
            disabled={loading}
            multiline
          />
          <div className="button-group">
            <button onClick={() => goToStep(STEP_NAMES.CONFIG_LLM)} disabled={loading}>Voltar</button>
            <button
              onClick={handleAdvanceFromProductInfo}
              disabled={loading || !isForm2Valid}
            >
              {loading ? 'Gerando...' : 'Gerar Épicos'}
            </button>
          </div>
        </div>
      )}

      {step === STEP_NAMES.ALERTA_VAZIO && emptyFields.length > 0 && (
        <div className="product-step">
          <h2>Atenção: Campos Opcionais Incompletos</h2>
          <div className="warning-message">
            <p>
              <strong>Recomendação:</strong> Para uma geração de conteúdo mais precisa e específica pela Inteligência Artificial, é altamente recomendado preencher todos os campos de informações do produto.
            </p>
            <p>Os seguintes campos estão incompletos:</p>
            <ul>
              {emptyFields.map((field, index) => (
                <li key={index}>{
                  field === 'nome' ? 'Nome do Produto' :
                    field === 'descricao' ? 'Descrição' :
                      field === 'personas' ? 'Personas Envolvidas' :
                        field === 'proposta' ? 'Proposta de Valor' :
                          field === 'canais' ? 'Canais/Plataformas' :
                            field
                }</li>
              ))}
            </ul>
            <p>Você pode voltar para preencher ou prosseguir com os dados atuais.</p>
          </div>
          <div className="button-group">
            <button onClick={() => goToStep(STEP_NAMES.INFO_PRODUTO)} disabled={loading} className="btn-secondary">
              Voltar para Preencher
            </button>
            <button onClick={handleGenerateEpics} disabled={loading}>
              Prosseguir Mesmo Assim
            </button>
          </div>
        </div>
      )}

      {step === STEP_NAMES.REVISAR_EPICOS && (
        <div className="product-step">
          <h2>Revisar Épicos</h2>
          <p>Épicos gerados! Revise e edite abaixo para ajustar conforme desejado.</p>

          <div className="epic-list-scroll">
            {epics.split(/\n\s*\n/).map((epic, index) => (
              <div key={index} className="epic-card">
                <TextField
                  value={epic.trim()}
                  onChange={(e) => {
                    const updatedEpics = [...epics.split(/\n\s*\n/)];
                    updatedEpics[index] = e.target.value;
                    setEpics(updatedEpics.join('\n\n'));
                  }}
                  multiline
                  fullWidth
                  margin="normal"
                  disabled={loading}
                  variant="outlined"
                />
              </div>
            ))}
          </div>

          <div className="button-group">
            <button onClick={() => goToStep(STEP_NAMES.INFO_PRODUTO)} disabled={loading}>Voltar</button>
            <button onClick={handleGenerateUserStories} disabled={loading || !epics}>
              {loading ? 'Gerando Histórias...' : 'Gerar Histórias de Usuário'}
            </button>
          </div>
        </div>
      )}

      {step === STEP_NAMES.REVISAR_HISTORIAS_USUARIO && (
        <div className="product-step">
          <h2>Revisar Histórias de Usuário</h2>
          <p>Histórias de usuário geradas! Revise e edite abaixo para ajustar conforme desejado.</p>

          <div className="user-story-list-scroll">
            {userStories
              .split(/\n\s*\n/)
              .map((story, index) => (
                <div key={index} className="user-story-card">
                  <TextField
                    value={story.trim()}
                    onChange={(e) => {
                      const updatedStories = [...userStories.split(/\n\s*\n/)];
                      updatedStories[index] = e.target.value;
                      setUserStories(updatedStories.join('\n\n'));
                    }}
                    multiline
                    fullWidth
                    margin="normal"
                    disabled={loading}
                    variant="outlined"
                  />
                </div>
              ))}
          </div>

          <div className="button-group">
            <button onClick={() => goToStep(STEP_NAMES.REVISAR_EPICOS)} disabled={loading}>Voltar</button>
            <button onClick={handleGenerateRequirements} disabled={loading || !userStories}>
              {loading ? 'Gerando Requisitos...' : 'Gerar Requisitos Funcionais'}
            </button>
          </div>
        </div>
      )}

      {step === STEP_NAMES.REVISAR_REQUISITOS && (
        <div className="product-step">
          <h2>Revisar Requisitos Funcionais</h2>
          <p>Requisitos funcionais gerados! Revise e edite abaixo conforme necessário.</p>

          <div className="requirements-list-scroll">
            {(Array.isArray(requirements) ? requirements : []).map((req, index) => (
              <div key={req.id || index} className="requirement-card">
                <TextField
                  label="ID do Requisito"
                  value={req.id || ''}
                  onChange={(e) => handleRequirementChange(index, 'id', e.target.value)}
                  fullWidth
                  margin="dense"
                  disabled={loading}
                  variant="outlined"
                />
                <TextField
                  label="Descrição"
                  value={req.descricao || ''}
                  onChange={(e) => handleRequirementChange(index, 'descricao', e.target.value)}
                  multiline
                  fullWidth
                  margin="dense"
                  disabled={loading}
                  variant="outlined"
                />
                <TextField
                  label="Prioridade"
                  value={req.prioridade || ''}
                  onChange={(e) => handleRequirementChange(index, 'prioridade', e.target.value)}
                  fullWidth
                  margin="dense"
                  disabled={loading}
                  variant="outlined"
                />
              </div>
            ))}
          </div>

          <div className="button-group">
            <button onClick={() => goToStep(STEP_NAMES.REVISAR_HISTORIAS_USUARIO)} disabled={loading}>Voltar</button>
            <button disabled={loading}>Finalizar</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductCreation;