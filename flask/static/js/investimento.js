document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal-overlay');
    const closeBtn = document.querySelector('.close-modal');
    const cards = document.querySelectorAll('.ativo-card');

    // Elementos do modal
    const modalImg = document.getElementById('modal-img');
    const modalNome = document.getElementById('modal-nome');
    const modalRisco = document.getElementById('modal-risco');
    const modalDesc = document.getElementById('modal-descricao');
    const modalPreco = document.getElementById('modal-preco');
    const modalAtivoId = document.getElementById('modal-ativo-id');
    const modalForm = document.querySelector('.quick-invest');

    // Abrir modal ao clicar no card
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.closest('.quick-invest')) return;

            const nome = this.dataset.nome;
            const desc = this.dataset.descricao;
            const preco = this.dataset.preco;
            const risco = this.dataset.risco;
            const img = this.dataset.img;
            const ativoId = this.dataset.ativoId;

            modalImg.src = img;
            modalNome.textContent = nome;
            modalRisco.textContent = 'Risco ' + risco;
            modalRisco.className = 'badge badge-risco ' + risco;
            modalDesc.textContent = desc;
            modalPreco.textContent = 'R$ ' + parseFloat(preco).toFixed(2).replace('.', ',');
            modalAtivoId.value = ativoId;

            carregarGrafico(ativoId);

            modal.classList.add('active');
        });
    });

    // Fechar modal
    closeBtn.addEventListener('click', function() {
        modal.classList.remove('active');
    });

    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });

    // Atualizar total no formulário
    const quantidadeInput = document.querySelector('.quick-invest input[name="quantidade"]');
    const totalSpan = document.querySelector('.calc-total');
    quantidadeInput.addEventListener('input', function() {
        const qtd = parseFloat(this.value) || 0;
        const precoTexto = modalPreco.textContent.replace('R$', '').replace(',', '.').trim();
        const preco = parseFloat(precoTexto) || 0;
        const total = qtd * preco;
        totalSpan.textContent = 'R$ ' + total.toFixed(2).replace('.', ',');
    });

    async function carregarGrafico(investimentoId) {
        try {
            const response = await fetch(`/investimento/historico/${investimentoId}`);
            const dados = await response.json();

            const labels = dados.map(item => {
                // Se a data vier como string ISO, pode formatar
                const data = new Date(item.data);
                return data.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' });
            });
            const precos = dados.map(item => item.preco);

            const ctx = document.getElementById('grafico-precos').getContext('2d');

            if (window.meuGrafico) {
                window.meuGrafico.destroy();
            }

            window.meuGrafico = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Preço da cota (R$)',
                        data: precos,
                        borderColor: '#0DA694',
                        backgroundColor: 'rgba(13, 166, 148, 0.1)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            ticks: {
                                callback: function(value) {
                                    return 'R$ ' + value.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Erro ao carregar histórico:', error);
        }
    }
});