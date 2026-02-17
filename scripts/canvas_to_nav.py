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
            # id : [name, taken, inputs, outputs]
            nodes[node['id']] = {
                'name'    : node['file'],
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
            name = re.search(r'Кирпичики/(.*?)\.md', nodes[id]['name']).group(1)
            content += "[[Кирпичики/" + name + "|" + name +"]]" + '\n'
        content
        with open("Навигация по курсу.md", "w", encoding="utf-8") as file:
            file.write(content)

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


if __name__ == "__main__":
    main()
