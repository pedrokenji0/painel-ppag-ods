import * as Plot from "@observablehq/plot";
import {html} from "npm:htl";

const territorios = ["Minas Gerais", "Brasil"];
const proporcao = new Intl.NumberFormat("pt-BR", {style: "percent", maximumFractionDigits: 1});
const taxa = new Intl.NumberFormat("pt-BR", {maximumFractionDigits: 2});

export function painelSerie(serie, etiqueta, cor, resize, motivo) {
  const cores = [cor, "#536583"];
  const percentual = serie.unidade === "Proporção (%)";
  const formatar = (valor) => {
    if (valor == null) return "Sem dado";
    return percentual ? proporcao.format(valor / 100) : taxa.format(valor);
  };
  const anos = Array.from(new Set(serie.pontos.map((d) => d.ano))).sort((a, b) => a - b);
  const valores = new Map(serie.pontos.map((d) => [d.territorio + d.ano, d.valor]));
  const ultimo = anos.findLast((ano) => territorios.every((t) => valores.get(t + ano) != null));
  const legenda = html`<ul class="series-legend">
    ${territorios.map((t, i) => html`<li><span style=${{background: cores[i]}}></span>${t} <strong>${formatar(valores.get(t + ultimo))}</strong></li>`)}
    <li>${ultimo ?? "Sem ano comum"}</li>
  </ul>`;
  const grafico = resize((width) => Plot.plot({
    width, height: 275, marginLeft: 57,
    style: {fontFamily: "var(--sans-serif)", fontSize: 13},
    ariaLabel: serie.nome + " em Minas Gerais e no Brasil",
    x: {label: null, tickFormat: String, ticks: width < 380 ? 4 : width < 700 ? 6 : anos},
    y: {label: percentual ? "%" : null, grid: true, zero: true},
    color: {domain: territorios, range: cores},
    marks: [
      Plot.lineY(serie.pontos, {x: "ano", y: (d) => d.valor ?? NaN, stroke: "territorio", strokeWidth: 2.5}),
      Plot.dot(serie.pontos.filter((d) => d.valor != null), {x: "ano", y: "valor", fill: "territorio", r: 3, tip: true,
        title: (d) => d.territorio + " · " + d.ano + " · " + formatar(d.valor)})
    ]
  }));
  return html`<section class="panel series-panel">
    <p class="eyebrow">INDICADOR ${serie.indicador} · ${anos[0]}–${anos.at(-1)}</p>
    ${motivo ? html`<h4 class="series-title">${etiqueta}</h4>` : html`<h2 class="series-title">${etiqueta}</h2>`}
    <p class="muted">${serie.nome}${percentual ? "" : " · " + serie.unidade}</p>
    ${motivo ? html`<p><strong>Por que acompanhar?</strong> ${motivo}</p>` : null}
    ${legenda}${grafico}
    <details><summary>Ver valores anuais</summary>
      <div class="table-scroll"><table>
        <thead><tr><th scope="col">Ano</th>${territorios.map((t) => html`<th scope="col">${t}</th>`)}</tr></thead>
        <tbody>${anos.map((ano) => html`<tr><th scope="row">${ano}</th>
          ${territorios.map((t) => html`<td>${formatar(valores.get(t + ano))}</td>`)}
        </tr>`)}</tbody>
      </table></div>
    </details>
    <p class="muted">Fonte <a href="https://sidra.ibge.gov.br/tabela/${serie.id}">IBGE/SIDRA · tabela ${serie.id}</a></p>
  </section>`;
}
