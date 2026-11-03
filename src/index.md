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
  <h1>Planejamento e<br>desenvolvimento sustentável</h1>
  <p>Explore os Objetivos de Desenvolvimento Sustentável e acompanhe a execução dos programas estaduais vinculados.</p>
  <div class="hero-links"><a class="primary" href="#objetivos">Explorar objetivos</a></div></div>
  <aside class="catalog-feature"><p class="eyebrow">PRIMEIRO PAINEL · ODS 1</p>
    <strong>${resumo}</strong><p>pagos em ${base.ano} nos programas estaduais vinculados à erradicação da pobreza.</p>
    <a href="./ods1.html">Ver execução e programas →</a>
  </aside>
</section>

## Objetivos

O catálogo reúne os 17 objetivos globais e o ODS 18, iniciativa brasileira pela igualdade étnico-racial. O ODS 1 já tem dados de execução e indicadores de pobreza.

<ul class="ods-grid" aria-label="Objetivos de Desenvolvimento Sustentável">
  <li><a href="./ods1.html"><img src="./assets/ods1.png" width="70" height="70" alt=""><strong>Erradicação da pobreza</strong><small>Dados disponíveis →</small></a></li>
  <li><img src="./assets/ods2.png" width="70" height="70" alt=""><strong>Fome zero e agricultura sustentável</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods3.png" width="70" height="70" alt=""><strong>Saúde e bem-estar</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods4.png" width="70" height="70" alt=""><strong>Educação de qualidade</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods5.png" width="70" height="70" alt=""><strong>Igualdade de gênero</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods6.png" width="70" height="70" alt=""><strong>Água potável e saneamento</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods7.png" width="70" height="70" alt=""><strong>Energia limpa e acessível</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods8.png" width="70" height="70" alt=""><strong>Trabalho decente e crescimento econômico</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods9.png" width="70" height="70" alt=""><strong>Indústria, inovação e infraestrutura</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods10.png" width="70" height="70" alt=""><strong>Redução das desigualdades</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods11.png" width="70" height="70" alt=""><strong>Cidades e comunidades sustentáveis</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods12.png" width="70" height="70" alt=""><strong>Consumo e produção responsáveis</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods13.png" width="70" height="70" alt=""><strong>Ação contra a mudança global do clima</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods14.png" width="70" height="70" alt=""><strong>Vida na água</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods15.png" width="70" height="70" alt=""><strong>Vida terrestre</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods16.png" width="70" height="70" alt=""><strong>Paz, justiça e instituições eficazes</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods17.png" width="70" height="70" alt=""><strong>Parcerias e meios de implementação</strong><small>Em preparação</small></li>
  <li><img src="./assets/ods18.png" width="70" height="70" alt=""><strong>Igualdade étnico-racial</strong><small>Brasil · em preparação</small></li>
</ul>
