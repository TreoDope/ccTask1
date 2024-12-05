# Задание №2

Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.
Зависимости определяются по имени пакета языка Python (pip). Для
описания графа зависимостей используется представление Mermaid.
Визуализатор должен выводить результат на экран в виде графического
изображения графа.
Конфигурационный файл имеет формат ini и содержит:
1. Путь к программе для визуализации графов.
2. Имя анализируемого пакета.
Все функции визуализатора зависимостей должны быть покрыты тестами.

## Тесты

### Тест в ручную

1. Создадим два примера конфигураций из разных предметных областей.

#### Конфигурация для базы данных `db.txt`


```cfg
{#
Это конфигурация для базы данных
#}

db_name = 'mydatabase'
db_user = 'admin'
db_password = 'secret'

struct {
    database {
        name = ?(db_name),
        user = ?(db_user),
        password = ?(db_password),
        max_connections = 50,
        timeout = 10
    }
}
```

#### Конфигурация для веб-сервера `network.txt`

```cfg
{#
Это конфигурация для веб-сервера
#}

port = 8080
host = 'localhost'

struct {
    server {
        port = ?(port),
        host = ?(host),
        max_connections = 100,
        timeout = 30
    }
}
```

2. Запустим скрипт из командной строки, передав путь к выходному `jaml` файлу через входной текст `db.txt`:

```sh
python parser.py < db.txt > output.yaml
```

Получаем выходной файл:

```yaml
struct:
  max_connections: 50
  name: mydatabase
  password: secret
  timeout: 10
  user: admin

```

3. Запустим скрипт из командной строки, передав путь к выходному `yaml` файлу через входной текст `network.txt`:

```sh
python parser.py < network.txt > output.yaml
```

Получаем выходной файл:

```yaml
struct:
  host: localhost
  max_connections: 100
  port: 8080
  timeout: 30

```

### Тест через `test_parser.py`

1. Запустим программу для тестов.

```sh
python test_parser.py
```

2. Получаем результаты пройденных тестов через `unittest`.

```sh
test_constant_declaration (__main__.TestConfigParser.test_constant_declaration) ... ok
test_constant_evaluation (__main__.TestConfigParser.test_constant_evaluation) ... ok
test_invalid_constant_evaluation (__main__.TestConfigParser.test_invalid_constant_evaluation) ... ok
test_multiline_comment (__main__.TestConfigParser.test_multiline_comment) ... ok
test_nested_struct (__main__.TestConfigParser.test_nested_struct) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```
