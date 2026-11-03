---
title: Execução orçamentária
toc: false
---

```js
import * as Inputs from "@observablehq/inputs";
import * as Plot from "@observablehq/plot";
import {painelSerie} from "./series.js";
import {metasEstaduais, metasMunicipais} from "./saude.js";

const ods = observable.params.ods;
const saude = ods === "3";
const objetivo = saude ? "Saúde e bem-estar" : "Erradicação da pobreza";
const exercicios = await FileAttachment(`./data/execucao-ods${observable.params.ods}.json`).json();
const brl = new Intl.NumberFormat("pt-BR", {style: "currency", currency: "BRL"});
const compacto = new Intl.NumberFormat("pt-BR", {style: "currency", currency: "BRL", notation: "compact", maximumFractionDigits: 1});
const moeda = (valor) => valor == null ? "Sem registro" : brl.format(valor / 100);
const moedaCurta = (valor) => compacto.format(valor / 100);
const meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
const etapas = [["pago", "Pago"], ["liquidado", "Liquidado"], ["empenhado", "Empenhado"]];
const normalizar = (texto) => texto.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
const cor = saude ? "#377e37" : "#c91f3c";
```

```js
const icone = await FileAttachment(`./assets/ods${observable.params.ods}.png`).url();
display(html`<section class=${"hero ods" + ods + "-theme"}>
  <div><p class="eyebrow">MINAS GERAIS <span> / </span> ODS ${ods}</p>
  <h1>${saude ? objetivo : html`Erradicação<br>da pobreza`}</h1>
  <p>Execução orçamentária dos programas estaduais vinculados ao ODS ${ods}.</p>
  <div class="hero-links">
    <a class="primary" href="#programas">Ver gastos por programa</a>
    <a href=${saude ? "#indicadores" : "./indicadores.html"}>${saude ? "Indicadores de saúde" : "Indicadores de pobreza"} →</a>
    ${saude ? html`<a href="#mapa-municipal">Mapa municipal →</a>` : null}
  </div></div>
  <img src=${icone} width="224" height="224" alt=${"ODS " + ods + " — " + objetivo}>
</section>`);
```

<h2 id="filtros">Filtros da execução</h2>

```js
const seletor = Inputs.radio(exercicios, {
  label: "Exercício",
  value: exercicios.find((d) => !d.parcial) ?? exercicios[0],
  format: (d) => d.ano + (d.parcial ? " · parcial" : " · completo")
});
seletor.classList.add("periodos");
const exercicio = view(seletor);
```

```js
const grupos = ["Todos", ...new Set(exercicios.flatMap((e) => e.programas.map((d) => d.grupo)))];
const seletorGrupo = Inputs.radio(grupos, {label: "Poder ou órgão", value: "Todos"});
seletorGrupo.classList.add("periodos");
const grupo = view(seletorGrupo);
```

```js
const programasDoGrupo = exercicio.programas.filter((d) => grupo === "Todos" || d.grupo === grupo);
const unidades = [...new Set(programasDoGrupo.map((d) => d.unidade))]
  .sort((a, b) => a.localeCompare(b, "pt-BR"));
const unidade = view(Inputs.select(["Todas", ...unidades], {label: "Unidade responsável"}));
```

```js
const programas = programasDoGrupo.filter((d) => unidade === "Todas" || d.unidade === unidade).sort((a, b) =>
  (b.pago ?? -Infinity) - (a.pago ?? -Infinity) || Number(a.codigo) - Number(b.codigo));
const comRegistro = programas.filter((d) => d.pago != null);
const total = Object.fromEntries(etapas.map(([campo]) => [
  campo, comRegistro.length ? comRegistro.reduce((soma, d) => soma + d[campo], 0) : null
]));
const previsto = programas.reduce((soma, d) => soma + d.previsto, 0);
const porMes = Array(exercicio.ultimoMes).fill(0);
for (const programa of comRegistro) {
  for (const {mes, pago} of programa.meses) porMes[mes - 1] += pago;
}
const pontos = porMes.map((pago, i) => ({mes: meses[i], pago}));
const maiores = comRegistro.filter((d) => d.pago > 0).slice(0, 6);
```

