import configparser
import pkg_resources
import subprocess
import os

def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['settings']['visualizer_path'], config['settings']['package_name']

def get_dependencies(package_name):
    try:
        package = pkg_resources.working_set.by_key[package_name]
        return [str(req) for req in package.requires()]
    except KeyError:
        return []

def generate_mermaid_graph(package_name, visited=None):
    if visited is None:
        visited = set()
    if package_name in visited:
        return ""
    visited.add(package_name)
    dependencies = get_dependencies(package_name)
    mermaid_graph = ""
    for dep in dependencies:
        dep_name = dep.split('==')[0]
        first_part = dep_name.split(">=")[0]
        mermaid_graph += f"\n  {package_name} --> {first_part}[{dep_name}];"
        mermaid_graph += generate_mermaid_graph(dep_name, visited)
    return mermaid_graph

def visualize_graph(mermaid_graph, visualizer_path):
    graph_content = f"graph TD;\n{mermaid_graph}"
    with open('graph.mmd', 'w') as f:
        f.write(graph_content)
    subprocess.run([visualizer_path, "-i", 'graph.mmd', '-o', 'graph.png'])
    os.remove('graph.mmd')
    os.startfile('graph.png')

def main(config_path):
    visualizer_path, package_name = read_config(config_path)
    mermaid_graph = generate_mermaid_graph(package_name)
    visualize_graph(mermaid_graph, visualizer_path)

if __name__ == "__main__":
    main('config.ini')
