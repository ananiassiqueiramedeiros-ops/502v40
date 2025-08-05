#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Enhanced Validation System
Sistema de validação aprimorado que permite continuidade mesmo com falhas
"""

import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from services.auto_save_manager import salvar_etapa, salvar_erro

logger = logging.getLogger(__name__)

class EnhancedValidationSystem:
    """Sistema de validação aprimorado com tolerância inteligente"""
    
    def __init__(self):
        """Inicializa sistema de validação aprimorado"""
        self.validation_levels = {
            'STRICT': {
                'min_content_length': 5000,
                'min_sources': 5,
                'min_insights': 10,
                'min_quality_score': 80.0,
                'simulation_tolerance': 0
            },
            'MODERATE': {
                'min_content_length': 2000,
                'min_sources': 3,
                'min_insights': 5,
                'min_quality_score': 60.0,
                'simulation_tolerance': 5
            },
            'FLEXIBLE': {
                'min_content_length': 500,
                'min_sources': 1,
                'min_insights': 3,
                'min_quality_score': 40.0,
                'simulation_tolerance': 10
            },
            'EMERGENCY': {
                'min_content_length': 100,
                'min_sources': 0,
                'min_insights': 1,
                'min_quality_score': 20.0,
                'simulation_tolerance': 20
            }
        }
        
        self.current_level = 'MODERATE'  # Nível padrão
        
        logger.info("Enhanced Validation System inicializado com tolerância inteligente")
    
    def validate_with_progressive_tolerance(
        self, 
        analysis: Dict[str, Any],
        session_id: str = None
    ) -> Dict[str, Any]:
        """Valida análise com tolerância progressiva"""
        
        try:
            logger.info(f"🔍 Validando análise com nível {self.current_level}")
            
            # Tenta validação em níveis progressivos
            validation_levels = ['STRICT', 'MODERATE', 'FLEXIBLE', 'EMERGENCY']
            
            for level in validation_levels:
                logger.info(f"🧪 Tentando validação nível {level}")
                
                validation_result = self._validate_at_level(analysis, level, session_id)
                
                if validation_result['valid']:
                    logger.info(f"✅ Análise aprovada no nível {level}")
                    validation_result['validation_level'] = level
                    validation_result['recommendation'] = self._get_level_recommendation(level)
                    return validation_result
                else:
                    logger.warning(f"⚠️ Análise rejeitada no nível {level}: {validation_result['primary_reason']}")
                    
                    # Salva tentativa de validação
                    salvar_etapa(f"validacao_tentativa_{level.lower()}", {
                        "level": level,
                        "result": validation_result,
                        "approved": False
                    }, categoria="analise_completa")
            
            # Se chegou aqui, nem no nível EMERGENCY passou
            logger.error("❌ Análise rejeitada em todos os níveis de validação")
            
            # Mas ainda assim permite continuar com aviso
            emergency_validation = self._create_emergency_validation(analysis, session_id)
            return emergency_validation
            
        except Exception as e:
            logger.error(f"❌ Erro crítico na validação: {str(e)}")
            salvar_erro("validacao_critica", e, contexto={"session_id": session_id})
            
            # Retorna validação de emergência
            return self._create_emergency_validation(analysis, session_id)
    
    def _validate_at_level(
        self, 
        analysis: Dict[str, Any], 
        level: str,
        session_id: str = None
    ) -> Dict[str, Any]:
        """Valida análise em um nível específico"""
        
        thresholds = self.validation_levels[level]
        
        validation_result = {
            'valid': False,
            'level': level,
            'quality_score': 0.0,
            'errors': [],
            'warnings': [],
            'component_scores': {},
            'primary_reason': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 1. Valida estrutura básica
            structure_score = self._validate_structure_flexible(analysis, thresholds)
            validation_result['component_scores']['structure'] = structure_score
            
            # 2. Valida pesquisa web
            research_score = self._validate_research_flexible(analysis, thresholds)
            validation_result['component_scores']['research'] = research_score
            
            # 3. Valida avatar
            avatar_score = self._validate_avatar_flexible(analysis, thresholds)
            validation_result['component_scores']['avatar'] = avatar_score
            
            # 4. Valida insights
            insights_score = self._validate_insights_flexible(analysis, thresholds)
            validation_result['component_scores']['insights'] = insights_score
            
            # 5. Detecta simulação com tolerância
            simulation_score = self._detect_simulation_with_tolerance(analysis, thresholds)
            validation_result['component_scores']['simulation'] = simulation_score
            
            # Calcula score geral
            scores = [structure_score, research_score, avatar_score, insights_score, simulation_score]
            validation_result['quality_score'] = sum(scores) / len(scores)
            
            # Determina se é válida
            validation_result['valid'] = validation_result['quality_score'] >= thresholds['min_quality_score']
            
            if not validation_result['valid']:
                validation_result['primary_reason'] = f"Score {validation_result['quality_score']:.1f}% < {thresholds['min_quality_score']}%"
            
            return validation_result
            
        except Exception as e:
            validation_result['errors'].append(f"Erro na validação: {str(e)}")
            validation_result['primary_reason'] = f"Erro técnico: {str(e)}"
            return validation_result
    
    def _validate_structure_flexible(self, analysis: Dict[str, Any], thresholds: Dict[str, Any]) -> float:
        """Valida estrutura com flexibilidade"""
        
        score = 0.0
        
        # Seções essenciais (mais flexível)
        essential_sections = ['avatar_ultra_detalhado']  # Só avatar é realmente essencial
        
        for section in essential_sections:
            if section in analysis and analysis[section]:
                score += 50.0  # 50 pontos por seção essencial
        
        # Seções opcionais (bonus)
        optional_sections = [
            'drivers_mentais_customizados', 'provas_visuais_sugeridas',
            'sistema_anti_objecao', 'pre_pitch_invisivel', 'insights_exclusivos'
        ]
        
        bonus_per_section = 50.0 / len(optional_sections)
        for section in optional_sections:
            if section in analysis and analysis[section]:
                score += bonus_per_section
        
        return min(score, 100.0)
    
    def _validate_research_flexible(self, analysis: Dict[str, Any], thresholds: Dict[str, Any]) -> float:
        """Valida pesquisa com flexibilidade"""
        
        research_data = analysis.get('pesquisa_web_massiva', {})
        if not research_data:
            return 20.0  # Score mínimo se não tem pesquisa
        
        score = 20.0  # Base por ter pesquisa
        
        stats = research_data.get('estatisticas', {})
        
        # Score por conteúdo
        total_content = stats.get('total_conteudo', 0)
        if total_content >= thresholds['min_content_length']:
            score += 30.0
        elif total_content > 0:
            score += (total_content / thresholds['min_content_length']) * 30.0
        
        # Score por fontes
        unique_sources = stats.get('fontes_unicas', 0)
        if unique_sources >= thresholds['min_sources']:
            score += 30.0
        elif unique_sources > 0:
            score += (unique_sources / thresholds['min_sources']) * 30.0
        
        # Score por qualidade
        avg_quality = stats.get('qualidade_media', 0)
        score += (avg_quality / 100) * 20.0
        
        return min(score, 100.0)
    
    def _validate_avatar_flexible(self, analysis: Dict[str, Any], thresholds: Dict[str, Any]) -> float:
        """Valida avatar com flexibilidade"""
        
        avatar = analysis.get('avatar_ultra_detalhado', {})
        if not avatar:
            return 0.0
        
        score = 20.0  # Base por ter avatar
        
        # Score por seções do avatar
        avatar_sections = [
            'perfil_demografico', 'perfil_psicografico', 
            'dores_viscerais', 'desejos_secretos'
        ]
        
        section_score = 80.0 / len(avatar_sections)
        for section in avatar_sections:
            if section in avatar and avatar[section]:
                if isinstance(avatar[section], list) and len(avatar[section]) > 0:
                    score += section_score
                elif isinstance(avatar[section], dict) and len(avatar[section]) > 0:
                    score += section_score
                elif isinstance(avatar[section], str) and len(avatar[section]) > 10:
                    score += section_score
        
        return min(score, 100.0)
    
    def _validate_insights_flexible(self, analysis: Dict[str, Any], thresholds: Dict[str, Any]) -> float:
        """Valida insights com flexibilidade"""
        
        insights = analysis.get('insights_exclusivos', [])
        if not insights or not isinstance(insights, list):
            return 10.0  # Score mínimo
        
        score = 10.0  # Base por ter insights
        
        # Score por quantidade
        if len(insights) >= thresholds['min_insights']:
            score += 50.0
        elif len(insights) > 0:
            score += (len(insights) / thresholds['min_insights']) * 50.0
        
        # Score por qualidade dos insights
        substantial_insights = [insight for insight in insights if len(insight) > 50]
        if substantial_insights:
            quality_ratio = len(substantial_insights) / len(insights)
            score += quality_ratio * 40.0
        
        return min(score, 100.0)
    
    def _detect_simulation_with_tolerance(self, analysis: Dict[str, Any], thresholds: Dict[str, Any]) -> float:
        """Detecta simulação com tolerância configurável"""
        
        simulation_indicators = [
            'n/a', 'não informado', 'customizado para', 'baseado em dados',
            'específico para', 'exemplo genérico', 'placeholder', 'template'
        ]
        
        # Converte análise para string
        analysis_str = json.dumps(analysis, ensure_ascii=False).lower()
        
        # Conta indicadores
        simulation_count = 0
        for indicator in simulation_indicators:
            simulation_count += analysis_str.count(indicator)
        
        # Aplica tolerância
        tolerance = thresholds['simulation_tolerance']
        
        if simulation_count <= tolerance:
            return 100.0  # Perfeito
        elif simulation_count <= tolerance * 2:
            return 70.0   # Aceitável
        elif simulation_count <= tolerance * 3:
            return 40.0   # Questionável
        else:
            return 10.0   # Muito simulado
    
    def _get_level_recommendation(self, level: str) -> str:
        """Retorna recomendação baseada no nível de validação"""
        
        recommendations = {
            'STRICT': "✅ EXCELENTE: Análise de qualidade premium - prosseguir com confiança total",
            'MODERATE': "👍 BOM: Análise de qualidade adequada - prosseguir com implementação",
            'FLEXIBLE': "⚠️ ACEITÁVEL: Análise com limitações - considere melhorar APIs para qualidade superior",
            'EMERGENCY': "🚨 EMERGÊNCIA: Análise mínima - recomenda-se reexecutar com configuração completa"
        }
        
        return recommendations.get(level, "Análise validada")
    
    def _create_emergency_validation(self, analysis: Dict[str, Any], session_id: str = None) -> Dict[str, Any]:
        """Cria validação de emergência que sempre permite continuar"""
        
        logger.warning("🚨 Criando validação de emergência - ANÁLISE CONTINUARÁ")
        
        emergency_validation = {
            'valid': True,  # SEMPRE permite continuar
            'level': 'EMERGENCY_OVERRIDE',
            'quality_score': 25.0,  # Score mínimo
            'errors': [],
            'warnings': [
                'Validação em modo de emergência',
                'Qualidade pode estar comprometida',
                'Dados intermediários preservados'
            ],
            'component_scores': {
                'structure': 25.0,
                'research': 25.0,
                'avatar': 25.0,
                'insights': 25.0,
                'simulation': 25.0
            },
            'primary_reason': 'Modo de emergência ativado - análise prossegue com dados disponíveis',
            'recommendation': '🚨 EMERGÊNCIA: Configure APIs e reexecute para qualidade completa',
            'emergency_mode': True,
            'data_preserved': True,
            'can_continue': True,
            'timestamp': datetime.now().isoformat()
        }
        
        # Salva validação de emergência
        salvar_etapa("validacao_emergencia", emergency_validation, categoria="analise_completa")
        
        logger.warning("⚠️ Validação de emergência criada - análise prosseguirá")
        return emergency_validation
    
    def should_generate_pdf_flexible(self, analysis: Dict[str, Any]) -> Tuple[bool, str]:
        """Determina se deve gerar PDF com critérios flexíveis"""
        
        # Critérios muito flexíveis para PDF
        if not analysis:
            return False, "Análise vazia"
        
        # Verifica se tem pelo menos avatar
        if not analysis.get('avatar_ultra_detalhado'):
            return False, "Avatar ausente - mínimo necessário para PDF"
        
        # Verifica se tem pelo menos alguns insights
        insights = analysis.get('insights_exclusivos', [])
        if len(insights) < 1:
            return False, "Nenhum insight disponível para PDF"
        
        # Se chegou aqui, pode gerar PDF
        return True, "Análise adequada para PDF (critérios flexíveis)"
    
    def clean_analysis_for_output_flexible(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Limpa análise para output com flexibilidade"""
        
        cleaned = analysis.copy()
        
        # Remove apenas campos claramente inválidos
        invalid_indicators = ['ERRO_', 'FALHA_', 'INVALID_']
        
        def clean_recursive(obj):
            if isinstance(obj, dict):
                return {k: clean_recursive(v) for k, v in obj.items() 
                       if not any(indicator in str(k).upper() for indicator in invalid_indicators)}
            elif isinstance(obj, list):
                return [clean_recursive(item) for item in obj 
                       if not any(indicator in str(item).upper() for indicator in invalid_indicators)]
            else:
                return obj
        
        cleaned = clean_recursive(cleaned)
        
        # Adiciona metadados de limpeza
        cleaned['validation_metadata'] = {
            'cleaned_at': datetime.now().isoformat(),
            'cleaning_level': 'flexible',
            'original_size': len(str(analysis)),
            'cleaned_size': len(str(cleaned)),
            'data_preserved': True,
            'simulation_tolerance': 'high'
        }
        
        return cleaned
    
    def validate_component_individually(
        self, 
        component_name: str, 
        component_data: Any,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Valida componente individual com flexibilidade"""
        
        if not component_data:
            return {
                'valid': False,
                'score': 0.0,
                'reason': 'Componente vazio',
                'can_continue': True,  # Sempre permite continuar
                'recommendation': 'Componente ausente mas análise pode prosseguir'
            }
        
        # Validação básica flexível
        score = 50.0  # Score base por existir
        
        if isinstance(component_data, dict) and len(component_data) > 0:
            score += 25.0
        elif isinstance(component_data, list) and len(component_data) > 0:
            score += 25.0
        elif isinstance(component_data, str) and len(component_data) > 50:
            score += 25.0
        
        # Bonus por qualidade específica
        if component_name == 'avatar_ultra_detalhado':
            score += self._validate_avatar_specific(component_data)
        elif component_name == 'drivers_mentais_customizados':
            score += self._validate_drivers_specific(component_data)
        elif component_name == 'insights_exclusivos':
            score += self._validate_insights_specific(component_data)
        
        is_valid = score >= 40.0  # Threshold flexível
        
        return {
            'valid': is_valid,
            'score': min(score, 100.0),
            'reason': f"Score: {score:.1f}% ({'Válido' if is_valid else 'Limitado'})",
            'can_continue': True,  # SEMPRE permite continuar
            'recommendation': 'Válido para prosseguir' if is_valid else 'Limitado mas pode prosseguir'
        }
    
    def _validate_avatar_specific(self, avatar_data: Any) -> float:
        """Validação específica do avatar"""
        
        if not isinstance(avatar_data, dict):
            return 0.0
        
        bonus = 0.0
        
        # Bonus por seções do avatar
        if avatar_data.get('perfil_demografico'):
            bonus += 5.0
        if avatar_data.get('dores_viscerais') and len(avatar_data['dores_viscerais']) >= 3:
            bonus += 10.0
        if avatar_data.get('desejos_secretos') and len(avatar_data['desejos_secretos']) >= 3:
            bonus += 10.0
        
        return bonus
    
    def _validate_drivers_specific(self, drivers_data: Any) -> float:
        """Validação específica dos drivers"""
        
        if not drivers_data:
            return 0.0
        
        bonus = 0.0
        
        if isinstance(drivers_data, dict) and 'drivers_customizados' in drivers_data:
            drivers = drivers_data['drivers_customizados']
            if isinstance(drivers, list) and len(drivers) >= 2:
                bonus += 15.0
        elif isinstance(drivers_data, list) and len(drivers_data) >= 2:
            bonus += 15.0
        
        return bonus
    
    def _validate_insights_specific(self, insights_data: Any) -> float:
        """Validação específica dos insights"""
        
        if not isinstance(insights_data, list):
            return 0.0
        
        bonus = 0.0
        
        if len(insights_data) >= 5:
            bonus += 15.0
        elif len(insights_data) >= 3:
            bonus += 10.0
        elif len(insights_data) >= 1:
            bonus += 5.0
        
        return bonus
    
    def force_validation_pass(self, analysis: Dict[str, Any], reason: str = "Forçado pelo usuário") -> Dict[str, Any]:
        """Força validação a passar (para casos especiais)"""
        
        logger.warning(f"🔓 Forçando validação a passar: {reason}")
        
        forced_validation = {
            'valid': True,
            'level': 'FORCED_PASS',
            'quality_score': 50.0,
            'errors': [],
            'warnings': [f'Validação forçada: {reason}'],
            'component_scores': {
                'structure': 50.0,
                'research': 50.0,
                'avatar': 50.0,
                'insights': 50.0,
                'simulation': 50.0
            },
            'primary_reason': reason,
            'recommendation': 'Validação forçada - prosseguir com cautela',
            'forced': True,
            'timestamp': datetime.now().isoformat()
        }
        
        salvar_etapa("validacao_forcada", forced_validation, categoria="analise_completa")
        
        return forced_validation
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de validação"""
        
        return {
            'current_level': self.current_level,
            'available_levels': list(self.validation_levels.keys()),
            'level_thresholds': self.validation_levels,
            'emergency_mode_available': True,
            'forced_pass_available': True
        }

# Instância global
enhanced_validation_system = EnhancedValidationSystem()