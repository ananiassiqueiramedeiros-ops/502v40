#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Aplicação Principal
Servidor Flask para análise de mercado ultra-detalhada
"""

import os
import sys
import logging
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def create_app():
    """Cria e configura a aplicação Flask"""
    
    # Carrega variáveis de ambiente
    from services.environment_loader import environment_loader
    
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuração CORS
    CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))
    
    # Registra blueprints
    from routes.analysis import analysis_bp
    from routes.enhanced_analysis import enhanced_analysis_bp
    from routes.progress import progress_bp
    from routes.user import user_bp
    from routes.files import files_bp
    from routes.pdf_generator import pdf_bp
    from routes.monitoring import monitoring_bp
    
    app.register_blueprint(analysis_bp, url_prefix='/api')
    app.register_blueprint(enhanced_analysis_bp, url_prefix='/api')
    app.register_blueprint(progress_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(files_bp, url_prefix='/api')
    app.register_blueprint(pdf_bp, url_prefix='/api')
    app.register_blueprint(monitoring_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        """Página principal"""
        return render_template('enhanced_index.html')
    
    @app.route('/archaeological')
    def archaeological():
        """Interface arqueológica"""
        return render_template('enhanced_interface.html')
    
    @app.route('/api/app_status')
    def app_status():
        """Status da aplicação"""
        try:
            from services.ai_manager import ai_manager
            from services.production_search_manager import production_search_manager
            from database import db_manager
            
            ai_status = ai_manager.get_provider_status()
            search_status = production_search_manager.get_provider_status()
            db_status = db_manager.test_connection()
            
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '2.0.0',
                'services': {
                    'ai_providers': {
                        'available': len([p for p in ai_status.values() if p['available']]),
                        'total': len(ai_status),
                        'providers': ai_status
                    },
                    'search_providers': {
                        'available': len([p for p in search_status.values() if p['available']]),
                        'total': len(search_status),
                        'providers': search_status
                    },
                    'database': {
                        'connected': db_status
                    }
                }
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint não encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Erro interno do servidor'}), 500
    
    return app

def main():
    """Função principal"""
    
    print("🚀 ARQV30 Enhanced v2.0 - Iniciando aplicação...")
    
    try:
        # Cria aplicação
        app = create_app()
        
        # Configurações do servidor
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_ENV', 'production') == 'development'
        
        print(f"🌐 Servidor: http://{host}:{port}")
        print(f"🔧 Modo: {'Desenvolvimento' if debug else 'Produção'}")
        print(f"📊 Interface: Análise Ultra-Detalhada de Mercado")
        print(f"🤖 IA: Gemini 2.5 Pro + Groq + Fallbacks")
        print(f"🔍 Pesquisa: WebSailor + Google + Múltiplos Engines")
        print(f"💾 Banco: Supabase + Arquivos Locais")
        print(f"🛡️ Sistema: Ultra-Robusto com Salvamento Automático")
        
        print("\n" + "=" * 60)
        print("✅ ARQV30 Enhanced v2.0 PRONTO!")
        print("=" * 60)
        print("Pressione Ctrl+C para parar o servidor")
        print("=" * 60)
        
        # Inicia servidor
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n✅ Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

    
    try:
        data = request.get_json() or {}
        provider_type = data.get('type')  # 'ai' ou 'search'
        provider_name = data.get('provider')  # nome específico do provedor
        
        if provider_type == 'ai':
            ai_manager.reset_provider_errors(provider_name)
            message = f"Reset erros do provedor de IA: {provider_name}" if provider_name else "Reset erros de todos os provedores de IA"
        elif provider_type == 'search':
            production_search_manager.reset_provider_errors(provider_name)
            message = f"Reset erros do provedor de busca: {provider_name}" if provider_name else "Reset erros de todos os provedores de busca"
        else:
            # Reset todos
            ai_manager.reset_provider_errors()
            production_search_manager.reset_provider_errors()
            message = "Reset erros de todos os provedores"
        
        logger.info(f"🔄 {message}")
        
        return jsonify({
            'success': True,
            'message': message,
            'ai_status': ai_manager.get_provider_status(),
            'search_status': production_search_manager.get_provider_status(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao resetar provedores: {str(e)}")
        return jsonify({
            'error': 'Erro ao resetar provedores',
            'message': str(e)
        }), 500

@analysis_bp.route('/test_search', methods=['POST'])
def test_search():
    """Testa sistema de busca"""
    
    try:
        data = request.get_json()
        query = data.get('query', 'teste mercado digital Brasil')
        max_results = min(int(data.get('max_results', 5)), 10)
        
        logger.info(f"🧪 Testando busca: {query}")
        
        # Testa busca
        results = production_search_manager.search_with_fallback(query, max_results)
        
        return jsonify({
            'success': True,
            'query': query,
            'results_count': len(results),
            'results': results,
            'provider_status': production_search_manager.get_provider_status(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro no teste de busca: {str(e)}")
        return jsonify({
            'error': 'Erro no teste de busca',
            'message': str(e)
        }), 500

@analysis_bp.route('/test_extraction', methods=['POST'])
def test_extraction():
    """Testa sistema de extração de conteúdo"""
    
    try:
        data = request.get_json()
        test_url = data.get('url', 'https://g1.globo.com/tecnologia/')
        
        logger.info(f"🧪 Testando extração: {test_url}")
        
        # Testa extração segura
        extraction_result = safe_content_extractor.safe_extract_content(test_url)
        
        if extraction_result['success']:
            return jsonify({
                'success': True,
                'url': test_url,
                'content_length': extraction_result['metadata']['content_length'],
                'content_preview': extraction_result['content'][:500] + '...' if len(extraction_result['content']) > 500 else extraction_result['content'],
                'validation': extraction_result['validation'],
                'metadata': extraction_result['metadata'],
                'extractor_stats': safe_content_extractor.get_extraction_stats(),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'url': test_url,
                'error': extraction_result['error'],
                'metadata': extraction_result['metadata'],
                'extractor_stats': safe_content_extractor.get_extraction_stats(),
                'timestamp': datetime.now().isoformat()
            })
        
    except Exception as e:
        logger.error(f"Erro no teste de extração: {str(e)}")
        return jsonify({
            'error': 'Erro no teste de extração',
            'message': str(e)
        }), 500

@analysis_bp.route('/extractor_stats', methods=['GET'])
def get_extractor_stats():
    """Obtém estatísticas dos extratores"""
    
    try:
        stats = safe_content_extractor.get_extraction_stats()
        
        return jsonify({
            'success': True,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter estatísticas dos extratores',
            'message': str(e)
        }), 500

@analysis_bp.route('/reset_extractors', methods=['POST'])
def reset_extractors():
    """Reset estatísticas dos extratores"""
    
    try:
        data = request.get_json() or {}
        extractor_name = data.get('extractor')
        
        # Reset através do extrator robusto
        from services.robust_content_extractor import robust_content_extractor
        robust_content_extractor.reset_extractor_stats(extractor_name)
        
        message = f"Reset estatísticas do extrator: {extractor_name}" if extractor_name else "Reset estatísticas de todos os extratores"
        
        return jsonify({
            'success': True,
            'message': message,
            'stats': safe_content_extractor.get_extraction_stats(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao resetar extratores: {str(e)}")
        return jsonify({
            'error': 'Erro ao resetar extratores',
            'message': str(e)
        }), 500

@analysis_bp.route('/validate_analysis', methods=['POST'])
def validate_analysis():
    """Valida qualidade de uma análise"""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Dados da análise não fornecidos'
            }), 400
        
        # Valida análise
        validation_result = analysis_quality_controller.validate_complete_analysis(data)
        
        # Gera relatório
        quality_report = analysis_quality_controller.generate_quality_report(data)
        
        return jsonify({
            'validation': validation_result,
            'quality_report': quality_report,
            'can_generate_pdf': analysis_quality_controller.should_generate_pdf(data),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro na validação: {str(e)}")
        return jsonify({
            'error': 'Erro na validação da análise',
            'message': str(e)
        }), 500

@analysis_bp.route('/analyze_simple', methods=['POST'])
def analyze_simple():
    """Endpoint alternativo mais simples para análise"""
    
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['segmento', 'produto', 'publico']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos obrigatórios: {", ".join(missing_fields)}'
            }), 400
        
        logger.info(f"🚀 Iniciando análise: {data.get('segmento')} - {data.get('produto')}")
        
        # Usar o engine de análise existente
        from services.enhanced_analysis_engine import enhanced_analysis_engine
        
        # Gerar análise completa
        analysis_result = enhanced_analysis_engine.generate_complete_analysis(data)
        
        if not analysis_result:
            return jsonify({
                'success': False,
                'error': 'Falha na geração da análise'
            }), 500
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@analysis_bp.route('/test_ai', methods=['POST'])
def test_ai():
    """Testa sistema de IA"""
    
    try:
        data = request.get_json()
        prompt = data.get('prompt', 'Gere um breve resumo sobre o mercado digital brasileiro em 2024.')
        
        logger.info("🧪 Testando sistema de IA...")
        
        # Testa IA
        response = ai_manager.generate_analysis(prompt, max_tokens=500)
        
        return jsonify({
            'success': bool(response),
            'prompt': prompt,
            'response': response,
            'response_length': len(response) if response else 0,
            'provider_status': ai_manager.get_provider_status(),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro no teste de IA: {str(e)}")
        return jsonify({
            'error': 'Erro no teste de IA',
            'message': str(e)
        }), 500

@analysis_bp.route('/upload_attachment', methods=['POST'])
def upload_attachment():
    """Upload e processamento de anexos"""
    
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nenhum arquivo enviado'
            }), 400
        
        file = request.files['file']
        session_id = request.form.get('session_id', f"session_{int(time.time())}")
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nome de arquivo vazio'
            }), 400
        
        # Processa anexo
        result = attachment_service.process_attachment(file, session_id)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erro no upload de anexo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno no processamento do anexo',
            'message': str(e)
        }), 500

@analysis_bp.route('/list_analyses', methods=['GET'])
def list_analyses():
    """Lista análises salvas"""
    
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        
        analyses = db_manager.list_analyses(limit, offset)
        
        return jsonify({
            'success': True,
            'analyses': analyses,
            'count': len(analyses),
            'limit': limit,
            'offset': offset,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar análises: {str(e)}")
        return jsonify({
            'error': 'Erro ao listar análises',
            'message': str(e)
        }), 500

@analysis_bp.route('/get_analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Obtém análise específica"""
    
    try:
        analysis = db_manager.get_analysis(analysis_id)
        
        if analysis:
            return jsonify({
                'success': True,
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Análise não encontrada'
            }), 404
            
    except Exception as e:
        logger.error(f"Erro ao obter análise {analysis_id}: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter análise',
            'message': str(e)
        }), 500

@analysis_bp.route('/stats', methods=['GET'])
def get_stats():
    """Obtém estatísticas do sistema"""
    
    try:
        db_stats = db_manager.get_stats()
        ai_status = ai_manager.get_provider_status()
        search_status = production_search_manager.get_provider_status()
        
        return jsonify({
            'database_stats': db_stats,
            'ai_providers': ai_status,
            'search_providers': search_status,
            'system_health': {
                'ai_available': len([p for p in ai_status.values() if p['available']]),
                'search_available': len([p for p in search_status.values() if p['available']]),
                'database_connected': db_manager.test_connection()
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {str(e)}")
        return jsonify({
            'error': 'Erro ao obter estatísticas',
            'message': str(e)
        }), 500
