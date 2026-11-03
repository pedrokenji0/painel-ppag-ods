import * as Plot from "@observablehq/plot";
import {html} from "npm:htl";
import {radio} from "@observablehq/inputs";

export function escolhaMunicipal(opcoes, tipo, titulo, {value = opcoes[0], format} = {}) {
  const controle = radio(opcoes, {label: titulo, value, format});
  controle.classList.add("escolha-municipal", `escolha-${tipo}`);
  const grupo = controle.querySelector("div");
  grupo.setAttribute("role", "radiogroup");
  grupo.setAttribute("aria-label", titulo);
  return controle;
}

export function escolhaMeta(metas, value) {
  return escolhaMunicipal(metas, "metas", "Meta", {
    value,
    format: ({codigo, titulo, indicadores}) => html`<span class="meta-cartao">
      <span class="meta-codigo">${codigo}</span><strong>${titulo}</strong>
      <small>${indicadores.length} ${indicadores.length === 1 ? "indicador" : "indicadores"}</small>
    </span>`
  });
}

export function painelMunicipal(municipal, malha, serieMunicipal, indicadorMunicipal, anoMunicipal, resize, esquema) {
  const valores = serieMunicipal.anos[anoMunicipal];
  const unidade = serieMunicipal.unidade;
  const categorica = unidade === "Sim/Não";
  const numero = new Intl.NumberFormat("pt-BR", unidade === "R$"
    ? {style: "currency", currency: "BRL"}
    : {maximumFractionDigits: 2});
  const formatar = (valor) => {
    if (valor == null) return "Sem dado";
    return categorica ? valor : numero.format(valor) + (unidade === "%" ? "%" : "");
  };
  const cores = categorica
    ? {type: "ordinal", domain: ["Não", "Sim"], range: ["#a6b5c7", esquema.escuro], legend: "swatches"}
    : {
        type: "linear", scheme: esquema.gradiente,
        domain: [0, Math.max(1, ...Object.values(serieMunicipal.anos).flatMap(Object.values))],
        legend: true, height: 56, marginTop: 24, marginLeft: 12, marginRight: 18,
        tickFormat: unidade === "R$" ? new Intl.NumberFormat("pt-BR", {notation: "compact"}).format : undefined
      };
  const municipios = municipal.municipios;
  const linhas = Object.entries(municipios).sort((a, b) => a[1].localeCompare(b[1], "pt-BR"));
  const [, etiqueta, motivo] = indicadorMunicipal;
  return html`<section class="panel mapa-municipal">
    <h4>${etiqueta} · ${anoMunicipal}</h4>
    <p class="muted">${serieMunicipal.nome} ${unidade ? " · " + unidade : ""}</p>
    <p><strong>Por que acompanhar?</strong> ${motivo}</p>
    <p class="coverage"><strong>${Object.keys(valores).length} de ${linhas.length} municípios com dado</strong>
      · <span class="mapa-sem-dado" aria-hidden="true"></span> Cinza indica ausência de dado.</p>
    ${resize((width) => Plot.plot({
      width, height: Math.min(490, width * 0.83), margin: 6,
      style: {fontFamily: "var(--sans-serif)", fontSize: 13},
      ariaLabel: `${etiqueta} por município de Minas Gerais em ${anoMunicipal}`,
      projection: {type: "mercator", domain: malha},
      color: {
        ...cores, unknown: "#dbe3eb", label: unidade,
        style: {fontFamily: "var(--sans-serif)", fontSize: 13}
      },
      marks: [Plot.geo(malha, {
        fill: (d) => valores[d.properties.codarea] ?? null,
        stroke: "#fff", strokeWidth: 0.45,
        title: (d) => `${municipios[d.properties.codarea]} · ${formatar(valores[d.properties.codarea])}`
      })]
    }))}
    <details><summary>Ver valores por município</summary>
      <div class="table-scroll" role="region" aria-label="Valores por município" tabindex="0"><table>
        <thead><tr><th scope="col">Município</th><th scope="col">${anoMunicipal}${unidade ? " · " + unidade : ""}</th></tr></thead>
        <tbody>${linhas.map(([codigo, nome]) => html`<tr><th scope="row">${nome}</th><td>${formatar(valores[codigo])}</td></tr>`)}</tbody>
      </table></div>
    </details>
    <p class="muted">Fontes <a href="https://dados.fjp.mg.gov.br/consultas/">CIS/FJP</a> e
      <a href="https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html">malha municipal do IBGE</a>.</p>
  </section>`;
}
