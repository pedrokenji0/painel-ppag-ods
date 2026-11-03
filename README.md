# PPAG × ODS · Minas Gerais

Catálogo dos 17 ODS globais e do ODS 18 brasileiro. O ODS 1 tem painel de execução orçamentária estadual e indicadores de pobreza. O ODS 3 compara indicadores de saúde de Minas Gerais e do Brasil. Usa Observable Framework e Plot no navegador e Pandas para preparar os dados.

## Rodar

```powershell
npm.cmd ci
npm.cmd run dev
```

Para abrir o build estático:

```powershell
npm.cmd run build
python -m http.server 8000 --directory dist
```

Acesse [localhost:8000](http://localhost:8000). O build usa os JSONs versionados. Publique somente o conteúdo de `dist/` em hospedagem estática. Na Vercel, use o preset **Other**, o comando `npm run build` e a saída `dist`.

## Fontes e critérios

- **Execução:** [SIAFI-MG 2025](https://www.dados.mg.gov.br/dataset/dados-armazem-siafi-2025) e [SIAFI-MG 2026](https://www.dados.mg.gov.br/dataset/dados-armazem-siafi-2026), recurso `execucao`. O pago usa `vlr_pago_orcamentario`. Os totais somam os movimentos em centavos, por código de programa e exercício, de todas as unidades executoras. Restos a pagar de exercícios anteriores estão fora do recorte. Ausência de registros é diferente de valor zero.
- **Vínculos e previsão:** programas ativos marcados com ODS 1 nos Excel do PPAG 2025 pós-emendas e da matriz PPAG 2026–2029. A previsão é anual. Cada programa é contado uma vez, com sua execução integral. A classificação temática não estima a parcela exclusiva de cada ODS nem o impacto do gasto.
- **Pobreza:** tabelas [5817](https://sidra.ibge.gov.br/tabela/5817), [5840](https://sidra.ibge.gov.br/tabela/5840) e [5877](https://sidra.ibge.gov.br/tabela/5877) do SIDRA para Minas Gerais e Brasil. O painel usa o recorte estadual.
- **Saúde:** tabelas [6694](https://sidra.ibge.gov.br/tabela/6694), [6695](https://sidra.ibge.gov.br/tabela/6695), [6696](https://sidra.ibge.gov.br/tabela/6696) e [8415](https://sidra.ibge.gov.br/tabela/8415) do SIDRA. Os indicadores são mortalidade materna, mortalidade em menores de 5 anos, mortalidade neonatal e incidência de hepatite B. Cada série mantém o período e a unidade da fonte.
- **Ícones:** versões em português dos ODS 1–17 fornecidas com o protótipo. A marca do ODS 18 foi criada por Brenda Gomes Virgens e divulgada pelo PNUD. [Diretrizes de uso](https://www.un.org/sustainabledevelopment/news/communications-material/).

## Atualizar o recorte

Requer Python 3.11 ou superior. Passe a pasta com os dois Excel de vínculos. O script baixa os arquivos públicos do SIAFI e do SIDRA, valida os recortes e gera os JSONs de `src/data/`. Sem `--atualizar`, reaproveita downloads em `.dados/`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/preparar_dados.py "PASTA_DOS_EXCEL" --atualizar
npm.cmd run build
```
