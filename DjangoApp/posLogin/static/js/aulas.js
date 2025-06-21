// ============ CONTEÚDOS ============
function editarAula(botao) {
  const linha = botao.closest('tr');
  const celulas = linha.querySelectorAll('td');

  const dataOriginal = celulas[0].innerText;
  const conteudoOriginal = celulas[1].innerText;

  celulas[0].innerHTML = `<input type="date" value="${formatarDataParaInput(dataOriginal)}">`;
  celulas[1].innerHTML = `<input type="text" value="${conteudoOriginal}">`;

  celulas[2].innerHTML = `
    <button onclick="salvarAula(this)">Salvar</button>
    <button onclick="cancelarEdicaoAula(this, '${dataOriginal}', '${conteudoOriginal}')">Cancelar</button>
  `;
}

function salvarAula(botao) {
  const linha = botao.closest('tr');
  const inputs = linha.querySelectorAll('input');

  const novaData = formatarDataParaExibicao(inputs[0].value);
  const novoConteudo = inputs[1].value;

  linha.cells[0].innerText = novaData;
  linha.cells[1].innerText = novoConteudo;
  linha.cells[2].innerHTML = `
    <button onclick="editarAula(this)">Editar</button>
    <button onclick="excluirAula(this)">Excluir</button>
  `;
}

function cancelarEdicaoAula(botao, dataOriginal, conteudoOriginal) {
  const linha = botao.closest('tr');
  linha.cells[0].innerText = dataOriginal;
  linha.cells[1].innerText = conteudoOriginal;
  linha.cells[2].innerHTML = `
    <button onclick="editarAula(this)">Editar</button>
    <button onclick="excluirAula(this)">Excluir</button>
  `;
}

function excluirAula(botao) {
  const linha = botao.closest('tr');
  linha.remove();
}

// ============ OBSERVAÇÕES ============
function editarObservacao(botao) {
  const linha = botao.closest('tr');
  const celulas = linha.querySelectorAll('td');

  const dataOriginal = celulas[0].innerText;
  const obsOriginal = celulas[1].innerText;

  celulas[0].innerHTML = `<input type="date" value="${formatarDataParaInput(dataOriginal)}">`;
  celulas[1].innerHTML = `<input type="text" value="${obsOriginal}">`;

  celulas[2].innerHTML = `
    <button onclick="salvarObservacao(this)">Salvar</button>
    <button onclick="cancelarEdicaoObservacao(this, '${dataOriginal}', '${obsOriginal}')">Cancelar</button>
  `;
}

function salvarObservacao(botao) {
  const linha = botao.closest('tr');
  const inputs = linha.querySelectorAll('input');

  const novaData = formatarDataParaExibicao(inputs[0].value);
  const novaObs = inputs[1].value;

  linha.cells[0].innerText = novaData;
  linha.cells[1].innerText = novaObs;
  linha.cells[2].innerHTML = `
    <button onclick="editarObservacao(this)">Editar</button>
    <button onclick="excluirObservacao(this)">Excluir</button>
  `;
}

function cancelarEdicaoObservacao(botao, dataOriginal, obsOriginal) {
  const linha = botao.closest('tr');
  linha.cells[0].innerText = dataOriginal;
  linha.cells[1].innerText = obsOriginal;
  linha.cells[2].innerHTML = `
    <button onclick="editarObservacao(this)">Editar</button>
    <button onclick="excluirObservacao(this)">Excluir</button>
  `;
}

function excluirObservacao(botao) {
  const linha = botao.closest('tr');
  linha.remove();
}

// ============ FORMATAÇÃO DE DATA ============
function formatarDataParaInput(data) {
  const partes = data.split('/');
  return `${partes[2]}-${partes[1]}-${partes[0]}`;
}

function formatarDataParaExibicao(dataISO) {
  const partes = dataISO.split('-');
  return `${partes[2]}/${partes[1]}/${partes[0]}`;
}
