# iasu_rpd_parser
Инструменты для расчёта книгообеспеченности по РПД из ИАСУ

## Описание

Этот код был разработан для личных нужд и выложен с намерением проиллюстрировать автоматизацию работы секретаря кафедры, а также ради получения мотивации улучшить качество собсьвенного кода.

Программа предназначена для
* получения сводки предметов по каждой специальности на основании нескольких учебных планов,
* обособления библиографических записей из рабочих программ дисциплин (РПД), сопровождающих учебные планы
* поиска книги в библиотеке elibrary.mai.ru и систематизации результатов

Входными данными являются отчёты системы ИАСУ МАИ на базе 1С Предприятие. Обращения к поисковой системе библиотеки http://elibrary.mai.ru/MegaPro/Web/ позволяют получить данные о наличии книг в библиотеке и наличии цифровой копии, доступной для зарегистрированных пользователей.

## Состав скриптов

В программу входит несколько скриптов:

* `run` - основной скрипт, запускающий обработку текстовых файлов с УП и РПД
* `query_library` производит обращения в библиотеку
* `selenium_lib` содержит функции открытия браузера firefox и автоматического обращения к библиотеке (selenium -- модуль автоматизации многих программ, один аргумент меняет тип браузера)
* `shorten_bib_entry` - функция для получения "ключа" из текстовой библиографической записи 

Поскольку библиография РПД представлена в свободном формате, там присутствуют опечатки, ошибки в годах и разные виды оформления (учебное пособие, уч.пособие, учеб. пособие), к которым поисковая система библиотеки оказывается чувствительна. Поэтому каждая библиографическая запись переводится в "ключ", который состоит из всей информации ссылки, которая предшествует "индикаторам окончания" - элементам ссылки, которые не могут следовать до названия книги. Эту работу выполняет `shorten_bib_entry`.

# Входные данные

Обработка начинается с файла `up_list.txt` с экспортированным из ИАСУ набором учебных планов (например, по одной выпускающей кафедре), в текстовом формате, в кодировке UTF-8, и с полями разделёнными точкой с запятой.

В директории программы должны быть созданы несколько папок, в которых будут располагаться входные файлы:

* `lists_disciplines` - списки РПД дисцлплин для каждого учебного плана (файлы с названиями вида `11325.txt`)
* `lists_internship` - списки РПД практик для каждого учебного плана (файлы с названиями вида `11325.txt`)
* `rpd_txt_files` - РПД дисциплин и практик вперемежку (с названиями файлов вида `rpd000017634.txt`)

Сохранять РПД удобнее всего, выделив все РПД обного УП и выбрав "Печать" - "Полная печать", после чего одна за другой РПД будут открываться в Word (после вопроса о приложениях, который лучше всего закрыть при помощи `Ctrl-Enter`). После сохранения открытых документов в одной папке, при помощи OpenOffice/StarOffice файлы doc были преобразованы в txt следующим скриптом:

```bash
FILES=*.doc
for f in $FILES
do
  filename="${f%.*}"
  echo "Converting $f"
  soffice --convert-to txt $filename.doc
done
```

# Выходные данные

После первого этапа `run`, в корневой папке программы появляются файлы `books.txt` и `records.txt`. В них содержатся библиографические записи и, во втором, сгенерированные для них "ключи".

Дальше `run` запускает `query_library`, в результате выполнения которой формируются файлы:
* `books_records_out.txt`,
* `books_records_unavailable.txt`,
* `books_records_last_unavailable.txt` и
* все `.docx` файлы в папке `out`.
