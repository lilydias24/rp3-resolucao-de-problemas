import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from functools import wraps
from aspects.llm_aspects import *
from src.utils.epics import *
from dotenv import load_dotenv
load_dotenv()

# Testes para o decorator llm_aspect
class TestLlmAspect:
    @patch.dict(os.environ, {"GROQ_API_KEY": "fake_api_key"})
    @patch("aspects.llm_aspects.Groq")
    def test_llm_aspect_success(self, mock_groq_client):
        mock_instance = mock_groq_client.return_value
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Conteúdo simulado da LLM"))]
        )

        @llm_aspect
        def test_func():
            return "Prompt de teste"

        result = test_func()

        mock_groq_client.assert_called_once_with(api_key="fake_api_key")
        mock_instance.chat.completions.create.assert_called_once()
        call_args, call_kwargs = mock_instance.chat.completions.create.call_args
        assert call_kwargs["messages"][0]["content"] == "Prompt de teste"
        assert result == "Conteúdo simulado da LLM"

    @patch.dict(os.environ, {}, clear=True)
    def test_llm_aspect_no_api_key(self):
        @llm_aspect
        def test_func():
            return "Prompt de teste"

        with pytest.raises(ValueError, match="GROQ_API_KEY não configurada nas variáveis de ambiente."):
            test_func()

    @patch.dict(os.environ, {"GROQ_API_KEY": "fake_api_key"})
    @patch("aspects.llm_aspects.Groq")
    def test_llm_aspect_api_failure(self, mock_groq_client):
        mock_instance = mock_groq_client.return_value
        mock_instance.chat.completions.create.side_effect = Exception("Erro de conexão da API")

        @llm_aspect
        def test_func():
            return "Prompt de teste"

        with pytest.raises(RuntimeError, match="Falha ao se comunicar com a LLM via aspecto: Erro de conexão da API"):
            test_func()

