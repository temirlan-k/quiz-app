insert into quizzes (
   id,
   is_active,
   created_at,
   updated_at
) values ( 'a3dfe514-f1cc-4852-a377-cfa7a2007084',
           true,
           now(),
           now() );

insert into quiz_localizations (
   id,
   quiz_id,
   language,
   title,
   description
) values ( 'b1dfe514-f1cc-4852-a377-cfa7a2007085',
           'a3dfe514-f1cc-4852-a377-cfa7a2007084',
           'EN',
           'Python Programming Quiz',
           'Test your knowledge of Python basics and advanced concepts.' ),( 'b2dfe514-f1cc-4852-a377-cfa7a2007086',
                                                                             'a3dfe514-f1cc-4852-a377-cfa7a2007084',
                                                                             'ES',
                                                                             'Cuestionario de Programación en Python',
                                                                             'Pon a prueba tus conocimientos de conceptos básicos y avanzados de Python.'
                                                                             ),( 'b3dfe514-f1cc-4852-a377-cfa7a2007087',
                                                                                                                                                          'a3dfe514-f1cc-4852-a377-cfa7a2007084'
                                                                                                                                                          ,
                                                                                                                                                          'PT'
                                                                                                                                                          ,
                                                                                                                                                          'Questionário de Programação em Python'
                                                                                                                                                          ,
                                                                                                                                                          'Teste seus conhecimentos sobre os conceitos básicos e avançados de Python.'
                                                                                                                                                          )
                                                                                                                                                          ,
                                                                                                                                                          (
                                                                                                                                                          'b4dfe514-f1cc-4852-a377-cfa7a2007088'
                                                                                                                                                          ,
                                                                                                                                                                                                                                       'a3dfe514-f1cc-4852-a377-cfa7a2007084'
                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                       'DE'
                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                       'Python-Programmierung Quiz'
                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                       'Testen Sie Ihr Wissen über grundlegende und fortgeschrittene Python-Konzepte.'
                                                                                                                                                                                                                                       )
                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                       (
                                                                                                                                                                                                                                       'b5dfe514-f1cc-4852-a377-cfa7a2007089'
                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                                                                                                       'a3dfe514-f1cc-4852-a377-cfa7a2007084'
                                                                                                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                                                                                                       'TR'
                                                                                                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                                                                                                       'Python Programlama Testi'
                                                                                                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                                                                                                       'Python temel ve ileri düzey kavramlar bilginizi test edin.'
                                                                                                                                                                                                                                                                                                                       )
                                                                                                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                                                                                                       (
                                                                                                                                                                                                                                                                                                                       'b6dfe514-f1cc-4852-a377-cfa7a2007090'
                                                                                                                                                                                                                                                                                                                       ,
                                                                                                                                                                                                                                                                                                                                                                                    'a3dfe514-f1cc-4852-a377-cfa7a2007084'
                                                                                                                                                                                                                                                                                                                                                                                    ,
                                                                                                                                                                                                                                                                                                                                                                                    'FR'
                                                                                                                                                                                                                                                                                                                                                                                    ,
                                                                                                                                                                                                                                                                                                                                                                                    'Quiz de Programmation Python'
                                                                                                                                                                                                                                                                                                                                                                                    ,
                                                                                                                                                                                                                                                                                                                                                                                    'Testez vos connaissances sur les concepts basiques et avancés de Python.'
                                                                                                                                                                                                                                                                                                                                                                                    )
                                                                                                                                                                                                                                                                                                                                                                                    ;


insert into questions (
   id,
   quiz_id,
   question_type,
   "order",
   created_at,
   updated_at
) values ( 'c1dfe514-f1cc-4852-a377-cfa7a2007084',
           'a3dfe514-f1cc-4852-a377-cfa7a2007084',
           'SINGLE_CHOICE',
           1,
           now(),
           now() ),( 'c2dfe514-f1cc-4852-a377-cfa7a2007084',
                     'a3dfe514-f1cc-4852-a377-cfa7a2007084',
                     'MULTIPLE_CHOICE',
                     2,
                     now(),
                     now() ),( 'c3dfe514-f1cc-4852-a377-cfa7a2007084',
                               'a3dfe514-f1cc-4852-a377-cfa7a2007084',
                               'FILL_BLANK',
                               3,
                               now(),
                               now() ),( 'c4dfe514-f1cc-4852-a377-cfa7a2007084',
                                         'a3dfe514-f1cc-4852-a377-cfa7a2007084',
                                         'MATCHING',
                                         4,
                                         now(),
                                         now() );


-- Question 1: SINGLE_CHOICE, English
insert into question_localizations (
   id,
   question_id,
   language,
   question_text,
   content
) values ( 'd1dfe514-f1cc-4852-a377-cfa7a2007091',
           'c1dfe514-f1cc-4852-a377-cfa7a2007084',
           'EN',
           'What is the output of print(2 ** 3)?',
           '{"public_data": {"options": [{"id": "opt1", "text": "6"}, {"id": "opt2", "text": "8"}, {"id": "opt3", "text": "9"}]}, "private_data": {"correct_options": ["opt2"]}}'
           );

