import sqlite3
from datetime import datetime

def popular_investimentos():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Lista de ativos iniciais para o Lumo Bank
    # Estrutura: (nome, descricao, valor_cota, risco)
    ativos = [
        ("Lumo Tesouro Seguro", "Renda fixa estável com liquidez diária, ideal para proteção de capital.", 102.30, "baixo"),
        ("Lumo Selic Plus", "Ativo pós-fixado com rendimento atrelado à taxa básica de juros.", 110.50, "baixo"),
        ("Lumo Imobiliário Prime (LIP11)", "Fundo com foco em imóveis comerciais premium e contratos de longo prazo.", 97.80, "baixo"),
        ("Lumo Infraestrutura", "Investimentos em projetos de energia e transporte com retorno previsível.", 120.40, "baixo"),

        ("Lumo Dividendos Brasil", "Carteira de empresas sólidas com foco em pagamento de dividendos.", 45.20, "medio"),
        ("Lumo Consumo & Varejo", "Empresas do setor de varejo e consumo interno com potencial de crescimento.", 32.75, "medio"),
        ("Lumo Tech Growth", "Empresas de tecnologia com alto potencial de valorização.", 28.90, "medio"),
        ("Lumo Global ETF", "Fundo que replica o desempenho das maiores empresas globais.", 185.70, "medio"),
        ("Lumo ESG Sustentável", "Empresas com práticas sustentáveis e governança forte.", 67.30, "medio"),
        ("Lumo Agro Brasil", "Setor agrícola com foco em exportação e commodities.", 54.60, "medio"),

        ("Lumo Startups", "Investimento em startups emergentes com alto potencial de retorno.", 15.40, "alto"),
        ("Cripto Lumo (LMC)", "Moeda digital com alta volatilidade e oportunidades de ganho rápido.", 450.00, "alto"),
        ("Lumo High Yield", "Crédito privado com risco elevado e retornos agressivos.", 88.30, "alto"),
        ("Lumo Energia Futuro", "Empresas de energia renovável em expansão global.", 23.80, "alto"),
        ("Lumo Small Caps", "Empresas de pequeno porte com alto potencial de crescimento e risco elevado.", 19.90, "alto")
    ]

    try:
        # 1. Limpa dados antigos para não duplicar IDs ao testar
        cursor.execute("DELETE FROM investimentos")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='investimentos'")

        # 2. Insere os novos ativos
        # Note que omitimos 'ativo' e 'criado_em' pois eles têm valores DEFAULT no banco
        cursor.executemany("""
            INSERT INTO investimentos (nome, descricao, valor_cota, risco, ultimo_update) 
            VALUES (?, ?, ?, ?, ?)
        """, [(a[0], a[1], a[2], a[3], datetime.now().isoformat()) for a in ativos])

        conn.commit()
        print(f"✅ Sucesso: {len(ativos)} ativos foram adicionados ao Lumo Bank!")

    except Exception as e:
        print(f"❌ Erro ao popular tabela: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    popular_investimentos()
    
