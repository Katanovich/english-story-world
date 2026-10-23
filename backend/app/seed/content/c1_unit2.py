"""C1 · Unit 2 "Voices and Futures" (C1 lessons 6-10).

{boy} looks back at his family's past and forward to his own future. Topics: Granny's
memories, coding and creativity, a job shadow day, artificial intelligence, a presentation.
Grammar: past perfect continuous, abstract nouns and collocations, formal register, past
modals of deduction, discourse markers. Lesson 10 closes C1 with a mixed review.
"""

from app.seed.content.helpers import (
    G,
    Item,
    P,
    V,
    blank,
    build,
    choice,
    matching,
    order,
    speak,
    true_false,
)

L6, L7, L8, L9, L10 = (
    "grannys-memories",
    "code-and-creativity",
    "job-shadow-day",
    "thinking-machines",
    "presentation-day",
)

ITEMS: dict[str, Item] = {
    # Lesson 6
    "vocab.memoir": (
        V,
        "memoir",
        "📔",
        "мемуары, воспоминания",
        L6,
        ["Granny is writing her memoir."],
        None,
    ),
    "vocab.generation": (
        V,
        "generation",
        "👵",
        "поколение",
        L6,
        ["Three generations live in this town."],
        None,
    ),
    "vocab.nostalgic": (
        V,
        "nostalgic",
        "🕰️",
        "ностальгический",
        L6,
        ["Old songs make Granny nostalgic."],
        None,
    ),
    "vocab.recall": (V, "recall", "🧠", "вспоминать", L6, ["She can recall every detail."], None),
    "vocab.era": (V, "era", "📜", "эпоха", L6, ["It was a very different era."], None),
    "vocab.hardship": (
        V,
        "hardship",
        "🧱",
        "трудности, лишения",
        L6,
        ["They faced real hardship after the factory closed."],
        None,
    ),
    "grammar.past_perfect_continuous": (
        G,
        "She had been working … for … before …",
        None,
        "Past perfect continuous: как долго длилось действие до момента в прошлом",
        L6,
        [
            "She had been working at the factory for ten years when it closed.",
            "They had been saving for months.",
        ],
        "had been + verb-ing: the duration of an activity up to a point in the past, or its visible result then.",
    ),
    # Lesson 7
    "vocab.creativity": (
        V,
        "creativity",
        "🎨",
        "креативность, творчество",
        L7,
        ["Coding needs a lot of creativity."],
        None,
    ),
    "vocab.innovation": (
        V,
        "innovation",
        "🚀",
        "инновация",
        L7,
        ["Innovation often comes from small teams."],
        None,
    ),
    "vocab.curiosity": (
        V,
        "curiosity",
        "🧐",
        "любопытство",
        L7,
        ["Curiosity is a scientist's best friend."],
        None,
    ),
    "vocab.collaboration": (
        V,
        "collaboration",
        "🤜",
        "сотрудничество",
        L7,
        ["The app was a collaboration between three schools."],
        None,
    ),
    "vocab.bug": (
        V,
        "bug",
        "🐞",
        "ошибка (в программе)",
        L7,
        ["We spent all night fixing a bug."],
        None,
    ),
    "grammar.abstract_nouns": (
        G,
        "curious → curiosity, create → creativity, decide → decision",
        None,
        "Абстрактные существительные и словообразование",
        L7,
        ["Her curiosity led to the discovery.", "The decision was difficult."],
        "Common suffixes: -ity, -tion/-sion, -ness, -ment, -ence/-ance.",
    ),
    "grammar.collocations": (
        G,
        "make progress / pay attention / take a risk / do research",
        None,
        "Устойчивые сочетания (коллокации)",
        L7,
        [
            "We've made a lot of progress.",
            "Pay attention to the details.",
            "Sometimes you have to take a risk.",
        ],
        "Some nouns go with specific verbs. Learn them as chunks: make a decision, do research, take responsibility.",
    ),
    # Lesson 8
    "vocab.colleague": (
        V,
        "colleague",
        "🧑‍💼",
        "коллега",
        L8,
        ["My colleagues were very welcoming."],
        None,
    ),
    "vocab.deadline": (
        V,
        "deadline",
        "📅",
        "крайний срок",
        L8,
        ["The deadline is Friday at noon."],
        None,
    ),
    "vocab.schedule": (
        V,
        "schedule",
        "🗓️",
        "расписание, график",
        L8,
        ["My schedule is very full today."],
        None,
    ),
    "vocab.enquiry": (V, "enquiry", "❓", "запрос", L8, ["Thank you for your enquiry."], None),
    "vocab.appropriate": (
        V,
        "appropriate",
        "👔",
        "уместный, подходящий",
        L8,
        ["Is jeans appropriate for the office?"],
        None,
    ),
    "grammar.formal_register": (
        G,
        "I would be grateful if … / Please do not hesitate to …",
        None,
        "Официальный стиль",
        L8,
        [
            "I would be grateful if you could send me the report.",
            "Please do not hesitate to contact me.",
        ],
        "Formal English avoids contractions and slang, uses longer Latin-based verbs (receive, require, assist) and polite indirect forms.",
    ),
    "phrase.formal_email": (
        P,
        "Dear Ms … / I am writing to … / Kind regards",
        None,
        "Уважаемая … / Пишу, чтобы … / С уважением",
        L8,
        ["Dear Ms Grant, I am writing to thank you for …", "Kind regards, {boy}"],
        "How to open and close a formal email.",
    ),
    # Lesson 9
    "vocab.algorithm": (
        V,
        "algorithm",
        "🧮",
        "алгоритм",
        L9,
        ["The algorithm recommends videos."],
        None,
    ),
    "vocab.dataset": (
        V,
        "dataset",
        "🗄️",
        "набор данных",
        L9,
        ["The AI was trained on a huge dataset."],
        None,
    ),
    "vocab.ethical": (
        V,
        "ethical",
        "🧭",
        "этичный",
        L9,
        ["Is it ethical to use AI for homework?"],
        None,
    ),
    "vocab.malfunction": (
        V,
        "malfunction",
        "⚠️",
        "сбой; работать со сбоями",
        L9,
        ["The robot malfunctioned during the demo."],
        None,
    ),
    "vocab.predict": (
        V,
        "predict",
        "🔮",
        "предсказывать",
        L9,
        ["The program predicts the weather."],
        None,
    ),
    "grammar.past_modals": (
        G,
        "must have / might have / can't have + past participle",
        None,
        "Модальные глаголы для предположений о прошлом",
        L9,
        [
            "The robot must have run out of battery.",
            "Someone might have changed the code.",
            "It can't have learned that by itself.",
        ],
        "must have = almost certain; might / may / could have = possible; can't / couldn't have = almost certainly not.",
    ),
    # Lesson 10
    "vocab.slide": (V, "slide", "🖼️", "слайд", L10, ["Let's move on to the next slide."], None),
    "vocab.rehearse": (
        V,
        "rehearse",
        "🔁",
        "репетировать",
        L10,
        ["We rehearsed the presentation three times."],
        None,
    ),
    "vocab.summarise": (
        V,
        "summarise",
        "📋",
        "подводить итог, резюмировать",
        L10,
        ["Let me summarise the main points."],
        None,
    ),
    "vocab.emphasise": (
        V,
        "emphasise",
        "❗",
        "подчёркивать, выделять",
        L10,
        ["I'd like to emphasise this point."],
        None,
    ),
    "vocab.handout": (
        V,
        "handout",
        "📃",
        "раздаточный материал",
        L10,
        ["Please take a handout."],
        None,
    ),
    "grammar.discourse_markers": (
        G,
        "First of all / Moving on to / Having said that / In short",
        None,
        "Дискурсивные маркеры: структура речи",
        L10,
        [
            "First of all, I'll explain the problem.",
            "Moving on to the results, …",
            "Having said that, there are limits.",
        ],
        "Discourse markers guide the listener: they introduce, move on, contrast, give examples and conclude.",
    ),
    "phrase.signposting": (
        P,
        "Let's turn to … / As I mentioned earlier, …",
        None,
        "Перейдём к … / Как я уже упоминал, …",
        L10,
        ["Let's turn to the results.", "As I mentioned earlier, the data is limited."],
        "Signposting phrases tell the audience where you are in a presentation.",
    ),
}


