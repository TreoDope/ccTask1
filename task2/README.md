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

Установим mermaid и библиотеку "pipdeptree" для проверки зависимостей

#### Содержимое файла config.ini
[settings]
visualizer_path = C:/Users/Dima/AppData/Local/fnm_multishells/35520_1733417156550/mmdc.cmd
package_name = pipdeptree

Запуск программы

![image](https://github.com/user-attachments/assets/d94faf8c-3576-406d-bba9-bef139c56160)

После завершения программа открывает результат в виде png графика

![graph](https://github.com/user-attachments/assets/07bfcf57-20e2-4a80-9c7a-98f1ba7364a9)

Проверим корректность данных

![image](https://github.com/user-attachments/assets/ea432480-50eb-4358-8d26-22f5a9722ef8)

Зависимости совпадают



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
