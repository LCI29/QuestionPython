# Сохранить Excel как .csv, удалив все строки, которые не являются вопросами, ответами
# или разделительными пустыми строками

import csv

# Настройки

# Путь к файлу .csv
FILE_LOC = "D:\\Dev\\Android\\MetroTest\\For MetroTest\\Test Files\\Butovo_2021.csv"

# Разделитель в файле .csv
CSV_FILE_DELIMITER = ";"

# Максимальная длина кода
MAX_CODE_LENGTH = 7

# Вопросы c кодами
HAS_CODE = True

# Какой код выдавать, если вопросы без кодов
CODE_STUB = ""


def main():

    with open(FILE_LOC) as file:
        reader = csv.reader(file, delimiter=CSV_FILE_DELIMITER)

        # Флаг для проверки одного и только одного правильного ответа на вопрос
        # Изначально True, потому что строка с 'в' требует чтобы флаг был в True
        was_right = True

        for row in reader:
            # Столбец А в файле Excel - в, п, о или пустой
            marker = row[0].strip()

            # Проверяем какой маркер
            # в - строка с вопросом
            if marker == 'в':
                # Если в предыдущем вопросе не было строки с правильным ответом
                if not was_right:
                    raise Exception("No right answer in last question")
                # Иначе начинается новый вопрос
                else:
                    was_right = False
                    # Разбиваем строку по точке, первая часть - это код вопроса
                    code = row[1].split('.')[0] if HAS_CODE else CODE_STUB
                    # Длина кода не может быть более количества символов в настройках
                    # (если подразумевается, что впоросы с кодом)
                    if len(code) > MAX_CODE_LENGTH and HAS_CODE:
                        raise Exception("Incorrect code")
                    # Вторая часть - это текст вопроса, либо (если без кодов) весь второй столбец - это текст вопроса
                    text = row[1].split('.', maxsplit=1)[1].strip() if HAS_CODE else row[1].strip()
                    print(code_line_question(code, text))

            # о - строка с неправильным ответом
            elif marker == 'о':
                # Извлечение текста ответа и небольшая чистка от лишних артефактов
                text = row[1].strip().rstrip(";.").lstrip("-").strip()
                print(code_line_answer(text))

            # п - строка с правильным ответом
            elif marker == 'п':
                # Извлечение текста ответа и небольшая чистка от лишних артефактов
                text = row[1].strip().rstrip(";.").lstrip("-").strip()
                # Если в этом вопросе еще не было строки с правильным ответом, то печатаем, иначе - исключение
                if not was_right:
                    was_right = True
                    print(code_line_answer(text, is_right=True))
                else:
                    raise Exception("More than one right answer in the question")

            # Ничего - пустая строка между блоками из вопроса и ответов
            elif marker == "":
                # Печать пустой строки между вопросами
                print()

            # Чего-либо еще не должно быть, выбрасываем исключение
            else:
                raise Exception("Incorrect marker")


# Generates code line for question
def code_line_question(code, text):
    return f'allQuestions.add(new Question("{code}", "{text}"));'


# Generates code line for answer
def code_line_answer(answer_text, is_right=False):
    return f'allQuestions.get(allQuestions.size() - 1).answers.add(new Answer("{answer_text}"{", true" if is_right else ""}));'


main()
