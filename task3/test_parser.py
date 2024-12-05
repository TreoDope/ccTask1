import unittest
from parser import ConfigParser

class TestConfigParser(unittest.TestCase):
    def test_multiline_comment(self):
        text = """
        {#
        Это многострочный
        комментарий
        #}
        """
        parser = ConfigParser()
        result = parser.parse(text)
        self.assertEqual(result, {})

    def test_constant_declaration(self):
        text = """
        db_name = 'mydatabase'
        db_user = 'admin'
        db_password = 'secret'
        """
        parser = ConfigParser()
        result = parser.parse(text)
        self.assertEqual(result, {})
        self.assertEqual(parser.constants, {
            'db_name': 'mydatabase',
            'db_user': 'admin',
            'db_password': 'secret'
        })

    def test_constant_evaluation(self):
        text = """
        db_name = 'mydatabase'
        db_user = 'admin'
        db_password = 'secret'

        struct {
            name = ?(db_name),
            user = ?(db_user),
            password = ?(db_password),
            max_connections = 50,
            timeout = 10
        }
        """
        parser = ConfigParser()
        result = parser.parse(text)
        self.assertEqual(result, {
            'struct': {
                'name': 'mydatabase',
                'user': 'admin',
                'password': 'secret',
                'max_connections': 50,
                'timeout': 10
            }
        })

    def test_nested_struct(self):
        text = """
        struct {
            port = 8080,
            host = 'localhost',
            max_connections = 100,
            timeout = 30
        }
        """
        parser = ConfigParser()
        result = parser.parse(text)
        self.assertEqual(result, {
            'struct': {
                'port': 8080,
                'host': 'localhost',
                'max_connections': 100,
                'timeout': 30
            }
        })

    def test_invalid_constant_evaluation(self):
        text = """
        struct {
            name = ?(db_name),
            user = ?(db_user),
            password = ?(db_password),
            max_connections = 50,
            timeout = 10
        }
        """
        parser = ConfigParser()
        with self.assertRaises(ValueError) as cm:
            parser.parse(text)
        self.assertEqual(str(cm.exception), "Constant 'db_name' is not defined")

if __name__ == '__main__':
    unittest.main(verbosity=2)
