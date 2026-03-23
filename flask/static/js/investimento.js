document.addEventListener('DOMContentLoaded', () => {
    // ========== Elementos DOM ==========
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

    // ========== Estado ==========
    let modalHistoricoChartInstance = null;
    let currentInvestimentoId = null;
    let currentPreco = 0;
    let currentQuantidadeCarteira = null;
    let currentUniqueId = null;
    let ultimoServerTime = null;
    let ultimoLocalTime = null;

    // ========== Utilitários ==========
    const formatBRL = (value) => {
        const n = Number(value);
        if (!Number.isFinite(n)) return 'R$ 0,00';
        return `R$ ${n.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    };

    const formatarTempoRestante = (expiraTimestamp, agora) => {
        if (!expiraTimestamp) return '';
        const agoraTimestamp = agora !== undefined ? agora : ultimoServerTime;
        if (!agoraTimestamp) return '';
        let diff = expiraTimestamp - agoraTimestamp;
        if (diff <= 0) return 'expirado';
        const horas = Math.floor(diff / 3600);
        const minutos = Math.floor((diff % 3600) / 60);
        const segundos = diff % 60;
        if (horas > 0) {
            return `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;
        } else {
            return `${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;
        }
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

    // ========== LocalStorage ==========
    function salvarInvestimentosNoStorage(carteira) {
        const investimentosStorage = {};
        carteira.forEach(item => {
            if (item.temporario && item.tempo_restante > 0) {
                investimentosStorage[item.id] = {
                    id: item.id,
                    investimentoId: item.investimento_id,
                    nome: item.nome,
                    quantidade: item.quantidade,
                    saldo: item.saldo,
                    lucroPrejuizo: item.lucro_prejuizo,
                    tempo_restante: item.tempo_restante,
                    tempo_inicio: item.tempo_inicio,
                    duracao: item.duracao,
                    temporario: true
                };
            }
        });
        localStorage.setItem('investimentos_temporarios', JSON.stringify(investimentosStorage));
    }

    function carregarInvestimentosDoStorage() {
        const storage = localStorage.getItem('investimentos_temporarios');
        if (!storage) return {};
        return JSON.parse(storage);
    }

    // ========== Renderização dos cards a partir do localStorage ==========
    function renderizarCards(investimentosDoServidor = null) {
        const container = document.querySelector('.investimentos-lista');
        if (!container) return;

        let investimentos;
        if (investimentosDoServidor) {
            // Converte os dados do servidor para o formato do storage
            investimentos = {};
            investimentosDoServidor.forEach(item => {
                if (item.temporario) {
                    investimentos[item.id] = {
                        id: item.id,
                        investimentoId: item.investimento_id,
                        nome: item.nome,
                        quantidade: item.quantidade,
                        saldo: item.saldo,
                        lucroPrejuizo: item.lucro_prejuizo,
                        tempo_restante: item.tempo_restante,
                        tempo_inicio: item.tempo_inicio,
                        duracao: item.duracao,
                        temporario: true
                    };
                }
            });
            // Salva no localStorage para uso futuro
            localStorage.setItem('investimentos_temporarios', JSON.stringify(investimentos));
        } else {
            investimentos = carregarInvestimentosDoStorage();
        }

        container.innerHTML = '';
        if (Object.keys(investimentos).length === 0) {
            container.innerHTML = '<div class="empty-state"><h3>Você ainda não tem investimentos</h3><p>Acesse a aba "Investir Agora" para começar.</p></div>';
            return;
        }

        for (const id in investimentos) {
            const inv = investimentos[id];
            const card = document.createElement('div');
            card.className = 'invest-item-card';
            card.dataset.id = inv.id;
            card.dataset.investimentoId = inv.investimentoId;
            card.dataset.temporario = '1';
            card.dataset.quantidade = inv.quantidade;
            card.dataset.saldo = inv.saldo;
            card.dataset.expira = inv.expira_em;
            card.innerHTML = `
                <div class="item-info"><strong>${inv.nome}</strong></div>
                <div class="item-details" style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div><small>Qtd:</small> <strong class="card-qtd">${inv.quantidade}</strong></div>
                    <div><small>Saldo:</small> <strong class="card-saldo">${formatBRL(inv.saldo)}</strong></div>
                    <div><small>Lucro/Prejuízo:</small> <strong class="card-lucro">${formatBRL(inv.lucroPrejuizo)}</strong></div>
                    <div><small>Tempo restante:</small> <strong class="tempo-restante">--</strong></div>
                </div>
                <button class="btn-sell" disabled style="opacity:0.5; cursor:not-allowed;">Vender (prazo)</button>
            `;
            container.appendChild(card);
        }
    }

    // ========== Atualização dos cards com dados do servidor ==========
    function atualizarCardsComDadosDoServidor(carteira) {
        // Atualiza o localStorage
        salvarInvestimentosNoStorage(carteira);
        // Atualiza os cards existentes (ou recria)
        const investimentosStorage = carregarInvestimentosDoStorage();
        document.querySelectorAll('.invest-item-card').forEach(card => {
            const uniqueId = card.dataset.id;
            if (!uniqueId) return;
            const inv = investimentosStorage[uniqueId];
            if (!inv) {
                card.remove();
                return;
            }
            const qtdEl = card.querySelector('.card-qtd');
            const saldoEl = card.querySelector('.card-saldo');
            const lucroEl = card.querySelector('.card-lucro');
            if (qtdEl) qtdEl.textContent = inv.quantidade;
            if (saldoEl) saldoEl.innerText = formatBRL(inv.saldo);
            if (lucroEl) lucroEl.innerText = formatBRL(inv.lucroPrejuizo);
            card.dataset.expira = inv.expira_em;
        });
    }

    function iniciarContagemLocal() {
        setInterval(() => {
            const investimentosStorage = carregarInvestimentosDoStorage();
            for (const id in investimentosStorage) {
                const inv = investimentosStorage[id];
                const card = document.querySelector(`.invest-item-card[data-id="${id}"]`);
                if (!card) continue;
                const tempoSpan = card.querySelector('.tempo-restante');
                if (tempoSpan) {
                    const agora = Date.now();
                    const tempoRestanteMs = inv.duracao - (agora - inv.tempo_inicio);

                    if (tempoRestanteMs <= 0) {
                        delete investimentosStorage[id];
                        card.remove();
                    } else {
                        const tempoRestanteSegundos = Math.floor(tempoRestanteMs / 1000);

                        const horas = Math.floor(tempoRestanteSegundos / 3600);
                        const minutos = Math.floor((tempoRestanteSegundos % 3600) / 60);
                        const segundos = tempoRestanteSegundos % 60;

                        let texto = horas > 0 
                            ? `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`
                            : `${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;

                        tempoSpan.textContent = texto;
                    }
                }
            }
            // NÃO decrementa tempo_restante aqui – ele será atualizado pelo servidor.
        }, 1000);
    }


    // ========== Gráfico ==========
    const carregarHistorico = async (investimentoId) => {
        try {
            const res = await fetch(`/investimento/historico/${investimentoId}`, { headers: { 'Accept': 'application/json' } });
            if (!res.ok) return null;
            return await res.json();
        } catch {
            return null;
        }
    };

    const renderizarGrafico = (historico) => {
        if (!modalHistoricoCanvas) return;
        if (modalHistoricoChartInstance) modalHistoricoChartInstance.destroy();
        let pontos = Array.isArray(historico) ? [...historico] : [];
        pontos.sort((a, b) => new Date(b.data) - new Date(a.data));
        pontos = pontos.slice(0, 10);
        const pontoAtual = { data: new Date().toISOString(), preco: currentPreco };
        const ultimoPonto = pontos[0];
        const jaTemAtual = ultimoPonto && new Date(ultimoPonto.data).toISOString().slice(0, 19) === pontoAtual.data.slice(0, 19);
        if (!jaTemAtual) {
            pontos.unshift(pontoAtual);
            if (pontos.length > 10) pontos.pop();
        }
        pontos.sort((a, b) => new Date(a.data) - new Date(b.data));
        const labels = pontos.map(p => formatarDataParaExibicao(p.data));
        const dados = pontos.map(p => Number(p.preco) || 0);
        let lineColor = '#0DA694';
        if (dados.length >= 2) {
            lineColor = dados[dados.length - 1] < dados[dados.length - 2] ? '#ef4444' : '#22c55e';
        }
        const lineBg = lineColor === '#ef4444' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(34, 197, 94, 0.15)';
        modalHistoricoChartInstance = new Chart(modalHistoricoCanvas.getContext('2d'), {
            type: 'line',
            data: { labels, datasets: [{ label: 'Preço da cota', data: dados, borderColor: lineColor, backgroundColor: lineBg, pointRadius: 2, borderWidth: 2, tension: 0.25 }] },
            options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { maxTicksLimit: 6 } }, y: { beginAtZero: false } } }
        });
    };

    const adicionarPontoAoGrafico = (novoPreco) => {
        if (!modalHistoricoChartInstance) return;
        const chart = modalHistoricoChartInstance;
        const novoLabel = formatarDataParaExibicao(new Date().toISOString());
        chart.data.labels.unshift(novoLabel);
        chart.data.datasets[0].data.unshift(novoPreco);
        if (chart.data.labels.length > 10) {
            chart.data.labels.pop();
            chart.data.datasets[0].data.pop();
        }
        const dados = chart.data.datasets[0].data;
        if (dados.length >= 2) {
            const lineColor = dados[dados.length - 1] < dados[dados.length - 2] ? '#ef4444' : '#22c55e';
            const lineBg = lineColor === '#ef4444' ? 'rgba(239, 68, 68, 0.15)' : 'rgba(34, 197, 94, 0.15)';
            chart.data.datasets[0].borderColor = lineColor;
            chart.data.datasets[0].backgroundColor = lineBg;
        }
        chart.update();
    };

    const carregarErenderizarGrafico = async () => {
        if (!currentInvestimentoId) return;
        const historico = await carregarHistorico(currentInvestimentoId);
        if (historico) renderizarGrafico(historico);
    };

    // ========== Forms ==========
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

    // ========== Modal ==========
    const carregarDetalhesModal = async (params) => {
        const { id, investimentoId, temporario } = params;
        currentUniqueId = id;
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
        let url;
        if (temporario !== undefined) {
            url = `/investimento/detalhes-item?tipo=${temporario ? 'temporario' : 'normal'}&id=${id}&investimento_id=${investimentoId}`;
        } else {
            url = `/investimento/detalhes/${investimentoId}`;
        }
        try {
            const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
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
                const ehTemporario = Boolean(data.temporario);
                const btnVender = formVender.querySelector('button[type="submit"]');
                if (ehTemporario) {
                    inputQuantidadeVender.value = '0';
                    inputQuantidadeVender.disabled = true;
                    modalTotalVendaEl.innerText = formatBRL(0);
                    if (btnVender) {
                        btnVender.disabled = true;
                        btnVender.title = 'Venda bloqueada: investimento com prazo';
                    }
                    let msg = formVender.querySelector('.temp-warning');
                    if (!msg) {
                        msg = document.createElement('p');
                        msg.className = 'temp-warning';
                        msg.style.color = '#f97316';
                        msg.style.fontSize = '0.8rem';
                        msg.style.marginTop = '5px';
                        formVender.appendChild(msg);
                    }
                    msg.textContent = 'Este investimento possui prazo e não pode ser vendido antes do vencimento.';
                } else {
                    inputQuantidadeVender.disabled = false;
                    inputQuantidadeVender.max = String(qtd);
                    inputQuantidadeVender.value = String(Math.min(1, qtd) || 1);
                    updateSellTotal();
                    if (btnVender) {
                        btnVender.disabled = false;
                        btnVender.title = '';
                    }
                    const msg = formVender.querySelector('.temp-warning');
                    if (msg) msg.remove();
                }
            } else {
                modalCarteiraExtra.style.display = 'none';
                formVender.style.display = 'none';
                currentQuantidadeCarteira = null;
            }
            await carregarErenderizarGrafico();
        } catch (err) {
            modalTitulo.innerText = 'Erro';
            modalInfo.innerText = err.message || 'Não foi possível abrir o modal.';
        }
    };

    // ========== Polling ==========
    const atualizarValoresPagina = async () => {
        if (!saldoAtualEl) return;
        try {
            const res = await fetch('/investimento/atualizar-precos', { headers: { 'Accept': 'application/json' } });
            if (!res.ok) return;
            const data = await res.json();
            ultimoServerTime = data.server_time;
            ultimoLocalTime = Date.now();
            saldoAtualEl.innerText = formatBRL(data.saldo || 0);
            // Atualiza cards a partir dos dados do servidor e salva no localStorage
            atualizarCardsComDadosDoServidor(data.carteira);
            // Atualiza ativos disponíveis
            const ativos = Array.isArray(data.ativos_disponiveis) ? data.ativos_disponiveis : [];
            const ativosPorId = new Map(ativos.map(item => [String(item.id), item]));
            document.querySelectorAll('.ativo-card').forEach(card => {
                const ativoId = card.dataset.ativoId;
                if (!ativoId) return;
                const ativo = ativosPorId.get(ativoId);
                if (!ativo) return;
                const precoEl = card.querySelector('.ativo-preco');
                if (precoEl) precoEl.innerText = formatBRL(ativo.valor_cota || 0);
                card.dataset.preco = String(ativo.valor_cota || 0);
                card.dataset.risco = String(ativo.risco || '');
            });
            // Atualiza modal se aberto (detalhes)
            if (modal.classList.contains('active') && currentUniqueId) {
                const investimentosStorage = carregarInvestimentosDoStorage();
                const item = investimentosStorage[currentUniqueId];
                if (item) {
                    const precoAtualizado = Number(item.preco_atual) || currentPreco;
                    const qtdAtualizada = Number(item.quantidade) || 0;
                    const lucroPrejuizo = item.lucroPrejuizo;
                    if (precoAtualizado !== currentPreco) {
                        currentPreco = precoAtualizado;
                        modalPrecoCota.innerText = formatBRL(currentPreco);
                        updateBuyTotal();
                        if (formVender.style.display === 'block') updateSellTotal();
                        adicionarPontoAoGrafico(currentPreco);
                    }
                    if (qtdAtualizada !== currentQuantidadeCarteira) {
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
                } else {
                    modal.classList.remove('active');
                }
            }
            // Notificações
            if (data.notificacoes && data.notificacoes.length > 0) {
                data.notificacoes.forEach(notif => {
                    if (notif.tipo === 'venda_automatica') {
                        const lucro = notif.lucro;
                        const lucroFormatado = formatBRL(lucro);
                        const mensagem = `${notif.quantidade} cota(s) do ativo ${notif.nome} foi vendida automaticamente. ${lucro >= 0 ? 'Lucro:' : 'Prejuízo:'} ${lucroFormatado}`;
                        const tipo = lucro >= 0 ? 'success' : 'error';
                        if (typeof showPopup === 'function') showPopup(mensagem, tipo);
                    } else {
                        if (typeof showPopup === 'function') showPopup(notif, 'info');
                    }
                });
            }
        } catch (err) {
            console.warn('Erro no polling de atualização:', err);
        }
    };

    // ========== Abrir modal a partir de card ==========
    const abrirModalPeloCard = async (e, card) => {
        if (e && (e.target.closest('form') || e.target.closest('button'))) return;
        const investimentoId = card.dataset.investimentoId || card.dataset.ativoId;
        if (!investimentoId) return;
        const uniqueId = card.dataset.id;
        const temporario = card.dataset.temporario === '1';
        if (uniqueId !== undefined) {
            await carregarDetalhesModal({ id: uniqueId, investimentoId, temporario });
        } else {
            await carregarDetalhesModal({ investimentoId });
        }
        modal.classList.add('active');
    };

    // ========== Event Listeners ==========
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
            setTimeout(() => { btn.disabled = true; }, 0);
            setTimeout(() => { btn.disabled = false; }, 3000);
        });
    });

    // ========== Inicialização ==========
    // Carrega cards do localStorage (se existirem)
    renderizarCards(window.initialCarteira);
    // Inicia contagem regressiva local
    iniciarContagemLocal();
    // Primeiro polling e repetição
    atualizarValoresPagina().catch(() => {});
    setInterval(() => atualizarValoresPagina().catch(() => {}), 5000);
});