export default {
  title: "PPAG × ODS | Minas Gerais",
  root: "src",
  style: "style.css",
  preserveExtension: false,
  dynamicPaths: ["/ods1", "/ods3", "/municipal2", "/municipal6"],
  sidebar: false,
  header: '<nav class="topbar" aria-label="Navegação principal"><a class="brand" href="./">PPAG <span>×</span> ODS <small>MINAS GERAIS</small></a><div><a href="./">Todos os ODS</a><a href="./ods1.html">ODS 1</a><a href="./ods1.html#indicadores">Pobreza</a></div></nav>',
  pages: [
    {name: "ODS 1 · Execução orçamentária", path: "/ods1"},
    {name: "ODS 3 · Saúde e bem-estar", path: "/ods3"},
    {name: "Indicadores de pobreza", path: "/indicadores"}
  ],
  footer: 'Painel de análise independente · <a href="https://www.un.org/sustainabledevelopment/news/communications-material/">Ícones dos ODS: Nações Unidas</a> · <a href="https://www.undp.org/pt/brazil/news/ods-18-marca-escolhida-enfatiza-jornada-coletiva-da-luta-pela-igualdade-etnico-racial">Marca ODS 18: Brenda Gomes Virgens / PNUD</a>'
};
