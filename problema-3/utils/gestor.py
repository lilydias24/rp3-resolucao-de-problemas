"""
Módulo para gerenciamento de regras de carreiras pelo Gestor Acadêmico.
"""
import json
import os
from typing import Dict, List, Any

class GestorRegras:
    """
    Classe para gerenciar as regras de carreiras.
    Permite adicionar, editar e remover regras sem alterar o código-fonte.
    """
    
    def __init__(self, caminho_regras: str):
        """
        Inicializa o gestor de regras.
        
        Args:
            caminho_regras: Caminho para o arquivo de regras JSON
        """
        self.caminho_regras = caminho_regras
        self.regras = self._carregar_regras()
    
    def _carregar_regras(self) -> List[Dict[str, Any]]:
        """
        Carrega as regras do arquivo JSON.
        
        Returns:
            Lista de regras carregadas
        """
        try:
            with open(self.caminho_regras, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _salvar_regras(self) -> None:
        """
        Salva as regras no arquivo JSON.
        """
        with open(self.caminho_regras, 'w', encoding='utf-8') as f:
            json.dump(self.regras, f, indent=4, ensure_ascii=False)
    
    def validar_regra(self, regra: Dict[str, Any]) -> bool:
        """
        Valida se uma regra está no formato correto.
        
        Args:
            regra: Regra a ser validada
            
        Returns:
            True se a regra é válida, False caso contrário
        """
        campos_obrigatorios = ['carreira', 'condicoes', 'justificativa']
        if not all(campo in regra for campo in campos_obrigatorios):
            return False
        
        condicoes = regra['condicoes']
        if not isinstance(condicoes, dict):
            return False
        
        
        campos_validos = ['interesses', 'habilidades', 'desempenho', 'pesos']
        if not all(campo in campos_validos for campo in condicoes.keys()):
            return False
        
        # validação dos tipos de dados
        if 'interesses' in condicoes and not isinstance(condicoes['interesses'], list):
            return False
        if 'habilidades' in condicoes and not isinstance(condicoes['habilidades'], list):
            return False
        if 'desempenho' in condicoes and not isinstance(condicoes['desempenho'], dict):
            return False
        if 'pesos' in condicoes and not isinstance(condicoes['pesos'], dict):
            return False
        
        return True
    
    def adicionar_regra(self, regra: Dict[str, Any]) -> bool:
        """
        Adiciona uma nova regra.
        
        Args:
            regra: Nova regra a ser adicionada
            
        Returns:
            True se a regra foi adicionada com sucesso, False caso contrário
        """
        if not self.validar_regra(regra):
            return False
        
        # ve se já existe uma regra p essa carreira
        if any(r['carreira'] == regra['carreira'] for r in self.regras):
            return False
        
        self.regras.append(regra)
        self._salvar_regras()
        return True
    
    def editar_regra(self, carreira: str, nova_regra: Dict[str, Any]) -> bool:
        """
        Edita uma regra existente.
        
        Args:
            carreira: Nome da carreira a ser editada
            nova_regra: Nova versão da regra
            
        Returns:
            True se a regra foi editada com sucesso, False caso contrário
        """
        if not self.validar_regra(nova_regra):
            return False
        
        for i, regra in enumerate(self.regras):
            if regra['carreira'] == carreira:
                self.regras[i] = nova_regra
                self._salvar_regras()
                return True
        
        return False
    
    def remover_regra(self, carreira: str) -> bool:
        """
        Remove uma regra existente.
        
        Args:
            carreira: Nome da carreira a ser removida
            
        Returns:
            True se a regra foi removida com sucesso, False caso contrário
        """
        for i, regra in enumerate(self.regras):
            if regra['carreira'] == carreira:
                del self.regras[i]
                self._salvar_regras()
                return True
        
        return False
    
    def listar_regras(self) -> List[Dict[str, Any]]:
        """
        Lista todas as regras existentes.
        
        Returns:
            Lista de todas as regras
        """
        return self.regras
    
    def obter_regra(self, carreira: str) -> Dict[str, Any]:
        """
        Obtém uma regra específica.
        
        Args:
            carreira: Nome da carreira
            
        Returns:
            Regra encontrada ou None se não existir
        """
        for regra in self.regras:
            if regra['carreira'] == carreira:
                return regra
        return None 