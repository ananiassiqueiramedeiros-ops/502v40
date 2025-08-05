#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Environment Loader
Carregador robusto de variáveis de ambiente com validação
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class EnvironmentLoader:
    """Carregador robusto de variáveis de ambiente"""
    
    def __init__(self):
        """Inicializa o carregador de ambiente"""
        self.env_loaded = False
        self.missing_vars = []
        self.load_environment()
    
    def load_environment(self):
        """Carrega variáveis de ambiente de múltiplas fontes"""
        try:
            # 1. Tenta carregar python-dotenv
            try:
                from dotenv import load_dotenv
                
                # Procura arquivo .env em múltiplos locais
                env_paths = [
                    '.env',
                    '../.env',
                    '../../.env',
                    os.path.join(os.path.dirname(__file__), '..', '..', '.env'),
                    os.path.join(os.getcwd(), '.env')
                ]
                
                for env_path in env_paths:
                    if os.path.exists(env_path):
                        load_dotenv(env_path, override=True)
                        logger.info(f"✅ Arquivo .env carregado: {env_path}")
                        self.env_loaded = True
                        break
                
                if not self.env_loaded:
                    logger.warning("⚠️ Arquivo .env não encontrado em nenhum local")
                    
            except ImportError:
                logger.warning("⚠️ python-dotenv não instalado, usando apenas variáveis do sistema")
            
            # 2. Valida variáveis críticas
            self.validate_critical_variables()
            
            # 3. Configura valores padrão
            self.set_default_values()
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar ambiente: {e}")
    
    def validate_critical_variables(self):
        """Valida variáveis críticas"""
        
        # Variáveis obrigatórias
        required_vars = {
            'SUPABASE_URL': 'https://kkjapanfbafrhlfekyks.supabase.co',
            'SUPABASE_ANON_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtramFwYW5mYmFmcmhsZmVreWtzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ0MjY5NjQsImV4cCI6MjA3MDAwMjk2NH0.e21yvQ8CGIGJrxBZogIW82tOqePd-8zRm9rmMo2PR_Q',
            'GEMINI_API_KEY': 'AIzaSyCERwa-oIFWewEpuAZt1mxxmm4A3sQo9Es'
        }
        
        # Variáveis recomendadas
        recommended_vars = {
            'GROQ_API_KEY': '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',
            'GOOGLE_SEARCH_KEY': 'AIzaSyDwIFvCvailaG6B7xtysujm0djJn1zlx18',
            'GOOGLE_CSE_ID': 'c207a51dd04f9488a'
        }
        
        # Configura variáveis obrigatórias se não estiverem definidas
        for var_name, default_value in required_vars.items():
            if not os.getenv(var_name):
                os.environ[var_name] = default_value
                logger.info(f"✅ {var_name} configurado")
        
        # Configura variáveis recomendadas se não estiverem definidas
        for var_name, default_value in recommended_vars.items():
            if not os.getenv(var_name):
                os.environ[var_name] = default_value
                logger.info(f"✅ {var_name} configurado")
        
        # Verifica se ainda há variáveis ausentes
        self.missing_vars = []
        for var_name in required_vars.keys():
            if not os.getenv(var_name):
                self.missing_vars.append(var_name)
        
        if self.missing_vars:
            logger.error(f"❌ Variáveis críticas ausentes: {', '.join(self.missing_vars)}")
        else:
            logger.info("✅ Todas as variáveis críticas configuradas")

# Instância global
environment_loader = EnvironmentLoader()

# Função de conveniência
def ensure_environment_loaded():
    """Garante que o ambiente foi carregado"""
    if not environment_loader.env_loaded:
        environment_loader.load_environment()
    return environment_loader.env_loaded