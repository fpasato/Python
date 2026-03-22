import sqlite3
from datetime import datetime

DB_PATH = "seu_banco.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def gerar_investimentos():
    conn = get_db()
    cursor = conn.cursor()

    investimentos = [
        # Tecnologia
        ("Tech Growth", "Empresa de tecnologia em expansão", 120.0, "alto"),
        ("AI Corp", "Inteligência artificial e automação", 200.0, "alto"),
        ("CloudNet", "Serviços de computação em nuvem", 140.0, "medio"),
        ("CyberSafe", "Segurança digital e proteção de dados", 110.0, "medio"),

        # Financeiro
        ("Safe Bank", "Banco consolidado com baixo risco", 80.0, "baixo"),
        ("Fintech Plus", "Plataforma de pagamentos digitais", 130.0, "medio"),
        ("CreditMax", "Empresa de crédito e financiamentos", 95.0, "medio"),

        # Energia
        ("Energy Plus", "Energia renovável", 95.0, "medio"),
        ("Solar Grid", "Painéis solares e energia limpa", 105.0, "medio"),
        ("OilMaster", "Exploração de petróleo", 150.0, "alto"),

        # Imobiliário
        ("Real Estate BR", "Fundo imobiliário nacional", 70.0, "baixo"),
        ("Urban Living", "Empreendimentos urbanos", 85.0, "medio"),
        ("Mega Construções", "Construtora de grande porte", 100.0, "medio"),

        # Agro
        ("Agro Future", "Investimento no agronegócio", 60.0, "medio"),
        ("GrainCorp", "Produção de grãos", 75.0, "baixo"),
        ("FarmTech", "Tecnologia aplicada ao campo", 90.0, "medio"),

        # Saúde
        ("Saúde+ Vida", "Rede hospitalar", 110.0, "baixo"),
        ("BioTech Labs", "Pesquisa farmacêutica", 180.0, "alto"),
        ("MedEquip", "Equipamentos médicos", 95.0, "medio"),

        # Logística
        ("Logística Sul", "Transporte e logística", 85.0, "medio"),
        ("FastDelivery", "Entrega rápida urbana", 120.0, "alto"),
        ("CargoMax", "Transporte internacional", 130.0, "medio"),

        # Sustentabilidade
        ("Green Planet", "Projetos ambientais", 90.0, "medio"),
        ("EcoFuture", "Soluções sustentáveis", 100.0, "medio"),
        ("RecycleTech", "Tecnologia de reciclagem", 80.0, "baixo"),

        # Digital / Crypto
        ("CryptoX", "Ativo digital volátil", 150.0, "alto"),
        ("BlockChain Hub", "Infraestrutura blockchain", 170.0, "alto"),
        ("Token Invest", "Plataforma de tokens digitais", 140.0, "alto"),

        # Diversificados
        ("Global Mix", "Carteira diversificada global", 110.0, "baixo"),
        ("Prime Invest", "Fundo multimercado", 125.0, "medio"),
        ("Alpha Capital", "Gestora de investimentos", 135.0, "medio"),
    ]

    inseridos = 0

    for nome, descricao, valor, risco in investimentos:
        # evita duplicado
        cursor.execute("SELECT id FROM investimentos WHERE nome = ?", (nome,))
        if cursor.fetchone():
            continue

        cursor.execute("""
            INSERT INTO investimentos (nome, descricao, valor_cota, risco)
            VALUES (?, ?, ?, ?)
        """, (nome, descricao, valor, risco))
        inseridos += 1

    conn.commit()
    conn.close()

    print(f"[{datetime.now()}] {inseridos} investimentos inseridos com sucesso!")


if __name__ == "__main__":
    gerar_investimentos()