-- Question 1: SINGLE_CHOICE, Spanish
insert into question_localizations (
   id,
   question_id,
   language,
   question_text,
   content
) values ( 'd2dfe514-f1cc-4852-a377-cfa7a2007092',
           'c1dfe514-f1cc-4852-a377-cfa7a2007084',
           'ES',
           '¿Cuál es el resultado de print(2 ** 3)?',
           '{"public_data": {"options": [{"id": "opt1", "text": "6"}, {"id": "opt2", "text": "8"}, {"id": "opt3", "text": "9"}]}, "private_data": {"correct_options": ["opt2"]}}'
           );

-- Question 2: MULTIPLE_CHOICE, English
insert into question_localizations (
   id,
   question_id,
   language,
   question_text,
   content
) values ( 'e1dfe514-f1cc-4852-a377-cfa7a2007093',
           'c2dfe514-f1cc-4852-a377-cfa7a2007084',
           'EN',
           'Which of the following are valid Python data types?',
           '{"public_data": {"options": [{"id": "opt1", "text": "int"}, {"id": "opt2", "text": "float"}, {"id": "opt3", "text": "decimal"}]}, "private_data": {"correct_options": ["opt1", "opt2"]}}'
           );

-- Question 2: MULTIPLE_CHOICE, Spanish
insert into question_localizations (
   id,
   question_id,
   language,
   question_text,
   content
) values ( 'e2dfe514-f1cc-4852-a377-cfa7a2007094',
           'c2dfe514-f1cc-4852-a377-cfa7a2007084',
           'ES',
           '¿Cuáles de los siguientes son tipos de datos válidos en Python?',
           '{"public_data": {"options": [{"id": "opt1", "text": "int"}, {"id": "opt2", "text": "float"}, {"id": "opt3", "text": "decimal"}]}, "private_data": {"correct_options": ["opt1", "opt2"]}}'
           );

-- Question 3: FILL_BLANK, English
insert into question_localizations (
   id,
   question_id,
   language,
   question_text,
   content
) values ( 'f1dfe514-f1cc-4852-a377-cfa7a2007095',
           'c3dfe514-f1cc-4852-a377-cfa7a2007084',
           'EN',
           'Fill in the blank: The keyword to define a function in Python is ___',
           '{"public_data": {"options": ["def", "function", "lambda"]}, "private_data": {"correct_answers": ["def"]}}' );

-- Question 3: FILL_BLANK, Spanish
insert into question_localizations (
   id,
   question_id,
   language,
   question_text,
   content
) values ( 'f2dfe514-f1cc-4852-a377-cfa7a2007096',
           'c3dfe514-f1cc-4852-a377-cfa7a2007084',
           'ES',
           'Rellena el espacio en blanco: La palabra clave para definir una función en Python es ___',
           '{"public_data": {"options": ["def", "function", "lambda"]}, "private_data": {"correct_answers": ["def"]}}' );

-- Question 4: MATCHING, English
insert into question_localizations (
   id,
   question_id,
   language,
   question_text,
   content
) values ( 'd1dfe514-f1cc-4852-a377-cfa7a2007092',
           'c4dfe514-f1cc-4852-a377-cfa7a2007084',
           'EN',
           'Match the function to its correct description:',
           '{
    "public_data": {
        "shuffled_left": ["len", "sorted", "type"],
        "shuffled_right": ["Returns the number of items in an object", "Returns a sorted list", "Returns the type of an object"]
    },
    "private_data": {
        "pairs": [
            {"left": "len", "right": "Returns the number of items in an object"},
            {"left": "sorted", "right": "Returns a sorted list"},
            {"left": "type", "right": "Returns the type of an object"}
        ]
    }
}' );

-- Question 4: MATCHING, Spanish
insert into question_localizations (
   id,
   question_id,
   language,
   question_text,
   content
) values ( 'd2dfe514-f1cc-4852-a377-cfa7a2007098',
           'c4dfe514-f1cc-4852-a377-cfa7a2007084',
           'ES',
           'Relaciona la función con su descripción correcta:',
           '{
    "public_data": {
        "shuffled_left": ["len", "sorted", "type"],
        "shuffled_right": ["Devuelve el número de elementos en un objeto", "Devuelve una lista ordenada", "Devuelve el tipo de un objeto"]
    },
    "private_data": {
        "pairs": [
            {"left": "len", "right": "Devuelve el número de elementos en un objeto"},
            {"left": "sorted", "right": "Devuelve una lista ordenada"},
            {"left": "type", "right": "Devuelve el tipo de un objeto"}
        ]
    }
}' );