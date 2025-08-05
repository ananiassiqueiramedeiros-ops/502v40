#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - System Validator
Validador completo do sistema com correção automática
"""

import sys
import os
import time
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Função principal de validação"""
    
    print("🚀 ARQV30 Enhanced v2.0 - Validação Completa do Sistema")
    print("=" * 80)
    
    try:
        # 1. Carrega ambiente
        print("🔧 Carregando configuração de ambiente...")
        from services.environment_loader import environment_loader
        environment_loader.print_configuration_status()
        
        # 2. Valida APIs
        print("\n🧪 Validando APIs...")
        from services.api_validator import api_validator
        validation_results = api_validator.validate_all_apis()
        
        # 3. Verifica prontidão do sistema
        readiness = api_validator.get_system_readiness()
        
        print(f"\n📊 PRONTIDÃO DO SISTEMA:")
        print(f"   • Nível: {readiness['level']}")
        print(f"   • Status: {readiness['message']}")
        print(f"   • APIs Críticas: {readiness['critical_working']}/2")
        print(f"   • APIs Recomendadas: {readiness['recommended_working']}")
        print(f"   • Total Funcionando: {readiness['total_working']}")
        
        # 4. Testa componentes principais
        print(f"\n🔍 Testando componentes principais...")
        
        # Testa AI Manager
        try:
            from services.ai_manager import ai_manager
            ai_status = ai_manager.get_provider_status()
            available_ai = sum(1 for p in ai_status.values() if p['available'])
            print(f"   ✅ AI Manager: {available_ai} provedores disponíveis")
        except Exception as e:
            print(f"   ❌ AI Manager: {e}")
        
        # Testa Search Manager
        try:
            from services.production_search_manager import production_search_manager
            search_status = production_search_manager.get_provider_status()
            available_search = sum(1 for p in search_status.values() if p['available'])
            print(f"   ✅ Search Manager: {available_search} provedores disponíveis")
        except Exception as e:
            print(f"   ❌ Search Manager: {e}")
        
        # Testa Database Manager
        try:
            from database import db_manager
            db_connected = db_manager.test_connection()
            print(f"   {'✅' if db_connected else '❌'} Database Manager: {'Conectado' if db_connected else 'Desconectado'}")
        except Exception as e:
            print(f"   ❌ Database Manager: {e}")
        
        # 5. Relatório final
        print(f"\n" + "=" * 80)
        print(f"🏁 RELATÓRIO FINAL DE VALIDAÇÃO")
        print(f"=" * 80)
        
        if readiness['system_ready']:
            print(f"🎉 SISTEMA PRONTO PARA USO!")
            print(f"✅ Todas as APIs críticas estão funcionando")
            print(f"🚀 Você pode executar análises ultra-detalhadas")
            
            print(f"\n📋 PRÓXIMOS PASSOS:")
            print(f"1. Execute: python src/run.py")
            print(f"2. Acesse: http://localhost:5000")
            print(f"3. Teste com uma análise simples")
            print(f"4. Monitore logs em: logs/arqv30.log")
            
            return True
        else:
            print(f"⚠️ SISTEMA PRECISA DE CONFIGURAÇÃO")
            print(f"🔧 Configure as APIs críticas ausentes")
            
            # Mostra APIs que precisam ser configuradas
            critical_missing = []
            for api_name, api_data in validation_results['apis'].items():
                if api_data['priority'] == 'CRITICAL' and not api_data['working']:
                    critical_missing.append(api_name)
            
            if critical_missing:
                print(f"\n🚨 APIs CRÍTICAS AUSENTES:")
                for api in critical_missing:
                    print(f"   • {api.upper()}")
            
            print(f"\n📋 AÇÕES NECESSÁRIAS:")
            print(f"1. Configure as APIs críticas no arquivo .env")
            print(f"2. Execute novamente: python validate_system.py")
            print(f"3. Consulte API_SETUP_GUIDE.md para instruções detalhadas")
            
            return False
    
    except Exception as e:
        print(f"❌ ERRO CRÍTICO na validação: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print(f"\n🎯 SISTEMA VALIDADO E PRONTO!")
        print(f"Execute: python src/run.py para iniciar")
    else:
        print(f"\n🔧 CONFIGURE AS APIS E TENTE NOVAMENTE")
        print(f"Consulte: API_SETUP_GUIDE.md")
    
    sys.exit(0 if success else 1)