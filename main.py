import os
import subprocess


def get_commit_graph(repo_path):
    """Получить граф коммитов в формате (commit_hash, parent_hash)."""
    cmd = ["git", "-C", repo_path, "log", "--pretty=format:%H"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Ошибка при выполнении команды git log.")
    commits = dict()
    a = result.stdout.splitlines()
    a.pop()
    i = len(a)
    for line in result.stdout.splitlines():
        if(not(line in commits.keys())):
            commits[line] = i
            i-=1
    cmd = ["git", "-C", repo_path, "log", "--pretty=format:%H %P"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Ошибка при выполнении команды git log.")

    commit_graph = []
    a=result.stdout.splitlines()
    a.pop()
    a.reverse()
    for line in a:
        parts = line.split(" ")
        for i in  range (len(parts)):
            parts[i] = commits[parts[i]]
        commit_hash = parts[0]
        parent_hashes = parts[1:]
        for parent in parent_hashes:
            commit_graph.append((parent, commit_hash))
    return commit_graph


def generate_plantuml(commit_graph):
    """Генерация кода PlantUML для графа зависимостей."""
    lines = ["@startuml", "digraph G {"]
    for commit, parent in commit_graph:
        lines.append(f'  "{commit}" -> "{parent}"')
    lines.append("}")
    lines.append("@enduml")
    return "\n".join(lines)


def save_to_file(file_path, content):
    """Сохранение контента в файл."""
    with open(file_path, "w") as file:
        file.write(content)


def visualize_with_plantuml(plantuml_path, file_path):
    """Визуализация графа с помощью PlantUML."""
    cmd = ["java", "-jar", plantuml_path, file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("Ошибка при выполнении PlantUML.")
    print(f"Граф успешно визуализирован. Результат сохранен рядом с файлом {file_path}.")


def main():
    # Укажите параметры здесь
    plantuml_path = "C:/Programs/plantuml-1.2024.7.jar"  # Путь к программе PlantUML
    repo_path = ("C:/Users/Alexander/GitHub/kispython")  # Путь к анализируемому git-репозиторию
    output_file = "C:/Users/Alexander/PycharmProjects/GHGRAPHICS/output.puml"  # Путь к файлу-результату

    # Проверка существования репозитория
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"Указанный путь {repo_path} не является git-репозиторием.")
        return

    try:
        # Получение графа зависимостей
        commit_graph = get_commit_graph(repo_path)

        # Генерация PlantUML-кода
        plantuml_code = generate_plantuml(commit_graph)

        # Сохранение результата в файл
        save_to_file(output_file, plantuml_code)

        # Вывод кода на экран
        print(plantuml_code)

        # Визуализация графа с помощью PlantUML
        visualize_with_plantuml(plantuml_path, output_file)

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
