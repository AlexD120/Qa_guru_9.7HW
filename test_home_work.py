import os
from zipfile import ZipFile
import pandas as pd
import fitz  # PyMuPDF
import pytest


"""СОЗДАЕМ ФИКСТУРУ С ПУТЕМ И ИМЕНЕМ АРХИВА"""
@pytest.fixture
def zip_arch():
    return "resources/archive.zip"


"""ТЕСТ КОТОРЫЙ ПРИНИМАЕТ ФАЙЛЫ И ДОБАВЛЯЕТ ИХ В НОВЫЙ  СОЗДАВАЯ ДИРЕКТОРИЮ ЕСЛИ ЕЕ НЕТ"""
def test_creat_archive(zip_arch):
    file_to_arch_pdf = [
        "tmp/Python Testing with Pytest (Brian Okken).pdf",
        "tmp/file_example_XLSX_501.csv",
        "tmp/file_example_XLSX_50 (1).xlsx"
    ]  # - путь к файлам
    directory = os.path.dirname(zip_arch)
    # Проверяем существование каталога, если нет, создаем его
    if not os.path.exists(directory):
        os.makedirs(directory)
    with ZipFile(zip_arch, "w") as zipfile:
        for file in file_to_arch_pdf:
            zipfile.write(file)


    """ТЕСТ КОТОРЫЙ ОТКРЫВАЕТ ФАЙЛ PDF В АРХИВЕ, ИЩЕТ СТРАНИЦУ, ТЕКСТ И ПРОИЗВОДИТ ПРОВЕРКА ТЕКСТА НА СТРАНИЦЕ"""
def test_check_pdf(zip_arch):
    file_in_arch = "tmp/Python Testing with Pytest (Brian Okken).pdf"
    page_number = 2  # - номер страницы
    expected_text = "About the Pragmatic Bookshelf"  # - текст для проверки
    with ZipFile(zip_arch, "r") as zipfile:
        with zipfile.open(file_in_arch) as file:
            pdf_document = fitz.open(file)
            page = pdf_document[page_number]
            text = page.get_text()
            assert expected_text in text


    """ТЕСТ КОТОРЫЙ ПРИНИМАЕТ ПАРАМЕТРЫ ПРОВЕРКИ, ОТКРЫВАЕТ ФАЙЛ, РАЗДЕЛЯЕТ СТРОКИ, БЕРЕТ АКТУАЛЬНЫЕ ДАННЫЕ И ПРОВЕРЯЕТ"""
def test_check_csv(zip_arch):
    file_in_arch_csv = "tmp/file_example_XLSX_501.csv"
    expected_data_csv = ('Mara', 1, 'First Name')  # данные для проверки
    with ZipFile(zip_arch, "r") as zipfile:
        with zipfile.open(file_in_arch_csv) as file:
            doc_file = pd.read_csv(file, delimiter=';')
            expected_value, row_index, column_name = expected_data_csv
            actual_value = doc_file.at[row_index, column_name]
            assert actual_value == expected_value


    """ТЕСТ КОТОРЫЙ ПРИНИМАЕТ ПАРАМЕТРЫ ПРОВЕРКИ, ОТКРЫВАЕТ ФАЙЛ, БЕРЕТ АКТУАЛЬНЫЕ ДАННЫЕ И ПРОВЕРЯЕТ"""
def test_check_xlsx(zip_arch):
    file_in_arch_excel = "tmp/file_example_XLSX_50 (1).xlsx"
    expected_data_excel = ('Mara', 1, 'First Name')  # данные для проверки
    with ZipFile(zip_arch, "r") as zipfile:
        with zipfile.open(file_in_arch_excel) as file:
            doc_file = pd.read_excel(file)
            expected_value, row_index, column_name = expected_data_excel
            actual_value = doc_file.at[row_index, column_name]
            assert actual_value == expected_value


