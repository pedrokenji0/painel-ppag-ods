"""Atualiza as séries municipais do ODS 3 da FJP e a malha do IBGE."""
import csv
import gzip
import io
import json
import re
import time
from pathlib import Path
from urllib.request import Request, urlopen


RAIZ = Path(__file__).resolve().parents[1]
FJP = "https://apidados.fjp.mg.gov.br/api"
MALHA = (
    "https://servicodados.ibge.gov.br/api/v3/malhas/estados/31"
    "?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio"
)
ANOS = range(2020, 2026)
INDICADORES = {
    586: "Cobertura vacinal de febre amarela em menores de 1 ano",
    587: "Cobertura vacinal de pentavalente em menores de 1 ano",
    588: "Cobertura vacinal de poliomielite em menores de 1 ano",
    589: "Cobertura vacinal de tríplice viral da população de 1 ano de idade",
    591: "Número médio de médicos por 1.000 habitantes",
    592: "Proporção da população atendida pela Estratégia de Saúde da Família",
    593: "Proporção de internações por condições sensíveis à atenção básica",
    594: "Proporção de internações por diabetes mellitus e suas complicações na população de 30 anos ou mais",
    595: "Proporção de internações por doenças cérebro vasculares na população de 40 anos ou mais",
    596: "Proporção de internações por doenças de veiculação hídrica",
    597: "Proporção de internações por doenças relacionadas ao saneamento ambiental inadequado",
    598: "Proporção de nascidos vivos com baixo peso",
    599: "Proporção de nascidos vivos cujas mães realizaram 7 ou mais consultas de pré-natal",
    600: "Proporção de óbitos por causas mal definidas",
    601: "Taxa de mortalidade por doenças crônicas não transmissíveis na população de 30 a 69 anos",
}


def baixar(url, dados=None):
    requisicao = Request(url, headers={"User-Agent": "Painel-PPAG-ODS/1.0"})
    if dados is not None:
        requisicao.data = json.dumps(dados).encode()
        requisicao.add_header("Content-Type", "application/json")
    with urlopen(requisicao, timeout=60) as resposta:
        corpo = resposta.read()
        if corpo.startswith(b"\x1f\x8b"):
            corpo = gzip.decompress(corpo)
        return corpo.decode("utf-8-sig")


def area_assinada(anel):
    return sum(x * v - u * y for (x, y), (u, v) in zip(anel, anel[1:]))


def main():
    malha = json.loads(baixar(MALHA))
    codigos = {f["properties"]["codarea"] for f in malha["features"]}
    if len(codigos) != 853 or len(malha["features"]) != 853:
        raise ValueError("Malha municipal de Minas Gerais com cobertura inesperada")
    for feicao in malha["features"]:
        g = feicao["geometry"]
        poligonos = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        # D3 usa sentido horário no anel externo e anti-horário nos furos.
        for poligono in poligonos:
            for i, anel in enumerate(poligono):
                if (area_assinada(anel) > 0) == (i == 0):
                    anel.reverse()

    filtro = f"{FJP}/filtros/obterFiltro"
    catalogo = json.loads(baixar(filtro, {"action": "ind2", "request_type": 0, "ind_data": {"tipo": 20}}))
    nomes = {item["id"]: item["label"].strip() for item in catalogo}
    if any(nomes.get(i) != nome for i, nome in INDICADORES.items()):
        raise ValueError("O catálogo da FJP diverge dos indicadores selecionados")
    localidades = json.loads(baixar(filtro, {"action": "geo2", "request_type": 0, "geo_data": {"tipo": 1}}))
    ids = sorted({item["id"] for item in localidades if item["group"] == "MG"})
    if len(ids) != 853:
        raise ValueError("Catálogo municipal da FJP com cobertura inesperada")

    por_nome = {nome: str(i) for i, nome in INDICADORES.items()}
    series = {}
    municipios = {}
    for inicio in range(0, len(ids), 50):
        csv_texto = baixar(f"{FJP}/dados/obterDados", {
            "action": "getData", "request_type": 0, "formato": "csv",
            "geo_data": {"tipo": 1, "ids_registros": ids[inicio:inicio + 50]},
            "ind_data": {"tipo": 20, "ids_registros": list(INDICADORES)},
            "tpo_data": {"tipo": 1, "ids_registros": [ano * 10000 + 1 for ano in ANOS]},
        })
        for linha in csv.DictReader(io.StringIO(csv_texto), delimiter=";"):
            codigo = linha["Código da Localidade"]
            if codigo not in codigos or linha["Tipo de Localidade"] != "Município":
                raise ValueError(f"Localidade fora da malha de Minas Gerais: {codigo}")
            municipios[codigo] = linha["Localidade"].removesuffix(" - MG")
            nome = linha["Indicador"].strip()
            i = por_nome[nome]
            unidade = linha["Unidade de medida"].strip()
            serie = series.setdefault(i, {"nome": nome, "unidade": unidade, "anos": {}})
            if serie["unidade"] != unidade:
                raise ValueError(f"Unidade inconsistente para o indicador {i}")
            for ano in map(str, ANOS):
                valor = (linha.get(ano) or "").strip()
                if valor in ("", "-", "..", "...", "–"):
                    continue
                if not re.fullmatch(r"-?[\d.]+(?:,\d+)?%?", valor):
                    raise ValueError(f"Valor inesperado para {i} em {codigo}: {valor}")
                valores = serie["anos"].setdefault(ano, {})
                if codigo in valores:
                    raise ValueError(f"Valor repetido para {i} em {codigo}, {ano}")
                valores[codigo] = float(valor.removesuffix("%").replace(".", "").replace(",", "."))
        print(f"Municípios consultados: {min(inicio + 50, len(ids))}/{len(ids)}", flush=True)
        time.sleep(0.6)

    if municipios.keys() != codigos or set(series) != set(map(str, INDICADORES)):
        raise ValueError("A exportação da FJP não cobriu todos os municípios e indicadores")
    for i, serie in sorted(series.items()):
        if not serie["anos"]:
            raise ValueError(f"Indicador {i} sem valores")
        print(i, {ano: len(valores) for ano, valores in sorted(serie["anos"].items())})
    for nome, dados in {
        "malha-mg": malha,
        "saude-municipal": {"municipios": municipios, "series": series},
    }.items():
        destino = RAIZ / "src" / "data" / f"{nome}.json"
        destino.write_text(json.dumps(dados, ensure_ascii=False, separators=(",", ":")) + "\n",
                           encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
