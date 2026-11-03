export function ativarAbas(lista, invalidation) {
  const abas = [...lista.querySelectorAll("[role=tab]")];
  const paineis = abas.map((aba) => document.getElementById(aba.getAttribute("aria-controls")));

  function selecionar(indice, atualizarEndereco = false) {
    abas.forEach((aba, i) => {
      aba.setAttribute("aria-selected", String(i === indice));
      aba.tabIndex = i === indice ? 0 : -1;
      paineis[i].hidden = i !== indice;
    });
    if (atualizarEndereco && location.hash !== "#" + paineis[indice].id) {
      history.pushState(null, "", "#" + paineis[indice].id);
    }
  }

  function lerEndereco() {
    const alvo = document.getElementById(location.hash.slice(1));
    const indice = paineis.findIndex((painel) => alvo && painel.contains(alvo));
    selecionar(Math.max(0, indice));
    if (indice >= 0) requestAnimationFrame(() => alvo.scrollIntoView());
  }

  abas.forEach((aba, i) => {
    aba.addEventListener("click", () => selecionar(i, true));
    aba.addEventListener("keydown", (evento) => {
      const ultimo = abas.length - 1;
      const destinos = {ArrowLeft: i === 0 ? ultimo : i - 1, ArrowRight: i === ultimo ? 0 : i + 1, Home: 0, End: ultimo};
      const destino = destinos[evento.key];
      if (destino === undefined) return;
      evento.preventDefault();
      selecionar(destino, true);
      abas[destino].focus();
    });
  });
  window.addEventListener("hashchange", lerEndereco);
  invalidation.then(() => window.removeEventListener("hashchange", lerEndereco));
  lerEndereco();
}
