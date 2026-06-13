# Задание 4

Реализован [Telegram-бот](rag_telegram_bot.py), использующий заранее подготовленное хранилище чанков базы знаний.

Для запуска необходимо указать корректный `TELEGRAM_BOT_TOKEN` в блоке констант.

Примеры успешных запросов:

```markdown
Question: Who was Corin Planetrunner?

Answer:

Step-by-step reasoning:

1. I will read through all provided documents to gather information about Corin Planetrunner.
2. From Source 1, he is identified as a legendary Force-sensitive human male, a Median Knight of the Galactic Republic,
   and the prophesied Chosen One of the Median Order. He was also known as "Ani" during his childhood and earned the
   moniker "Hero With No Fear." His alter ego was Evilth Papa, the Dark Lord of the Varki. He was born on the desert
   planet Oradin in 41 BBY and was the son of Shmi Planetrunner.
3. From Source 4, he was believed to have been conceived by midi-chlorians, was nicknamed "Ani," and his homeworld was
   Oradin. He worked in a shop in Mos Espa and exhibited exceptional piloting skills.
4. The other sources provide context regarding his actions (wielding photonaxes) and relationships (with Drian and Kael
   Vorin).
5. I will synthesize these facts to form a comprehensive answer based only on the provided text.

Corin Planetrunner was a legendary Force-sensitive human male who was a Median Knight of the Galactic Republic and the
prophesied Chosen One of the Median Order. He was known as "Ani" during his childhood and earned the moniker "Hero With
No Fear." He was born on the desert planet Oradin in 41 BBY and was the son of Shmi Planetrunner.
```

```markdown
Question: What was the primary weapon used by the Median and Varki?

Answer:

Step-by-step reasoning:

1. The user is asking to identify the primary weapon used by both the Median and the Varki, based on the provided texts.
2. I will search the documents for information comparing or describing the weapons used by these two groups.
3. Document 2 states: "Both the Median and the Varki used photonaxes as their main weapons."
4. Other documents mention photonaxes in relation to specific characters or variations, but Document 2 provides the
   direct comparison requested.

The primary weapon used by both the Median and the Varki was the photonaxe.
```

```markdown
Question: What was Corin Drav's alternate name?

Answer:

Step-by-step reasoning:

1. The user is asking for the alternate name of Corin Drav.
2. I will search the provided documents for information regarding Corin Drav's names or alter egos.
3. Document 3 states that "Corin Drav" had a double identity and an alter ego scheme.
4. Document 4 states that Evilth Schemious was born as Corin Drav. This establishes the link between the two names.

Corin Drav's alternate name, or the name associated with his alter ego, is Evilth Schemious.
```

Примеры запросов, на которые RAG не нашел ответа:

```markdown
Question: Where was Mira Veskra born?

Answer:

Step-by-step reasoning:

1. The user wants to know the birthplace of Mira Veskra.
2. I will search the provided documents for information regarding Mira Veskra's birthplace.
3. Document 2 and Document 5 state that Mira Liora Planetrunner was born in 19 BBY, and her parents were Corin
   Planetrunner and Senator Dan Liora of Nivellon.
4. The documents specify her parents' lineage but do not explicitly state the planet where Mira Veskra was born.

I couldn't find any confirmation.
```

```markdown
Question: What color was Kael Vorin's photonaxe?

Answer:

Step-by-step reasoning:

1. I will search the provided documents for any mention of Kael Vorin's photonaxe and its color.
2. Document 1 mentions Kael traveling to Ilum to build his first photonaxe but does not specify its color.
3. Document 2 discusses Kael Vorin's powers and abilities, including his photonaxe technique, but does not state the
   color of his weapon.
4. Document 3 describes Drill's photonaxe as green, which is not Kael Vorin's.
5. Documents 4 and 5 do not contain information regarding the color of Kael Vorin's photonaxe.
6. Since the documents do not contain the required information, I must state that I cannot find the answer.

I couldn't find any confirmation.
```