# Testes para as funções que geram prompts
class TestPromptGenerators:
    @patch.dict(os.environ, {"GROQ_API_KEY": "fake_api_key"})
    @patch("aspects.llm_aspects.Groq")
    def test_gerar_epicos_prompt(self, mock_groq_client):
        mock_instance = mock_groq_client.return_value
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Épicos gerados"))]
        )

        product_info = "Um aplicativo de gerenciamento de tarefas para equipes pequenas."
        result = gerar_epicos_prompt(product_info)

        expected_prompt_part = (
            "Gere uma hierarquia de 10 Épicos para um novo projeto de software. "
            "Baseie-se nas seguintes informações do produto:\n\nUm aplicativo de gerenciamento de tarefas para equipes pequenas.\n\n"
            "Para cada épico, forneça apenas a numeração, o 'Nome do Épico' e, em seguida, uma 'Breve Descrição'. "
            "Não inclua introduções, encerramentos ou qualquer texto adicional além dos épicos solicitados."
        )
        call_args, call_kwargs = mock_instance.chat.completions.create.call_args
        assert call_kwargs["messages"][1]["content"] == expected_prompt_part
        assert result == "Épicos gerados"

    @patch.dict(os.environ, {"GROQ_API_KEY": "fake_api_key"})
    @patch("aspects.llm_aspects.Groq")
    def test_gerar_historia_usuario_prompt_without_adjustment(self, mock_groq_client):
        mock_instance = mock_groq_client.return_value
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Histórias de usuário geradas"))]
        )

        product_info = "Um sistema de e-commerce."
        epics_summary = "1. Gestão de Produtos, 2. Carrinho de Compras."
        result = gerar_historia_usuario_prompt(product_info, epics_summary)

        expected_prompt_part = (
            "Gere um conjunto de histórias de usuário detalhadas. "
            "Use as seguintes informações do produto:\nUm sistema de e-commerce.\n\n"
            "E os seguintes Épicos para contextualização:\n1. Gestão de Produtos, 2. Carrinho de Compras.\n\n"
            "Para cada história, utilize o formato exato: 'Como <persona>, quero <ação>, para que <benefício>'. "
            "Após a história, indique a prioridade: 'Prioridade: [Alto/Médio/Baixo]'. "
            "Não adicione introduções, encerramentos, numeração ou qualquer texto extra."
            "Em cada história adicione o número do épico relacionado. Como exemplo: ( 1. Nome do Épico )\n\n"
        )
        call_args, call_kwargs = mock_instance.chat.completions.create.call_args
        assert call_kwargs["messages"][1]["content"] == expected_prompt_part
        assert result == "Histórias de usuário geradas"

    @patch.dict(os.environ, {"GROQ_API_KEY": "fake_api_key"})
    @patch("aspects.llm_aspects.Groq")
    def test_gerar_historia_usuario_prompt_with_adjustment(self, mock_groq_client):
        mock_instance = mock_groq_client.return_value
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Histórias de usuário com ajuste geradas"))]
        )

        product_info = "Um sistema de e-commerce."
        epics_summary = "1. Gestão de Produtos, 2. Carrinho de Compras."
        user_prompt_adjustment = "Focar em histórias para usuários administradores."
        result = gerar_historia_usuario_prompt(product_info, epics_summary, user_prompt_adjustment)

        expected_prompt_part = (
            "Gere um conjunto de histórias de usuário detalhadas. "
            "Use as seguintes informações do produto:\nUm sistema de e-commerce.\n\n"
            "E os seguintes Épicos para contextualização:\n1. Gestão de Produtos, 2. Carrinho de Compras.\n\n"
            "Para cada história, utilize o formato exato: 'Como <persona>, quero <ação>, para que <benefício>'. "
            "Após a história, indique a prioridade: 'Prioridade: [Alto/Médio/Baixo]'. "
            "Não adicione introduções, encerramentos, numeração ou qualquer texto extra."
            "Em cada história adicione o número do épico relacionado. Como exemplo: ( 1. Nome do Épico )\n\n"
            "\n\nConsidere também o seguinte ajuste adicional para a geração: Focar em histórias para usuários administradores."
        )
        call_args, call_kwargs = mock_instance.chat.completions.create.call_args
        assert call_kwargs["messages"][1]["content"] == expected_prompt_part
        assert result == "Histórias de usuário com ajuste geradas"

    @patch.dict(os.environ, {"GROQ_API_KEY": "fake_api_key"})
    @patch("aspects.llm_aspects.Groq")
    def test_gerar_requisitos_prompt(self, mock_groq_client):
        mock_instance = mock_groq_client.return_value
        mock_instance.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content='[{"id": "RF-001", "descricao": "Teste", "prioridade": "Alta"}]'))]
        )

        user_stories = "Como usuário, quero fazer login."
        product_info = "Um app de autenticação."
        result = gerar_requisitos_prompt(user_stories, product_info)

        expected_prompt_part = (
            "Com base nas seguintes histórias de usuário:\n\nComo usuário, quero fazer login.\n\nE no produto com informações: "
            " Um app de autenticação.\n\n Gere uma lista de requisitos funcionais detalhados. "
            "Retorne o resultado estritamente no formato JSON, como um array de objetos, onde cada objeto tem as chaves: "
            "'id' (string única, ex: 'RF-001'), 'descricao' (string clara do requisito), e 'prioridade' (string: 'Alta', 'Média', ou 'Baixa').\n"
            "Não inclua introduções, encerramentos, ou qualquer texto adicional fora do objeto JSON."
            "Exemplo de formato esperado: "
            '```json\n[\n  {"id": "RF-001", "descricao": "O sistema deve permitir login de usuários.", "prioridade": "Alta"},\n  {"id": "RF-002", "descricao": "O sistema deve exibir a lista de produtos.", "prioridade": "Média"}}\n]\n```\n'
            "Certifique-se de que a saída seja apenas o JSON."
        )
        call_args, call_kwargs = mock_instance.chat.completions.create.call_args
        assert call_kwargs["messages"][1]["content"] == expected_prompt_part
        assert result == '[{"id": "RF-001", "descricao": "Teste", "prioridade": "Alta"}]'