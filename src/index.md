---
title: Todos os ODS
toc: false
---

```js
const exercicios = await FileAttachment("./data/execucao-ods1.json").json();
const base = exercicios.findLast((d) => !d.parcial) ?? exercicios[0];
const pago = base.programas.reduce((total, programa) => total + (programa.pago ?? 0), 0);
const resumo = new Intl.NumberFormat("pt-BR", {
  style: "currency", currency: "BRL", notation: "compact", maximumFractionDigits: 2
}).format(pago / 100);
```

<section class="hero catalog-hero">
  <div><p class="eyebrow">MINAS GERAIS <span> / </span> AGENDA 2030</p>
  <h1>Planejamento e desenvolvimento sustentável</h1>
  <p>Explore os Objetivos de Desenvolvimento Sustentável e acompanhe a execução dos programas estaduais vinculados.</p>
  <div class="hero-links"><a class="primary" href="#objetivos">Explorar objetivos</a></div></div>
  <aside class="catalog-feature"><p class="eyebrow">PRIMEIRO PAINEL · ODS 1</p>
    <strong>${resumo}</strong><p>pagos em ${base.ano} nos programas estaduais vinculados à erradicação da pobreza.</p>
    <a href="./ods1.html">Ver execução e programas →</a>
  </aside>
</section>

## Objetivos

O catálogo reúne os 17 objetivos globais e o ODS 18, iniciativa brasileira pela igualdade étnico-racial.

<ul class="ods-grid" aria-label="Objetivos de Desenvolvimento Sustentável">
  <li><a href="./ods1.html"><img src="./assets/ods1.png" alt="ODS 1 — Erradicação da pobreza"></a></li>
  <li><img src="./assets/ods2.png" alt="ODS 2 — Fome zero e agricultura sustentável"></li>
  <li><a href="./ods3.html"><img src="./assets/ods3.png" alt="ODS 3 — Saúde e bem-estar"></a></li>
  <li><img src="./assets/ods4.png" alt="ODS 4 — Educação de qualidade"></li>
  <li><img src="./assets/ods5.png" alt="ODS 5 — Igualdade de gênero"></li>
  <li><img src="./assets/ods6.png" alt="ODS 6 — Água potável e saneamento"></li>
  <li><img src="./assets/ods7.png" alt="ODS 7 — Energia limpa e acessível"></li>
  <li><img src="./assets/ods8.png" alt="ODS 8 — Trabalho decente e crescimento econômico"></li>
  <li><img src="./assets/ods9.png" alt="ODS 9 — Indústria, inovação e infraestrutura"></li>
  <li><img src="./assets/ods10.png" alt="ODS 10 — Redução das desigualdades"></li>
  <li><img src="./assets/ods11.png" alt="ODS 11 — Cidades e comunidades sustentáveis"></li>
  <li><img src="./assets/ods12.png" alt="ODS 12 — Consumo e produção responsáveis"></li>
  <li><img src="./assets/ods13.png" alt="ODS 13 — Ação contra a mudança global do clima"></li>
  <li><img src="./assets/ods14.png" alt="ODS 14 — Vida na água"></li>
  <li><img src="./assets/ods15.png" alt="ODS 15 — Vida terrestre"></li>
  <li><img src="./assets/ods16.png" alt="ODS 16 — Paz, justiça e instituições eficazes"></li>
  <li><img src="./assets/ods17.png" alt="ODS 17 — Parcerias e meios de implementação"></li>
  <li><img src="./assets/ods18.png" alt="ODS 18 — Igualdade étnico-racial"></li>
</ul>
