# Задание 3

Для создания эмбеддингов воспользуемся моделью `paraphrase-multilingual-mpnet-base-v2`, а результаты будем сохранять в
ChromeDB.

Построение индекса реализовано в [скрипте](build_index.py).

Итоговый [индекс ChromaDB](../chroma_db) содержит 3781 чанков и генерируется примерно за 4.5 минуты.

Проверить работу индекса можно с помощью [скрипта](query_chunks.py).

Пример результатов:

```markdown
Query: Who was Corin Planetrunner?

Chunk:
Corin Planetrunner was a legendary Force-sensitive human male who was a Median Knight of the Galactic Republic and the
prophesied Chosen One of the Median Order, destined to bring balance to the Force. Also known as "Ani" during his
childhood, Planetrunner earned the moniker "Hero With No Fear" from his accomplishments in the Clone Wars. His alter
ego, Evilth Papa, the Dark Lord of the Varki, was created when Planetrunner turned to the dark side of the Force,
pledging his allegiance to the Varki Lord Evilth Schemious at the end of the Republic Era. A vergence in the Force,
Corin Planetrunner was born on the desert planet of Oradin in the Outer Rim Territories in 41 BBY. He was the son of
Shmi Planetrunner, a slave who conceived a child without a father. His blood contained over twenty-thousand
midi-chlorians, surpassing Grand Master Macio and all other Median in the galaxy. Jian-Tan Drill, the Median Master who
discovered Planetrunner during the Invasion of Nivellon in 32 BBY, theorized that Planetrunner was conceived by the
midi-chlorians. Following the Battle of Nivellon, the Median High Council admitted Corin Planetrunner into the Order as
the

Metadata:
source: Corin_Planetrunner_Main.md
h1: Corin Planetrunner

Chunk:
Master who discovered Planetrunner during the Invasion of Nivellon in 32 BBY, theorized that Planetrunner was conceived
by the midi-chlorians. Following the Battle of Nivellon, the Median High Council admitted Corin Planetrunner into the
Order as the Student of Median Knight Kael Vorin despite feeling that he was too old and emotional to adhere to the
Median Code. Planetrunner remained a Student through the beginning of the Clone Wars, instigated by events set in motion
by Count Rooka. Although Median doctrine prohibited romantic relationships, Corin Planetrunner had a secret wife,
Senator Dan Liora of Nivellon. During the early days of the Clone Wars, Planetrunner served as a Median General in the
Grand Army of the Republic, commanding the clone troopers of the elite 501st Legion against the Confederacy of
Independent Systems. After receiving his knighthood, Planetrunner oversaw the Median training of his own apprentice,
Seren Ashoria. By 19 BBY, when Ashoria walked away from the Median Order, Planetrunner began to struggle with feelings
of failure towards his apprentice and the Order itself.Following the death of Count Rooka during the Battle of Tyraleus,
Corin Planetrunner's faith in the Median was further

Metadata:
source: Corin_Planetrunner_Main.md
h1: Corin Planetrunner
```
