from PyPDF2 import PdfReader
import sys
import json

YEAR = sys.argv[1]
DAY = sys.argv[2]

TEST_PATH = f"./novas_amarelo/{YEAR}-{DAY}.pdf"

start_page = 1

reader = PdfReader(TEST_PATH)

test_questions = []

i = start_page
while i < len(reader.pages) - 1:
    content = reader.pages[i].extract_text()
    
    if "PROPOSTA DE REDAÇÃO" in content.upper():
        i += 1
        continue

    page_questions = []

    page_questions1 = content.split("QUESTÃO")
    for item in page_questions1:
        for q in item.split("QUESTAO"):
            page_questions.append(q)
    if len(page_questions) <= 1:
        page_questions = content.split("Questão")

    page_questions = page_questions[1:]

    for j in range(len(page_questions)):
        q = page_questions[j].split("\n")[1:]

        if q[-1] == '': q = q[:-1]

        if "AMARELO" in q[-1]: q = q[:-1]

        if j == len(page_questions) - 1:
            if '*' in q[-1]:
               q[-1] = q[-1][:-12]

        merged_q = " ".join( q )

        test_questions.append( merged_q.expandtabs(1) )
    i += 1


if len(test_questions) > 90:
    test_questions = test_questions[5:]

print(test_questions)
print(len(test_questions))

q = input("Save result? (y/n): ")

if q == 'y' or q == 'Y':
    with open("./question_texts.json") as f:
        result_json = json.load(f)

    if not result_json.get(f"{YEAR}"):
        result_json[f"{YEAR}"] = {}

    result_json[f"{YEAR}"][f"P{DAY}"] = test_questions


    with  open("./question_texts.json", 'w') as f:
        json.dump(result_json, f)

