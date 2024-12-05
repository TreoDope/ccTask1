# Задание №3

Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из входного формата в выходной. Синтаксические ошибки выявляются с выдачей сообщений.

Входной текст на **учебном конфигурационном** языке принимается из стандартного ввода. Выходной текст на **языке yaml** попадает в стандартный вывод.

### Многострочные комментарии

```cfg
{#
Это многострочный
комментарий
#}
```

### Словари

```cfg
struct {
имя = значение,
имя = значение,
имя = значение,
...
}
```

### Имена

```cfg
[a-zA-Z][_a-zA-Z0-9]*
```

### Значения

- Числа.
- Строки.
- Словари.

### Строки

```cfg
'Это строка'
```

### Объявление константы на этапе трансляции

```cfg
имя = значение
```

### Вычисление константы на этапе трансляции

```cfg
?(имя)
```

Результатом вычисления константного выражения является значение.

Все конструкции учебного конфигурационного языка (с учетом их возможной вложенности) должны быть покрыты тестами. Необходимо показать 2 примера описания конфигураций из разных предметных областей.

# Использование

```sh
python parser.py output.xml < input.txt > output.yaml
```

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
