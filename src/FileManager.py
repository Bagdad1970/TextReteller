import os

class FileManager:

    @staticmethod
    def read_from_file(filepath: str) -> str:
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Файл не найден: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read().strip()

    @staticmethod
    def write_to_file(filepath: str, text: str) -> None:
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(text)
        except IOError as e:
            raise IOError(f"Не удалось записать в файл: {filepath}. Ошибка: {e}")