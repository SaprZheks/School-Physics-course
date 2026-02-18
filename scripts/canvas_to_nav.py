import sys
import json
import re

def main():
    if len(sys.argv) < 2:
        return

    arg = sys.argv[1]
    if arg == "Граф физики.canvas":

        with open(arg, "r", encoding="utf-8") as f:
            canvas = json.load(f)
        nodes = {}

        for node in canvas['nodes']:
            # id : [path, taken, inputs, outputs]
            nodes[node['id']] = {
                'path'    : node['file'],
                'taken'   : False,
                'inputs'  : [],
                'outputs' : []
            }

        for link in canvas['edges']:
            nodes[link['toNode']]['inputs'].append(link['fromNode'])
            nodes[link['fromNode']]['outputs'].append(link['toNode'])

        sorted_ids = topologicalSort(nodes).copy()

        content = "# Механика\n"
        content += "<div class=\"hide-links\"></div>\n\n"
        content +="## Кинематика\n"

        for id in sorted_ids:
            name = name_from_path(nodes[id]['path'])
            content += "[[Кирпичики/" + name + "|" + name +"]]" + '\n'
        content
        with open("Навигация по курсу.md", "w", encoding="utf-8") as file:
            file.write(content)
        
        ####################################################
        #                                                  #
        #      РАССТАНОВКА ССЫЛОК ДЛЯ КАЖДОЙ ЗАМЕТКИ       #
        #                                                  #
        ####################################################

        pattern = r"\-{3}[\s\S]*?Уровень[\s\S]*?\-{3}\n" 
        pattern_exists = (
                    r"(\-{3}[\s\S]*?Уровень[\s\S]*?\-{3}\n)"
                    r"<div style=\"display:\s*flex;\s*justify-content:\s*space-between;\">"
                    r"[\s\S]*?"
                    r"</div>\n\n"
        )

        # Все заметки
        for i in range(len(sorted_ids)):
            id = sorted_ids[i]
            path = nodes[id]['path']

            # Формирование строки со ссылками
            new_line = "<div style=\"display: flex; justify-content: space-between;\">"

            # Предыдущая
            if i > 0:
                id_prev = sorted_ids[i-1]
                name_prev = name_from_path(nodes[id_prev]['path'])
                new_line += "<a href=\"Кирпичики/" + name_prev + "\" class=\"internal-link\">Предыдущая</a>"

            # Следующая
            if i < (len(sorted_ids)-1):
                id_next = sorted_ids[i+1]
                name_next = name_from_path(nodes[id_next]['path'])
                new_line += "<a href=\"Кирпичики/" + name_next + "\" class=\"internal-link\" style=\"margin-left: auto;\">Следующая</a>"

            # Конец
            new_line += "</div>\n\n"

            # Чтение заметки
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            # Если ссылки уже есть и их надо просто обновить
            if re.search(pattern_exists, content):
                updated_content = re.sub(pattern_exists, r"\g<1>" + new_line, content)
            else:
                updated_content = re.sub(pattern, r"\g<0>" + new_line, content)

            # Запись изменений
            with open(path, "w", encoding="utf-8") as file:
                file.write(updated_content)

def topologicalSort(nodes):
    ans = []
    # Очистить taken
    for node in nodes:
        nodes[node]['taken'] = False
    
    # Обход для каждой непосещенной вершины
    for node in nodes:
        if nodes[node]['taken'] == False:
            dfs(node, nodes, ans)

    ans.reverse()
    return ans


def dfs(node, nodes, ans):
    # Отметить вершину как посещенную
    nodes[node]['taken'] = True
    
    outputs = nodes[node]['outputs']

    for output in outputs:
        if nodes[output]['taken'] == False:
            dfs(output, nodes, ans)

    ans.append(node)

def name_from_path(path):
    return re.search(r'Кирпичики/(.*?)\.md', path).group(1)


if __name__ == "__main__":
    main()
