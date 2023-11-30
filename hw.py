from zipfile import ZipFile
import pandas as pd
import fitz  # PyMuPDF

"""СОЗДАЕМ ФУНКЦИЮ КОТОРАЯ ПРИНИМАЕТ ФАЙЛЫ И ДОБАВЛЯЕТ ИХ В НОВЫЙ АРХИВ"""
def creat_archive(zip_arch, file_to_arch):
    with ZipFile(zip_arch, "w") as zipfile:
        for file in file_to_arch:
            zipfile.write(file)


file_to_arch_pdf = [
    "tmp/Python Testing with Pytest (Brian Okken).pdf",
    "tmp/file_example_XLSX_501.csv",
    "tmp/file_example_XLSX_50 (1).xlsx"
]  # - путь к файлам
zip_arch = "resources/archive.zip"  # - путь и имя для архива
creat_archive(zip_arch, file_to_arch_pdf)

"""СОЗДАЕМ ФУНКЦИЮ КОТОРАЯ ОТКРЫВАЕТ ФАЙЛ PDF В АРХИВЕ, ИЩЕТ СТРАНИЦУ, ТЕКСТ И ПРОИЗВОДИТ ПРОВЕРКА ТЕКСТА НА СТРАНИЦЕ"""
def check_pdf(zip_arch, file_in_arch, page_num, expected_text):
    with ZipFile(zip_arch, "r") as zipfile:
        with zipfile.open(file_in_arch) as file:
            pdf_document = fitz.open(file)
            page = pdf_document[page_num]
            text = page.get_text()
            assert expected_text in text


"""ПУТЬ К ФАЙЛУ В АРХИВЕ И ДАННЫМ ПРОВЕРКИ"""
file_in_arch = "tmp/Python Testing with Pytest (Brian Okken).pdf"
page_number = 2  # - номер страницы
expected_text = "About the Pragmatic Bookshelf"  # - текст для проверки
check_pdf(zip_arch, file_in_arch, page_number, expected_text)


"""СОЗДАЕМ ФУНКЦИЮ КОТОРАЯ ПРИНИМАЕТ ПАРАМЕТРЫ ПРОВЕРКИ, ОТКРЫВАЕТ ФАЙЛ, РАЗДЕЛЯЕТ СТРОКИ, БЕРЕТ АКТУАЛЬНЫЕ ДАННЫЕ И ПРОВЕРЯЕТ"""
def check_csv(zip_arch, file_in_arch, expected_data):
    expected_value, row_index, column_name = expected_data
    with ZipFile(zip_arch, "r") as zipfile:
        with zipfile.open(file_in_arch) as file:
            doc_file = pd.read_csv(file, delimiter=';')
            actual_value = doc_file.at[row_index, column_name]
            assert actual_value == expected_value

"""ПУТЬ К ФАЙЛУ В АРХИВЕ И ДАННЫМ ПРОВЕРКИ"""
file_in_arch_csv = "tmp/file_example_XLSX_501.csv"
check_params_csv = ('Mara', 1, 'First Name') # - данные для проверки
check_csv(zip_arch, file_in_arch_csv, check_params_csv)



