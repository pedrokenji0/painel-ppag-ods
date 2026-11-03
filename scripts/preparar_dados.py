"""Gera os recortes dos ODS 1 e 3 a partir do PPAG, SIAFI-MG e SIDRA."""
import argparse
import json
from pathlib import Path
from shutil import copyfileobj
from urllib.request import urlopen

import pandas as pd


RAIZ = Path(__file__).resolve().parents[1]
PORTAL = "https://www.dados.mg.gov.br"
BASES = {
    2025: (
        "programas_planejamento_pós emenda 2025_ODS.xlsx",
        "programas_planejamento",
        "PPAG 2025 pós-emendas",
        "38c3c647-df4e-48a8-8887-87b7f27be451",
        "3e387b87-a7a2-4f3e-ac6c-ab9b06704a24",
    ),
    2026: (
        "Matriz de ODSs por OU e programa.xlsx",
        "Planilha1",
        "Matriz de ODS do PPAG 2026–2029",
        "3ac62062-6b32-4623-9298-9bf949a68d04",
        "a6ebbe98-59b6-498f-9e27-106b88995dcf",
    ),
}
MEDIDAS = {
    "vlr_pago_orcamentario": "pago",
    "vlr_liquidado": "liquidado",
    "vlr_empenhado": "empenhado",
}
TABELAS_POBREZA = {"5817": ("1.1.1", None), "5840": ("1.1.1", None), "5877": ("1.2.1", None)}
TABELAS_SAUDE = {
    "6694": ("3.1.1", "9730"),
    "6695": ("3.2.1", "9731"),
    "6696": ("3.2.2", "9732"),
    "8415": ("3.3.4", "12381"),
}


def obter(url, caminho, atualizar):
    if atualizar or not caminho.exists():
        temporario = caminho.with_suffix(".part")
        with urlopen(url, timeout=90) as resposta, temporario.open("wb") as arquivo:
            copyfileobj(resposta, arquivo)
        temporario.replace(caminho)
    return caminho


def centavos(valores):
    if not valores.str.fullmatch(r"-?\d+(\.\d{1,2})?").fillna(False).all():
        raise ValueError("Valor monetário inválido ou com precisão superior a centavos")
    return pd.to_numeric(valores, errors="raise").mul(100).round().astype("int64")


def ler_vinculos(arquivo, aba, ano):
    dados = pd.read_excel(arquivo, sheet_name=aba, dtype="string")
    ativos = dados["Exclusão Lógica do Programa"].str.strip().str.casefold().eq("não")
    ods1 = dados["Título do Objetivo de Desenvolvimento Sustentável"].str.match(r"^1\s*-")
    colunas = {
        "Código do Programa": "codigo",
        "Nome do Programa": "nome",
        "Unidade Orçamentária Responsável pelo Programa": "unidade",
        f"Previsão Orçamentária {ano}": "previsto",
    }
    programas = dados.loc[ativos & ods1, list(colunas)].rename(columns=colunas)
    programas["codigo"] = programas["codigo"].str.strip().str.lstrip("0")
    if programas.empty or not programas["codigo"].str.fullmatch(r"\d+").fillna(False).all():
        raise ValueError(f"Vínculos vazios ou código de programa inválido em {arquivo.name}")
    programas = programas.drop_duplicates()
    if programas["codigo"].duplicated().any() or programas.isna().any().any():
        raise ValueError(f"Cadastro ou previsão ausente ou conflitante em {arquivo.name}")
    programas["previsto"] = centavos(programas["previsto"])
    return programas


def ler_execucao(arquivo, ano, codigos):
    chaves = ["programa_cod", "mes_cod"]
    partes = []
    meses = set()
    with pd.read_csv(arquivo, usecols=["ano", *chaves, *MEDIDAS], dtype="string", chunksize=200_000) as leitor:
        for lote in leitor:
            if not lote["ano"].eq(str(ano)).fillna(False).all():
                raise ValueError(f"Exercício inesperado em {arquivo.name}")
            meses.update(lote["mes_cod"].unique())
            lote["programa_cod"] = lote["programa_cod"].str.strip().str.lstrip("0")
            selecionados = lote.loc[lote["programa_cod"].isin(codigos), [*chaves, *MEDIDAS]].copy()
            for medida in MEDIDAS:
                selecionados[medida] = centavos(selecionados[medida])
            partes.append(selecionados.groupby(chaves)[list(MEDIDAS)].sum())
    meses = sorted(map(int, meses))
    if not meses or meses[-1] > 12 or meses != list(range(1, meses[-1] + 1)):
        raise ValueError(f"Meses ausentes ou inválidos em {arquivo.name}")
    movimentos = pd.concat(partes).groupby(level=[0, 1]).sum().rename(columns=MEDIDAS)
    if movimentos.empty:
        raise ValueError(f"Nenhum código do PPAG encontrado em {arquivo.name}")
    return meses[-1], movimentos


