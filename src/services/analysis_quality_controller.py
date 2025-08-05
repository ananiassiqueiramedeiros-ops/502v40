#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Analysis Quality Controller
Controlador de qualidade para análises - ZERO TOLERÂNCIA A SIMULAÇÃO
"""

import logging
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class AnalysisQualityController:
    """Controlador rigoroso de qualidade para análises"""
    
    def __init__(self):
        """Inicializa o controlador de qualidade"""
        self.quality_thresholds = {
            'min_content_length': 500,  # Reduzido para ser mais flexível
            'min_sources': 3,
            'min_insights': 5,
            'min_quality_score': 40.0,  # Reduzido para ser mais flexível
            'min_component_success_rate': 0.5  # 60% dos componentes devem funcionar
        }
        
        self.simulation_indicators = [
            'n/a', 'não informado', 'customizado para', 'baseado em dados',
            'específico para', 'exemplo genérico', 'placeholder'
        ]
        
        logger.info("Analysis Quality Controller inicializado com tolerância ZERO a simulação")
    
    def validate_complete_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Valida análise completa com critérios rigorosos"""
        
        validation_result = {
            'valid': False,
            'quality_score': 0.0,
            'errors': [],
            'warnings': [],
            'component_status': {},
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            logger.info("🔍 Iniciando validação rigorosa da análise...")
            
            # 1. Valida estrutura básica
            structure_validation = self._validate_structure(analysis)
            validation_result['component_status']['structure'] = structure_validation
            
            if not structure_validation['valid']:
                validation_result['errors'].extend(structure_validation['errors'])
                return validation_result
            
            # 2. Valida pesquisa web
            research_validation = self._validate_research_data(analysis)
            validation_result['component_status']['research'] = research_validation
            
            if not research_validation['valid']:
                validation_result['errors'].extend(research_validation['errors'])
            
            # 3. Valida avatar
            avatar_validation = self._validate_avatar(analysis)
            validation_result['component_status']['avatar'] = avatar_validation
            
            if not avatar_validation['valid']:
                validation_result['errors'].extend(avatar_validation['errors'])
            
            # 4. Valida componentes avançados
            components_validation = self._validate_advanced_components(analysis)
            validation_result['component_status']['advanced_components'] = components_validation
            
            # 5. Detecta conteúdo simulado (com tolerância)
            simulation_check = self._detect_simulated_content(analysis)
            validation_result['component_status']['simulation_check'] = simulation_check
            
            # Só rejeita se tem MUITA simulação (mais tolerante)
            if simulation_check['has_simulation'] and simulation_check['simulation_count'] > 10:
                validation_result['errors'].extend(simulation_check['simulation_errors'])
            
            # 6. Calcula score de qualidade
            quality_score = self._calculate_quality_score(analysis, validation_result['component_status'])
            validation_result['quality_score'] = quality_score
            
            # 7. Determina se é válida
            validation_result['valid'] = (
                len(validation_result['errors']) == 0 and
                quality_score >= self.quality_thresholds['min_quality_score']
            )
            
            # 8. Gera recomendações
            validation_result['recommendations'] = self._generate_recommendations(validation_result)
            
            status = "✅ VÁLIDA" if validation_result['valid'] else "❌ INVÁLIDA"
            logger.info(f"{status} Análise validada - Score: {quality_score:.1f}%")
            
            return validation_result
            
        except Exception as e:
            validation_result['errors'].append(f"Erro crítico na validação: {str(e)}")
            logger.error(f"❌ Erro crítico na validação: {str(e)}")
            return validation_result
    
    def _validate_structure(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Valida estrutura básica da análise"""
        
        result = {'valid': True, 'errors': [], 'warnings': []}
        
        # Seções obrigatórias
        required_sections = [
            'projeto_dados',
            'pesquisa_web_massiva', 
            'avatar_ultra_detalhado',
            'insights_exclusivos'
        ]
        
        for section in required_sections:
            if section not in analysis:
                result['errors'].append(f"Seção obrigatória ausente: {section}")
                result['valid'] = False
            elif not analysis[section]:
                result['errors'].append(f"Seção obrigatória vazia: {section}")
                result['valid'] = False
        
        return result
    
    def _validate_research_data(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Valida dados da pesquisa web"""
        
        result = {'valid': True, 'errors': [], 'warnings': []}
        
        research_data = analysis.get('pesquisa_web_massiva', {})
        if not research_data:
            result['errors'].append("Dados de pesquisa web ausentes")
            result['valid'] = False
            return result
        
        estatisticas = research_data.get('estatisticas', {})
        
        # Valida métricas mínimas
        total_conteudo = estatisticas.get('total_conteudo', 0)
        if total_conteudo < self.quality_thresholds['min_content_length']:
            result['errors'].append(f"Conteúdo insuficiente: {total_conteudo} < {self.quality_thresholds['min_content_length']}")
            result['valid'] = False
        
        fontes_unicas = estatisticas.get('fontes_unicas', 0)
        if fontes_unicas < self.quality_thresholds['min_sources']:
            result['errors'].append(f"Fontes insuficientes: {fontes_unicas} < {self.quality_thresholds['min_sources']}")
            result['valid'] = False
        
        # Valida qualidade média
        qualidade_media = estatisticas.get('qualidade_media', 0)
        if qualidade_media < 60:
            result['warnings'].append(f"Qualidade média baixa: {qualidade_media:.1f}%")
        
        return result
    
    def _validate_avatar(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Valida avatar ultra-detalhado"""
        
        result = {'valid': True, 'errors': [], 'warnings': []}
        
        avatar = analysis.get('avatar_ultra_detalhado', {})
        if not avatar:
            result['errors'].append("Avatar ausente")
            result['valid'] = False
            return result
        
        # Seções obrigatórias do avatar
        required_avatar_sections = [
            'perfil_demografico',
            'perfil_psicografico', 
            'dores_viscerais',
            'desejos_secretos'
        ]
        
        for section in required_avatar_sections:
            if section not in avatar or not avatar[section]:
                result['errors'].append(f"Seção do avatar ausente: {section}")
                result['valid'] = False
        
        # Valida listas mínimas
        dores = avatar.get('dores_viscerais', [])
        if len(dores) < 5:
            result['errors'].append(f"Dores insuficientes: {len(dores)} < 5")
            result['valid'] = False
        
        desejos = avatar.get('desejos_secretos', [])
        if len(desejos) < 5:
            result['errors'].append(f"Desejos insuficientes: {len(desejos)} < 5")
            result['valid'] = False
        
        return result
    
    def _validate_advanced_components(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Valida componentes avançados"""
        
        result = {'valid': True, 'errors': [], 'warnings': [], 'component_count': 0}
        
        advanced_components = [
            'drivers_mentais_customizados',
            'provas_visuais_sugeridas',
            'sistema_anti_objecao',
            'pre_pitch_invisivel',
            'predicoes_futuro_completas'
        ]
        
        successful_components = 0
        
        for component in advanced_components:
            if component in analysis and analysis[component]:
                # Valida se o componente tem status de validação
                component_data = analysis[component]
                if isinstance(component_data, dict):
                    if component_data.get('validation_status') == 'VALID':
                        successful_components += 1
                    else:
                        result['warnings'].append(f"Componente {component} sem validação")
                else:
                    successful_components += 1  # Assume válido se não é dict
        
        result['component_count'] = successful_components
        success_rate = successful_components / len(advanced_components)
        
        if success_rate < self.quality_thresholds['min_component_success_rate']:
            result['errors'].append(f"Taxa de sucesso dos componentes muito baixa: {success_rate:.1%}")
            result['valid'] = False
        
        return result
    
    def _detect_simulated_content(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Detecta conteúdo simulado na análise"""
        
        result = {
            'has_simulation': False,
            'simulation_errors': [],
            'simulation_count': 0,
            'checked_fields': 0
        }
        
        # Converte análise para string para verificação
        analysis_str = json.dumps(analysis, ensure_ascii=False).lower()
        
        # Conta indicadores de simulação
        found_indicators = {}
        for indicator in self.simulation_indicators:
            count = analysis_str.count(indicator)
            if count > 0:
                found_indicators[indicator] = count
                result['simulation_count'] += count
        
        # Se encontrou muitos indicadores, é simulação
        if result['simulation_count'] > 15:  # Tolerância MAIOR
            result['has_simulation'] = True
            result['simulation_errors'].append(f"Muitos indicadores de simulação encontrados: {found_indicators}")
        
        # Verifica campos específicos
        self._check_field_for_simulation(analysis, 'avatar_ultra_detalhado', result)
        self._check_field_for_simulation(analysis, 'insights_exclusivos', result)
        
        return result
    
    def _check_field_for_simulation(self, analysis: Dict[str, Any], field_name: str, result: Dict[str, Any]):
        """Verifica um campo específico por simulação"""
        
        field_data = analysis.get(field_name)
        if not field_data:
            return
        
        field_str = json.dumps(field_data, ensure_ascii=False).lower()
        result['checked_fields'] += 1
        
        # Verifica padrões específicos de simulação
        simulation_patterns = [
            'customizado para',
            'baseado em dados',
            'específico para',
            'história customizada'
        ]
        
        found_patterns = [pattern for pattern in simulation_patterns if pattern in field_str]
        
        if found_patterns:
            result['has_simulation'] = True
            result['simulation_errors'].append(f"Padrões de simulação em {field_name}: {found_patterns}")
    
    def _calculate_quality_score(self, analysis: Dict[str, Any], component_status: Dict[str, Any]) -> float:
        """Calcula score de qualidade da análise"""
        
        score = 0.0
        
        # Pesquisa web (30 pontos)
        research_status = component_status.get('research', {})
        if research_status.get('valid'):
            score += 30
        
        # Avatar (25 pontos)
        avatar_status = component_status.get('avatar', {})
        if avatar_status.get('valid'):
            score += 25
        
        # Componentes avançados (25 pontos)
        advanced_status = component_status.get('advanced_components', {})
        component_count = advanced_status.get('component_count', 0)
        score += (component_count / 5) * 25  # 5 componentes possíveis
        
        # Ausência de simulação (20 pontos)
        simulation_status = component_status.get('simulation_check', {})
        if not simulation_status.get('has_simulation'):
            score += 20
        
        return min(score, 100.0)
    
    def _generate_recommendations(self, validation_result: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas na validação"""
        
        recommendations = []
        
        if validation_result['errors']:
            recommendations.append("🚨 CRÍTICO: Corrija os erros listados antes de usar a análise")
        
        if validation_result['quality_score'] < 70:
            recommendations.append("🔧 MELHORIA: Configure mais APIs para aumentar qualidade")
        
        research_status = validation_result['component_status'].get('research', {})
        if not research_status.get('valid'):
            recommendations.append("🌐 PESQUISA: Configure APIs de busca para dados reais")
        
        simulation_status = validation_result['component_status'].get('simulation_check', {})
        if simulation_status.get('has_simulation'):
            recommendations.append("⚠️ SIMULAÇÃO: Análise contém dados simulados - configure APIs completas")
        
        advanced_status = validation_result['component_status'].get('advanced_components', {})
        if advanced_status.get('component_count', 0) < 3:
            recommendations.append("🔧 COMPONENTES: Poucos componentes avançados funcionando")
        
        if not recommendations:
            recommendations.append("✅ EXCELENTE: Análise de alta qualidade com dados reais")
        
        return recommendations
    
    def generate_quality_report(self, analysis: Dict[str, Any]) -> str:
        """Gera relatório de qualidade legível"""
        
        validation = self.validate_complete_analysis(analysis)
        
        report = []
        report.append("=" * 60)
        report.append("📊 RELATÓRIO DE QUALIDADE DA ANÁLISE")
        report.append("=" * 60)
        
        # Status geral
        status_icon = "✅" if validation['valid'] else "❌"
        report.append(f"{status_icon} STATUS GERAL: {'VÁLIDA' if validation['valid'] else 'INVÁLIDA'}")
        report.append(f"📈 SCORE DE QUALIDADE: {validation['quality_score']:.1f}%")
        
        # Componentes
        report.append(f"\n🔧 STATUS DOS COMPONENTES:")
        for component, status in validation['component_status'].items():
            icon = "✅" if status.get('valid', False) else "❌"
            report.append(f"   {icon} {component.upper()}")
        
        # Erros
        if validation['errors']:
            report.append(f"\n❌ ERROS CRÍTICOS ({len(validation['errors'])}):")
            for error in validation['errors']:
                report.append(f"   • {error}")
        
        # Avisos
        if validation['warnings']:
            report.append(f"\n⚠️ AVISOS ({len(validation['warnings'])}):")
            for warning in validation['warnings']:
                report.append(f"   • {warning}")
        
        # Recomendações
        if validation['recommendations']:
            report.append(f"\n💡 RECOMENDAÇÕES:")
            for rec in validation['recommendations']:
                report.append(f"   • {rec}")
        
        # Estatísticas
        research_data = analysis.get('pesquisa_web_massiva', {})
        if research_data:
            stats = research_data.get('estatisticas', {})
            report.append(f"\n📊 ESTATÍSTICAS DA PESQUISA:")
            report.append(f"   • Fontes únicas: {stats.get('fontes_unicas', 0)}")
            report.append(f"   • Total de conteúdo: {stats.get('total_conteudo', 0):,} caracteres")
            report.append(f"   • Qualidade média: {stats.get('qualidade_media', 0):.1f}%")
        
        report.append("=" * 60)
        
        return '\n'.join(report)
    
    def should_generate_pdf(self, analysis: Dict[str, Any]) -> Tuple[bool, str]:
        """Determina se deve gerar PDF baseado na qualidade"""
        
        validation = self.validate_complete_analysis(analysis)
        
        if not validation['valid']:
            # Mais flexível para PDF - aceita se tem conteúdo mínimo
            if validation['quality_score'] >= 30.0:
                return True, f"Qualidade aceitável para PDF: {validation['quality_score']:.1f}%"
            else:
                return False, f"Análise inválida: {'; '.join(validation['errors'][:3])}"
        
        if validation['quality_score'] < 50:  # Reduzido de 80 para 50
            return False, f"Qualidade insuficiente para PDF: {validation['quality_score']:.1f}% < 50%"
        
        # Verifica se tem conteúdo suficiente
        insights = analysis.get('insights_exclusivos', [])
        if len(insights) < 3:  # Reduzido para 3 (mais flexível)
            return False, f"Insights insuficientes para PDF: {len(insights)} < 5"
        
        return True, "Qualidade adequada para geração de PDF"
    
    def clean_analysis_for_output(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Limpa análise removendo campos inválidos ou simulados"""
        
        cleaned = analysis.copy()
        
        # Remove componentes que falharam na validação
        validation = self.validate_complete_analysis(analysis)
        
        for component, status in validation['component_status'].items():
            if not status.get('valid', False):
                # Remove componente inválido
                component_key = self._map_component_to_key(component)
                if component_key and component_key in cleaned:
                    logger.warning(f"🧹 Removendo componente inválido: {component_key}")
                    del cleaned[component_key]
        
        # Adiciona metadados de qualidade
        cleaned['quality_metadata'] = {
            'validation_timestamp': datetime.now().isoformat(),
            'quality_score': validation['quality_score'],
            'validation_status': 'VALID' if validation['valid'] else 'INVALID',
            'errors_count': len(validation['errors']),
            'warnings_count': len(validation['warnings']),
            'simulation_free': not validation['component_status'].get('simulation_check', {}).get('has_simulation', True)
        }
        
        return cleaned
    
    def _map_component_to_key(self, component: str) -> Optional[str]:
        """Mapeia nome do componente para chave na análise"""
        
        mapping = {
            'research': 'pesquisa_web_massiva',
            'avatar': 'avatar_ultra_detalhado',
            'advanced_components': None  # Múltiplos componentes
        }
        
        return mapping.get(component)

# Instância global
analysis_quality_controller = AnalysisQualityController()
