import ast
import sys
from igraph import Graph, plot
import matplotlib.pyplot as plt

# 深さ優先探索関数の定義
def dfs(graph, start_vertex, visited=None):
    if visited is None:
        visited = set()
    visited.add(start_vertex)
    result = []  # 訪れた頂点を記録するリスト
    if graph.neighbors(start_vertex)!=None:
        for neighbor in graph.neighbors(start_vertex):
            if (start_vertex,neighbor) not in visited:
                result.extend(dfs(graph, neighbor, visited))
    else :
        return result

# グラフ比較関数の定義
def extract_unique_elements(tree1, tree2):
    # 頂点のラベルを基に一意の頂点を抽出
    unique_vertices_tree1 = set(tree1.vs["name"]) - set(tree2.vs["name"])
    unique_vertices_tree2 = set(tree2.vs["name"]) - set(tree1.vs["name"])
    
    # 頂点名からインデックスへのマッピングを取得
    name_to_index_tree1 = {v["name"]: v.index for v in tree1.vs}
    name_to_index_tree2 = {v["name"]: v.index for v in tree2.vs}
    
    # 固有の頂点を保持するためのリスト
    unique_vertices = list(unique_vertices_tree1.union(unique_vertices_tree2))
    
    # エッジを一意の頂点に基づいてフィルタリング
    unique_edges_tree1 = [
        e.tuple for e in tree1.es 
        if tree1.vs[e.source]["name"] in unique_vertices_tree1 or tree1.vs[e.target]["name"] in unique_vertices_tree1
    ]
    
    unique_edges_tree2 = [
        e.tuple for e in tree2.es 
        if tree2.vs[e.source]["name"] in unique_vertices_tree2 or tree2.vs[e.target]["name"] in unique_vertices_tree2
    ]
    
    # 新しい木を作成
    new_tree = Graph()
    new_tree.add_vertices(len(unique_vertices))
    new_tree.vs["name"] = unique_vertices

    # 新しい木のエッジを追加
    new_edges = []
    for e in unique_edges_tree1 + unique_edges_tree2:
        src_name = tree1.vs[e[0]]["name"] if e[0] in name_to_index_tree1 else tree2.vs[e[0]]["name"]
        tgt_name = tree1.vs[e[1]]["name"] if e[1] in name_to_index_tree1 else tree2.vs[e[1]]["name"]
        if src_name in unique_vertices and tgt_name in unique_vertices:
            new_edges.append((unique_vertices.index(src_name), unique_vertices.index(tgt_name)))

    new_tree.add_edges(new_edges)
    return new_tree
class ASTGraphBuilder(ast.NodeVisitor):
    def __init__(self):
        self.graph = Graph(directed=True)
        self.node_index = 0
        self.node_map = {}  # ASTノードからグラフノードへのマップ

    def add_node(self, node, label):
        index = self.node_index
        self.graph.add_vertex(name=str(index), label=label)
        self.node_map[node] = index
        self.node_index += 1
        return index

    def visit(self, node):
        node_label = type(node).__name__
        node_index = self.add_node(node, node_label)

        for child in ast.iter_child_nodes(node):
            child_index = self.visit(child)
            self.graph.add_edge(node_index, child_index)

        return node_index

    def build_graph(self, node):
        self.visit(node)
        return self.graph

# 1. PythonのASTを生成
if len(sys.argv) > 2:
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
else:
    print("not enough argument")
    exit(0)

f1=open(filename1, encoding="utf-8")
parsed_ast1 = ast.parse(f1.read())

f2=open(filename2, encoding="utf-8")
parsed_ast2 = ast.parse(f2.read())


# グラフを構築
builder1 = ASTGraphBuilder()
graph1 = builder1.build_graph(parsed_ast1)

builder2 = ASTGraphBuilder()
graph2 = builder2.build_graph(parsed_ast2)

new_graph = extract_unique_elements(graph1, graph2)

# 3. igraphで解析
layout1 = graph1.layout("rt")
layout2 = graph2.layout("rt")
layout3 = new_graph.layout("rt")

# グラフ1のノードの色を黄色に設定
graph1.vs["color"] = "yellow"
graph1.vs["label"]=""

graph2.vs["label"]=""

new_graph.vs["label"]=""

# プロットの作成
fig, axes = plt.subplots(1, 2, figsize=(24, 8))

# グラフ1のプロット
plot(
    graph1,
    target=axes[0],
    layout=layout1,
    vertex_label=graph1.vs["label"],
    vertex_size=20,
    edge_arrow_size=0.5,
    vertex_color=graph1.vs["color"]
)
axes[0].set_title(filename1)

# グラフ2のプロット
plot(
    graph2,
    target=axes[0],
    layout=layout2,
    vertex_label=graph2.vs["label"],
    vertex_size=20,
    edge_arrow_size=0.5,
)
axes[1].set_title(filename2)

print(i.index for i in new_graph.vs)
print(new_graph)
plot(
    new_graph,
    target=axes[1],
    layout=layout3,
    vertex_label=graph2.vs["label"],
    vertex_size=20,
    edge_arrow_size=0.5,
)
plt.show()