def preparar_execucao(origem, cache, atualizar):
    exercicios = []
    for ano, (nome, aba, vinculos, dataset, recurso) in BASES.items():
        programas = ler_vinculos(origem / nome, aba, ano)
        fonte = f"{PORTAL}/dataset/dados-armazem-siafi-{ano}/resource/{recurso}"
        url = f"{PORTAL}/dataset/{dataset}/resource/{recurso}/download/execucao.csv.gz"
        arquivo = obter(url, cache / f"execucao-{ano}.csv.gz", atualizar)
        ultimo_mes, movimentos = ler_execucao(arquivo, ano, programas["codigo"])
        codigos = set(movimentos.index.get_level_values(0))
        registros = programas.to_dict('records')
        for programa in registros:
            codigo = programa["codigo"]
            mensal = movimentos.loc[codigo] if codigo in codigos else None
            programa["meses"] = [] if mensal is None else sorted(
                (dict(mes=int(mes), **valores) for mes, valores in mensal.to_dict("index").items()),
                key=lambda registro: registro["mes"],
            )
            for medida in MEDIDAS.values():
                programa[medida] = None if mensal is None else int(mensal[medida].sum())
        exercicios.append({
            "ano": ano,
            "ultimoMes": ultimo_mes,
            "parcial": ultimo_mes < 12 or ano >= pd.Timestamp.today().year,
            "fonte": fonte,
            "vinculos": vinculos,
            "programas": registros,
        })
    return exercicios


def preparar_series(cache, atualizar, tabelas):
    series = []
    for codigo, (indicador, variavel) in tabelas.items():
        url = f"https://apisidra.ibge.gov.br/values/t/{codigo}/n1/1/n3/31/v/all/p/all"
        arquivo = obter(url, cache / f"sidra-{codigo}.json", atualizar)
        dados = pd.DataFrame(json.loads(arquivo.read_text(encoding="utf-8-sig"))[1:])
        if variavel is not None:
            dados = dados.loc[dados["D2C"].eq(variavel)]
        if codigo == "8415":
            dados = dados.loc[dados["D4C"].eq("95253")]  # Total dos grupos de idade
        if (set(dados["D1C"]) != {"1", "31"} or dados.duplicated(["D1C", "D3C"]).any()
                or not dados["D3C"].str.fullmatch(r"\d{4}").all()
                or dados["D2C"].nunique() != 1 or dados["MC"].nunique() != 1):
            raise ValueError(f"Série anual ou recorte inesperado na tabela SIDRA {codigo}")
        valores = pd.to_numeric(dados["V"].replace({"..": None, "...": None, "-": 0}), errors="raise")
        series.append({
            "id": codigo,
            "indicador": indicador,
            "nome": dados["D2N"].iat[0],
            "unidade": dados["MN"].iat[0],
            "pontos": [
                {"ano": int(ano), "territorio": territorio, "valor": None if pd.isna(valor) else float(valor)}
                for ano, territorio, valor in zip(dados["D3C"], dados["D1N"], valores)
            ],
        })
    return series


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("origem", type=Path, help="Pasta com os Excel de vínculos do PPAG")
    parser.add_argument("--atualizar", action="store_true", help="Baixar novamente as fontes públicas")
    args = parser.parse_args()
    cache = RAIZ / ".dados"
    cache.mkdir(exist_ok=True)
    execucao = preparar_execucao(args.origem, cache, args.atualizar)
    pobreza = preparar_series(cache, args.atualizar, TABELAS_POBREZA)
    saude = preparar_series(cache, args.atualizar, TABELAS_SAUDE)
    destino = RAIZ / "src" / "data"
    destino.mkdir(parents=True, exist_ok=True)
    for nome, dados in [("execucao-ods1", execucao), ("series-ods1", pobreza), ("series-ods3", saude)]:
        (destino / f"{nome}.json").write_text(
            json.dumps(dados, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    for exercicio in execucao:
        print(f"{exercicio['ano']}: {len(exercicio['programas'])} programas; mês {exercicio['ultimoMes']}")


if __name__ == "__main__":
    main()
