import {html} from "npm:htl";

export function seletorUnidade(unidades, normalizar) {
  const todas = "Todas";
  const rotulo = (unidade) => unidade === todas ? "Todas as unidades" : unidade;
  const controle = html`<details class="filtro-unidade">
    <summary>
      <span class="filtro-unidade-titulo">Unidade responsável</span>
      <strong>${rotulo(todas)}</strong>
    </summary>
    <div class="filtro-unidade-painel">
      <label>Buscar unidade <input type="search" placeholder="Digite parte do nome" autocomplete="off"></label>
      <div class="filtro-unidade-opcoes" role="group" aria-label="Unidades responsáveis"></div>
      <p class="muted" role="status" hidden>Nenhuma unidade encontrada.</p>
    </div>
  </details>`;
  const resumo = controle.querySelector("summary");
  const busca = controle.querySelector("input");
  const lista = controle.querySelector(".filtro-unidade-opcoes");
  const aviso = controle.querySelector("[role=status]");
  controle.value = todas;
  const opcoes = [todas, ...unidades].map((unidade) => {
    const botao = html`<button type="button" aria-pressed=${String(unidade === todas)}>${rotulo(unidade)}</button>`;
    botao.addEventListener("click", () => {
      const anterior = controle.value;
      controle.value = unidade;
      resumo.querySelector("strong").textContent = rotulo(unidade);
      for (const opcao of opcoes) opcao.botao.setAttribute("aria-pressed", String(opcao.unidade === unidade));
      controle.open = false;
      busca.value = "";
      filtrar();
      resumo.focus();
      if (anterior !== unidade) controle.dispatchEvent(new Event("input", {bubbles: true}));
    });
    return {unidade, botao, nome: normalizar(unidade)};
  });
  lista.append(...opcoes.map(({botao}) => botao));

  function filtrar() {
    const consulta = normalizar(busca.value.trim());
    for (const {botao, unidade, nome} of opcoes) botao.hidden = unidade !== todas && !nome.includes(consulta);
    aviso.hidden = !consulta || opcoes.slice(1).some(({botao}) => !botao.hidden);
  }
  busca.addEventListener("input", (evento) => {
    evento.stopPropagation();
    filtrar();
  });
  controle.addEventListener("toggle", () => {
    if (controle.open) busca.focus();
  });
  controle.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && controle.open) {
      evento.preventDefault();
      controle.open = false;
      resumo.focus();
    }
  });
  return controle;
}
