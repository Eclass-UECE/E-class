document.getElementById('btnAdicionarAula').addEventListener('click', function() {
    const dataInput = document.getElementById('data');
    const partesData = dataInput.value.split('-');
    
    if (partesData.length < 3) {
        alert("Selecione uma data válida!");
        return;
    }

    // Criar data sem problemas de fuso horário
    const dataSelecionada = new Date(partesData[0], partesData[1] - 1, partesData[2]);
    
    // Período permitido (01/03/2025 até 01/11/2025)
    const dataInicio = new Date(2025, 2, 1);   // 01/03/2025
    const dataFim = new Date(2025, 10, 1);     // 01/11/2025

    if (dataSelecionada < dataInicio || dataSelecionada > dataFim) {
        alert("Data fora do período permitido (01/03/2025 a 01/11/2025)");
        return;
    }

    const mes = String(dataSelecionada.getMonth() + 1).padStart(2, '0');
    const ano = String(dataSelecionada.getFullYear()).slice(-2);
    const dia = dataSelecionada.getDate();
    const mesAno = `${mes}/${ano}`;

    const thead = document.querySelector('thead');
    const thMeses = thead.rows[0]; // Linha de meses
    const thDias = thead.rows[1];  // Linha de dias
    const tbody = document.querySelector('tbody');
    const linhas = tbody.rows;

    // 1. Encontrar o mês correspondente (ignorando as 2 primeiras colunas fixas)
    let mesIndex = -1;
    let totalColunasAntes = 2; // Matrícula e Nome
    
    for (let i = 2; i < thMeses.cells.length - 1; i++) {
        if (thMeses.cells[i].textContent === mesAno) {
            mesIndex = i;
            break;
        }
        totalColunasAntes += parseInt(thMeses.cells[i].getAttribute('colspan') || '1');
    }

    // 2. Se o mês não existe, criar novo
    if (mesIndex === -1) {
        // Encontrar posição correta para inserir (ordenado por mês)
        let posicaoInsercao = thMeses.cells.length - 1;
        for (let i = 2; i < thMeses.cells.length - 1; i++) {
            const [mExistente] = thMeses.cells[i].textContent.split('/');
            if (parseInt(mes) < parseInt(mExistente)) {
                posicaoInsercao = i;
                break;
            }
        }

        // Criar nova coluna para o mês
        const novoThMes = document.createElement('th');
        novoThMes.textContent = mesAno;
        novoThMes.setAttribute('colspan', '1');
        thMeses.insertBefore(novoThMes, thMeses.cells[posicaoInsercao]);

        // Criar coluna para o dia
        const novoThDia = document.createElement('th');
        novoThDia.textContent = dia;
        thDias.insertBefore(novoThDia, thDias.cells[posicaoInsercao]);

        // Adicionar checkbox em todas as linhas
        for (let i = 0; i < linhas.length; i++) {
            const novaTd = document.createElement('td');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            novaTd.appendChild(checkbox);
            linhas[i].insertBefore(novaTd, linhas[i].cells[posicaoInsercao]);
        }
    } 
    // 3. Se o mês existe, adicionar o dia
    else {
        // Calcular posição inicial dos dias deste mês
        let inicioDias = 2; // Depois de Matrícula e Nome
        for (let i = 2; i < mesIndex; i++) {
            inicioDias += parseInt(thMeses.cells[i].getAttribute('colspan') || '1');
        }
        
        const qtdDias = parseInt(thMeses.cells[mesIndex].getAttribute('colspan')) || 1;
        
        // Verificar se o dia já existe
        for (let i = inicioDias; i < inicioDias + qtdDias; i++) {
            if (parseInt(thDias.cells[i].textContent) === dia) {
                alert("Este dia já foi adicionado!");
                return;
            }
        }

        // Encontrar posição correta para inserir (ordem crescente)
        let posicaoInsercao = inicioDias + qtdDias; // Padrão: inserir no final
        for (let i = inicioDias; i < inicioDias + qtdDias; i++) {
            const diaAtual = parseInt(thDias.cells[i].textContent);
            if (dia < diaAtual) {
                posicaoInsercao = i;
                break;
            }
        }

        // Adicionar coluna do dia
        const novoThDia = document.createElement('th');
        novoThDia.textContent = dia;
        thDias.insertBefore(novoThDia, thDias.cells[posicaoInsercao]);

        // Atualizar colspan do mês (CRUCIAL para permitir múltiplos dias)
        thMeses.cells[mesIndex].setAttribute('colspan', qtdDias + 1);

        // Adicionar checkbox em todas as linhas na POSIÇÃO CORRETA
        for (let i = 0; i < linhas.length; i++) {
            const novaTd = document.createElement('td');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            novaTd.appendChild(checkbox);
            linhas[i].insertBefore(novaTd, linhas[i].cells[posicaoInsercao]);
        }
    }

    dataInput.value = ''; // Limpa o campo de data
});