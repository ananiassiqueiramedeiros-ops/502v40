#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - API Validator
Validador de APIs para garantir funcionamento correto
"""

import os
import logging
import time
from typing import Dict, Any, Tuple
import requests

logger = logging.getLogger(__name__)

class APIValidator:
    """Validador de APIs para ARQV30 Enhanced"""
    
    def __init__(self):
        """Inicializa o validador de APIs"""
        self.validation_results = {}
        self.last_validation = None
        
    def validate_all_apis(self) -> Dict[str, Any]:
        """Valida todas as APIs configuradas"""
        
        logger.info("🔍 Iniciando validação completa de APIs...")
        
        validation_results = {
            'timestamp': time.time(),
            'apis': {},
            'summary': {
                'total_apis': 0,
                'configured_apis': 0,
                'working_apis': 0,
                'critical_apis_working': 0,
                'system_ready': False
            }
        }
        
        # APIs para validar
        apis_to_validate = [
            ('supabase', self._validate_supabase, 'CRITICAL'),
            ('gemini', self._validate_gemini, 'CRITICAL'),
            ('groq', self._validate_groq, 'RECOMMENDED'),
            ('openai', self._validate_openai, 'OPTIONAL'),
            ('google_search', self._validate_google_search, 'RECOMMENDED'),
            ('serper', self._validate_serper, 'OPTIONAL'),
            ('jina', self._validate_jina, 'OPTIONAL')
        ]
        
        validation_results['summary']['total_apis'] = len(apis_to_validate)
        
        for api_name, validator_func, priority in apis_to_validate:
            try:
                logger.info(f"🧪 Validando {api_name.upper()}...")
                
                configured, working, details = validator_func()
                
                validation_results['apis'][api_name] = {
                    'configured': configured,
                    'working': working,
                    'priority': priority,
                    'details': details,
                    'status': 'OK' if working else 'ERROR' if configured else 'NOT_CONFIGURED'
                }
                
                if configured:
                    validation_results['summary']['configured_apis'] += 1
                
                if working:
                    validation_results['summary']['working_apis'] += 1
                    
                    if priority == 'CRITICAL':
                        validation_results['summary']['critical_apis_working'] += 1
                
                status_icon = "✅" if working else "⚠️" if configured else "❌"
                print(f"   {status_icon} {api_name.upper()}: {details}")
                
            except Exception as e:
                logger.error(f"❌ Erro ao validar {api_name}: {e}")
                validation_results['apis'][api_name] = {
                    'configured': False,
                    'working': False,
                    'priority': priority,
                    'details': f'Erro na validação: {str(e)}',
                    'status': 'ERROR'
                }
        
        # Determina se sistema está pronto
        critical_apis = [api for api, data in validation_results['apis'].items() 
                        if data['priority'] == 'CRITICAL']
        critical_working = sum(1 for api in critical_apis 
                              if validation_results['apis'][api]['working'])
        
        validation_results['summary']['system_ready'] = critical_working >= 2  # Supabase + pelo menos 1 IA
        
        self.validation_results = validation_results
        self.last_validation = time.time()
        
        return validation_results
    
    def _validate_supabase(self) -> Tuple[bool, bool, str]:
        """Valida Supabase"""
        
        url = os.getenv('SUPABASE_URL')
        anon_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not url or not anon_key:
            return False, False, "URL ou chave não configuradas"
        
        try:
            from supabase import create_client
            client = create_client(url, anon_key)
            
            # Testa conexão simples
            result = client.table('analyses').select('id').limit(1).execute()
            return True, True, "Conectado e funcionando"
            
        except Exception as e:
            return True, False, f"Configurado mas com erro: {str(e)[:50]}"
    
    def _validate_gemini(self) -> Tuple[bool, bool, str]:
        """Valida Google Gemini"""
        
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            return False, False, "API key não configurada"
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content("Responda apenas: GEMINI_OK")
            
            if response.text and "GEMINI_OK" in response.text:
                return True, True, "Conectado e respondendo"
            else:
                return True, False, "Configurado mas não responde corretamente"
                
        except Exception as e:
            return True, False, f"Erro: {str(e)[:50]}"
    
    def _validate_groq(self) -> Tuple[bool, bool, str]:
        """Valida Groq"""
        
        api_key = os.getenv('GROQ_API_KEY')
        
        if not api_key:
            return False, False, "API key não configurada"
        
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Responda apenas: GROQ_OK"}],
                model="llama3-70b-8192",
                max_tokens=10
            )
            
            if response.choices[0].message.content and "GROQ_OK" in response.choices[0].message.content:
                return True, True, "Conectado e respondendo"
            else:
                return True, False, "Configurado mas não responde corretamente"
                
        except Exception as e:
            return True, False, f"Erro: {str(e)[:50]}"
    
    def _validate_openai(self) -> Tuple[bool, bool, str]:
        """Valida OpenAI"""
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            return False, False, "API key não configurada"
        
        try:
            import openai
            client = openai.OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Responda apenas: OPENAI_OK"}],
                max_tokens=10
            )
            
            if response.choices[0].message.content and "OPENAI_OK" in response.choices[0].message.content:
                return True, True, "Conectado e respondendo"
            else:
                return True, False, "Configurado mas não responde corretamente"
                
        except Exception as e:
            return True, False, f"Erro: {str(e)[:50]}"
    
    def _validate_google_search(self) -> Tuple[bool, bool, str]:
        """Valida Google Custom Search"""
        
        api_key = os.getenv('GOOGLE_SEARCH_KEY')
        cse_id = os.getenv('GOOGLE_CSE_ID')
        
        if not api_key or not cse_id:
            return False, False, "API key ou CSE ID não configurados"
        
        try:
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': cse_id,
                'q': 'teste',
                'num': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'items' in data:
                    return True, True, "Conectado e retornando resultados"
                else:
                    return True, False, "Conectado mas sem resultados"
            else:
                return True, False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return True, False, f"Erro: {str(e)[:50]}"
    
    def _validate_serper(self) -> Tuple[bool, bool, str]:
        """Valida Serper API"""
        
        api_key = os.getenv('SERPER_API_KEY')
        
        if not api_key:
            return False, False, "API key não configurada"
        
        try:
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': api_key,
                'Content-Type': 'application/json'
            }
            payload = {'q': 'teste', 'num': 1}
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'organic' in data:
                    return True, True, "Conectado e retornando resultados"
                else:
                    return True, False, "Conectado mas sem resultados"
            else:
                return True, False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return True, False, f"Erro: {str(e)[:50]}"
    
    def _validate_jina(self) -> Tuple[bool, bool, str]:
        """Valida Jina AI"""
        
        api_key = os.getenv('JINA_API_KEY')
        
        if not api_key:
            return False, False, "API key não configurada"
        
        try:
            url = "https://r.jina.ai/https://example.com"
            headers = {'Authorization': f'Bearer {api_key}'}
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200 and len(response.text) > 100:
                return True, True, "Conectado e extraindo conteúdo"
            else:
                return True, False, f"HTTP {response.status_code}"
                
        except Exception as e:
            return True, False, f"Erro: {str(e)[:50]}"
    
    def get_system_readiness(self) -> Dict[str, Any]:
        """Retorna prontidão do sistema"""
        
        if not self.validation_results:
            self.validate_all_apis()
        
        apis = self.validation_results['apis']
        
        # Conta APIs críticas funcionando
        critical_working = sum(1 for api_data in apis.values() 
                              if api_data['priority'] == 'CRITICAL' and api_data['working'])
        
        # Conta APIs recomendadas funcionando
        recommended_working = sum(1 for api_data in apis.values() 
                                 if api_data['priority'] == 'RECOMMENDED' and api_data['working'])
        
        # Determina nível de funcionalidade
        if critical_working >= 2 and recommended_working >= 1:
            readiness_level = 'FULL'
            readiness_message = 'Sistema totalmente operacional'
        elif critical_working >= 2:
            readiness_level = 'BASIC'
            readiness_message = 'Funcionalidade básica disponível'
        elif critical_working >= 1:
            readiness_level = 'LIMITED'
            readiness_message = 'Funcionalidade limitada'
        else:
            readiness_level = 'NOT_READY'
            readiness_message = 'Sistema não está pronto'
        
        return {
            'level': readiness_level,
            'message': readiness_message,
            'critical_working': critical_working,
            'recommended_working': recommended_working,
            'total_working': self.validation_results['summary']['working_apis'],
            'system_ready': readiness_level in ['FULL', 'BASIC']
        }

# Instância global
api_validator = APIValidator()

# Função de conveniência
def validate_system_apis():
    """Valida todas as APIs do sistema"""
    return api_validator.validate_all_apis()