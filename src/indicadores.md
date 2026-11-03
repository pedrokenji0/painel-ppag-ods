---
title: Indicadores de pobreza
toc: false
---

```js
import {painelSerie} from "./series.js";

const series = await FileAttachment("./data/series-ods1.json").json();
const etiquetas = {
  "5817": "Pobreza pela linha internacional",
  "5840": "Pobreza entre pessoas ocupadas de 14 anos ou mais",
  "5877": "Pobreza pela linha nacional"
};
```

<section class="section-hero ods1-theme">
  <img src="./assets/ods1.png" width="96" height="96" alt="ODS 1 — Erradicação da pobreza">
  <div><p class="eyebrow">INDICADORES <span> / </span> ODS 1</p><h1>Pobreza em Minas Gerais</h1>
  <p>Três séries do IBGE mostram a evolução de Minas Gerais e do Brasil pelos mesmos critérios.</p></div>
</section>

[Consultar o mapa municipal do ODS 1](./municipal1.html)

```js
for (const serie of series) {
  display(painelSerie(serie, etiquetas[serie.id], "#c91f3c", resize));
}
```

As séries cobrem o estado de Minas Gerais e o Brasil. Os pagamentos dos programas e os indicadores de pobreza têm fontes e períodos diferentes.