<div class="metrics" aria-live="polite">
  <section class="metric metric-main"><span>Valor pago no exercício</span><strong>${moeda(total.pago)}</strong><small>jan a ${meses[exercicio.ultimoMes - 1]} de ${exercicio.ano}${exercicio.parcial ? " · último mês parcial" : ""}</small></section>
  <section class="metric"><span>Valor liquidado</span><strong>${moeda(total.liquidado)}</strong><small>Despesas reconhecidas</small></section>
  <section class="metric"><span>Valor empenhado</span><strong>${moeda(total.empenhado)}</strong><small>Compromissos assumidos</small></section>
</div>
<p class="coverage"><strong>${programas.length} programas vinculados</strong> · ${comRegistro.length} com registros no SIAFI-MG · Previsão anual do PPAG <strong>${moeda(previsto)}</strong>. O total soma os pagamentos do exercício, sem os restos a pagar de anos anteriores.</p>

<div class="overview">
  <section class="panel">
    <p class="eyebrow">EXECUÇÃO</p><h2>Pagamentos por mês</h2>
    ${comRegistro.length ? resize((width) => Plot.plot({
      width, height: 270, marginLeft: 83,
      ariaLabel: "Valor pago por mês",
      x: {domain: pontos.map((d) => d.mes), label: null},
      y: {label: null, grid: true, tickFormat: moedaCurta},
      marks: [Plot.ruleY([0]), Plot.barY(pontos, {x: "mes", y: "pago", fill: cor, tip: true, title: (d) => moeda(d.pago)})]
    })) : html`<p class="muted">Sem registros no SIAFI-MG para este recorte.</p>`}
  </section>
  <section class="panel">
    <p class="eyebrow">RANKING</p><h2>Maiores pagamentos</h2>
    ${maiores.length ? html`<ol class="ranking">${maiores.map((d) => html`<li>
      <span class="program-name"><small>${d.codigo}</small> ${d.nome}</span><strong>${moedaCurta(d.pago)}</strong>
      <div class="rank-track"><span style=${{width: (100 * d.pago / maiores[0].pago) + "%"}}></span></div>
    </li>`)}</ol>` : html`<p class="muted">Nenhum pagamento positivo para este recorte.</p>`}
  </section>
</div>

## Programas

