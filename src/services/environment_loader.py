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
                logger.info(f"✅ Configurado {var_name} com valor padrão")
        
        # Configura variáveis recomendadas se não estiverem definidas
        for var_name, default_value in recommended_vars.items():
            if not os.getenv(var_name):
                os.environ[var_name] = default_value
                logger.info(f"✅ Configurado {var_name} com valor padrão")
        
        # Verifica se ainda há variáveis ausentes
        self.missing_vars = []
        for var_name in required_vars.keys():
            if not os.getenv(var_name):
                self.missing_vars.append(var_name)
        
        if self.missing_vars:
            logger.error(f"❌ Variáveis críticas ausentes: {', '.join(self.missing_vars)}")
        else:
            logger.info("✅ Todas as variáveis críticas configuradas")
    
    def set_default_values(self):
        """Define valores padrão para configurações"""
        
        defaults = {
            'FLASK_ENV': 'production',
            'HOST': '0.0.0.0',
            'PORT': '5000',
            'LOG_LEVEL': 'INFO',
            'AUTO_SAVE_ENABLED': 'true',
            'RESILIENT_MODE': 'true',
            'URL_FILTERING_ENABLED': 'true',
            'WEBSAILOR_ENABLED': 'true',
            'ULTRA_DETAILED_MODE': 'true',
            'CONTENT_QUALITY_THRESHOLD': '60.0',
            'MIN_CONTENT_LENGTH': '500',
            'MIN_SOURCES_REQUIRED': '3',
            'ANALYSIS_TIMEOUT': '600'
        }
        
        for var_name, default_value in defaults.items():
            if not os.getenv(var_name):
                os.environ[var_name] = default_value
    
    def get_api_status(self) -> Dict[str, Any]:
        """Retorna status das APIs configuradas"""
        
        apis = {
            'supabase': {
                'configured': bool(os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_ANON_KEY')),
                'url': os.getenv('SUPABASE_URL', 'Not configured'),
                'priority': 'CRITICAL'
            },
            'gemini': {
                'configured': bool(os.getenv('GEMINI_API_KEY')),
                'key_preview': f"{os.getenv('GEMINI_API_KEY', '')[:10]}..." if os.getenv('GEMINI_API_KEY') else 'Not configured',
                'priority': 'CRITICAL'
            },
            'groq': {
                'configured': bool(os.getenv('GROQ_API_KEY')),
                'key_preview': f"{os.getenv('GROQ_API_KEY', '')[:10]}..." if os.getenv('GROQ_API_KEY') else 'Not configured',
                'priority': 'RECOMMENDED'
            },
            'openai': {
                'configured': bool(os.getenv('OPENAI_API_KEY')),
                'key_preview': f"{os.getenv('OPENAI_API_KEY', '')[:10]}..." if os.getenv('OPENAI_API_KEY') else 'Not configured',
                'priority': 'OPTIONAL'
            },
            'google_search': {
                'configured': bool(os.getenv('GOOGLE_SEARCH_KEY') and os.getenv('GOOGLE_CSE_ID')),
                'key_preview': f"{os.getenv('GOOGLE_SEARCH_KEY', '')[:10]}..." if os.getenv('GOOGLE_SEARCH_KEY') else 'Not configured',
                'priority': 'RECOMMENDED'
            },
            'serper': {
                'configured': bool(os.getenv('SERPER_API_KEY')),
                'key_preview': f"{os.getenv('SERPER_API_KEY', '')[:10]}..." if os.getenv('SERPER_API_KEY') else 'Not configured',
                'priority': 'OPTIONAL'
            },
            'jina': {
                'configured': bool(os.getenv('JINA_API_KEY')),
                'key_preview': f"{os.getenv('JINA_API_KEY', '')[:10]}..." if os.getenv('JINA_API_KEY') else 'Not configured',
                'priority': 'OPTIONAL'
            }
        }
        
        return apis
    
    def print_configuration_status(self):
        """Imprime status da configuração"""
        
        print("\n" + "=" * 80)
        print("🔧 STATUS DA CONFIGURAÇÃO DE APIS")
        print("=" * 80)
        
        apis = self.get_api_status()
        
        critical_configured = 0
        critical_total = 0
        
        for api_name, api_info in apis.items():
            priority = api_info['priority']
            configured = api_info['configured']
            
            if priority == 'CRITICAL':
                critical_total += 1
                if configured:
                    critical_configured += 1
            
            status_icon = "✅" if configured else "❌"
            priority_icon = {
                'CRITICAL': '🚨',
                'RECOMMENDED': '⭐',
                'OPTIONAL': '💡'
            }.get(priority, '📌')
            
            print(f"{status_icon} {priority_icon} {api_name.upper()}: {'CONFIGURADO' if configured else 'AUSENTE'}")
            
            if configured and 'key_preview' in api_info:
                print(f"    Chave: {api_info['key_preview']}")
            elif configured and 'url' in api_info:
                print(f"    URL: {api_info['url']}")
        
        print(f"\n📊 RESUMO:")
        print(f"   • APIs Críticas: {critical_configured}/{critical_total}")
        print(f"   • Status Geral: {'✅ PRONTO' if critical_configured == critical_total else '⚠️ CONFIGURAÇÃO INCOMPLETA'}")
        
        if critical_configured < critical_total:
            print(f"\n🚨 AÇÃO NECESSÁRIA:")
            print(f"   Configure as APIs críticas ausentes para funcionamento completo")
        else:
            print(f"\n🎉 CONFIGURAÇÃO COMPLETA!")
            print(f"   Sistema pronto para análise ultra-detalhada")

# Instância global
environment_loader = EnvironmentLoader()

# Função de conveniência
def ensure_environment_loaded():
    """Garante que o ambiente foi carregado"""
    if not environment_loader.env_loaded:
        environment_loader.load_environment()
    return environment_loader.env_loaded