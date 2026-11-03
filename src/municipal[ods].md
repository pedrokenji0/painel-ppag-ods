---
title: Indicadores municipais
toc: false
---

```js
import {escolhaMeta, escolhaMunicipal, painelMunicipal} from "./municipal.js";
import {recortesMunicipais} from "./recortes-municipais.js";

const ods = observable.params.ods;
const recorte = recortesMunicipais[ods];
const icone = FileAttachment(`./assets/ods${observable.params.ods}.png`).url();
const municipal = FileAttachment(`./data/municipal-ods${observable.params.ods}.json`).json();
const malha = FileAttachment("./data/malha-mg.json").json();
```

```js
display(html`<section class=${"section-hero ods" + ods + "-theme"}>
  <img src=${icone} width="96" height="96" alt=${"ODS " + ods}>
  <div>
    <p class="eyebrow">INDICADORES MUNICIPAIS <span> / </span> ODS ${ods}</p>
    <h1>${recorte.titulo}</h1>
    <p>Explore os dados do CIS/FJP para os municípios de Minas Gerais.</p>
  </div>
</section>`);
```

## Mapa municipal de Minas Gerais

Escolha o indicador e o ano para ver os valores por município. O painel mostra a unidade de medida e explica o vínculo de cada indicador com a meta.

```js
const meta = view(escolhaMeta(recorte.metas));
```

```js
const indicador = view(escolhaMunicipal(meta.indicadores, "indicadores", "Indicador", {
  format: ([, nome]) => nome
}));
```

```js
const serie = municipal.series[indicador[0]];
const ano = view(escolhaMunicipal(Object.keys(serie.anos).sort().reverse(), "anos", "Ano"));
```

```js
display(painelMunicipal(municipal, malha, serie, indicador, ano, resize, recorte));
if (ods === "1") display(html`<p><a href="./indicadores.html">Ver séries de pobreza de Minas Gerais e Brasil →</a></p>`);
```
