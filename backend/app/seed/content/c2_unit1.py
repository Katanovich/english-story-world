"""C2 · Unit 1 "The Art of Language" (C2 lessons 1-5).

{boy} is eighteen and in his final year of school. Topics: idioms at the family dinner table,
reading the classics, humour and wordplay, the academic essay, a formal debate. Grammar:
fixed idiomatic expressions, participle clauses, understatement, nominalisation, fronting
for emphasis. Lesson 5 reviews the unit.
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

L1, L2, L3, L4, L5 = (
    "idioms-at-the-dinner-table",
    "reading-the-classics",
    "humour-and-wordplay",
    "the-academic-essay",
    "the-formal-debate",
)

ITEMS: dict[str, Item] = {
    # Lesson 1
    "vocab.idiom": (V, "idiom", "🗝️", "идиома", L1, ["'Break the ice' is a common idiom."], None),
    "vocab.literal": (
        V,
        "literal",
        "📏",
        "буквальный",
        L1,
        ["The literal meaning is quite different."],
        None,
    ),
    "vocab.figurative": (
        V,
        "figurative",
        "🎭",
        "переносный, образный",
        L1,
        ["Here 'cold' is used in a figurative sense."],
        None,
    ),
    "vocab.metaphor": (
        V,
        "metaphor",
        "🌉",
        "метафора",
        L1,
        ["'Time is money' is a metaphor."],
        None,
    ),
    "phrase.break_the_ice": (
        P,
        "break the ice",
        "🧊",
        "растопить лёд, начать общение",
        L1,
        ["Dad told a joke to break the ice."],
        "Make people feel relaxed at the start of a conversation.",
    ),
    "phrase.spill_the_beans": (
        P,
        "spill the beans",
        "🫘",
        "проболтаться, выдать секрет",
        L1,
        ["Who spilled the beans about the party?"],
        "Tell a secret too early.",
    ),
    "phrase.bite_off_more": (
        P,
        "bite off more than you can chew",
        "🍖",
        "взяться за непосильное",
        L1,
        ["I bit off more than I could chew with three clubs."],
        "Try to do more than you are able to.",
    ),
    "grammar.idiom_form": (
        G,
        "Idioms: fixed words, flexible tense",
        None,
        "Идиомы: слова фиксированы, время меняется",
        L1,
        ["She spilled the beans.", "He's always biting off more than he can chew."],
        "You can change the verb tense and pronouns in an idiom, but not its key words or their order.",
    ),
    # Lesson 2
    "vocab.protagonist": (
        V,
        "protagonist",
        "🦸",
        "главный герой",
        L2,
        ["The protagonist is a young orphan."],
        None,
    ),
    "vocab.narrator": (
        V,
        "narrator",
        "🗣️",
        "рассказчик",
        L2,
        ["The narrator is not entirely honest."],
        None,
    ),
    "vocab.theme": (
        V,
        "theme",
        "🧵",
        "тема (произведения)",
        L2,
        ["The main theme is loneliness."],
        None,
    ),
    "vocab.symbolism": (
        V,
        "symbolism",
        "🕊️",
        "символизм",
        L2,
        ["The dove has a clear symbolism."],
        None,
    ),
    "vocab.imagery": (
        V,
        "imagery",
        "🖌️",
        "образность, образы",
        L2,
        ["The poem is full of sea imagery."],
        None,
    ),
    "vocab.tone": (
        V,
        "tone",
        "🎚️",
        "тон, настроение",
        L2,
        ["The tone becomes darker in chapter three."],
        None,
    ),
    "grammar.participle_clauses": (
        G,
        "Having finished …, / Written in 1847, … / Looking back, …",
        None,
        "Причастные обороты",
        L2,
        [
            "Written in 1847, the novel shocked its readers.",
            "Having lost her family, the heroine moves to London.",
        ],
        "Participle clauses make writing concise: -ing (active), past participle (passive), having + V3 (earlier action).",
    ),
    # Lesson 3
    "vocab.pun": (V, "pun", "🍞", "каламбур", L3, ["'I knead you' is a bread pun."], None),
    "vocab.irony": (
        V,
        "irony",
        "🙃",
        "ирония",
        L3,
        ["The irony is that the fire station burned down."],
        None,
    ),
    "vocab.understatement": (
        V,
        "understatement",
        "🤏",
        "преуменьшение",
        L3,
        ["'It's a bit wet' — during a flood — is an understatement."],
        None,
    ),
    "vocab.sarcasm": (
        V,
        "sarcasm",
        "😏",
        "сарказм",
        L3,
        ["'Oh, great,' he said with sarcasm."],
        None,
    ),
    "vocab.wit": (V, "wit", "⚡", "остроумие", L3, ["Granny is famous for her wit."], None),
    "vocab.ambiguous": (
        V,
        "ambiguous",
        "❔",
        "двусмысленный",
        L3,
        ["The headline was ambiguous."],
        None,
    ),
    "grammar.understatement": (
        G,
        "not bad / not exactly / a bit of a … / hardly",
        None,
        "Преуменьшение и литота",
        L3,
        [
            "The film wasn't bad at all. (= it was very good)",
            "It was a bit of a disaster. (= a complete disaster)",
        ],
        "British English often says less than it means: not bad, not exactly, a bit, rather, hardly ideal.",
    ),
    # Lesson 4
    "vocab.thesis": (
        V,
        "thesis statement",
        "🎯",
        "главный тезис",
        L4,
        ["Your thesis statement should be clear."],
        None,
    ),
    "vocab.cite": (
        V,
        "cite",
        "🔖",
        "цитировать, ссылаться",
        L4,
        ["Always cite your sources."],
        None,
    ),
    "vocab.plagiarism": (
        V,
        "plagiarism",
        "🚫",
        "плагиат",
        L4,
        ["Plagiarism is taken very seriously."],
        None,
    ),
    "vocab.coherent": (
        V,
        "coherent",
        "🔗",
        "связный, логичный",
        L4,
        ["The argument is clear and coherent."],
        None,
    ),
    "vocab.concise": (
        V,
        "concise",
        "✂️",
        "сжатый, краткий",
        L4,
        ["Be concise: cut every unnecessary word."],
        None,
    ),
    "grammar.nominalisation": (
        G,
        "They decided → The decision …",
        None,
        "Номинализация (замена глаголов существительными)",
        L4,
        [
            "The introduction of the law led to protests.",
            "There has been a significant increase in screen time.",
        ],
        "Academic English turns verbs and adjectives into nouns to sound objective and concise.",
    ),
    # Lesson 5
    "vocab.motion": (
        V,
        "motion",
        "📜",
        "тема дебатов (тезис)",
        L5,
        ["The motion is: This house would ban homework."],
        None,
    ),
    "vocab.rebuttal": (
        V,
        "rebuttal",
        "🛡️",
        "опровержение",
        L5,
        ["Her rebuttal was devastating."],
        None,
    ),
    "vocab.concede": (
        V,
        "concede",
        "🏳️",
        "признавать, уступать",
        L5,
        ["I concede that the cost is high."],
        None,
    ),
    "vocab.eloquent": (
        V,
        "eloquent",
        "🎙️",
        "красноречивый",
        L5,
        ["He gave an eloquent speech."],
        None,
    ),
    "vocab.rhetorical_question": (
        V,
        "rhetorical question",
        "❓",
        "риторический вопрос",
        L5,
        ["'Who wants to fail?' is a rhetorical question."],
        None,
    ),
    "grammar.fronting": (
        G,
        "Far from …, / So … that … / Such was … that …",
        None,
        "Вынесение в начало (fronting) для эмфазы",
        L5,
        [
            "Far from solving the problem, the ban would make it worse.",
            "So strong was the evidence that the judges agreed.",
        ],
        "Move an element to the front for emphasis; with So / Such + be, invert the verb.",
    ),
}


LESSON_1 = {
    "slug": L1,
    "title": "Idioms at the Dinner Table",
    "description": "Sunday dinner with the whole family — and Granny {gran2}'s idioms fly across the table.",
    "minutes": 40,
    "objectives": [
        "Understand and use common idioms: break the ice, spill the beans, bite off more than you can chew.",
        "Distinguish between literal and figurative meaning.",
        "Adapt the tense of an idiom without changing its fixed words.",
    ],
    "review": [
        "grammar.discourse_markers",
        "phrase.signposting",
        "vocab.rehearse",
        "grammar.past_modals",
        "grammar.collocations",
        "grammar.hedging",
        "grammar.inversion",
        "phrase.break_a_leg",
        "vocab.surprise",
        "vocab.family",
    ],
    "episode": (
        "Who Spilled the Beans?",
        "The family plans a surprise for Granny {gran2}'s eightieth birthday. Then somebody spills the beans.",
    ),
    "content": {
        "story_intro": "{boy} is eighteen and in his final year of school. Every Sunday the whole family has dinner together.",
        "reading": {
            "title": "Sunday Dinner",
            "paragraphs": [
                {
                    "sentences": [
                        "At our Sunday dinners, idioms fly across the table faster than the potatoes.",
                        "Granny {gran2} is the champion: she can't say two sentences without one.",
                    ]
                },
                {
                    "sentences": [
                        "Last Sunday, Aunt {aunt} brought her new colleague, who was very shy. Dad told a terrible joke to break the ice, and it worked — everyone groaned, then laughed.",
                        "Taken literally, 'break the ice' sounds like something you'd do on a frozen lake, but its figurative meaning is much friendlier.",
                    ]
                },
                {
                    "sentences": [
                        "Then I mentioned that I had joined three clubs and applied to five universities. Granny raised an eyebrow: 'You've bitten off more than you can chew, my dear.'",
                        "She wasn't wrong. I had been sleeping five hours a night.",
                    ]
                },
                {
                    "sentences": [
                        "The real drama came at dessert. We had been planning a surprise party for Granny's eightieth birthday for weeks.",
                        "Suddenly {little} said: 'Granny, are you excited about Saturday?' She had spilled the beans!",
                    ]
                },
                {
                    "sentences": [
                        "Granny just smiled. 'Don't worry, love. At my age, every day is a surprise.'",
                        "Idioms, I've realised, are a kind of family memory: metaphors we pass down along with the recipes.",
                    ]
                },
            ],
            "highlight": [
                "break the ice",
                "Taken literally",
                "figurative",
                "bitten off more than you can chew",
                "spilled the beans",
                "idioms",
                "metaphors",
            ],
        },
        "listening": [
            {
                "id": "c2-1-colleague",
                "title": "Breaking the ice",
                "transcript": [
                    {
                        "speaker": "Aunt {aunt}",
                        "text": "This is Jonas. He's just moved here from Norway.",
                    },
                    {
                        "speaker": "Dad",
                        "text": "Welcome! So, Jonas — what do polar bears eat for lunch? Ice-burgers!",
                    },
                    {"speaker": "Jonas", "text": "That's... actually quite funny."},
                    {"speaker": "Mum", "text": "Well, at least it broke the ice."},
                ],
            },
            {
                "id": "c2-1-secret",
                "title": "Who told her?",
                "transcript": [
                    {
                        "speaker": "{teen}",
                        "text": "Someone must have spilled the beans. Granny knows about the party.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "It wasn't me! I've been keeping it under my hat for weeks.",
                    },
                    {"speaker": "{little}", "text": "Oops. I think it might have been me..."},
                    {"speaker": "{teen}", "text": "Never mind. It's water under the bridge now."},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Idioms: fixed form, flexible grammar",
                "explanation": (
                    "An idiom's meaning cannot be guessed from its individual words. "
                    "Its key words are fixed: you can't say 'spill the peas' or 'break the snow'. "
                    "But the grammar around it is flexible: change the tense and pronouns to fit the sentence. "
                    "Present: She always spills the beans. Past: He spilled / spilt the beans. Perfect: You've bitten off more than you can chew. "
                    "Some idioms are informal — use them in conversation, not in academic essays."
                ),
                "explanation_ru": (
                    "Значение идиомы нельзя понять из отдельных слов. Ключевые слова менять нельзя, "
                    "но время и местоимения — можно: He spilled the beans, You've bitten off more than you can chew."
                ),
                "examples": [
                    "We need someone to break the ice.",
                    "Don't spill the beans!",
                    "I've bitten off more than I can chew this term.",
                ],
            },
            {
                "title": "Literal and figurative meaning",
                "explanation": (
                    "Literal = the basic, physical meaning: He broke the ice on the pond. "
                    "Figurative = an extended or metaphorical meaning: He broke the ice at the party. "
                    "Metaphors describe one thing as another: Time is money. Life is a journey."
                ),
                "explanation_ru": "Буквальное значение — прямое; переносное — образное, метафорическое.",
                "examples": [
                    "Her words were a knife. (metaphor)",
                    "She has a heart of gold. (figurative)",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "idiom-meanings",
            "VOCABULARY",
            "Match each idiom to its meaning.",
            [
                ("break the ice", "help people relax when they first meet", None),
                ("spill the beans", "reveal a secret too early", None),
                ("bite off more than you can chew", "try to do too much", None),
            ],
            ["phrase.break_the_ice", "phrase.spill_the_beans", "phrase.bite_off_more"],
            "Think about the figurative meaning, not the food!",
            "break the ice = help people relax; spill the beans = reveal a secret; bite off more than you can chew = try to do too much.",
        ),
        matching(
            "language-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("literal", "the basic, exact meaning of a word", None),
                ("figurative", "used in a non-literal, imaginative way", None),
                ("metaphor", "describing something as if it were something else", None),
                ("idiom", "a phrase whose meaning differs from its words", None),
            ],
            ["vocab.literal", "vocab.figurative", "vocab.metaphor", "vocab.idiom"],
            "'Time is money' is a metaphor.",
            "literal = exact meaning; figurative = imaginative; metaphor = A is B; idiom = meaning differs from the words.",
        ),
        choice(
            "find-ice",
            "VOCABULARY",
            "Tap the picture that matches the idiom.",
            "Which idiom does this picture remind you of? 🧊🔨",
            [("break the ice", "🧊"), ("spill the beans", "🫘"), ("a piece of cake", "🍰")],
            "a",
            ["phrase.break_the_ice"],
            "Ice that gets broken.",
            "🧊 break the ice.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-idiom",
            "LISTENING",
            "Listen. What does the speaker mean?",
            "The speaker means that …",
            [
                ("she has taken on too much work", "📚"),
                ("she is very hungry", "🍽️"),
                ("she has a toothache", "🦷"),
            ],
            "a",
            ["phrase.bite_off_more", "grammar.idiom_form"],
            "Think figuratively.",
            "I've bitten off more than I can chew = I've taken on too much.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Three essays, a part-time job and the school play? I think I've bitten off more than I can chew this term.",
        ),
        true_false(
            "listen-broke-ice",
            "LISTENING",
            "Listen to the dinner conversation. True or false?",
            "Dad's joke helped everyone to relax.",
            True,
            ["phrase.break_the_ice"],
            "Listen to Mum's comment.",
            "Mum: Well, at least it broke the ice.",
            listening_id="c2-1-colleague",
        ),
        true_false(
            "listen-who-told",
            "LISTENING",
            "Listen to {teen}, {boy} and {little}. True or false?",
            "{boy} spilled the beans about the party.",
            False,
            ["phrase.spill_the_beans", "grammar.past_modals"],
            "Who says 'Oops'?",
            "{little} admits it might have been her.",
            listening_id="c2-1-secret",
        ),
        blank(
            "idiom-tense-blank",
            "GRAMMAR",
            "Complete the idioms in the correct form.",
            "Yesterday {little} ___ the beans. This term I've ___ off more than I can chew.",
            ["spilled", "bitten"],
            ["spilled", "spills", "bitten", "bit"],
            ["grammar.idiom_form", "phrase.spill_the_beans", "phrase.bite_off_more"],
            "Past simple; present perfect (bite → bitten).",
            "Yesterday {little} spilled the beans. This term I've bitten off more than I can chew.",
        ),
        choice(
            "idiom-fixed",
            "GRAMMAR",
            "Which sentence uses the idiom correctly?",
            "Choose one.",
            [
                ("He told a joke to break the ice.", None),
                ("He told a joke to break the snow.", None),
                ("He told a joke to crack the ice cube.", None),
            ],
            "a",
            ["grammar.idiom_form", "phrase.break_the_ice"],
            "The key words of an idiom are fixed.",
            "He told a joke to break the ice.",
        ),
        choice(
            "literal-or-fig",
            "GRAMMAR",
            "In which sentence is the phrase used figuratively?",
            "Choose one.",
            [
                ("At the party, Jonas finally broke the ice by asking about football.", None),
                ("The fisherman broke the ice to catch a fish.", None),
                ("The ship broke the ice in the frozen harbour.", None),
            ],
            "a",
            ["vocab.figurative", "vocab.literal", "phrase.break_the_ice"],
            "Which one has no real ice?",
            "Breaking the ice at a party is figurative.",
        ),
        choice(
            "idiom-register",
            "GRAMMAR",
            "Where would the idiom be least appropriate?",
            "'She spilled the beans about the merger.'",
            [
                ("in an academic essay", None),
                ("in a chat with friends", None),
                ("in an informal email to a colleague", None),
            ],
            "a",
            ["grammar.idiom_form", "phrase.spill_the_beans"],
            "Many idioms are informal.",
            "In an academic essay, write 'revealed the information' instead.",
        ),
        build(
            "build-idiom",
            "GRAMMAR",
            "Put the words in order.",
            "Who spilled the beans about the party?",
            ["phrase.spill_the_beans", "grammar.idiom_form"],
            "Start with 'Who'.",
            "Who spilled the beans about the party?",
        ),
        choice(
            "read-memory",
            "READING",
            "Read the text. Then answer.",
            "How does {boy} describe idioms at the end?",
            [
                ("as a kind of family memory passed down like recipes", "📖"),
                ("as a waste of time", "⏳"),
                ("as something only old people use", "👵"),
            ],
            "a",
            ["vocab.idiom", "vocab.metaphor"],
            "Look at the last paragraph.",
            "Idioms are a kind of family memory: metaphors we pass down along with the recipes.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-surprise",
            "READING",
            "Read the text. True or false?",
            "Granny {gran2} was upset that the surprise was ruined.",
            False,
            ["phrase.spill_the_beans"],
            "Look at the last paragraph.",
            "Granny just smiled: At my age, every day is a surprise.",
        ),
        speak(
            "say-idioms",
            "Tell a short story about a time when you (or someone you know) broke the ice, spilled the beans, or bit off more than you could chew.",
            "Last year I … I had bitten off more than I could chew … / Someone spilled the beans …",
            "Last year I joined the drama club, the debate club and the football team. I had definitely bitten off more than I could chew, so I dropped football.",
            ["grammar.idiom_form", "phrase.bite_off_more"],
        ),
        choice(
            "quiz-marker",
            "QUIZ",
            "Choose the best discourse marker.",
            "Idioms are colourful. ___, they can confuse learners.",
            [("Having said that", None), ("First of all", None), ("In short", None)],
            "a",
            ["grammar.discourse_markers"],
            "Remember C1, Lesson 10.",
            "Having said that, they can confuse learners.",
        ),
        choice(
            "quiz-must-have-told",
            "QUIZ",
            "Choose the best deduction.",
            "Granny knew about the party, and only {little} talked to her.",
            [
                ("{little} must have told her.", None),
                ("{little} can't have told her.", None),
                ("{little} must told her.", None),
            ],
            "a",
            ["grammar.past_modals"],
            "Remember C1, Lesson 9.",
            "{little} must have told her.",
        ),
        blank(
            "quiz-break-a-leg",
            "QUIZ",
            "Complete the idiom.",
            "Before the play, {teen} wished me luck: 'Break a ___!'",
            ["leg"],
            ["leg", "arm", "heart"],
            ["phrase.break_a_leg"],
            "Remember B1, Lesson 5.",
            "Break a leg!",
        ),
    ],
}

LESSON_2 = {
    "slug": L2,
    "title": "Reading the Classics",
    "description": "{boy}'s literature class studies a nineteenth-century novel. Having read it, he has opinions!",
    "minutes": 40,
    "objectives": [
        "Use literary analysis vocabulary: protagonist, narrator, theme, symbolism, imagery, tone.",
        "Use participle clauses to write concisely.",
        "Write a short literary analysis.",
    ],
    "review": [
        "grammar.idiom_form",
        "vocab.figurative",
        "vocab.metaphor",
        "grammar.narrative_tenses",
        "grammar.past_perfect_continuous",
        "grammar.hedging",
        "grammar.relative_clauses",
        "vocab.character",
        "vocab.plot",
        "vocab.setting",
    ],
    "episode": (
        "The Storm in Chapter Nine",
        "{boy} argues with his literature teacher about what the storm in the novel really means.",
    ),
    "content": {
        "story_intro": "In literature class, {boy}'s group is analysing a classic novel set on the wild Yorkshire moors.",
        "reading": {
            "title": "An Essay on the Novel",
            "paragraphs": [
                {
                    "sentences": [
                        "Written in 1847, the novel shocked many of its first readers.",
                        "Its protagonist, a proud and passionate orphan, is unlike any hero of the time.",
                    ]
                },
                {
                    "sentences": [
                        "The story is told by two narrators, neither of whom can be fully trusted.",
                        "Having heard only their versions, the reader must decide what really happened.",
                    ]
                },
                {
                    "sentences": [
                        "One central theme is the conflict between nature and civilisation.",
                        "Describing the moors with dark, violent imagery, the author makes the landscape almost a character.",
                    ]
                },
                {
                    "sentences": [
                        "The storm in chapter nine is rich in symbolism. Breaking the old tree, it seems to mark the end of the protagonist's childhood.",
                        "My teacher, however, read it as a symbol of anger rather than loss.",
                    ]
                },
                {
                    "sentences": [
                        "Looking back, I think we were both right. The tone of the novel is deliberately ambiguous.",
                        "That, perhaps, is why it is still read and argued about almost two centuries later.",
                    ]
                },
            ],
            "highlight": [
                "Written in 1847",
                "Having heard",
                "Describing",
                "Breaking",
                "Looking back",
                "protagonist",
                "narrators",
                "theme",
                "imagery",
                "symbolism",
                "tone",
            ],
        },
        "listening": [
            {
                "id": "c2-2-seminar",
                "title": "The seminar",
                "transcript": [
                    {"speaker": "Teacher", "text": "So what does the storm symbolise, {boy}?"},
                    {
                        "speaker": "{boy}",
                        "text": "Having read the chapter twice, I'd say it represents the end of childhood.",
                    },
                    {
                        "speaker": "Teacher",
                        "text": "Interesting. I've always seen it as an image of rage.",
                    },
                    {
                        "speaker": "Maya",
                        "text": "Couldn't it be both? The tone is ambiguous on purpose.",
                    },
                ],
            },
            {
                "id": "c2-2-library",
                "title": "In the library",
                "transcript": [
                    {
                        "speaker": "Librarian",
                        "text": "Looking for the novel? The last copy was borrowed this morning.",
                    },
                    {"speaker": "{boy}", "text": "Oh no. Is there an e-book version?"},
                    {
                        "speaker": "Librarian",
                        "text": "Yes. Published so long ago, it's free online — no copyright.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Participle clauses",
                "explanation": (
                    "Participle clauses replace longer clauses and make writing more concise and literary. "
                    "Present participle (-ing), active, same time: Describing the moors, the author uses dark imagery. (= When she describes …) "
                    "Past participle, passive: Written in 1847, the novel shocked readers. (= Because it was written …) "
                    "Perfect participle (having + V3), an earlier action: Having heard only their versions, the reader must decide. "
                    "The subject of the participle clause must be the same as the subject of the main clause."
                ),
                "explanation_ru": (
                    "Причастные обороты сокращают предложения: -ing (активное действие одновременно), "
                    "V3 (пассив), having + V3 (действие раньше). Подлежащее у оборота и главного предложения — одно и то же."
                ),
                "examples": [
                    "Having finished the novel, I wrote my essay.",
                    "Set in Yorkshire, the story begins in winter.",
                    "Walking across the moors, she felt free.",
                ],
            },
            {
                "title": "The dangling participle",
                "explanation": (
                    "Avoid a participle clause whose subject is different from the main clause — it sounds funny or confusing. "
                    "✗ Walking across the moors, the wind was cold. (The wind wasn't walking!) "
                    "✓ Walking across the moors, she felt the cold wind."
                ),
                "explanation_ru": "Ошибка «висячее причастие»: подлежащие должны совпадать.",
                "examples": ["✓ Having lost the key, he climbed through the window."],
            },
        ],
    },
    "exercises": [
        matching(
            "literary-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("protagonist", "the main character of a story", None),
                ("narrator", "the voice that tells the story", None),
                ("theme", "a central idea explored in a work", None),
                ("tone", "the attitude or mood of the writing", None),
            ],
            ["vocab.protagonist", "vocab.narrator", "vocab.theme", "vocab.tone"],
            "The protagonist is the hero (or anti-hero).",
            "protagonist = main character; narrator = the storyteller; theme = central idea; tone = mood.",
        ),
        matching(
            "literary-pictures",
            "VOCABULARY",
            "Match the term to the picture.",
            [("symbolism", None, "🕊️"), ("imagery", None, "🖌️"), ("narrator", None, "🗣️")],
            ["vocab.symbolism", "vocab.imagery", "vocab.narrator"],
            "A dove often symbolises peace.",
            "symbolism 🕊️, imagery 🖌️, narrator 🗣️.",
        ),
        choice(
            "find-symbol",
            "VOCABULARY",
            "Tap the right picture.",
            "Which image is a common symbol of peace?",
            [(None, "🕊️"), (None, "⚔️"), (None, "🌩️")],
            "a",
            ["vocab.symbolism"],
            "A white bird.",
            "🕊️ the dove symbolises peace.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-participle",
            "LISTENING",
            "Listen. What did the student do first?",
            "First she …",
            [("finished the novel", "📕"), ("wrote the essay", "📝"), ("watched the film", "🎬")],
            "a",
            ["grammar.participle_clauses"],
            "Listen for 'Having …'.",
            "Having finished the novel, she started her essay.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Having finished the novel late on Sunday, she started her essay at midnight — and then watched the film for 'research'.",
        ),
        true_false(
            "listen-storm-both",
            "LISTENING",
            "Listen to the seminar. True or false?",
            "Maya suggests the storm could mean both things.",
            True,
            ["vocab.symbolism", "vocab.tone"],
            "Listen to Maya.",
            "Couldn't it be both? The tone is ambiguous on purpose.",
            listening_id="c2-2-seminar",
        ),
        true_false(
            "listen-ebook",
            "LISTENING",
            "Listen to the librarian. True or false?",
            "{boy} has to pay for the e-book.",
            False,
            ["grammar.participle_clauses"],
            "Why is it free?",
            "Published so long ago, it's free online — no copyright.",
            listening_id="c2-2-library",
        ),
        blank(
            "participle-blank",
            "GRAMMAR",
            "Choose the right participles.",
            "___ in 1847, the novel shocked readers. ___ read it twice, I understood the ending.",
            ["Written", "Having"],
            ["Written", "Writing", "Having", "Had"],
            ["grammar.participle_clauses"],
            "The novel was written (passive); I had read it before (perfect).",
            "Written in 1847, … Having read it twice, …",
        ),
        choice(
            "participle-rewrite",
            "GRAMMAR",
            "Choose the best concise version.",
            "After she had lost her family, the heroine moved to London.",
            [
                ("Having lost her family, the heroine moved to London.", None),
                ("Lost her family, the heroine moved to London.", None),
                ("Having losing her family, the heroine moved to London.", None),
            ],
            "a",
            ["grammar.participle_clauses"],
            "An earlier action → having + V3.",
            "Having lost her family, the heroine moved to London.",
        ),
        choice(
            "dangling",
            "GRAMMAR",
            "Which sentence is correct (no dangling participle)?",
            "Choose one.",
            [
                ("Walking across the moors, she felt the cold wind.", None),
                ("Walking across the moors, the wind was cold.", None),
                ("Walking across the moors, the cold was felt.", None),
            ],
            "a",
            ["grammar.participle_clauses"],
            "Who is walking?",
            "Walking across the moors, she felt the cold wind.",
        ),
        blank(
            "describing-blank",
            "GRAMMAR",
            "Choose the right participle.",
            "___ the landscape with violent imagery, the author makes it feel alive.",
            ["Describing"],
            ["Describing", "Described", "Having described"],
            ["grammar.participle_clauses", "vocab.imagery"],
            "Active, at the same time as the main verb.",
            "Describing the landscape with violent imagery, …",
        ),
        build(
            "build-participle",
            "GRAMMAR",
            "Put the words in order.",
            "Set in Yorkshire, the story begins in winter.",
            ["grammar.participle_clauses", "vocab.setting"],
            "Start with 'Set in'.",
            "Set in Yorkshire, the story begins in winter.",
        ),
        choice(
            "read-narrators",
            "READING",
            "Read the essay. Then answer.",
            "Why must the reader decide what really happened?",
            [
                ("Neither narrator can be fully trusted.", "🤥"),
                ("The last chapter is missing.", "📄"),
                ("The novel has no plot.", "❌"),
            ],
            "a",
            ["vocab.narrator"],
            "Look at paragraph 2.",
            "The story is told by two narrators, neither of whom can be fully trusted.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-theme",
            "READING",
            "Read the essay. True or false?",
            "One central theme is the conflict between nature and civilisation.",
            True,
            ["vocab.theme"],
            "Look at paragraph 3.",
            "One central theme is the conflict between nature and civilisation.",
        ),
        speak(
            "say-analysis",
            "Talk about a book or film you know well. Describe its protagonist, a theme and one symbol. Use at least two participle clauses.",
            "Set in …, the story … Having …, the protagonist … One theme is … The … symbolises …",
            "Set in a magical school, the story follows a lonely boy. Having lost his parents, the protagonist searches for a family. One theme is friendship. The scar symbolises his past.",
            ["grammar.participle_clauses", "vocab.protagonist", "vocab.theme"],
        ),
        choice(
            "quiz-idiom-chew",
            "QUIZ",
            "Choose the correct form of the idiom.",
            "Reading five classics in a month? I think you've ___.",
            [
                ("bitten off more than you can chew", None),
                ("bitten more than you can eat", None),
                ("chewed more than you can bite", None),
            ],
            "a",
            ["phrase.bite_off_more", "grammar.idiom_form"],
            "Remember Lesson 1.",
            "You've bitten off more than you can chew.",
        ),
        blank(
            "quiz-ppc-reading",
            "QUIZ",
            "Complete the sentence.",
            "By the time the seminar began, I had ___ reading for six hours.",
            ["been"],
            ["been", "being", "be"],
            ["grammar.past_perfect_continuous"],
            "Remember C1.",
            "I had been reading for six hours.",
        ),
        choice(
            "quiz-hedge-symbol",
            "QUIZ",
            "Choose the most academic, hedged claim.",
            "Write about the storm.",
            [
                ("The storm appears to symbolise the end of childhood.", None),
                ("The storm is 100% about childhood.", None),
                ("The storm means childhood, obviously.", None),
            ],
            "a",
            ["grammar.hedging", "vocab.symbolism"],
            "Remember C1: hedging.",
            "The storm appears to symbolise the end of childhood.",
        ),
    ],
}

LESSON_3 = {
    "slug": L3,
    "title": "Humour and Wordplay",
    "description": "Granny {gran1}'s puns, Dad's sarcasm and a very British understatement. Not bad, eh?",
    "minutes": 40,
    "objectives": [
        "Use vocabulary for humour: pun, irony, sarcasm, understatement, wit, ambiguous.",
        "Recognise and use understatement: not bad, a bit of a …, hardly ideal.",
        "Explain why something is funny.",
    ],
    "review": [
        "grammar.participle_clauses",
        "vocab.tone",
        "vocab.narrator",
        "grammar.idiom_form",
        "vocab.literal",
        "grammar.hedging",
        "grammar.cleft_sentences",
        "vocab.newspaper",
        "vocab.headline",
        "vocab.rainy",
    ],
    "episode": (
        "The Pun Championship",
        "The family holds its annual pun competition. Granny {gran1} has been champion for eleven years.",
    ),
    "content": {
        "story_intro": "Every New Year's Day, the family holds a pun championship. Granny {gran1} has never lost.",
        "reading": {
            "title": "The Family Pun Championship",
            "paragraphs": [
                {
                    "sentences": [
                        "A pun is a joke that plays with words that have two meanings or sound alike.",
                        "Granny {gran1}'s opening line this year: 'I used to be a baker, but I couldn't make enough dough.'",
                    ]
                },
                {
                    "sentences": [
                        "Dad prefers sarcasm. When it started pouring with rain during our picnic, he said: 'Oh, perfect weather for a picnic!'",
                        "The irony was that he had chosen the date after checking three forecasts.",
                    ]
                },
                {
                    "sentences": [
                        "Then there is understatement — the most British kind of humour.",
                        "When the barbecue caught fire last summer, Mum calmly remarked: 'Well, that's a bit of a problem.'",
                    ]
                },
                {
                    "sentences": [
                        "{little}'s favourite jokes are based on ambiguous newspaper headlines, like 'Kids Make Nutritious Snacks'.",
                        "Read one way, it's about cooking; read the other way, it's a horror story!",
                    ]
                },
                {
                    "sentences": [
                        "This year, for the first time, {little} beat Granny with a joke about a tired bicycle — it was two-tired.",
                        "Granny's verdict? 'Not bad at all.' From her, that is the highest praise imaginable.",
                    ]
                },
            ],
            "highlight": [
                "pun",
                "dough",
                "sarcasm",
                "irony",
                "understatement",
                "a bit of a problem",
                "ambiguous",
                "two-tired",
                "Not bad at all",
            ],
        },
        "listening": [
            {
                "id": "c2-3-weather",
                "title": "A very British conversation",
                "transcript": [
                    {"speaker": "Jonas", "text": "Is it always this cold and wet here in January?"},
                    {"speaker": "Dad", "text": "Oh, it's a little on the chilly side, I suppose."},
                    {"speaker": "Jonas", "text": "A little? It's minus five and there's a storm!"},
                    {"speaker": "Mum", "text": "Welcome to British understatement, Jonas."},
                ],
            },
            {
                "id": "c2-3-sarcasm",
                "title": "Sarcasm or not?",
                "transcript": [
                    {"speaker": "{teen}", "text": "I failed my driving test again."},
                    {"speaker": "{boy}", "text": "Oh, brilliant. Third time lucky, they said."},
                    {"speaker": "{teen}", "text": "Thanks for the sarcasm. Very helpful."},
                    {
                        "speaker": "{boy}",
                        "text": "Sorry. Seriously, you'll pass next time. You were hardly far off.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Understatement",
                "explanation": (
                    "Understatement means saying less than you mean, often for humour or politeness. "
                    "Common patterns: a bit of a + noun (a bit of a disaster = a total disaster); "
                    "not + positive adjective (not bad = good; not exactly cheap = expensive); "
                    "rather / slightly / somewhat (rather disappointing = very disappointing); "
                    "hardly + adjective (hardly ideal = very bad); "
                    "not the best / not the most … (not the most exciting film = boring)."
                ),
                "explanation_ru": (
                    "Преуменьшение (особенно британское): говорим меньше, чем имеем в виду. "
                    "a bit of a disaster — полная катастрофа; not bad — хорошо; hardly ideal — очень плохо."
                ),
                "examples": [
                    "The exam wasn't exactly easy. (= it was hard)",
                    "Losing the passport was a bit of a nuisance. (= a big problem)",
                    "The weather was hardly ideal for a picnic.",
                ],
            },
            {
                "title": "Puns, irony and sarcasm",
                "explanation": (
                    "A pun plays with two meanings or similar sounds: two-tired / too tired. "
                    "Irony: the opposite of what you expect happens (a fire station burns down). "
                    "Sarcasm: saying the opposite of what you mean in order to criticise or mock: 'Oh, great!' when something bad happens."
                ),
                "explanation_ru": "Каламбур — игра слов; ирония — неожиданная противоположность; сарказм — насмешка, сказанная «наоборот».",
                "examples": [
                    "'Oh, wonderful,' he said, as the rain began. (sarcasm)",
                    "The dentist had terrible teeth. (irony)",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "humour-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("pun", "a joke using a word with two meanings", None),
                ("irony", "when the opposite of what you expect happens", None),
                ("sarcasm", "saying the opposite of what you mean, to mock", None),
                ("understatement", "describing something as less than it is", None),
            ],
            ["vocab.pun", "vocab.irony", "vocab.sarcasm", "vocab.understatement"],
            "'It's a bit wet' during a flood = understatement.",
            "pun = two meanings; irony = unexpected opposite; sarcasm = mocking opposite; understatement = less than it is.",
        ),
        matching(
            "humour-pictures",
            "VOCABULARY",
            "Match the word to the picture.",
            [("wit", None, "⚡"), ("ambiguous", None, "❔"), ("sarcasm", None, "😏")],
            ["vocab.wit", "vocab.ambiguous", "vocab.sarcasm"],
            "Wit = quick, clever humour.",
            "wit ⚡, ambiguous ❔, sarcasm 😏.",
        ),
        choice(
            "find-pun",
            "VOCABULARY",
            "Tap the right picture.",
            "'I couldn't make enough dough.' Which picture shows the pun?",
            [(None, "🍞"), (None, "🚗"), (None, "📚")],
            "a",
            ["vocab.pun"],
            "Dough = bread mixture AND (slang) money.",
            "🍞 dough — bread and money!",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-understatement",
            "LISTENING",
            "Listen. What does the man really mean?",
            "He really means that the hotel was …",
            [("terrible", "😖"), ("excellent", "🌟"), ("cheap", "💷")],
            "a",
            ["grammar.understatement", "vocab.understatement"],
            "'Not exactly' + positive adjective.",
            "Not exactly luxurious = terrible.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="The hotel wasn't exactly luxurious. The roof leaked, the shower was cold, and there was a goat in the car park.",
        ),
        true_false(
            "listen-chilly",
            "LISTENING",
            "Listen to Jonas and the family. True or false?",
            "Dad thinks the weather is only a little cold.",
            False,
            ["grammar.understatement"],
            "It's minus five and stormy. Is Dad being literal?",
            "Dad is using understatement — he knows it is very cold.",
            listening_id="c2-3-weather",
        ),
        true_false(
            "listen-brilliant",
            "LISTENING",
            "Listen to {teen} and {boy}. True or false?",
            "{boy}'s 'Oh, brilliant' is sarcastic.",
            True,
            ["vocab.sarcasm"],
            "Listen to {teen}'s reply.",
            "{teen}: Thanks for the sarcasm.",
            listening_id="c2-3-sarcasm",
        ),
        blank(
            "understatement-blank",
            "GRAMMAR",
            "Complete the understatements.",
            "The barbecue fire was a ___ of a problem. The weather was ___ ideal for a picnic.",
            ["bit", "hardly"],
            ["bit", "lot", "hardly", "very"],
            ["grammar.understatement"],
            "a bit of a + noun; hardly + adjective.",
            "a bit of a problem; hardly ideal.",
        ),
        choice(
            "not-bad-meaning",
            "GRAMMAR",
            "What does Granny mean?",
            "'Not bad at all.'",
            [("It was really good.", None), ("It was terrible.", None), ("It was average.", None)],
            "a",
            ["grammar.understatement"],
            "Litotes: not + negative = positive.",
            "Not bad at all = very good (high praise from Granny!).",
        ),
        choice(
            "choose-understatement",
            "GRAMMAR",
            "Which sentence is an understatement?",
            "You missed the last train and had to walk 15 km.",
            [
                ("Well, that was slightly inconvenient.", None),
                ("That was the worst night of my entire life!", None),
                ("I walked 15 km.", None),
            ],
            "a",
            ["grammar.understatement", "vocab.understatement"],
            "Say much less than you mean.",
            "Slightly inconvenient — a classic understatement.",
        ),
        choice(
            "irony-or-sarcasm",
            "GRAMMAR",
            "Which example shows situational irony?",
            "Choose one.",
            [
                ("The fire station burned down.", None),
                ("'Great job!' he said when I dropped the cake.", None),
                ("I knead you — said the baker.", None),
            ],
            "a",
            ["vocab.irony", "vocab.sarcasm", "vocab.pun"],
            "Irony = the opposite of what you expect happens.",
            "A fire station burning down is situational irony.",
        ),
        build(
            "build-understatement",
            "GRAMMAR",
            "Put the words in order.",
            "The exam wasn't exactly easy.",
            ["grammar.understatement"],
            "Start with 'The exam'.",
            "The exam wasn't exactly easy.",
        ),
        choice(
            "read-headline",
            "READING",
            "Read the text. Then answer.",
            "Why is 'Kids Make Nutritious Snacks' funny?",
            [
                ("It is ambiguous: it can mean two different things.", "❔"),
                ("It has a spelling mistake.", "✏️"),
                ("It is very long.", "📏"),
            ],
            "a",
            ["vocab.ambiguous", "vocab.headline"],
            "Look at paragraph 4.",
            "Read one way it's about cooking; read the other way, it's a horror story.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-winner",
            "READING",
            "Read the text. True or false?",
            "Granny {gran1} won the championship again this year.",
            False,
            ["vocab.pun"],
            "Look at the last paragraph.",
            "For the first time, {little} beat Granny.",
        ),
        speak(
            "say-understate",
            "Describe a small disaster (real or imaginary) using understatement, then explain what really happened.",
            "It was a bit of a … / It wasn't exactly … / It was hardly … What actually happened was …",
            "Our camping trip was a bit of a disaster. The tent wasn't exactly waterproof, and the weather was hardly ideal. What actually happened was that we slept in the car.",
            ["grammar.understatement", "grammar.cleft_sentences"],
        ),
        blank(
            "quiz-participle-joke",
            "QUIZ",
            "Choose the right participle.",
            "___ heard the joke before, Granny didn't laugh.",
            ["Having"],
            ["Having", "Had", "Heard"],
            ["grammar.participle_clauses"],
            "Remember Lesson 2.",
            "Having heard the joke before, Granny didn't laugh.",
        ),
        choice(
            "quiz-literal",
            "QUIZ",
            "Choose the right word.",
            "Puns work because a word has both a ___ and another meaning.",
            [("literal", None), ("eloquent", None), ("concise", None)],
            "a",
            ["vocab.literal"],
            "Remember Lesson 1.",
            "A literal and another meaning.",
        ),
        choice(
            "quiz-cleft-funny",
            "QUIZ",
            "Choose the correct cleft sentence.",
            "The double meaning makes it funny.",
            [
                ("What makes it funny is the double meaning.", None),
                ("What makes it funny it is the double meaning.", None),
                ("It is funny what makes the double meaning.", None),
            ],
            "a",
            ["grammar.cleft_sentences"],
            "Remember C1.",
            "What makes it funny is the double meaning.",
        ),
    ],
}

LESSON_4 = {
    "slug": L4,
    "title": "The Academic Essay",
    "description": "{boy}'s university application essay needs to sound academic. Nominalisation to the rescue!",
    "minutes": 45,
    "objectives": [
        "Use academic vocabulary: thesis statement, cite, plagiarism, coherent, concise.",
        "Use nominalisation to write in an academic style.",
        "Restructure informal sentences into formal academic prose.",
    ],
    "review": [
        "grammar.understatement",
        "vocab.irony",
        "vocab.ambiguous",
        "grammar.participle_clauses",
        "vocab.theme",
        "grammar.abstract_nouns",
        "grammar.formal_register",
        "grammar.hedging",
        "vocab.source",
        "vocab.evidence",
    ],
    "episode": (
        "Draft Number Seven",
        "{boy} rewrites his university essay for the seventh time. {teen}, now at university, is a strict editor.",
    ),
    "content": {
        "story_intro": "{boy} is applying to university. His application essay has to be in a clear academic style.",
        "reading": {
            "title": "Seven Drafts",
            "paragraphs": [
                {
                    "sentences": [
                        "My first draft began: 'Loads of people think social media is bad for teenagers, and I kind of agree.'",
                        "{teen}, who is studying linguistics at university, sent it back covered in red.",
                    ]
                },
                {
                    "sentences": [
                        "'You need a thesis statement,' she wrote. 'And stop writing like you talk. Use nouns!'",
                        "So 'Teenagers use their phones a lot more than they did' became 'There has been a significant increase in teenagers' phone use.'",
                    ]
                },
                {
                    "sentences": [
                        "This process is called nominalisation: turning verbs and adjectives into nouns.",
                        "It makes writing more objective, because the focus moves from people to ideas.",
                    ]
                },
                {
                    "sentences": [
                        "I also learned to cite every source correctly. Copying even one sentence without a reference counts as plagiarism.",
                        "By draft seven, my essay was concise, coherent and — {teen} admitted — 'not bad at all'.",
                    ]
                },
                {
                    "sentences": [
                        "Having said that, too much nominalisation makes writing heavy and hard to read.",
                        "The aim is clarity, not complication.",
                    ]
                },
            ],
            "highlight": [
                "thesis statement",
                "a significant increase in teenagers' phone use",
                "nominalisation",
                "cite",
                "plagiarism",
                "concise",
                "coherent",
                "clarity",
                "complication",
            ],
        },
        "listening": [
            {
                "id": "c2-4-tutor",
                "title": "Feedback from {teen}",
                "transcript": [
                    {
                        "speaker": "{teen}",
                        "text": "This sentence: 'Because the government changed the law, people protested.' Make it more academic.",
                    },
                    {"speaker": "{boy}", "text": "'The change in the law led to protests'?"},
                    {"speaker": "{teen}", "text": "Perfect. Shorter, clearer and more objective."},
                    {"speaker": "{boy}", "text": "And should I cite the newspaper article here?"},
                    {"speaker": "{teen}", "text": "Always. Otherwise it's plagiarism."},
                ],
            },
            {
                "id": "c2-4-lecture",
                "title": "A short lecture",
                "transcript": [
                    {
                        "speaker": "Professor",
                        "text": "A good thesis statement makes a clear, arguable claim.",
                    },
                    {
                        "speaker": "Professor",
                        "text": "'Social media is interesting' is not a thesis. 'The regulation of social media is essential for teenage well-being' is.",
                    },
                    {
                        "speaker": "Professor",
                        "text": "Notice the nouns: regulation, well-being. That is academic style.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Nominalisation",
                "explanation": (
                    "Nominalisation turns verbs and adjectives into nouns. It is typical of academic and formal writing. "
                    "Verb → noun: decide → decision, increase → increase, develop → development, fail → failure. "
                    "Adjective → noun: important → importance, difficult → difficulty, able → ability. "
                    "Informal: Because prices rose quickly, people bought less. "
                    "Academic: The rapid rise in prices led to a decrease in consumption. "
                    "Adverbs often become adjectives (quickly → rapid), and people often disappear from the sentence."
                ),
                "explanation_ru": (
                    "Номинализация — замена глаголов и прилагательных существительными: decide → decision. "
                    "Типична для академического стиля: The rapid rise in prices led to … "
                    "Наречия становятся прилагательными (quickly → rapid)."
                ),
                "examples": [
                    "The introduction of the law led to protests.",
                    "There was a significant reduction in waste.",
                    "Her failure to respond caused confusion.",
                ],
            },
            {
                "title": "Useful nominal patterns",
                "explanation": (
                    "There has been a + adjective + noun + in …: There has been a sharp increase in screen time. "
                    "noun + led to / resulted in + noun: The closure of the factory resulted in unemployment. "
                    "The + noun + of + noun: The development of the vaccine took a decade."
                ),
                "explanation_ru": "Частые модели: There has been a sharp increase in …; … led to / resulted in …",
                "examples": [
                    "There has been a steady decline in reading.",
                    "The lack of funding resulted in delays.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "academic-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("thesis statement", "the main claim of an essay", None),
                ("cite", "give the source of a quotation or idea", None),
                ("plagiarism", "using someone's work without credit", None),
                ("coherent", "logical and well connected", None),
            ],
            ["vocab.thesis", "vocab.cite", "vocab.plagiarism", "vocab.coherent"],
            "Plagiarism = copying without credit.",
            "thesis statement = main claim; cite = give the source; plagiarism = copying; coherent = logical.",
        ),
        matching(
            "nominal-pairs",
            "VOCABULARY",
            "Match the verb or adjective to its noun.",
            [
                ("reduce", "reduction", None),
                ("fail", "failure", None),
                ("difficult", "difficulty", None),
                ("concise", "concision", None),
            ],
            ["grammar.nominalisation", "vocab.concise"],
            "Look at the suffixes: -tion, -ure, -y, -sion.",
            "reduce → reduction, fail → failure, difficult → difficulty, concise → concision.",
        ),
        choice(
            "find-plagiarism",
            "VOCABULARY",
            "Tap the right picture.",
            "Which symbol best represents what you must never do with someone else's work?",
            [(None, "🚫"), (None, "🔖"), (None, "🎯")],
            "a",
            ["vocab.plagiarism"],
            "Copying without credit is forbidden.",
            "🚫 no plagiarism.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-nominal",
            "LISTENING",
            "Listen. Which sentence did the student write in her essay?",
            "She wrote: …",
            [
                ("The closure of the library resulted in a decline in reading.", "📚"),
                ("They closed the library so kids read less.", "🏫"),
                ("Reading is bad now.", "👎"),
            ],
            "a",
            ["grammar.nominalisation"],
            "Listen for the nouns: closure, decline.",
            "The closure of the library resulted in a decline in reading.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="I rewrote 'They closed the library so kids read less' as: 'The closure of the library resulted in a decline in reading.' Much more academic!",
        ),
        true_false(
            "listen-cite",
            "LISTENING",
            "Listen to {teen} and {boy}. True or false?",
            "{teen} says it's fine not to cite the newspaper.",
            False,
            ["vocab.cite", "vocab.plagiarism"],
            "Listen to {teen}'s last line.",
            "Always cite it — otherwise it's plagiarism.",
            listening_id="c2-4-tutor",
        ),
        true_false(
            "listen-thesis",
            "LISTENING",
            "Listen to the professor. True or false?",
            "'Social media is interesting' is a good thesis statement.",
            False,
            ["vocab.thesis"],
            "Does it make an arguable claim?",
            "It is not a thesis. A thesis makes a clear, arguable claim.",
            listening_id="c2-4-lecture",
        ),
        blank(
            "nominal-blank",
            "GRAMMAR",
            "Complete the academic sentence.",
            "There has been a significant ___ in screen time, which has ___ to concerns about sleep.",
            ["increase", "led"],
            ["increase", "increasing", "led", "caused"],
            ["grammar.nominalisation"],
            "a + adjective + noun; noun + led to.",
            "There has been a significant increase in screen time, which has led to concerns about sleep.",
        ),
        choice(
            "nominal-rewrite",
            "GRAMMAR",
            "Choose the best academic version.",
            "Because the government changed the law, people protested.",
            [
                ("The change in the law led to protests.", None),
                ("The government changed it so people were protesting.", None),
                ("Protesting happened because of changing.", None),
            ],
            "a",
            ["grammar.nominalisation"],
            "Turn change and protest into nouns.",
            "The change in the law led to protests.",
        ),
        choice(
            "adverb-adjective",
            "GRAMMAR",
            "Choose the correct nominalised sentence.",
            "Prices rose rapidly.",
            [
                ("There was a rapid rise in prices.", None),
                ("There was a rapidly rise in prices.", None),
                ("There was a rise rapid of prices.", None),
            ],
            "a",
            ["grammar.nominalisation"],
            "The adverb becomes an adjective.",
            "There was a rapid rise in prices.",
        ),
        blank(
            "failure-blank",
            "GRAMMAR",
            "Choose the right nouns.",
            "The company's ___ to respond caused great ___ among customers.",
            ["failure", "confusion"],
            ["failure", "failing", "confusion", "confused"],
            ["grammar.nominalisation"],
            "fail → failure; confuse → confusion.",
            "The company's failure to respond caused great confusion.",
        ),
        build(
            "build-nominal",
            "GRAMMAR",
            "Put the words in order.",
            "The introduction of the law led to protests.",
            ["grammar.nominalisation"],
            "Start with 'The introduction'.",
            "The introduction of the law led to protests.",
        ),
        choice(
            "read-why-nouns",
            "READING",
            "Read the text. Then answer.",
            "Why does nominalisation make writing more objective?",
            [
                ("The focus moves from people to ideas.", "💡"),
                ("The sentences become longer.", "📏"),
                ("It uses more idioms.", "🗝️"),
            ],
            "a",
            ["grammar.nominalisation"],
            "Look at paragraph 3.",
            "The focus moves from people to ideas.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-too-much",
            "READING",
            "Read the text. True or false?",
            "{boy} says you should use as much nominalisation as possible.",
            False,
            ["grammar.nominalisation", "vocab.concise"],
            "Look at the last paragraph.",
            "Too much nominalisation makes writing heavy. The aim is clarity.",
        ),
        speak(
            "say-academic",
            "Give a short academic summary of a change in your town or school. Use at least three nominalisations.",
            "There has been a … in … The … of … led to … This … resulted in …",
            "There has been a significant increase in cycling in our town. The introduction of new bike lanes led to a reduction in traffic. This development resulted in an improvement in air quality.",
            ["grammar.nominalisation", "grammar.formal_register"],
        ),
        choice(
            "quiz-understatement-essay",
            "QUIZ",
            "What did {teen} mean?",
            "'Your first draft was hardly ideal.'",
            [("It was very poor.", None), ("It was perfect.", None), ("It was quite good.", None)],
            "a",
            ["grammar.understatement"],
            "Remember Lesson 3.",
            "Hardly ideal = very poor.",
        ),
        blank(
            "quiz-participle-essay",
            "QUIZ",
            "Choose the right participle.",
            "___ seven drafts, {boy} finally sent his essay.",
            ["Having written"],
            ["Having written", "Written", "Writing seven"],
            ["grammar.participle_clauses"],
            "Remember Lesson 2: an earlier action.",
            "Having written seven drafts, {boy} sent his essay.",
        ),
        choice(
            "quiz-idiom-essay",
            "QUIZ",
            "Which phrase is too informal for an academic essay?",
            "Choose one.",
            [
                ("The minister spilled the beans.", None),
                ("The minister revealed the information.", None),
                ("The information was disclosed.", None),
            ],
            "a",
            ["grammar.idiom_form", "phrase.spill_the_beans"],
            "Remember Lesson 1: idioms are often informal.",
            "'Spilled the beans' is too informal for an academic essay.",
        ),
    ],
}

LESSON_5 = {
    "slug": L5,
    "title": "The Formal Debate",
    "description": "The national schools debating final. Far from being nervous, {boy} is ready. Then a review of the unit.",
    "minutes": 45,
    "objectives": [
        "Use debate vocabulary: motion, rebuttal, concede, eloquent, rhetorical question.",
        "Use fronting for emphasis: Far from …, So … that …, Such was … that ….",
        "Build and rebut an argument, and review Unit 1.",
    ],
    "review": [
        "grammar.nominalisation",
        "vocab.thesis",
        "vocab.coherent",
        "grammar.understatement",
        "grammar.participle_clauses",
        "grammar.inversion",
        "grammar.linking_arguments",
        "phrase.agree_disagree",
        "vocab.debate",
        "vocab.persuade",
    ],
    "episode": (
        "This House Believes …",
        "{boy}'s team reaches the national debating final. The motion: 'This house believes that AI will make us more creative.'",
    ),
    "content": {
        "story_intro": "Four years after his first debate, {boy} is in the national schools debating final.",
        "reading": {
            "title": "The Final",
            "paragraphs": [
                {
                    "sentences": [
                        "The motion was: 'This house believes that artificial intelligence will make humans more creative.' We were arguing against it.",
                        "So tense was the atmosphere in the hall that you could hear the clock ticking.",
                    ]
                },
                {
                    "sentences": [
                        "Their first speaker was eloquent. She opened with a rhetorical question: 'Did the camera kill painting?'",
                        "Such was the force of her argument that the audience applauded before she had finished.",
                    ]
                },
                {
                    "sentences": [
                        "My job was the rebuttal. I began by conceding a point: 'We accept that AI is a powerful tool.'",
                        "'Far from making us more creative, however, it risks making us passive consumers of other people's ideas.'",
                    ]
                },
                {
                    "sentences": [
                        "I cited a study on students who used AI to write essays. The reduction in original thinking was striking.",
                        "Not only had they written less, but they also remembered less of what they had 'written'.",
                    ]
                },
                {
                    "sentences": [
                        "We lost by a single vote. Disappointing? A little. But so close was the result that the judges asked both teams to publish their speeches.",
                        "Granny {gran2}'s comment: 'Losing to a good argument is not the worst thing in the world.' Understatement runs in the family.",
                    ]
                },
            ],
            "highlight": [
                "So tense was the atmosphere",
                "Such was the force",
                "Far from making us",
                "Not only had they",
                "so close was the result",
                "motion",
                "eloquent",
                "rhetorical question",
                "rebuttal",
                "conceding",
            ],
        },
        "listening": [
            {
                "id": "c2-5-rebuttal",
                "title": "The rebuttal",
                "transcript": [
                    {
                        "speaker": "Opponent",
                        "text": "AI gives everyone access to creative tools. Isn't that democratic?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "I concede that access matters. But far from democratising creativity, AI may standardise it.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "If everyone uses the same tool, will we not all produce the same work?",
                    },
                    {"speaker": "Chair", "text": "Thank you. Time."},
                ],
            },
            {
                "id": "c2-5-result",
                "title": "The result",
                "transcript": [
                    {
                        "speaker": "Chair",
                        "text": "So strong were both teams that the judges needed forty minutes to decide.",
                    },
                    {"speaker": "Chair", "text": "By a single vote, the motion is carried."},
                    {
                        "speaker": "{teen}",
                        "text": "You were brilliant. Honestly, that rebuttal was the best speech of the night.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Fronting for emphasis",
                "explanation": (
                    "Moving a phrase to the front of the sentence gives it emphasis — a key rhetorical technique. "
                    "Far from + -ing / noun: Far from solving the problem, the ban would make it worse. "
                    "So + adjective + be + subject + that …: So tense was the atmosphere that you could hear the clock. "
                    "Such + be + noun phrase + that …: Such was the force of her argument that the audience applauded. "
                    "Note the inversion of be and the subject after So and Such."
                ),
                "explanation_ru": (
                    "Вынесение в начало для эмфазы: Far from … — «вовсе не …, а наоборот»; "
                    "So tense was the atmosphere that … ; Such was the force … that … — с инверсией."
                ),
                "examples": [
                    "Far from being a waste of time, debating builds confidence.",
                    "So convincing was her speech that we changed our minds.",
                    "Such was the noise that nobody heard the bell.",
                ],
            },
            {
                "title": "Rhetorical devices",
                "explanation": (
                    "Rhetorical question: a question that expects no answer — Did the camera kill painting? "
                    "Concession + rebuttal: We accept that …; however, … "
                    "Rule of three: clear, fair and effective."
                ),
                "explanation_ru": "Риторический вопрос, уступка + опровержение, «правило трёх».",
                "examples": [
                    "Who among us has never made a mistake?",
                    "We concede that …; nevertheless, …",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "debate-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("motion", "the statement that is debated", None),
                ("rebuttal", "a speech that answers and attacks the other side's arguments", None),
                ("concede", "admit that the other side is right about something", None),
                ("eloquent", "speaking fluently and persuasively", None),
            ],
            ["vocab.motion", "vocab.rebuttal", "vocab.concede", "vocab.eloquent"],
            "You concede a point.",
            "motion = the debated statement; rebuttal = an answer that attacks; concede = admit; eloquent = fluent and persuasive.",
        ),
        matching(
            "debate-pictures",
            "VOCABULARY",
            "Match the term to the picture.",
            [("rhetorical question", None, "❓"), ("rebuttal", None, "🛡️"), ("concede", None, "🏳️")],
            ["vocab.rhetorical_question", "vocab.rebuttal", "vocab.concede"],
            "A white flag = conceding.",
            "rhetorical question ❓, rebuttal 🛡️, concede 🏳️.",
        ),
        choice(
            "find-rebuttal",
            "VOCABULARY",
            "Tap the right picture.",
            "Which picture best represents a rebuttal?",
            [(None, "🛡️"), (None, "🎙️"), (None, "📜")],
            "a",
            ["vocab.rebuttal"],
            "Defending your side against attack.",
            "🛡️ rebuttal.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-fronting",
            "LISTENING",
            "Listen. What happened because of the speech?",
            "Because the speech was so powerful, …",
            [
                ("several people changed their vote", "🗳️"),
                ("the debate was cancelled", "❌"),
                ("the speaker forgot her words", "😶"),
            ],
            "a",
            ["grammar.fronting"],
            "Listen for 'So powerful was …'.",
            "So powerful was her speech that several people changed their vote.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="So powerful was her closing speech that several members of the audience changed their vote at the last minute.",
        ),
        true_false(
            "listen-concede",
            "LISTENING",
            "Listen to the rebuttal. True or false?",
            "{boy} concedes that access to creative tools matters.",
            True,
            ["vocab.concede", "vocab.rebuttal"],
            "Listen to {boy}'s first line.",
            "I concede that access matters.",
            listening_id="c2-5-rebuttal",
        ),
        true_false(
            "listen-quick",
            "LISTENING",
            "Listen to the result. True or false?",
            "The judges decided very quickly.",
            False,
            ["grammar.fronting"],
            "How long did they need?",
            "So strong were both teams that the judges needed forty minutes.",
            listening_id="c2-5-result",
        ),
        blank(
            "fronting-blank",
            "GRAMMAR",
            "Complete the fronted sentences.",
            "___ tense was the atmosphere that you could hear the clock. ___ was the force of her argument that people applauded.",
            ["So", "Such"],
            ["So", "Such", "Far"],
            ["grammar.fronting"],
            "So + adjective; Such + be + noun.",
            "So tense was the atmosphere … Such was the force of her argument …",
        ),
        choice(
            "far-from",
            "GRAMMAR",
            "Which sentence is correct?",
            "Emphasise that AI does the opposite.",
            [
                ("Far from making us creative, AI may make us passive.", None),
                ("Far from make us creative, AI may make us passive.", None),
                ("Far making us creative, AI may make us passive.", None),
            ],
            "a",
            ["grammar.fronting"],
            "Far from + -ing.",
            "Far from making us creative, AI may make us passive.",
        ),
        choice(
            "so-inversion",
            "GRAMMAR",
            "Which sentence is correct?",
            "The result was very close.",
            [
                ("So close was the result that the judges hesitated.", None),
                ("So close the result was that the judges hesitated.", None),
                ("So the result was close that the judges hesitated.", None),
            ],
            "a",
            ["grammar.fronting"],
            "So + adjective + be + subject.",
            "So close was the result that the judges hesitated.",
        ),
        choice(
            "rhetorical-q",
            "GRAMMAR",
            "Which is a rhetorical question?",
            "Choose one.",
            [
                ("Who among us has never made a mistake?", None),
                ("What time does the debate start?", None),
                ("Could you pass me the water, please?", None),
            ],
            "a",
            ["vocab.rhetorical_question"],
            "It expects no real answer.",
            "Who among us has never made a mistake? — a rhetorical question.",
        ),
        build(
            "build-far-from",
            "GRAMMAR",
            "Put the words in order.",
            "Far from being nervous, he felt completely calm.",
            ["grammar.fronting"],
            "Start with 'Far from'.",
            "Far from being nervous, he felt completely calm.",
        ),
        order(
            "read-order",
            "READING",
            "Put the debate in order.",
            [
                "The motion about AI and creativity was announced.",
                "The first opponent asked a rhetorical question.",
                "{boy} conceded a point and began his rebuttal.",
                "{boy} cited a study about students and AI.",
                "The judges announced the result.",
            ],
            ["vocab.motion", "vocab.rebuttal", "vocab.cite"],
            "The result comes last.",
            "Motion → rhetorical question → rebuttal → study → result.",
        ),
        choice(
            "read-granny",
            "READING",
            "Read the text. Then answer.",
            "What does {boy} mean by 'Understatement runs in the family'?",
            [
                ("Granny, like others in the family, says less than she means.", "🤏"),
                ("Granny doesn't understand debates.", "🤷"),
                ("The family runs together every week.", "🏃"),
            ],
            "a",
            ["grammar.understatement", "vocab.understatement"],
            "Look at the last paragraph.",
            "Granny's comment is an understatement — a family habit.",
            ex_type="READING_COMPREHENSION",
        ),
        speak(
            "say-rebuttal",
            "Motion: 'Exams should be abolished.' Give a short rebuttal against it. Concede one point, then use fronting and a rhetorical question.",
            "I concede that … Far from …, however, … So … is … that … Would we really …?",
            "I concede that exams are stressful. Far from being useless, however, they show what we have learned. So important is this feedback that schools cannot do without it. Would we really trust a doctor who had never been tested?",
            ["grammar.fronting", "vocab.concede", "vocab.rhetorical_question"],
        ),
        choice(
            "quiz-idiom-ice-debate",
            "QUIZ",
            "Choose the correct idiom.",
            "The chair told a joke to ___ before the debate.",
            [("break the ice", None), ("break the beans", None), ("spill the ice", None)],
            "a",
            ["phrase.break_the_ice"],
            "Remember Lesson 1.",
            "The chair told a joke to break the ice.",
        ),
        blank(
            "quiz-participle-debate",
            "QUIZ",
            "Choose the right participle.",
            "___ the study carefully, {boy} found the key statistic.",
            ["Having read"],
            ["Having read", "Read", "Had read"],
            ["grammar.participle_clauses", "vocab.protagonist"],
            "Remember Lesson 2.",
            "Having read the study carefully, {boy} found the key statistic.",
        ),
        choice(
            "quiz-understatement-loss",
            "QUIZ",
            "Which sentence is an understatement?",
            "Losing the national final by one vote.",
            [
                ("It was slightly disappointing.", None),
                ("It was the worst moment of my life!", None),
                ("We lost by one vote.", None),
            ],
            "a",
            ["grammar.understatement", "vocab.sarcasm"],
            "Remember Lesson 3.",
            "Slightly disappointing — an understatement.",
        ),
        choice(
            "quiz-nominal-debate",
            "QUIZ",
            "Choose the most academic version.",
            "Students thought less originally when they used AI.",
            [
                ("The use of AI led to a reduction in original thinking.", None),
                ("AI made students think less, basically.", None),
                ("Students using AI, they thought less.", None),
            ],
            "a",
            ["grammar.nominalisation", "vocab.thesis"],
            "Remember Lesson 4.",
            "The use of AI led to a reduction in original thinking.",
        ),
        choice(
            "quiz-eloquent",
            "QUIZ",
            "Choose the right word.",
            "Her speech was so fluent and persuasive — truly ___.",
            [("eloquent", None), ("ambiguous", None), ("literal", None)],
            "a",
            ["vocab.eloquent", "vocab.ambiguous", "vocab.literal"],
            "Fluent and persuasive.",
            "Truly eloquent.",
        ),
        blank(
            "quiz-inversion-not-only",
            "QUIZ",
            "Complete the inversion.",
            "Not only ___ they written less, but they also remembered less.",
            ["had"],
            ["had", "did", "were"],
            ["grammar.inversion"],
            "Remember C1: Not only + auxiliary + subject.",
            "Not only had they written less, …",
        ),
    ],
}

UNIT = {
    "slug": "the-art-of-language",
    "title": "The Art of Language",
    "description": "Idioms, classic novels, puns and understatement, the academic essay and a national debating final.",
    "lessons": [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5],
}
