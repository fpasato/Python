document.addEventListener('DOMContentLoaded', () => {
    // ==================== Elementos do DOM ====================
    const modal = document.getElementById('modal-overlay');
    const btnClose = document.querySelector('.close-modal');
    const modalTitulo = document.getElementById('modal-titulo');
    const modalRisco = document.getElementById('modal-risco');
    const modalInfo = document.getElementById('modal-info');
    const modalPrecoCota = document.getElementById('modal-preco');
    const modalValorCarteiraEl = document.getElementById('modal-valor-carteira');
    const modalSaldoContaEl = document.getElementById('modal-saldo-conta');
    const modalCarteiraExtra = document.getElementById('modal-carteira-extra');
    const modalQtdCarteiraEl = document.getElementById('modal-qtd-carteira');
    const modalLucroPrejuizoEl = document.getElementById('modal-lucro-prejuizo');
    const modalQtdVenderAtualEl = document.getElementById('modal-qtd-vender-atual');
    const formComprar = document.getElementById('form-comprar');
    const inputInvestimentoIdComprar = document.getElementById('input-investimento-id');
    const inputQuantidadeComprar = document.getElementById('input-quantidade-compra');
    const modalTotalCompraEl = document.getElementById('modal-total-compra');
    const formVender = document.getElementById('form-vender');
    const inputInvestimentoIdVender = document.getElementById('input-investimento-id-vender');
    const inputQuantidadeVender = document.getElementById('input-quantidade-vender');
    const modalTotalVendaEl = document.getElementById('modal-total-venda');
    const saldoAtualEl = document.getElementById('saldo-atual');
    const modalHistoricoCanvas = document.getElementById('modal-historico-chart');

    // ==================== Estado ====================
    let modalHistoricoChartInstance = null;
    let currentInvestimentoId = null;
    let currentPreco = 0;
    let currentQuantidadeCarteira = null;

    // ==================== Utilitários ====================
    const formatBRL = (value) => {
        const n = Number(value);
        if (!Number.isFinite(n)) return 'R$ 0,00';
        return `R$ ${n.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    };

    const parsePositiveInt = (value, fallback = 1) => {
        const n = parseInt(value, 10);
        return (!Number.isFinite(n) || n < 1) ? fallback : n;
    };

    const formatarDataParaExibicao = (dataISO) => {
        try {
            const d = new Date(dataISO);
            return `${d.getDate().toString().padStart(2,'0')}/${(d.getMonth()+1).toString().padStart(2,'0')} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`;
        } catch {
            return dataISO;
        }
    };

    const aplicarCoresRisco = (risco) => {
        const riscoLower = (risco || '').toLowerCase();
        const styles = {
            alto: { background: '#fee2e2', color: '#ef4444' },
            médio: { background: '#fef3c7', color: '#f59e0b' },
            medio: { background: '#fef3c7', color: '#f59e0b' },
            baixo: { background: '#dcfce7', color: '#22c55e' }
        };
        const style = styles[riscoLower] || { background: '#f1f5f9', color: '#64748b' };
        Object.assign(modalRisco.style, style);
    };

    // ==================== Lógica do Gráfico ====================
    const carregarHistorico = async (investimentoId) => {
        try {
            const res = await fetch(`/investimento/historico/${investimentoId}`, {
                headers: { 'Accept': 'application/json' }
            });
            if (!res.ok) return null;
            return await res.json();
        } catch {
            return null;
        }
    };

    const renderizarGrafico = (historico) => {
        if (!modalHistoricoCanvas) return;

        // Destroi instância anterior
        if (modalHistoricoChartInstance) {
            modalHistoricoChartInstance.destroy();
            modalHistoricoChartInstance = null;
        }

        let pontos = Array.isArray(historico) ? [...historico] : [];

        // 1. Ordena por data decrescente (mais recente primeiro)
        pontos.sort((a, b) => new Date(b.data) - new Date(a.data));

        // 2. Mantém apenas os 10 mais recentes
        pontos = pontos.slice(0, 10);

        // 3. Adiciona o preço atual como ponto mais recente, se não existir um ponto com a mesma data/hora
        const pontoAtual = { data: new Date().toISOString(), preco: currentPreco };
        const ultimoPonto = pontos[0]; // mais recente

        // Compara a data (segundo a segundo) para evitar duplicação
        const jaTemAtual = ultimoPonto && new Date(ultimoPonto.data).toISOString().slice(0, 19) === pontoAtual.data.slice(0, 19);

        if (!jaTemAtual) {
            pontos.unshift(pontoAtual);
            if (pontos.length > 10) pontos.pop();
        }

        // 4. Ordena por data crescente para exibição
        pontos.sort((a, b) => new Date(a.data) - new Date(b.data));

        const labels = pontos.map(p => formatarDataParaExibicao(p.data));
        const dados = pontos.map(p => Number(p.preco) || 0);

        // Cor da linha baseada na tendência
        let lineColor = '#0DA694';
        if (dados.length >= 2) {
            lineColor = dados[dados.length - 1] < dados[dados.length - 2] ? '#ef4444' : '#22c55e';
        }
        const lineBg = lineColor === '#ef4444' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(34, 197, 94, 0.15)';

        modalHistoricoChartInstance = new Chart(modalHistoricoCanvas.getContext('2d'), {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Preço da cota',
                    data: dados,
                    borderColor: lineColor,
                    backgroundColor: lineBg,
                    pointRadius: 2,
                    borderWidth: 2,
                    tension: 0.25
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { maxTicksLimit: 6 } },
                    y: { beginAtZero: false }
                }
            }
        });
    };

    const atualizarGraficoModal = async () => {
        if (!currentInvestimentoId || !modal.classList.contains('active')) return;
        const historico = await carregarHistorico(currentInvestimentoId);
        if (historico) {
            renderizarGrafico(historico);
        } else {
            if (modalHistoricoChartInstance) modalHistoricoChartInstance.destroy();
            modalHistoricoChartInstance = null;
        }
    };
// NOVA FUNÇÃO: Adiciona o ponto em tempo real (entra o novo, sai o mais antigo)
    const adicionarPontoAoGrafico = (novoPreco) => {
        if (!modalHistoricoChartInstance) return;

        const chart = modalHistoricoChartInstance;
        const novoLabel = formatarDataParaExibicao(new Date().toISOString());

        // 1. Adiciona o novo preço e label no início (mais recente na esquerda)
        chart.data.labels.unshift(novoLabel);
        chart.data.datasets[0].data.unshift(novoPreco);

        // 2. Se passar de 10 pontos, remove o último (mais antigo) da direita
        if (chart.data.labels.length > 10) {
            chart.data.labels.pop();
            chart.data.datasets[0].data.pop();
        }

        // 3. Atualiza as cores dependendo se o preço subiu ou desceu
        const dados = chart.data.datasets[0].data;
        if (dados.length >= 2) {
            const lineColor = dados[dados.length - 1] < dados[dados.length - 2] ? '#ef4444' : '#22c55e';
            const lineBg = lineColor === '#ef4444' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(34, 197, 94, 0.15)';
            chart.data.datasets[0].borderColor = lineColor;
            chart.data.datasets[0].backgroundColor = lineBg;
        }

        // 4. Manda o gráfico se redesenhar de forma fluida
        chart.update();
    };
    
    // NOVA FUNÇÃO: carrega histórico e renderiza gráfico independente do modal estar ativo
    const carregarErenderizarGrafico = async () => {
        if (!currentInvestimentoId) return;
        const historico = await carregarHistorico(currentInvestimentoId);
        if (historico) renderizarGrafico(historico);
    };

    // ==================== Atualização de valores nos forms ====================
    const updateBuyTotal = () => {
        const qtd = parsePositiveInt(inputQuantidadeComprar.value, 1);
        inputQuantidadeComprar.value = qtd;
        modalTotalCompraEl.innerText = formatBRL(currentPreco * qtd);
    };

    const updateSellTotal = () => {
        const max = currentQuantidadeCarteira;
        let qtd = parsePositiveInt(inputQuantidadeVender.value, 1);
        if (typeof max === 'number') qtd = Math.min(qtd, max);
        inputQuantidadeVender.value = qtd;
        if (modalQtdVenderAtualEl) modalQtdVenderAtualEl.innerText = String(qtd);
        modalTotalVendaEl.innerText = formatBRL(currentPreco * qtd);
    };

    // ==================== Carregar detalhes no modal ====================
    const carregarDetalhesModal = async (investimentoId) => {
        currentInvestimentoId = investimentoId;
        modalTitulo.innerText = 'Carregando...';
        modalInfo.innerText = '...';
        modalPrecoCota.innerText = formatBRL(0);
        modalTotalCompraEl.innerText = formatBRL(0);
        modalTotalVendaEl.innerText = formatBRL(0);
        currentPreco = 0;
        currentQuantidadeCarteira = null;

        inputInvestimentoIdComprar.value = investimentoId;
        inputInvestimentoIdVender.value = investimentoId;
        inputQuantidadeComprar.value = 1;
        inputQuantidadeVender.value = 1;

        try {
            const res = await fetch(`/investimento/detalhes/${investimentoId}`, {
                headers: { 'Accept': 'application/json' }
            });
            if (!res.ok) throw new Error('Falha ao carregar dados do investimento.');

            const data = await res.json();
            currentPreco = Number(data.preco_atual) || 0;

            modalTitulo.innerText = data.nome || 'Investimento';
            modalInfo.innerText = data.descricao || 'Nenhuma descrição disponível.';
            modalPrecoCota.innerText = formatBRL(currentPreco);
            modalValorCarteiraEl.innerText = formatBRL(data.valor_carteira_total || 0);
            modalSaldoContaEl.innerText = formatBRL(data.saldo_conta || 0);

            if (data.risco) {
                modalRisco.style.display = 'inline-block';
                modalRisco.innerText = `Risco: ${data.risco}`;
                aplicarCoresRisco(data.risco);
            } else {
                modalRisco.style.display = 'none';
            }

            updateBuyTotal();

            if (data.tipo === 'carteira') {
                const qtd = parsePositiveInt(data.quantidade, 0);
                currentQuantidadeCarteira = qtd;
                modalCarteiraExtra.style.display = 'block';
                modalQtdCarteiraEl.innerText = String(qtd);
                if (typeof data.lucro_prejuizo !== 'undefined') {
                    modalLucroPrejuizoEl.innerText = formatBRL(data.lucro_prejuizo);
                }
                formVender.style.display = 'block';
                inputQuantidadeVender.max = String(qtd);
                inputQuantidadeVender.value = String(Math.min(1, qtd) || 1);
                updateSellTotal();
            } else {
                modalCarteiraExtra.style.display = 'none';
                formVender.style.display = 'none';
                currentQuantidadeCarteira = null;
            }

            // Carrega o histórico e renderiza o gráfico AGORA (antes de abrir o modal)
            await carregarErenderizarGrafico();
        } catch (err) {
            modalTitulo.innerText = 'Erro';
            modalInfo.innerText = err.message || 'Não foi possível abrir o modal.';
        }
    };

    // ==================== Polling de atualização de valores ====================
    const atualizarValoresPagina = async () => {
        if (!saldoAtualEl) return;

        try {
            const res = await fetch('/investimento/atualizar-precos', {
                headers: { 'Accept': 'application/json' }
            });
            if (!res.ok) return;

            const data = await res.json();

            // Atualiza saldo
            saldoAtualEl.innerText = formatBRL(data.saldo || 0);

            // Mapa de carteira (ID -> item)
            const carteira = Array.isArray(data.carteira) ? data.carteira : [];
            const carteiraPorId = new Map(carteira.map(item => [String(item.investimento_id), item]));

            // Atualiza cards da carteira (sem remover, apenas atualiza)
            document.querySelectorAll('.invest-item-card').forEach(card => {
                const investId = card.dataset.investimentoId ? String(card.dataset.investimentoId) : null;
                if (!investId) return;
                const item = carteiraPorId.get(investId);
                if (!item) {
                    // Se não está mais na carteira, remove o card
                    card.remove();
                    return;
                }
                const qtdEl = card.querySelector('.card-qtd');
                const saldoEl = card.querySelector('.card-saldo');
                const lucroEl = card.querySelector('.card-lucro');
                if (qtdEl) qtdEl.textContent = String(item.quantidade);
                if (saldoEl) saldoEl.innerText = formatBRL(item.saldo || 0);
                if (lucroEl) lucroEl.innerText = formatBRL(item.lucro_prejuizo || 0);
                card.dataset.quantidade = String(item.quantidade);
                card.dataset.saldo = String(item.saldo || 0);
                const hiddenQtd = card.querySelector('input[name="quantidade"]');
                if (hiddenQtd) hiddenQtd.value = String(item.quantidade);
            });

            // Atualiza cards de explorar
            const ativos = Array.isArray(data.ativos_disponiveis) ? data.ativos_disponiveis : [];
            const ativosPorId = new Map(ativos.map(item => [String(item.id), item]));
            document.querySelectorAll('.ativo-card').forEach(card => {
                const ativoId = card.dataset.ativoId ? String(card.dataset.ativoId) : null;
                if (!ativoId) return;
                const ativo = ativosPorId.get(ativoId);
                if (!ativo) return;
                const precoEl = card.querySelector('.ativo-preco');
                if (precoEl) precoEl.innerText = formatBRL(ativo.valor_cota || 0);
                card.dataset.preco = String(ativo.valor_cota || 0);
                card.dataset.risco = String(ativo.risco || '');
            });

            // Se o modal está aberto, atualiza preço e informações do ativo atual
            if (modal.classList.contains('active') && currentInvestimentoId) {
                const itemCarteira = carteiraPorId.get(String(currentInvestimentoId));
                const ativo = ativosPorId.get(String(currentInvestimentoId));
                let precoAtualizado = null;
                let qtdAtualizada = null;
                let lucroPrejuizo = null;

                if (itemCarteira) {
                    precoAtualizado = Number(itemCarteira.preco_atual) || currentPreco;
                    qtdAtualizada = Number(itemCarteira.quantidade) || 0;
                    lucroPrejuizo = itemCarteira.lucro_prejuizo;
                } else if (ativo) {
                    precoAtualizado = Number(ativo.valor_cota) || currentPreco;
                }

                if (precoAtualizado !== null && precoAtualizado !== currentPreco) {
                    currentPreco = precoAtualizado;
                    modalPrecoCota.innerText = formatBRL(currentPreco);
                    updateBuyTotal();
                    if (formVender.style.display === 'block') updateSellTotal();
                    
                    // Adiciona o ponto novo no gráfico existente empurrando o antigo pra fora
                    adicionarPontoAoGrafico(currentPreco); 
                }

                if (qtdAtualizada !== null && qtdAtualizada !== currentQuantidadeCarteira) {
                    currentQuantidadeCarteira = qtdAtualizada;
                    modalQtdCarteiraEl.innerText = String(currentQuantidadeCarteira);
                    inputQuantidadeVender.max = String(currentQuantidadeCarteira);
                    if (inputQuantidadeVender.value > currentQuantidadeCarteira) {
                        inputQuantidadeVender.value = String(currentQuantidadeCarteira);
                        updateSellTotal();
                    }
                }

                if (lucroPrejuizo !== null) {
                    modalLucroPrejuizoEl.innerText = formatBRL(lucroPrejuizo);
                }

                if (data.valor_carteira_total !== undefined) {
                    modalValorCarteiraEl.innerText = formatBRL(data.valor_carteira_total);
                }
                if (data.saldo_conta !== undefined) {
                    modalSaldoContaEl.innerText = formatBRL(data.saldo_conta);
                }
            }
        } catch (err) {
            // silencia erros de polling
        }
    };

    // ==================== Abrir modal a partir de card ====================
    const abrirModalPeloCard = async (e, card) => {
        if (e && (e.target.closest('form') || e.target.closest('button'))) return;
        const investimentoId = card.dataset.investimentoId || card.dataset.ativoId;
        if (!investimentoId) return;
        await carregarDetalhesModal(investimentoId);
        modal.classList.add('active');
    };

    // ==================== Event Listeners ====================
    if (inputQuantidadeComprar) inputQuantidadeComprar.addEventListener('input', updateBuyTotal);
    if (inputQuantidadeVender) inputQuantidadeVender.addEventListener('input', updateSellTotal);

    btnClose.addEventListener('click', () => modal.classList.remove('active'));
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.remove('active'); });

    document.querySelectorAll('.invest-item-card, .ativo-card').forEach(card => {
        card.addEventListener('click', (e) => abrirModalPeloCard(e, card));
    });

    document.querySelectorAll('button[type="submit"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (btn.disabled) {
                e.preventDefault();
                return;
            }
            
            // Um setTimeout de 0ms coloca a desativação no fim da fila de execução,
            // permitindo que o formulário dispare o submit antes de o botão "apagar".
            setTimeout(() => { 
                btn.disabled = true; 
            }, 0);
            
            // Reativa o botão após 3 segundos, caso a página não tenha recarregado
            setTimeout(() => { 
                btn.disabled = false; 
            }, 3000);
        });
    });

    // ==================== Inicialização ====================
    atualizarValoresPagina().catch(() => {});
    setInterval(() => {
        atualizarValoresPagina().catch(() => {});
    }, 5000);
});