from github import Github
import base64

token = "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"
repo_name = 'svb505/statistick'

def update_file(file_path: str, increment: int,token: str = token, repo_name: str = repo_name, commit_message: str = "Update number"):
    # Инициализация клиента
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Получаем содержимое файла
    file_content = repo.get_contents(file_path)
    decoded_content = base64.b64decode(file_content.content).decode("utf-8")

    # Парсим и увеличиваем число
    try:
        number = int(decoded_content.strip())
    except ValueError:
        raise ValueError("Содержимое файла не является целым числом.")

    number += increment

    # Обновляем файл
    repo.update_file(
        path=file_path,
        message=commit_message,
        content=str(number),
        sha=file_content.sha
    )

    print(f"✅ Файл '{file_path}' обновлён. Новое значение: {number}")
def update_elpsed(file_path: str, increment: int,token: str = token, repo_name: str = repo_name, commit_message: str = "Update number"):
    # Инициализация клиента
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Получаем содержимое файла
    file_content = repo.get_contents(file_path)
    decoded_content = base64.b64decode(file_content.content).decode("utf-8")

    # Парсим и увеличиваем число
    try:
        number = int(decoded_content.strip())
    except ValueError:
        raise ValueError("Содержимое файла не является целым числом.")

    if int(increment) > int(number):
        number += increment

        # Обновляем файл
        repo.update_file(
            path=file_path,
            message=commit_message,
            content=str(number),
            sha=file_content.sha
        )
        print(f"✅ Файл '{file_path}' обновлён. Новое значение: {number}")