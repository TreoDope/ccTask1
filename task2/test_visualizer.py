import unittest
from unittest.mock import patch, mock_open, MagicMock
import configparser
import pkg_resources
import subprocess
import os

from dependency_visualizer import read_config, get_dependencies, generate_mermaid_graph, visualize_graph, main

class TestVisualizer(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="[settings]\nvisualizer_path=/path/to/visualizer\npackage_name=example_package")
    def test_read_config(self, mock_file):
        visualizer_path, package_name = read_config('config.ini')
        self.assertEqual(visualizer_path, '/path/to/visualizer')
        self.assertEqual(package_name, 'example_package')

    @patch('pkg_resources.working_set.by_key')
    def test_get_dependencies(self, mock_by_key):
        mock_package = MagicMock()
        mock_package.requires.return_value = [pkg_resources.Requirement.parse('dep1==1.0.0'), pkg_resources.Requirement.parse('dep2>=2.0.0')]
        mock_by_key.get.return_value = mock_package

        dependencies = get_dependencies('example_package')
        self.assertEqual(dependencies, [])

    @patch('dependency_visualizer.get_dependencies')
    def test_generate_mermaid_graph(self, mock_get_dependencies):
        mock_get_dependencies.side_effect = [
            ['dep1==1.0.0', 'dep2>=2.0.0'],
            [],
            []
        ]

        mermaid_graph = generate_mermaid_graph('example_package')
        expected_graph = (
            "\n  example_package --> dep1[dep1];"
            "\n  example_package --> dep2[dep2>=2.0.0];"
        )
        self.assertEqual(mermaid_graph, expected_graph)

    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.run')
    @patch('os.remove')
    @patch('os.startfile')
    def test_visualize_graph(self, mock_startfile, mock_remove, mock_run, mock_file):
        visualize_graph("graph TD;\n  A --> B;", '/path/to/visualizer')
        mock_file.assert_called_once_with('graph.mmd', 'w')
        mock_file().write.assert_called_once_with("graph TD;\ngraph TD;\n  A --> B;")
        mock_run.assert_called_once_with(['/path/to/visualizer', '-i', 'graph.mmd', '-o', 'graph.png'])
        mock_remove.assert_called_once_with('graph.mmd')
        mock_startfile.assert_called_once_with('graph.png')

    @patch('dependency_visualizer.read_config')
    @patch('dependency_visualizer.generate_mermaid_graph')
    @patch('dependency_visualizer.visualize_graph')
    def test_main(self, mock_visualize_graph, mock_generate_mermaid_graph, mock_read_config):
        mock_read_config.return_value = '/path/to/visualizer', 'example_package'
        mock_generate_mermaid_graph.return_value = "graph TD;\n  A --> B;"

        main('config.ini')

        mock_read_config.assert_called_once_with('config.ini')
        mock_generate_mermaid_graph.assert_called_once_with('example_package')
        mock_visualize_graph.assert_called_once_with("graph TD;\n  A --> B;", '/path/to/visualizer')

if __name__ == '__main__':
    unittest.main()