A tabela segue os [filtros da execução](#filtros). A previsão é anual, enquanto a execução reflete o período disponível.

```js
const busca = view(Inputs.text({label: "Buscar programa", placeholder: "Digite um código ou nome"}));
```

```js
const consulta = normalizar(busca.trim());
const filtrados = programas.filter((d) => normalizar(d.codigo + " " + d.nome).includes(consulta));
display(filtrados.length ? html`<div class="table-scroll" role="region" aria-label="Execução por programa" tabindex="0">
  <table class="program-table">
    <thead><tr><th scope="col">Código e programa</th><th scope="col">Pago</th><th scope="col">Liquidado</th><th scope="col">Empenhado</th><th scope="col">Previsão PPAG</th></tr></thead>
    <tbody>${filtrados.map((d) => html`<tr>
      <th scope="row"><span class="program-code">${d.codigo}</span> ${d.nome}<small>${d.unidade}</small></th>
      <td><strong>${moeda(d.pago)}</strong></td><td>${moeda(d.liquidado)}</td><td>${moeda(d.empenhado)}</td><td>${moeda(d.previsto)}</td>
    </tr>`)}</tbody>
  </table>
</div>` : html`<p class="panel">Nenhum programa encontrado para esta busca.</p>`);
```

## Fontes e critérios

```js
display(html`<p>A execução orçamentária vem do <a href=${exercicio.fonte}>SIAFI-MG, exercício ${exercicio.ano}</a>. Os vínculos temáticos e a previsão vêm da base de referência ${exercicio.vinculos}.</p>`);
```

Valores nominais por código de programa e exercício. O pago corresponde ao campo **Valor Pago Orçamentário**. Cada programa entra uma vez no total, com seu valor integral. O filtro de poder ou órgão usa a unidade responsável no PPAG, conferida com as unidades executoras do SIAFI. O vínculo é temático. Um mesmo programa pode estar associado a mais de um ODS, por isso a soma entre painéis pode contar o mesmo gasto mais de uma vez.

```js
if (saude) {
  display(html`<h2 id="indicadores">Indicadores de saúde</h2>
    <p>O mapa usa indicadores locais do CIS/FJP vinculados às metas pela revisão de 2026.
    As séries do IBGE/SIDRA comparam Minas Gerais e Brasil.</p>
    <h3 id="mapa-municipal">Mapa municipal de Minas Gerais</h3>
    <p>Escolha uma meta, um indicador e um ano. Os indicadores municipais têm aderência B na revisão do CIS
    e ajudam a acompanhar aspectos das <a href="https://brasil.un.org/pt-br/sdgs/3">metas do ODS 3</a>.</p>`);
}
```

```js
const municipal = saude ? await FileAttachment("./data/saude-municipal.json").json() : null;
const malha = saude ? await FileAttachment("./data/malha-mg.json").json() : null;
const metaMunicipal = saude ? view(Inputs.radio(metasMunicipais, {
  label: "Meta", value: metasMunicipais[1], format: (d) => `${d.codigo} · ${d.titulo}`
})) : null;
```

```js
const indicadorMunicipal = saude ? view(Inputs.select(metaMunicipal.indicadores, {
  label: "Indicador", format: ([, nome]) => nome
})) : null;
```

```js
const serieMunicipal = saude ? municipal.series[indicadorMunicipal[0]] : null;
const anoMunicipal = saude ? view(Inputs.select(Object.keys(serieMunicipal.anos).sort().reverse(), {
  label: "Ano"
})) : null;
```

```js
if (saude) {
  const valores = serieMunicipal.anos[anoMunicipal];
  const maximo = Math.max(1, ...Object.values(serieMunicipal.anos).flatMap(Object.values));
  const unidade = serieMunicipal.unidade;
  const numero = new Intl.NumberFormat("pt-BR", {maximumFractionDigits: 2});
  const formatar = (valor) => valor == null ? "Sem dado" : numero.format(valor) + (unidade === "%" ? "%" : "");
  const municipios = municipal.municipios;
  const linhas = Object.entries(municipios).sort((a, b) => a[1].localeCompare(b[1], "pt-BR"));
  const [, etiqueta, motivo] = indicadorMunicipal;
  display(html`<section class="panel mapa-saude">
    <h4>${etiqueta} · ${anoMunicipal}</h4>
    <p class="muted">${serieMunicipal.nome} · ${unidade}</p>
    <p><strong>Por que acompanhar?</strong> ${motivo}</p>
    <p class="coverage"><strong>${Object.keys(valores).length} de ${linhas.length} municípios com dado</strong>
      · <span class="mapa-sem-dado" aria-hidden="true"></span> Cinza indica ausência de dado.</p>
    ${resize((width) => Plot.plot({
      width, height: Math.min(490, width * 0.83), margin: 6,
      ariaLabel: `${etiqueta} por município de Minas Gerais em ${anoMunicipal}`,
      projection: {type: "mercator", domain: malha},
      color: {type: "linear", scheme: "greens", domain: [0, maximo], unknown: "#dbe3eb", legend: true, label: unidade},
      marks: [Plot.geo(malha, {
        fill: (d) => valores[d.properties.codarea] ?? NaN,
        stroke: "#fff", strokeWidth: 0.45,
        title: (d) => `${municipios[d.properties.codarea]} · ${formatar(valores[d.properties.codarea])}`
      })]
    }))}
    <details><summary>Ver valores por município</summary>
      <div class="table-scroll" role="region" aria-label="Valores por município" tabindex="0"><table>
        <thead><tr><th scope="col">Município</th><th scope="col">${anoMunicipal} · ${unidade}</th></tr></thead>
        <tbody>${linhas.map(([codigo, nome]) => html`<tr><th scope="row">${nome}</th><td>${formatar(valores[codigo])}</td></tr>`)}</tbody>
      </table></div>
    </details>
    <p class="muted">Fontes <a href="https://dados.fjp.mg.gov.br/consultas/">CIS/FJP</a> e
      <a href="https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html">malha municipal do IBGE</a>.</p>
  </section>`);
}
```

```js
if (saude) {
  const series = await FileAttachment("./data/series-ods3.json").json();
  display(html`<h3 id="series-estaduais">Séries de Minas Gerais e Brasil</h3>`);
  for (const {codigo, titulo, indicadores} of metasEstaduais) {
    display(html`<h4 class="meta-saude">Meta ${codigo} · ${titulo}</h4>`);
    for (const [id, etiqueta, motivo] of indicadores) {
      display(painelSerie(series.find((s) => s.id === id), etiqueta, cor, resize, motivo));
    }
  }
}
```