LESSON_6 = {
    "slug": L6,
    "title": "Granny's Memories",
    "description": "Granny {gran1} is writing her memoir. What had she been dreaming of all those years?",
    "minutes": 40,
    "objectives": [
        "Use life-writing vocabulary: memoir, generation, era, recall, nostalgic, hardship.",
        "Use the past perfect continuous for duration and causes in the past.",
        "Retell a life story with a range of past tenses.",
    ],
    "review": [
        "grammar.inversion",
        "vocab.charity",
        "vocab.raise_money",
        "grammar.mixed_conditionals",
        "grammar.narrative_tenses",
        "grammar.used_to",
        "grammar.past_perfect_continuous",
        "vocab.childhood",
        "vocab.letter",
        "vocab.radio",
    ],
    "episode": (
        "The Blue Suitcase",
        "While helping Granny {gran1} write her memoir, {boy} finds a suitcase of letters from 1975.",
    ),
    "content": {
        "story_intro": "Granny {gran1} has decided to write her memoir. {boy} is helping her type it.",
        "reading": {
            "title": "From Granny's Memoir",
            "paragraphs": [
                {
                    "sentences": [
                        "I was born in a small village in a very different era. We didn't have a telephone, and the nearest library was ten kilometres away.",
                        "I had been dreaming of becoming a teacher since I was six.",
                    ]
                },
                {
                    "sentences": [
                        "When I was sixteen, the factory where my father had been working for twenty years suddenly closed.",
                        "It was a time of real hardship. My mother had been saving for my studies, but now we needed every penny.",
                    ]
                },
                {
                    "sentences": [
                        "For two years I worked in a shop. By the time I finally went to college, I had been reading every evening for so long that I was ahead of the other students.",
                        "Never had I felt so proud as on my first day there.",
                    ]
                },
                {
                    "sentences": [
                        "I met your grandfather at a dance. He had been waiting all evening to ask me, he admitted later, but he was too shy.",
                        "We wrote to each other every week for a year. I still have every one of those letters in a blue suitcase.",
                    ]
                },
                {
                    "sentences": [
                        "When I recall those years, I feel nostalgic, but not sad.",
                        "Each generation has its own challenges. What matters is how we face them.",
                    ]
                },
            ],
            "highlight": [
                "had been dreaming",
                "had been working",
                "had been saving",
                "had been reading",
                "had been waiting",
                "era",
                "hardship",
                "recall",
                "nostalgic",
                "generation",
            ],
        },
        "listening": [
            {
                "id": "c1-6-suitcase",
                "title": "The blue suitcase",
                "transcript": [
                    {"speaker": "{boy}", "text": "Granny, why were you crying when I came in?"},
                    {
                        "speaker": "Granny {gran1}",
                        "text": "I wasn't sad, love. I'd been reading Grandad's old letters all afternoon.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "How long had you two been writing to each other before you got married?",
                    },
                    {
                        "speaker": "Granny {gran1}",
                        "text": "About a year. He'd been saving to buy a ring the whole time.",
                    },
                ],
            },
            {
                "id": "c1-6-generations",
                "title": "Three generations",
                "transcript": [
                    {"speaker": "Mum", "text": "Your generation has so many opportunities, {boy}."},
                    {
                        "speaker": "{boy}",
                        "text": "I know. But every generation has its own problems, like Granny says.",
                    },
                    {
                        "speaker": "Mum",
                        "text": "That's true. Mine had no internet, yours has too much!",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Past perfect continuous",
                "explanation": (
                    "Form: had been + verb-ing. Use it to describe an activity that continued up to a moment in the past. "
                    "Duration: My father had been working at the factory for twenty years when it closed. "
                    "Cause or result visible at that moment: Her eyes were red because she had been crying. "
                    "Compare: past perfect simple focuses on completion: She had read all the letters (finished). "
                    "Past perfect continuous focuses on the activity: She had been reading letters all afternoon."
                ),
                "explanation_ru": (
                    "had been + -ing: как долго что-то длилось до момента в прошлом, или причина состояния в тот момент. "
                    "Ср.: had read (закончила) / had been reading (процесс)."
                ),
                "examples": [
                    "We had been walking for hours before we found the village.",
                    "He was tired because he had been working nights.",
                    "How long had she been living there when you met?",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "memoir-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("memoir", None, "📔"),
                ("generation", None, "👵"),
                ("nostalgic", None, "🕰️"),
                ("era", None, "📜"),
            ],
            ["vocab.memoir", "vocab.generation", "vocab.nostalgic", "vocab.era"],
            "A memoir is a book about your own life.",
            "memoir 📔, generation 👵, nostalgic 🕰️, era 📜.",
        ),
        matching(
            "memoir-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("recall", "remember something from the past", None),
                ("hardship", "a situation that is difficult, often with little money", None),
                ("nostalgic", "feeling happy and a little sad about the past", None),
            ],
            ["vocab.recall", "vocab.hardship", "vocab.nostalgic"],
            "Old photos often make people feel nostalgic.",
            "recall = remember; hardship = difficult conditions; nostalgic = fond of the past.",
        ),
        choice(
            "find-memoir",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: memoir",
            [(None, "📔"), (None, "📰"), (None, "🖼️")],
            "a",
            ["vocab.memoir"],
            "A book about the writer's own life.",
            "📔 memoir.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-ppc",
            "LISTENING",
            "Listen. Why were the man's clothes covered in paint?",
            "His clothes were covered in paint because …",
            [
                ("he had been decorating the kitchen", "🎨"),
                ("he had fallen into a pot of paint", "🪣"),
                ("he worked as an artist", "🖌️"),
            ],
            "a",
            ["grammar.past_perfect_continuous"],
            "Listen for 'had been'.",
            "He had been decorating the kitchen all morning.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="When I got home, Dad's clothes were covered in white paint. He had been decorating the kitchen all morning.",
        ),
        true_false(
            "listen-crying",
            "LISTENING",
            "Listen to {boy} and Granny. True or false?",
            "Granny was crying because she was sad.",
            False,
            ["grammar.past_perfect_continuous", "vocab.letter"],
            "What had she been doing?",
            "She wasn't sad — she had been reading Grandad's old letters.",
            listening_id="c1-6-suitcase",
        ),
        true_false(
            "listen-generation",
            "LISTENING",
            "Listen to Mum and {boy}. True or false?",
            "{boy} agrees that every generation has its own problems.",
            True,
            ["vocab.generation"],
            "Listen to {boy}'s line.",
            "Every generation has its own problems, like Granny says.",
            listening_id="c1-6-generations",
        ),
        blank(
            "ppc-blank",
            "GRAMMAR",
            "Complete with the past perfect continuous.",
            "Her father had ___ ___ at the factory for twenty years when it closed.",
            ["been", "working"],
            ["been", "being", "working", "worked"],
            ["grammar.past_perfect_continuous"],
            "had been + -ing.",
            "Her father had been working at the factory for twenty years.",
        ),
        choice(
            "simple-or-cont",
            "GRAMMAR",
            "Choose the best sentence.",
            "You want to say that Granny finished all the letters.",
            [
                ("By six o'clock she had read all the letters.", None),
                ("By six o'clock she had been reading all the letters.", None),
                ("By six o'clock she has read all the letters.", None),
            ],
            "a",
            ["grammar.past_perfect_continuous", "grammar.narrative_tenses"],
            "Completion → past perfect simple.",
            "She had read all the letters (finished).",
        ),
        choice(
            "cause-result",
            "GRAMMAR",
            "Choose the best explanation.",
            "When I saw {boy}, he was out of breath.",
            [
                ("He had been running.", None),
                ("He has been running.", None),
                ("He had been run.", None),
            ],
            "a",
            ["grammar.past_perfect_continuous"],
            "A visible result in the past.",
            "He was out of breath because he had been running.",
        ),
        blank(
            "how-long-blank",
            "GRAMMAR",
            "Complete the question.",
            "How long ___ they been writing to each other before they ___ married?",
            ["had", "got"],
            ["had", "have", "got", "had got"],
            ["grammar.past_perfect_continuous"],
            "had been + -ing … before + past simple.",
            "How long had they been writing to each other before they got married?",
        ),
        build(
            "build-ppc",
            "GRAMMAR",
            "Put the words in order.",
            "She had been dreaming of teaching since childhood.",
            ["grammar.past_perfect_continuous", "vocab.childhood"],
            "Start with 'She had been'.",
            "She had been dreaming of teaching since childhood.",
        ),
        order(
            "read-order",
            "READING",
            "Put Granny's life events in order.",
            [
                "She dreamed of becoming a teacher as a little girl.",
                "Her father's factory closed.",
                "She worked in a shop for two years.",
                "She went to college.",
                "She met Grandad at a dance.",
            ],
            ["vocab.memoir", "grammar.past_perfect_continuous"],
            "The factory closed when she was sixteen.",
            "Dream → factory closes → shop → college → Grandad.",
        ),
        choice(
            "read-ahead",
            "READING",
            "Read the memoir. Then answer.",
            "Why was Granny ahead of the other students at college?",
            [
                ("She had been reading every evening for years.", "📚"),
                ("She had studied at a private school.", "🏫"),
                ("Her father had taught her at home.", "👨‍🏫"),
            ],
            "a",
            ["grammar.past_perfect_continuous"],
            "Look at paragraph 3.",
            "She had been reading every evening for so long.",
            ex_type="READING_COMPREHENSION",
        ),
        speak(
            "say-memoir",
            "Interview an older family member in your imagination, or think of your own life. Describe a turning point using the past perfect continuous.",
            "I had been … for … when … By the time …, I had been …",
            "I had been living in the same town for twelve years when we suddenly moved. By the time I started at my new school, I had been feeling nervous for weeks.",
            ["grammar.past_perfect_continuous", "grammar.narrative_tenses"],
        ),
        choice(
            "quiz-inversion-proud",
            "QUIZ",
            "Choose the correct sentence.",
            "Granny was never so proud.",
            [
                ("Never had Granny felt so proud.", None),
                ("Never Granny had felt so proud.", None),
                ("Never did Granny felt so proud.", None),
            ],
            "a",
            ["grammar.inversion"],
            "Remember Unit 1, Lesson 5.",
            "Never had Granny felt so proud.",
        ),
        blank(
            "quiz-mixed-granny",
            "QUIZ",
            "Complete the mixed conditional.",
            "If Granny hadn't kept the letters, we ___ know this story now.",
            ["wouldn't"],
            ["wouldn't", "won't", "didn't"],
            ["grammar.mixed_conditionals"],
            "Remember Unit 1, Lesson 4: past → present.",
            "If she hadn't kept the letters, we wouldn't know this story now.",
        ),
        choice(
            "quiz-used-to-granny",
            "QUIZ",
            "Choose the right form.",
            "In Granny's village, people ___ listen to the radio every evening.",
            [("used to", None), ("were used", None), ("use to", None)],
            "a",
            ["grammar.used_to", "vocab.radio"],
            "Remember B1.",
            "People used to listen to the radio.",
        ),
    ],
}

LESSON_7 = {
    "slug": L7,
    "title": "Code and Creativity",
    "description": "{boy}'s team builds an app at a 24-hour hackathon. Make progress, take risks, pay attention!",
    "minutes": 40,
    "objectives": [
        "Use abstract nouns: creativity, innovation, curiosity, collaboration.",
        "Form abstract nouns with suffixes: -ity, -tion, -ness, -ment, -ence.",
        "Use common collocations: make progress, take a risk, pay attention, do research.",
    ],
    "review": [
        "grammar.past_perfect_continuous",
        "vocab.generation",
        "vocab.recall",
        "grammar.cleft_sentences",
        "grammar.relative_clauses",
        "grammar.gerund_infinitive",
        "vocab.program",
        "vocab.ai",
        "vocab.invention",
        "vocab.prototype",
    ],
    "episode": (
        "The 24-Hour Hackathon",
        "{boy}, Maya and Sam have 24 hours to build an app that helps older people. At 3 am, everything crashes.",
    ),
    "content": {
        "story_intro": "{boy}'s team has entered a 24-hour hackathon. The challenge: build an app that connects generations.",
        "reading": {
            "title": "Twenty-Four Hours",
            "paragraphs": [
                {
                    "sentences": [
                        "Our idea came from Granny's memoir: an app where older people record stories and teenagers turn them into illustrated books.",
                        "Many people think coding is only about logic, but in fact it requires a huge amount of creativity.",
                    ]
                },
                {
                    "sentences": [
                        "In the first six hours we made rapid progress. Maya did the research, Sam designed the screens, and I wrote most of the code.",
                        "It was a genuine collaboration — nobody could have done it alone.",
                    ]
                },
                {
                    "sentences": [
                        "At three in the morning, disaster struck. A tiny bug crashed the whole app, and we had no idea why.",
                        "We had to pay close attention to every line of code. Sam was ready to give up, but curiosity kept me going.",
                    ]
                },
                {
                    "sentences": [
                        "At five, we made a decision: we would take a risk and rewrite the main part from scratch.",
                        "It worked. By the time the sun rose, the app was faster than ever.",
                    ]
                },
                {
                    "sentences": [
                        "We didn't win first prize, but the judges praised our innovation and our kindness towards older users.",
                        "What I learned is that real creativity often comes after failure.",
                    ]
                },
            ],
            "highlight": [
                "creativity",
                "made rapid progress",
                "did the research",
                "collaboration",
                "pay close attention",
                "curiosity",
                "made a decision",
                "take a risk",
                "innovation",
                "kindness",
                "failure",
            ],
        },
        "listening": [
            {
                "id": "c1-7-mentor",
                "title": "Advice from a mentor",
                "transcript": [
                    {"speaker": "Mentor", "text": "How's it going? Have you made any progress?"},
                    {
                        "speaker": "Maya",
                        "text": "Some. But we can't decide which feature to build first.",
                    },
                    {
                        "speaker": "Mentor",
                        "text": "Do some quick research with real users. Their feedback will help you make the decision.",
                    },
                    {
                        "speaker": "Maya",
                        "text": "Good idea. We'll ask Granny {gran1} and her friends.",
                    },
                ],
            },
            {
                "id": "c1-7-judges",
                "title": "The judges' comments",
                "transcript": [
                    {
                        "speaker": "Judge",
                        "text": "What impressed us most was your team's resilience.",
                    },
                    {
                        "speaker": "Judge",
                        "text": "Rewriting the code at five in the morning took real courage.",
                    },
                    {
                        "speaker": "Judge",
                        "text": "Pay attention to accessibility, though — the buttons are a bit small for older users.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Abstract nouns",
                "explanation": (
                    "Abstract nouns name ideas, qualities and feelings. Many are formed with suffixes. "
                    "-ity: creative → creativity, curious → curiosity. "
                    "-tion / -sion: innovate → innovation, decide → decision. "
                    "-ness: kind → kindness, aware → awareness. "
                    "-ment: improve → improvement, develop → development. "
                    "-ence / -ance: resilient → resilience, important → importance. "
                    "Abstract nouns make writing more formal and concise: Because she was curious … → Her curiosity …"
                ),
                "explanation_ru": (
                    "Абстрактные существительные образуются суффиксами -ity, -tion, -ness, -ment, -ence: "
                    "curious → curiosity, decide → decision, kind → kindness."
                ),
                "examples": [
                    "Her curiosity led to an important discovery.",
                    "The improvement was obvious.",
                    "Failure is part of learning.",
                ],
            },
            {
                "title": "Collocations",
                "explanation": (
                    "Collocations are words that naturally go together. Learn them as chunks. "
                    "make: a decision, progress, a mistake, an effort. "
                    "do: research, your best, damage. "
                    "take: a risk, responsibility, a break. "
                    "pay: attention, a compliment. "
                    "We say make progress (not do progress) and take a risk (not make a risk)."
                ),
                "explanation_ru": "Коллокации — устойчивые сочетания: make a decision, do research, take a risk, pay attention.",
                "examples": [
                    "We made a lot of progress.",
                    "Take a break — you've earned it.",
                    "Please pay attention to the instructions.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "abstract-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("creativity", None, "🎨"),
                ("innovation", None, "🚀"),
                ("curiosity", None, "🧐"),
                ("bug", None, "🐞"),
            ],
            ["vocab.creativity", "vocab.innovation", "vocab.curiosity", "vocab.bug"],
            "A bug is a mistake in a program.",
            "creativity 🎨, innovation 🚀, curiosity 🧐, bug 🐞.",
        ),
        matching(
            "collocations-match",
            "VOCABULARY",
            "Match the verb to the noun it goes with.",
            [
                ("make", "a decision", None),
                ("take", "a risk", None),
                ("pay", "attention", None),
                ("do", "research", None),
            ],
            ["grammar.collocations"],
            "make a decision; take a risk.",
            "make a decision, take a risk, pay attention, do research.",
        ),
        choice(
            "find-collaboration",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: collaboration",
            [(None, "🤜"), (None, "🐞"), (None, "🎨")],
            "a",
            ["vocab.collaboration"],
            "People working together.",
            "🤜 collaboration.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-collocation",
            "LISTENING",
            "Listen. What does the coach tell the team to do?",
            "The coach tells them to …",
            [("take a break", "☕"), ("make a mistake", "❌"), ("do the washing", "🧺")],
            "a",
            ["grammar.collocations"],
            "Listen for 'take'.",
            "Take a break for fifteen minutes.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="You've been coding for eight hours. You've made great progress, but now I want you to take a break for fifteen minutes.",
        ),
        true_false(
            "listen-research",
            "LISTENING",
            "Listen to the mentor and Maya. True or false?",
            "The mentor suggests doing research with real users.",
            True,
            ["grammar.collocations"],
            "Listen to the mentor's second line.",
            "Do some quick research with real users.",
            listening_id="c1-7-mentor",
        ),
        true_false(
            "listen-buttons",
            "LISTENING",
            "Listen to the judges. True or false?",
            "The judges say the buttons are perfect for older users.",
            False,
            ["grammar.collocations", "grammar.abstract_nouns"],
            "Listen to the last comment.",
            "The buttons are a bit small for older users.",
            listening_id="c1-7-judges",
        ),
        blank(
            "abstract-blank",
            "GRAMMAR",
            "Complete with the abstract noun.",
            "She is very curious. Her ___ led to the discovery. He was kind. Everyone remembers his ___.",
            ["curiosity", "kindness"],
            ["curiosity", "curiousness", "kindness", "kindment"],
            ["grammar.abstract_nouns", "vocab.curiosity"],
            "curious → -ity; kind → -ness.",
            "Her curiosity … his kindness.",
        ),
        blank(
            "collocation-blank",
            "GRAMMAR",
            "Choose the right verbs.",
            "We ___ a lot of progress, so we decided to ___ a risk.",
            ["made", "take"],
            ["made", "did", "take", "make"],
            ["grammar.collocations"],
            "make progress; take a risk.",
            "We made a lot of progress, so we decided to take a risk.",
        ),
        choice(
            "collocation-wrong",
            "GRAMMAR",
            "Which sentence is correct?",
            "Choose the natural collocation.",
            [
                ("Please pay attention to the details.", None),
                ("Please make attention to the details.", None),
                ("Please do attention to the details.", None),
            ],
            "a",
            ["grammar.collocations"],
            "attention goes with pay.",
            "Please pay attention to the details.",
        ),
        choice(
            "nominalise",
            "GRAMMAR",
            "Choose the more formal version with an abstract noun.",
            "Because the team was resilient, they finished the app.",
            [
                ("The team's resilience allowed them to finish the app.", None),
                ("The team's resilient allowed them to finish the app.", None),
                ("The team resilienced and finished the app.", None),
            ],
            "a",
            ["grammar.abstract_nouns"],
            "resilient → resilience.",
            "The team's resilience allowed them to finish the app.",
        ),
        build(
            "build-collocation",
            "GRAMMAR",
            "Put the words in order.",
            "At five we made an important decision.",
            ["grammar.collocations", "grammar.abstract_nouns"],
            "Start with 'At five'.",
            "At five we made an important decision.",
        ),
        choice(
            "read-idea",
            "READING",
            "Read the text. Then answer.",
            "Where did the idea for the app come from?",
            [("Granny's memoir", "📔"), ("a video game", "🎮"), ("the judges", "🧑‍⚖️")],
            "a",
            ["vocab.memoir", "vocab.innovation"],
            "Look at paragraph 1.",
            "The idea came from Granny's memoir.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-alone",
            "READING",
            "Read the text. True or false?",
            "{boy} says he could have built the app alone.",
            False,
            ["vocab.collaboration"],
            "Look at paragraph 2.",
            "It was a genuine collaboration — nobody could have done it alone.",
        ),
        speak(
            "say-project",
            "Describe a project you worked on with others. Use at least two abstract nouns and three collocations.",
            "The project needed a lot of … We did … / made … / took … What I learned was the importance of …",
            "Our school magazine needed a lot of creativity. We did research, made some mistakes and took a few risks. What I learned was the importance of collaboration.",
            ["grammar.abstract_nouns", "grammar.collocations"],
        ),
        blank(
            "quiz-ppc-coding",
            "QUIZ",
            "Complete the sentence.",
            "By three a.m. we had ___ coding for eighteen hours.",
            ["been"],
            ["been", "being", "be"],
            ["grammar.past_perfect_continuous"],
            "Remember Lesson 6.",
            "We had been coding for eighteen hours.",
        ),
        choice(
            "quiz-cleft-courage",
            "QUIZ",
            "Choose the correct cleft sentence.",
            "The rewrite impressed the judges most.",
            [
                ("What impressed the judges most was the rewrite.", None),
                ("What impressed the judges most it was the rewrite.", None),
                ("It was the rewrite what impressed the judges most.", None),
            ],
            "a",
            ["grammar.cleft_sentences"],
            "Remember Unit 1, Lesson 3.",
            "What impressed the judges most was the rewrite.",
        ),
        choice(
            "quiz-hedge-app",
            "QUIZ",
            "Choose the most careful claim.",
            "Describe early user feedback.",
            [
                ("Early feedback suggests that the app may be useful for older people.", None),
                ("The app is definitely perfect for everyone.", None),
                ("Everybody will use this app.", None),
            ],
            "a",
            ["grammar.hedging"],
            "Remember Unit 1, Lesson 2.",
            "Early feedback suggests that the app may be useful.",
        ),
    ],
}

LESSON_8 = {
    "slug": L8,
    "title": "Job Shadow Day",
    "description": "{boy} spends a day at an architecture firm. Time to switch to formal English!",
    "minutes": 40,
    "objectives": [
        "Use workplace vocabulary: colleague, deadline, schedule, enquiry, appropriate.",
        "Recognise and use formal register in emails and conversations.",
        "Write a formal thank-you email.",
    ],
    "review": [
        "grammar.collocations",
        "grammar.abstract_nouns",
        "vocab.collaboration",
        "grammar.past_perfect_continuous",
        "grammar.indirect_questions",
        "phrase.polite_complaint",
        "grammar.passive_all",
        "grammar.would_like",
        "vocab.interview",
        "vocab.organise",
    ],
    "episode": (
        "A Day at the Studio",
        "{boy} shadows an architect for a day and learns that the way you speak matters as much as what you say.",
    ),
    "content": {
        "story_intro": "Every Year 12 student spends one day shadowing a professional. {boy} has chosen an architecture studio.",
        "reading": {
            "title": "Formal and Informal",
            "paragraphs": [
                {
                    "sentences": [
                        "Two weeks before my job shadow day, I sent an email to the studio. My first draft began: 'Hi! Can I come and see what you do?'",
                        "Mum read it and laughed. She said it was not appropriate for a professional enquiry.",
                    ]
                },
                {
                    "sentences": [
                        "My second version began: 'Dear Ms Grant, I am writing to enquire whether it would be possible to shadow one of your architects.'",
                        "Ms Grant replied the next day and invited me to come on Thursday.",
                    ]
                },
                {
                    "sentences": [
                        "At the studio, everybody was friendly, but I noticed that people changed their language depending on the situation.",
                        "With colleagues they said, 'Can you send me that?' With clients they said, 'Would you be able to forward the plans at your earliest convenience?'",
                    ]
                },
                {
                    "sentences": [
                        "Ms Grant's schedule was incredibly busy. She had three meetings and a deadline at five.",
                        "Despite this, she found time to show me how a building is designed, from the first sketch to the 3D model.",
                    ]
                },
                {
                    "sentences": [
                        "The next day I wrote a formal email to thank her: 'I would be grateful if you could keep me in mind for a summer placement.'",
                        "She replied: 'Please do not hesitate to contact me next spring.' I think that's a yes!",
                    ]
                },
            ],
            "highlight": [
                "Dear Ms Grant",
                "I am writing to enquire whether",
                "Would you be able to",
                "at your earliest convenience",
                "I would be grateful if",
                "Please do not hesitate to",
                "appropriate",
                "enquiry",
                "colleagues",
                "schedule",
                "deadline",
            ],
        },
        "listening": [
            {
                "id": "c1-8-phone",
                "title": "A formal phone call",
                "transcript": [
                    {
                        "speaker": "Receptionist",
                        "text": "Good morning, Grant Architects. How may I help you?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "Good morning. I'm calling to confirm my visit on Thursday. My name is {boy}.",
                    },
                    {
                        "speaker": "Receptionist",
                        "text": "Thank you. Could you please arrive at nine and report to reception?",
                    },
                    {"speaker": "{boy}", "text": "Certainly. Thank you for your help."},
                ],
            },
            {
                "id": "c1-8-colleagues",
                "title": "Between colleagues",
                "transcript": [
                    {
                        "speaker": "Tom",
                        "text": "Hey, have you finished the drawings for the library?",
                    },
                    {
                        "speaker": "Ms Grant",
                        "text": "Almost. Can you check them before lunch? The deadline's at five.",
                    },
                    {"speaker": "Tom", "text": "No problem. I'll grab a coffee and take a look."},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Formal register",
                "explanation": (
                    "Formal English is used in professional emails, letters and with people you don't know. "
                    "Features: no contractions (I am, not I'm); no slang; full, polite structures; "
                    "longer verbs: get → receive, need → require, help → assist, ask → enquire, start → commence. "
                    "Indirect polite forms: I would be grateful if you could … / Would you be able to …? / I was wondering whether … "
                    "Passive and abstract nouns: Your application has been received."
                ),
                "explanation_ru": (
                    "Официальный стиль: без сокращений и сленга, вежливые косвенные конструкции, «длинные» глаголы "
                    "(receive вместо get, assist вместо help)."
                ),
                "examples": [
                    "I am writing to apply for the position.",
                    "I would be grateful if you could send me further information.",
                    "Please find attached my CV.",
                    "I look forward to hearing from you.",
                ],
            },
            {
                "title": "Opening and closing a formal email",
                "explanation": (
                    "Open: Dear Mr / Ms + surname, (or Dear Sir or Madam, if you don't know the name). "
                    "First line: I am writing to … "
                    "Close: I look forward to hearing from you. Kind regards / Yours sincerely, + full name."
                ),
                "explanation_ru": "Начало: Dear Ms Grant, I am writing to … Окончание: I look forward to hearing from you. Kind regards, …",
                "examples": ["Dear Sir or Madam,", "Yours sincerely,", "Kind regards,"],
            },
        ],
    },
    "exercises": [
        matching(
            "work-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("colleague", None, "🧑‍💼"),
                ("deadline", None, "📅"),
                ("schedule", None, "🗓️"),
                ("enquiry", None, "❓"),
            ],
            ["vocab.colleague", "vocab.deadline", "vocab.schedule", "vocab.enquiry"],
            "A deadline is the last moment to finish something.",
            "colleague 🧑‍💼, deadline 📅, schedule 🗓️, enquiry ❓.",
        ),
        matching(
            "formal-informal",
            "VOCABULARY",
            "Match the informal word to its formal equivalent.",
            [
                ("get", "receive", None),
                ("help", "assist", None),
                ("ask", "enquire", None),
                ("need", "require", None),
            ],
            ["grammar.formal_register"],
            "Formal verbs are often longer.",
            "get → receive, help → assist, ask → enquire, need → require.",
        ),
        choice(
            "find-deadline",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: deadline",
            [(None, "📅"), (None, "🧑‍💼"), (None, "👔")],
            "a",
            ["vocab.deadline"],
            "The date you must finish by.",
            "📅 deadline.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-formal",
            "LISTENING",
            "Listen. Which situation is this?",
            "This is …",
            [
                ("a formal voicemail to a company", "📞"),
                ("a chat between two friends", "💬"),
                ("a teacher talking to a class", "🧑‍🏫"),
            ],
            "a",
            ["grammar.formal_register"],
            "Notice the polite, formal phrases.",
            "I would be grateful if you could return my call — that's formal.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Good afternoon. This is a message for Ms Grant regarding my placement enquiry. I would be grateful if you could return my call at your earliest convenience.",
        ),
        true_false(
            "listen-nine",
            "LISTENING",
            "Listen to the phone call. True or false?",
            "{boy} should arrive at nine and go to reception.",
            True,
            ["grammar.formal_register"],
            "Listen to the receptionist's second line.",
            "Could you please arrive at nine and report to reception?",
            listening_id="c1-8-phone",
        ),
        true_false(
            "listen-colleagues-formal",
            "LISTENING",
            "Listen to Tom and Ms Grant. True or false?",
            "The colleagues speak very formally to each other.",
            False,
            ["vocab.colleague", "grammar.formal_register"],
            "Listen to 'Hey' and 'grab a coffee'.",
            "They speak informally: Hey, No problem, grab a coffee.",
            listening_id="c1-8-colleagues",
        ),
        blank(
            "formal-blank",
            "GRAMMAR",
            "Complete the formal email.",
            "Dear Ms Grant, I am writing ___ enquire ___ it would be possible to visit your studio.",
            ["to", "whether"],
            ["to", "for", "whether", "what"],
            ["grammar.formal_register", "phrase.formal_email"],
            "I am writing to + verb; enquire whether …",
            "I am writing to enquire whether it would be possible …",
        ),
        choice(
            "most-formal",
            "GRAMMAR",
            "Which request is the most formal?",
            "You need the plans from a client.",
            [
                ("I would be grateful if you could send the plans.", None),
                ("Send me the plans, please.", None),
                ("Can you send the plans? Thanks!", None),
            ],
            "a",
            ["grammar.formal_register"],
            "I would be grateful if …",
            "I would be grateful if you could send the plans.",
        ),
        choice(
            "formal-close",
            "GRAMMAR",
            "Choose the best ending for a formal email.",
            "Finish your email to Ms Grant.",
            [
                ("I look forward to hearing from you. Kind regards,", None),
                ("Write back soon! Lots of love,", None),
                ("Bye for now, see ya!", None),
            ],
            "a",
            ["phrase.formal_email"],
            "Formal = polite and impersonal.",
            "I look forward to hearing from you. Kind regards,",
        ),
        blank(
            "formal-verbs-blank",
            "GRAMMAR",
            "Choose the formal verbs.",
            "We have ___ your application. Please let us know if you ___ any further information.",
            ["received", "require"],
            ["received", "got", "require", "need"],
            ["grammar.formal_register"],
            "get → receive; need → require.",
            "We have received your application … if you require any further information.",
        ),
        build(
            "build-formal",
            "GRAMMAR",
            "Put the words in order.",
            "Please do not hesitate to contact me.",
            ["grammar.formal_register"],
            "Start with 'Please do not'.",
            "Please do not hesitate to contact me.",
        ),
        choice(
            "read-first-draft",
            "READING",
            "Read the text. Then answer.",
            "Why did Mum laugh at {boy}'s first email?",
            [
                ("It was too informal for a professional enquiry.", "😅"),
                ("It had many spelling mistakes.", "✏️"),
                ("It was sent to the wrong company.", "📧"),
            ],
            "a",
            ["vocab.appropriate", "vocab.enquiry"],
            "Look at paragraph 1.",
            "It was not appropriate for a professional enquiry.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-schedule",
            "READING",
            "Read the text. True or false?",
            "Ms Grant had a quiet day with no meetings.",
            False,
            ["vocab.schedule", "vocab.deadline"],
            "Look at paragraph 4.",
            "She had three meetings and a deadline at five.",
        ),
        speak(
            "say-formal",
            "Say a short formal voicemail: you are asking a company if you can do a summer placement with them.",
            "Good morning. My name is … I am calling to enquire whether … I would be grateful if … I look forward to …",
            "Good morning. My name is Alex Smith. I am calling to enquire whether you offer summer placements for students. I would be grateful if you could call me back. I look forward to hearing from you.",
            ["grammar.formal_register", "phrase.formal_email"],
        ),
        choice(
            "quiz-collocation-deadline",
            "QUIZ",
            "Choose the natural collocation.",
            "To meet the deadline, we need to ___ an effort.",
            [("make", None), ("do", None), ("take", None)],
            "a",
            ["grammar.collocations", "vocab.deadline"],
            "Remember Lesson 7.",
            "We need to make an effort.",
        ),
        choice(
            "quiz-indirect-formal",
            "QUIZ",
            "Choose the polite indirect question.",
            "When does the placement start?",
            [
                ("Could you tell me when the placement starts?", None),
                ("Could you tell me when does the placement start?", None),
                ("Tell me when starts the placement.", None),
            ],
            "a",
            ["grammar.indirect_questions"],
            "Remember B2.",
            "Could you tell me when the placement starts?",
        ),
        blank(
            "quiz-ppc-office",
            "QUIZ",
            "Complete the sentence.",
            "Ms Grant looked tired. She had ___ working since six.",
            ["been"],
            ["been", "being", "be"],
            ["grammar.past_perfect_continuous"],
            "Remember Lesson 6.",
            "She had been working since six.",
        ),
    ],
}

LESSON_9 = {
    "slug": L9,
    "title": "Thinking Machines",
    "description": "The school robot goes wrong during a demonstration. What must have happened? The class discusses AI.",
    "minutes": 40,
    "objectives": [
        "Use AI vocabulary: algorithm, dataset, predict, malfunction, ethical.",
        "Make deductions about the past: must have, might have, can't have.",
        "Discuss the benefits and risks of artificial intelligence.",
    ],
    "review": [
        "grammar.formal_register",
        "vocab.colleague",
        "vocab.schedule",
        "grammar.collocations",
        "grammar.abstract_nouns",
        "grammar.hedging",
        "grammar.relative_clauses",
        "vocab.ai",
        "vocab.robot",
        "vocab.sensor",
    ],
    "episode": (
        "The Robot Who Said Hello to a Plant",
        "During open day, the school's AI robot greets a potted plant. {boy}'s team investigates.",
    ),
    "content": {
        "story_intro": "On open day, the IT club showed visitors a robot that recognises faces. It didn't go exactly to plan.",
        "reading": {
            "title": "What Went Wrong?",
            "paragraphs": [
                {
                    "sentences": [
                        "Our robot, Robo-Rex 2, had worked perfectly in rehearsals. But in front of fifty parents, it turned to a potted plant and said: 'Hello, Mr Lee!'",
                        "Everyone laughed — except Mr Lee.",
                    ]
                },
                {
                    "sentences": [
                        "Afterwards, we tried to work out what had happened. The battery was full, so it can't have been a power problem.",
                        "Maya suggested that the camera might have been affected by the bright sunlight from the window.",
                    ]
                },
                {
                    "sentences": [
                        "Then we checked the dataset. The algorithm had been trained on only two hundred photos, and many of them had been taken in the same room.",
                        "It must have learned that 'green background' meant 'Mr Lee', because he always stood next to the plant!",
                    ]
                },
                {
                    "sentences": [
                        "This led to a serious discussion in class. If a simple robot can make this mistake, what about AI systems that predict who gets a loan or a job?",
                        "Sam argued that they could be dangerous if nobody checks the data. Ms Okafor added that it is an ethical question as well as a technical one.",
                    ]
                },
                {
                    "sentences": [
                        "We retrained the robot with a much larger, more varied dataset. It hasn't malfunctioned since.",
                        "And Mr Lee has moved the plant — just in case.",
                    ]
                },
            ],
            "highlight": [
                "can't have been",
                "might have been affected",
                "must have learned",
                "algorithm",
                "dataset",
                "predict",
                "ethical",
                "malfunctioned",
            ],
        },
        "listening": [
            {
                "id": "c1-9-detectives",
                "title": "Robot detectives",
                "transcript": [
                    {"speaker": "Sam", "text": "Someone must have changed the code last night."},
                    {
                        "speaker": "{boy}",
                        "text": "It can't have been the code. Nobody has touched it for a week.",
                    },
                    {
                        "speaker": "Maya",
                        "text": "The cleaner might have moved the robot. Then the camera angle would be different.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "That's possible. Let's check the security video.",
                    },
                ],
            },
            {
                "id": "c1-9-ethics",
                "title": "A class discussion",
                "transcript": [
                    {"speaker": "Ms Okafor", "text": "Should AI be used to mark exams?"},
                    {"speaker": "Maya", "text": "It could save teachers a lot of time."},
                    {
                        "speaker": "{boy}",
                        "text": "But if the algorithm was trained on biased data, it might be unfair to some students.",
                    },
                    {
                        "speaker": "Ms Okafor",
                        "text": "Exactly. So who checks the algorithm? That's the ethical question.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Past modals of deduction",
                "explanation": (
                    "Use modal + have + past participle to make guesses about the past, based on evidence. "
                    "must have = I'm almost sure it happened: It must have learned the wrong pattern. "
                    "might / may / could have = it's possible: The light might have affected the camera. "
                    "can't / couldn't have = I'm almost sure it didn't happen: It can't have been the battery — it was full. "
                    "Passive: The camera might have been affected."
                ),
                "explanation_ru": (
                    "Предположения о прошлом: must have done — наверняка; might/could have done — возможно; "
                    "can't have done — не может быть, чтобы."
                ),
                "examples": [
                    "You must have been tired after the race.",
                    "She might have missed the bus.",
                    "He can't have seen us — he didn't wave.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "ai-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("algorithm", None, "🧮"),
                ("dataset", None, "🗄️"),
                ("predict", None, "🔮"),
                ("malfunction", None, "⚠️"),
            ],
            ["vocab.algorithm", "vocab.dataset", "vocab.predict", "vocab.malfunction"],
            "To predict = to say what will happen.",
            "algorithm 🧮, dataset 🗄️, predict 🔮, malfunction ⚠️.",
        ),
        matching(
            "ai-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("algorithm", "a set of rules a computer follows to solve a problem", None),
                ("dataset", "a collection of data used to train or test a system", None),
                ("ethical", "morally right or acceptable", None),
            ],
            ["vocab.algorithm", "vocab.dataset", "vocab.ethical"],
            "An AI learns from a dataset.",
            "algorithm = rules for solving a problem; dataset = collection of data; ethical = morally right.",
        ),
        choice(
            "find-malfunction",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: malfunction",
            [(None, "⚠️"), (None, "🔮"), (None, "🧭")],
            "a",
            ["vocab.malfunction"],
            "A warning that something isn't working properly.",
            "⚠️ malfunction.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-deduction",
            "LISTENING",
            "Listen. What does the speaker think happened to the phone?",
            "She thinks …",
            [
                ("someone must have taken it by mistake", "📱"),
                ("it can't have been in her bag", "👜"),
                ("it was stolen at home", "🏠"),
            ],
            "a",
            ["grammar.past_modals"],
            "Listen for 'must have'.",
            "Someone must have taken it by mistake.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="My phone was on the table a minute ago, and now it's gone. Someone must have taken it by mistake — they all look the same!",
        ),
        true_false(
            "listen-code",
            "LISTENING",
            "Listen to the robot detectives. True or false?",
            "{boy} is sure the problem was the code.",
            False,
            ["grammar.past_modals"],
            "Listen for 'can't have'.",
            "{boy}: It can't have been the code.",
            listening_id="c1-9-detectives",
        ),
        true_false(
            "listen-biased",
            "LISTENING",
            "Listen to the class discussion. True or false?",
            "{boy} thinks an algorithm trained on biased data might be unfair.",
            True,
            ["vocab.algorithm", "vocab.ethical"],
            "Listen to {boy}'s line.",
            "If the algorithm was trained on biased data, it might be unfair.",
            listening_id="c1-9-ethics",
        ),
        blank(
            "modals-blank",
            "GRAMMAR",
            "Choose the right modals.",
            "The battery was full, so it ___ have been a power problem. The sunlight ___ have affected the camera — we're not sure.",
            ["can't", "might"],
            ["can't", "must", "might"],
            ["grammar.past_modals"],
            "Impossible → can't have; possible → might have.",
            "It can't have been a power problem. The sunlight might have affected the camera.",
        ),
        choice(
            "must-have",
            "GRAMMAR",
            "Choose the best deduction.",
            "The robot always said 'Mr Lee' when it saw green. Mr Lee always stood next to the plant.",
            [
                ("It must have learned the wrong pattern.", None),
                ("It can't have learned anything.", None),
                ("It must learn the wrong pattern yesterday.", None),
            ],
            "a",
            ["grammar.past_modals", "vocab.algorithm"],
            "The evidence is very strong.",
            "It must have learned the wrong pattern.",
        ),
        choice(
            "modal-passive",
            "GRAMMAR",
            "Which sentence is correct?",
            "Make a passive deduction about the camera.",
            [
                ("The camera might have been affected by the light.", None),
                ("The camera might have affected by the light.", None),
                ("The camera might been affected by the light.", None),
            ],
            "a",
            ["grammar.past_modals"],
            "modal + have been + V3.",
            "The camera might have been affected by the light.",
        ),
        blank(
            "must-have-blank",
            "GRAMMAR",
            "Complete the deduction.",
            "You ran 21 kilometres? You must have ___ exhausted!",
            ["been"],
            ["been", "be", "being"],
            ["grammar.past_modals"],
            "must have + past participle.",
            "You must have been exhausted!",
        ),
        build(
            "build-modal",
            "GRAMMAR",
            "Put the words in order.",
            "Someone must have changed the code.",
            ["grammar.past_modals"],
            "Start with 'Someone must'.",
            "Someone must have changed the code.",
        ),
        choice(
            "read-cause",
            "READING",
            "Read the text. Then answer.",
            "What was the real cause of the robot's mistake?",
            [
                ("The dataset was too small and not varied enough.", "🗄️"),
                ("The battery was empty.", "🔋"),
                ("Mr Lee had changed the code.", "💻"),
            ],
            "a",
            ["vocab.dataset", "grammar.past_modals"],
            "Look at paragraph 3.",
            "It was trained on only two hundred photos, many from the same room.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-retrained",
            "READING",
            "Read the text. True or false?",
            "After retraining, the robot has malfunctioned several more times.",
            False,
            ["vocab.malfunction"],
            "Look at the last paragraph.",
            "It hasn't malfunctioned since.",
        ),
        speak(
            "say-ai",
            "Should AI be allowed to help students write essays? Give your opinion, one benefit, one risk and one deduction about why many schools have banned it.",
            "In my opinion … One benefit is … However, … Schools must have / might have …",
            "In my opinion, AI can be a useful tool. One benefit is that it explains difficult ideas. However, it might stop students from thinking. Schools must have banned it because they were worried about cheating.",
            ["grammar.past_modals", "vocab.ethical", "grammar.linking_arguments"],
        ),
        choice(
            "quiz-formal-apology",
            "QUIZ",
            "Choose the most formal sentence.",
            "Apologise to parents for the robot's mistake.",
            [
                ("We apologise for any confusion caused during the demonstration.", None),
                ("Sorry about the robot thing, guys!", None),
                ("Oops, our bad!", None),
            ],
            "a",
            ["grammar.formal_register"],
            "Remember Lesson 8.",
            "We apologise for any confusion caused during the demonstration.",
        ),
        blank(
            "quiz-noun-rely",
            "QUIZ",
            "Complete with the abstract noun.",
            "We need to improve the ___ of the system. (reliable)",
            ["reliability"],
            ["reliability", "reliableness", "reliance"],
            ["grammar.abstract_nouns"],
            "Remember Lesson 7: -able → -ability.",
            "We need to improve the reliability of the system.",
        ),
        choice(
            "quiz-seems-bias",
            "QUIZ",
            "Choose the best hedged sentence.",
            "Talk carefully about the robot's data.",
            [
                ("The dataset appears to have been too small.", None),
                ("The dataset appears being too small.", None),
                ("The dataset is appear to be too small.", None),
            ],
            "a",
            ["grammar.hedging", "vocab.dataset"],
            "Remember Unit 1, Lesson 2.",
            "The dataset appears to have been too small.",
        ),
    ],
}

LESSON_10 = {
    "slug": L10,
    "title": "Presentation Day",
    "description": "{boy} presents the hackathon app to the whole school. First of all … Then a big C1 review!",
    "minutes": 45,
    "objectives": [
        "Use presentation vocabulary: slide, handout, rehearse, summarise, emphasise.",
        "Structure a talk with discourse markers and signposting.",
        "Review C1: narrative tenses, hedging, cleft sentences, conditionals, inversion, modals, formal register.",
    ],
    "review": [
        "grammar.past_modals",
        "vocab.algorithm",
        "vocab.ethical",
        "grammar.formal_register",
        "grammar.collocations",
        "grammar.abstract_nouns",
        "grammar.past_perfect_continuous",
        "grammar.inversion",
        "grammar.mixed_conditionals",
        "grammar.cleft_sentences",
        "grammar.hedging",
        "grammar.narrative_tenses",
    ],
    "episode": (
        "Five Hundred Faces",
        "{boy} gives his first big presentation to the whole school. The projector fails in the first minute.",
    ),
    "content": {
        "story_intro": "The hackathon app, 'Story Bridge', has been chosen for a school assembly. {boy} has ten minutes to present it.",
        "reading": {
            "title": "My First Big Presentation",
            "paragraphs": [
                {
                    "sentences": [
                        "I had rehearsed my presentation at least ten times. First of all, I would introduce the problem; then I would show the app; finally, I would summarise the results.",
                        "What I hadn't planned for was the projector breaking in the first minute.",
                    ]
                },
                {
                    "sentences": [
                        "For a moment I froze. Then I remembered Ms Grant's advice: the slides support you, but you are the presentation.",
                        "So I said: 'As you can see — or rather, as you can't see — technology doesn't always cooperate!' Everyone laughed, and I relaxed.",
                    ]
                },
                {
                    "sentences": [
                        "Moving on to the app itself, I explained how Granny {gran1}'s memoir had inspired us. Luckily, Maya had printed handouts with screenshots.",
                        "I wanted to emphasise one point above all: the app connects generations.",
                    ]
                },
                {
                    "sentences": [
                        "Having said that, I was honest about the limits. The app appears to work well for small groups, but we haven't tested it with large numbers of users yet.",
                        "As I mentioned earlier, our first prototype had crashed at three in the morning — so we know about failure!",
                    ]
                },
                {
                    "sentences": [
                        "In short, it was not the presentation I had planned, but it may have been a better one.",
                        "Never have I been so nervous — or so proud — in front of five hundred people.",
                    ]
                },
            ],
            "highlight": [
                "First of all",
                "then",
                "finally",
                "Moving on to",
                "Having said that",
                "As I mentioned earlier",
                "In short",
                "rehearsed",
                "summarise",
                "slides",
                "handouts",
                "emphasise",
            ],
        },
        "listening": [
            {
                "id": "c1-10-talk",
                "title": "Part of {boy}'s talk",
                "transcript": [
                    {
                        "speaker": "{boy}",
                        "text": "First of all, I'd like to thank Granny {gran1}, without whom this app wouldn't exist.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "Let's turn to the problem we wanted to solve: older and younger people rarely share stories.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "To give you an example, my granny had been keeping her letters in a suitcase for fifty years.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "In short, Story Bridge helps those stories reach the next generation.",
                    },
                ],
            },
            {
                "id": "c1-10-questions",
                "title": "Questions from the audience",
                "transcript": [
                    {"speaker": "Student", "text": "How do you protect people's private stories?"},
                    {
                        "speaker": "{boy}",
                        "text": "That's a great question. At the moment, all stories are private unless the family decides to share them.",
                    },
                    {"speaker": "Student", "text": "And will the app be free?"},
                    {
                        "speaker": "{boy}",
                        "text": "Yes. Having said that, we might need sponsors to keep it running.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Discourse markers",
                "explanation": (
                    "Discourse markers organise speech and writing and guide the listener. "
                    "Introducing: First of all, … / To begin with, … "
                    "Moving on: Moving on to … / Let's turn to … / Next, … "
                    "Referring back: As I mentioned earlier, … "
                    "Adding: What's more, … / On top of that, … "
                    "Contrasting / conceding: Having said that, … / Even so, … / That said, … "
                    "Examples: To give you an example, … / For instance, … "
                    "Concluding: In short, … / To summarise, … / To conclude, …"
                ),
                "explanation_ru": (
                    "Дискурсивные маркеры организуют речь: First of all — прежде всего; Moving on to — переходя к; "
                    "Having said that — тем не менее; As I mentioned earlier — как я уже говорил; In short — короче говоря."
                ),
                "examples": [
                    "First of all, let me explain the problem.",
                    "Moving on to the results, …",
                    "Having said that, there is still a lot to do.",
                    "In short, the project was a success.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "presentation-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("slide", None, "🖼️"),
                ("handout", None, "📃"),
                ("rehearse", None, "🔁"),
                ("emphasise", None, "❗"),
            ],
            ["vocab.slide", "vocab.handout", "vocab.rehearse", "vocab.emphasise"],
            "You give a handout to the audience.",
            "slide 🖼️, handout 📃, rehearse 🔁, emphasise ❗.",
        ),
        matching(
            "markers-match",
            "VOCABULARY",
            "Match each discourse marker to its function.",
            [
                ("First of all", "introducing the first point", None),
                ("Having said that", "adding a contrast", None),
                ("In short", "concluding", None),
                ("As I mentioned earlier", "referring back", None),
            ],
            ["grammar.discourse_markers", "phrase.signposting"],
            "In short = in a few words.",
            "First of all → introduce; Having said that → contrast; In short → conclude; As I mentioned earlier → refer back.",
        ),
        choice(
            "find-handout",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: handout",
            [(None, "🖼️"), (None, "📃"), (None, "🎤")],
            "b",
            ["vocab.handout"],
            "Printed paper for the audience.",
            "📃 handout.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-marker",
            "LISTENING",
            "Listen. Which part of the presentation is the speaker starting?",
            "She is starting …",
            [("the conclusion", "🏁"), ("the introduction", "👋"), ("the questions", "❓")],
            "a",
            ["grammar.discourse_markers", "vocab.summarise"],
            "Listen for 'To summarise'.",
            "To summarise … — this is the conclusion.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="So, to summarise what we've seen today: the problem is real, the solution is simple, and we need your help.",
        ),
        true_false(
            "listen-suitcase",
            "LISTENING",
            "Listen to {boy}'s talk. True or false?",
            "{boy} gives an example about his granny's letters.",
            True,
            ["grammar.discourse_markers", "grammar.past_perfect_continuous"],
            "Listen for 'To give you an example'.",
            "My granny had been keeping her letters in a suitcase for fifty years.",
            listening_id="c1-10-talk",
        ),
        true_false(
            "listen-private",
            "LISTENING",
            "Listen to the questions. True or false?",
            "All stories in the app are public.",
            False,
            ["grammar.discourse_markers"],
            "Listen to {boy}'s first answer.",
            "All stories are private unless the family decides to share them.",
            listening_id="c1-10-questions",
        ),
        blank(
            "markers-blank",
            "GRAMMAR",
            "Choose the right discourse markers.",
            "___ to the results, the app works well. ___, we haven't tested it with large groups.",
            ["Moving on", "Having said that"],
            ["Moving on", "Having said that", "In short"],
            ["grammar.discourse_markers"],
            "Move on, then contrast.",
            "Moving on to the results … Having said that, we haven't tested it with large groups.",
        ),
        choice(
            "marker-conclude",
            "GRAMMAR",
            "Choose the best way to start your conclusion.",
            "You are finishing your presentation.",
            [
                ("In short, the app helps families share their stories.", None),
                ("First of all, the app helps families share their stories.", None),
                ("Moving on to, the app helps families share their stories.", None),
            ],
            "a",
            ["grammar.discourse_markers"],
            "Conclusion → In short / To summarise.",
            "In short, the app helps families share their stories.",
        ),
        choice(
            "signpost-back",
            "GRAMMAR",
            "Choose the best phrase to refer to an earlier point.",
            "You talked about the crash at the start.",
            [
                ("As I mentioned earlier, the prototype crashed at 3 a.m.", None),
                ("To begin with, the prototype crashed at 3 a.m.", None),
                ("Let's turn to, the prototype crashed at 3 a.m.", None),
            ],
            "a",
            ["phrase.signposting", "grammar.discourse_markers"],
            "Refer back → As I mentioned earlier.",
            "As I mentioned earlier, the prototype crashed at 3 a.m.",
        ),
        choice(
            "having-said-that",
            "GRAMMAR",
            "What does 'Having said that' introduce?",
            "The app is free. Having said that, we might need sponsors.",
            [
                ("a point that contrasts with or limits the previous one", None),
                ("an example", None),
                ("the first point of the talk", None),
            ],
            "a",
            ["grammar.discourse_markers"],
            "It's similar to 'However' or 'Even so'.",
            "Having said that = however / even so.",
        ),
        build(
            "build-marker",
            "GRAMMAR",
            "Put the words in order.",
            "Let's turn to the problem we wanted to solve.",
            ["phrase.signposting"],
            "Start with 'Let's turn'.",
            "Let's turn to the problem we wanted to solve.",
        ),
        order(
            "read-order",
            "READING",
            "Put {boy}'s presentation in order.",
            [
                "{boy} rehearsed the talk ten times.",
                "The projector broke in the first minute.",
                "He made a joke, and the audience laughed.",
                "He explained how Granny's memoir inspired the app.",
                "He talked honestly about the app's limits.",
            ],
            ["vocab.rehearse", "grammar.discourse_markers"],
            "The rehearsals came before the presentation.",
            "Rehearse → projector breaks → joke → the app → limits.",
        ),
        choice(
            "read-projector",
            "READING",
            "Read the text. Then answer.",
            "How did {boy} deal with the broken projector?",
            [
                ("He made a joke and continued without slides.", "😄"),
                ("He stopped the presentation.", "🛑"),
                ("He asked a teacher to fix it.", "🔧"),
            ],
            "a",
            ["vocab.slide"],
            "Look at paragraph 2.",
            "He made a joke, everyone laughed, and he relaxed.",
            ex_type="READING_COMPREHENSION",
        ),
        speak(
            "say-presentation",
            "Give a one-minute presentation about a project or hobby. Use at least four discourse markers.",
            "First of all, … Moving on to … Having said that, … As I mentioned earlier, … In short, …",
            "First of all, I'd like to talk about my photography project. Moving on to the results, I have taken over a thousand photos. Having said that, only ten are really good! In short, practice makes progress.",
            ["grammar.discourse_markers", "phrase.signposting"],
        ),
        choice(
            "quiz-must-have-projector",
            "QUIZ",
            "Choose the best deduction.",
            "The projector worked yesterday, and today it smells of smoke.",
            [
                ("Something must have overheated.", None),
                ("Something can't have overheated.", None),
                ("Something must overheat yesterday.", None),
            ],
            "a",
            ["grammar.past_modals"],
            "Remember Lesson 9.",
            "Something must have overheated.",
        ),
        choice(
            "quiz-formal-thanks",
            "QUIZ",
            "Choose the most formal sentence.",
            "Thank the head teacher after the assembly.",
            [
                ("I would like to express my gratitude for the opportunity.", None),
                ("Thanks a lot, it was cool!", None),
                ("Cheers for letting me talk.", None),
            ],
            "a",
            ["grammar.formal_register", "grammar.abstract_nouns"],
            "Remember Lesson 8.",
            "I would like to express my gratitude for the opportunity.",
        ),
        blank(
            "quiz-collocation-progress",
            "QUIZ",
            "Choose the natural collocation.",
            "Since the hackathon, the team has ___ a lot of progress.",
            ["made"],
            ["made", "done", "taken"],
            ["grammar.collocations"],
            "Remember Lesson 7.",
            "The team has made a lot of progress.",
        ),
        blank(
            "quiz-ppc-letters",
            "QUIZ",
            "Complete the sentence.",
            "Granny had ___ ___ the letters for fifty years before {boy} found them.",
            ["been", "keeping"],
            ["been", "being", "keeping", "kept"],
            ["grammar.past_perfect_continuous"],
            "Remember Lesson 6.",
            "Granny had been keeping the letters for fifty years.",
        ),
        choice(
            "quiz-inversion-nervous",
            "QUIZ",
            "Choose the correct sentence.",
            "Emphasise that you have never been so nervous.",
            [
                ("Never have I been so nervous.", None),
                ("Never I have been so nervous.", None),
                ("Never did I have been so nervous.", None),
            ],
            "a",
            ["grammar.inversion"],
            "Remember Unit 1, Lesson 5.",
            "Never have I been so nervous.",
        ),
        choice(
            "quiz-cleft-plan",
            "QUIZ",
            "Choose the correct cleft sentence.",
            "I hadn't planned for the projector breaking.",
            [
                ("What I hadn't planned for was the projector breaking.", None),
                ("What I hadn't planned for it was the projector breaking.", None),
                ("It was the projector what I hadn't planned for.", None),
            ],
            "a",
            ["grammar.cleft_sentences"],
            "Remember Unit 1, Lesson 3.",
            "What I hadn't planned for was the projector breaking.",
        ),
        blank(
            "quiz-mixed-rehearse",
            "QUIZ",
            "Complete the mixed conditional.",
            "If I hadn't rehearsed so much, I ___ be so calm now.",
            ["wouldn't"],
            ["wouldn't", "won't", "hadn't"],
            ["grammar.mixed_conditionals", "vocab.rehearse"],
            "Remember Unit 1, Lesson 4.",
            "If I hadn't rehearsed so much, I wouldn't be so calm now.",
        ),
        choice(
            "quiz-hedge-users",
            "QUIZ",
            "Choose the most careful claim.",
            "Describe the app's results.",
            [
                ("The app appears to work well for small groups.", None),
                ("The app works perfectly for everyone, always.", None),
                ("The app appears working well for small groups.", None),
            ],
            "a",
            ["grammar.hedging"],
            "Remember Unit 1, Lesson 2.",
            "The app appears to work well for small groups.",
        ),
        blank(
            "quiz-narrative-froze",
            "QUIZ",
            "Choose the best tenses.",
            "I ___ rehearsed ten times, but when the projector broke, I ___ for a moment.",
            ["had", "froze"],
            ["had", "have", "froze", "was freezing"],
            ["grammar.narrative_tenses"],
            "Remember Unit 1, Lesson 1.",
            "I had rehearsed ten times, but when the projector broke, I froze.",
        ),
    ],
}

UNIT = {
    "slug": "voices-and-futures",
    "title": "Voices and Futures",
    "description": "Granny's memoir, a hackathon, a job shadow day, a confused robot and a big presentation.",
    "lessons": [LESSON_6, LESSON_7, LESSON_8, LESSON_9, LESSON_10],
}
