import pandas as pd
import json
import sys

YEAR = sys.argv[1]
MICRODATA_PATH = f"./microdados/microdados_enem_{YEAR}/DADOS/MICRODADOS_ENEM_{YEAR}.csv"
QUESTIONS_PATH = f"./microdados//microdados_enem_{YEAR}/DICIONÁRIO/Dicionário_Microdados_Enem_{YEAR}.xlsx"
columns = ["CO_PROVA_CN","CO_PROVA_CH","CO_PROVA_LC","CO_PROVA_MT","TX_RESPOSTAS_CN","TX_RESPOSTAS_CH","TX_RESPOSTAS_LC","TX_RESPOSTAS_MT","TX_GABARITO_CN","TX_GABARITO_CH","TX_GABARITO_LC","TX_GABARITO_MT"]

data = {
    "CH": {
        "total": 0,
        "code": None,
        "right_count": [ 0 for i in range(45) ]
    },
    "CN": {
        "total": 0,
        "code": None,
        "right_count": [ 0 for i in range(45) ]
    },
    "LC": {
        "total": 0,
        "code": None,
        "right_count": [ 0 for i in range(45) ]
    },
    "MT": {
        "total": 0,
        "code": None,
        "right_count": [ 0 for i in range(45) ]
    }
}


def count_answers(row, subject):
    if row[f"CO_PROVA_{subject}"] == data[subject]["code"]:
        data[subject]["total"] += 1
        for i in range(45):
            if row[f"TX_RESPOSTAS_{subject}"][i] == row[f"TX_GABARITO_{subject}"][i]:
                data[subject]["right_count"][i] += 1


questions = pd.read_excel(QUESTIONS_PATH, header=2, names=["NOME DA VARIÁVEL", "Descrição", "Categoria", "Description", "Tamanho", "Tipo"])
df = questions.ffill()
df["Description"] = df["Description"].apply(lambda row: str(row).lower())

for cat in data:
    data[cat]["code"] = df[ (df["NOME DA VARIÁVEL"] == f"CO_PROVA_{cat}") & ((df["Description"] == "amarela") | (df["Description"] == "amarelo")) ]["Categoria"].iloc[0]

del df
del questions

for chunk in pd.read_csv(MICRODATA_PATH, sep=';', encoding="ISO-8859-1", chunksize=5*(10**5)):
    df = chunk.drop("TP_LINGUA", axis=1)
    df = df.dropna(subset=columns)
    df = df[(df["CO_PROVA_CH"] == data["CH"]["code"]) | (df["CO_PROVA_CN"] == data["CN"]["code"]) | (df["CO_PROVA_LC"] == data["LC"]["code"]) | (df["CO_PROVA_MT"] == data["MT"]["code"])]

    for index, row in df.iterrows():
        for cat in data:
            count_answers(row, cat)


with open("./result.json") as f:
    result_json = json.load(f)

result_json[YEAR] = data

print(result_json)

with  open("./result.json", 'w') as f:
    json.dump(result_json, f)
