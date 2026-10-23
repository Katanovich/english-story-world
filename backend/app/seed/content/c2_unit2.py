"""C2 · Unit 2 "Our Story" (C2 lessons 6-10).

The course comes full circle: the family's stories, retold. Topics: translating Granny's
tales, explaining science to everyone, a family negotiation, poetry, and the family film.
Grammar: register shifts, comparative structures, diplomatic language, emphatic structures,
the subjunctive. Lesson 10 is the final review of the whole course.
"""

from app.seed.content.helpers import (
    G,
    Item,
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
    "translating-grannys-tales",
    "science-for-everyone",
    "the-negotiation",
    "poetry-and-rhythm",
    "the-family-film",
)

ITEMS: dict[str, Item] = {
    # Lesson 6
    "vocab.translate": (
        V,
        "translate",
        "🔤",
        "переводить",
        L6,
        ["{teen} is translating Granny's tales."],
        None,
    ),
    "vocab.nuance": (
        V,
        "nuance",
        "🎨",
        "нюанс, оттенок",
        L6,
        ["The nuance is lost in translation."],
        None,
    ),
    "vocab.connotation": (
        V,
        "connotation",
        "💭",
        "коннотация, оттенок значения",
        L6,
        ["'Cheap' has a negative connotation."],
        None,
    ),
    "vocab.colloquial": (
        V,
        "colloquial",
        "💬",
        "разговорный",
        L6,
        ["'Gonna' is very colloquial."],
        None,
    ),
    "vocab.dialect": (
        V,
        "dialect",
        "🗺️",
        "диалект",
        L6,
        ["Granny's village has its own dialect."],
        None,
    ),
    "vocab.untranslatable": (
        V,
        "untranslatable",
        "🚧",
        "непереводимый",
        L6,
        ["Some jokes are untranslatable."],
        None,
    ),
    "grammar.register_shift": (
        G,
        "colloquial → neutral → formal",
        None,
        "Смена регистра: разговорный, нейтральный, официальный",
        L6,
        [
            "Colloquial: 'Kids loved it.' Formal: 'The children were delighted.'",
            "Phrasal verb: find out → formal: discover",
        ],
        "Choose words and grammar that match the reader: phrasal verbs and contractions are informal; single Latin-based verbs are formal.",
    ),
    # Lesson 7
    "vocab.jargon": (
        V,
        "jargon",
        "🧪",
        "профессиональный жаргон",
        L7,
        ["Avoid jargon when you explain science to children."],
        None,
    ),
    "vocab.analogy": (
        V,
        "analogy",
        "🔁",
        "аналогия",
        L7,
        ["She used the analogy of a library to explain DNA."],
        None,
    ),
    "vocab.accessible": (
        V,
        "accessible",
        "🚪",
        "доступный, понятный",
        L7,
        ["The book makes physics accessible."],
        None,
    ),
    "vocab.misconception": (
        V,
        "misconception",
        "🤯",
        "заблуждение",
        L7,
        ["It's a common misconception that bats are blind."],
        None,
    ),
    "vocab.layperson": (
        V,
        "layperson",
        "🧑",
        "неспециалист",
        L7,
        ["Explain it so that a layperson can understand."],
        None,
    ),
    "grammar.comparative_structures": (
        G,
        "the more …, the more … / just as …, so … / not so much … as …",
        None,
        "Сложные сравнительные конструкции",
        L7,
        [
            "The more you practise, the easier it gets.",
            "Just as a library stores books, so DNA stores information.",
        ],
        "Advanced comparisons: the + comparative …, the + comparative; just as … so …; not so much A as B; twice as … as.",
    ),
    # Lesson 8
    "vocab.compromise": (
        V,
        "compromise",
        "🤝",
        "компромисс",
        L8,
        ["We reached a compromise."],
        None,
    ),
    "vocab.concession": (
        V,
        "concession",
        "🎁",
        "уступка",
        L8,
        ["Both sides made concessions."],
        None,
    ),
    "vocab.proposal": (
        V,
        "proposal",
        "📝",
        "предложение (план)",
        L8,
        ["Here is my proposal."],
        None,
    ),
    "vocab.tactful": (V, "tactful", "🕊️", "тактичный", L8, ["Please be tactful with Granny."], None),
    "vocab.consensus": (
        V,
        "consensus",
        "✅",
        "единодушие, консенсус",
        L8,
        ["We finally reached a consensus."],
        None,
    ),
    "grammar.diplomatic_language": (
        G,
        "I was wondering whether … / It might be worth … / Wouldn't it be better …?",
        None,
        "Дипломатичный язык: смягчение",
        L8,
        [
            "I was wondering whether we could change the date.",
            "It might be worth considering another option.",
        ],
        "Soften requests and disagreement: past tenses (I was wondering), modals (might, could), negative questions, softeners (slightly, a little).",
    ),
    # Lesson 9
    "vocab.rhyme": (
        V,
        "rhyme",
        "🎵",
        "рифма; рифмоваться",
        L9,
        ["'Moon' rhymes with 'June'."],
        None,
    ),
    "vocab.stanza": (V, "stanza", "🧱", "строфа", L9, ["The poem has four stanzas."], None),
    "vocab.alliteration": (
        V,
        "alliteration",
        "🅱️",
        "аллитерация",
        L9,
        ["'Big blue boats' is alliteration."],
        None,
    ),
    "vocab.rhythm": (V, "rhythm", "🥁", "ритм", L9, ["The rhythm sounds like a heartbeat."], None),
    "vocab.stress": (
        V,
        "stress (in words)",
        "🔊",
        "ударение",
        L9,
        ["The stress is on the first syllable."],
        None,
    ),
    "grammar.emphatic_structures": (
        G,
        "I DO like it / the very … / whatsoever / do + imperative",
        None,
        "Эмфатические конструкции",
        L9,
        [
            "I did read the poem — I promise!",
            "That's the very book I was looking for.",
            "There's no doubt whatsoever.",
        ],
        "Add emphasis with stressed auxiliaries (do / does / did), the very, at all / whatsoever, and Do + imperative.",
    ),
    # Lesson 10
    "vocab.screenplay": (
        V,
        "screenplay",
        "📄",
        "сценарий",
        L10,
        ["{boy} wrote the screenplay."],
        None,
    ),
    "vocab.premiere": (V, "premiere", "🎟️", "премьера", L10, ["The premiere is on Saturday."], None),
    "vocab.legacy": (
        V,
        "legacy",
        "🌳",
        "наследие",
        L10,
        ["Granny's stories are her legacy."],
        None,
    ),
    "vocab.montage": (
        V,
        "montage",
        "🎞️",
        "монтажная последовательность",
        L10,
        ["The film opens with a montage of old photos."],
        None,
    ),
    "grammar.subjunctive": (
        G,
        "It is essential that he be … / I suggest that she go …",
        None,
        "Сослагательное наклонение (формальное)",
        L10,
        [
            "It is essential that every member of the family be included.",
            "Granny insisted that the film be shown at the village hall.",
        ],
        "After formal verbs and adjectives of demand or importance (insist, suggest, essential, vital), use the base form for all persons.",
    ),
}


LESSON_6 = {
    "slug": L6,
    "title": "Translating Granny's Tales",
    "description": "{teen} translates Granny {gran2}'s village stories. How do you translate a joke, a dialect, a feeling?",
    "minutes": 45,
    "objectives": [
        "Use translation vocabulary: nuance, connotation, colloquial, dialect, untranslatable.",
        "Shift between colloquial, neutral and formal register.",
        "Discuss cultural nuance in language.",
    ],
    "review": [
        "grammar.fronting",
        "vocab.concede",
        "vocab.eloquent",
        "grammar.nominalisation",
        "grammar.formal_register",
        "grammar.idiom_form",
        "vocab.literal",
        "vocab.figurative",
        "vocab.language",
        "vocab.culture",
    ],
    "episode": (
        "Words Without a Home",
        "{teen} tries to translate Granny {gran2}'s favourite story for her friend Chloe in Canada.",
    ),
    "content": {
        "story_intro": "{teen} wants to share Granny {gran2}'s village tales with her Canadian friend Chloe. She has to translate them.",
        "reading": {
            "title": "Lost — and Found — in Translation",
            "paragraphs": [
                {
                    "sentences": [
                        "Granny {gran2} tells her stories in the dialect of her village, full of words you won't find in any dictionary.",
                        "Translating them, I quickly discovered, is not just a matter of changing words.",
                    ]
                },
                {
                    "sentences": [
                        "Take the word Granny uses for the first warm evening of spring. It has a connotation of hope, of childhood, of the smell of wet earth.",
                        "In English, 'a warm evening' is accurate but flat. The nuance simply disappears.",
                    ]
                },
                {
                    "sentences": [
                        "Then there's register. Granny's stories are colloquial: 'So the old fella turns round and says …'",
                        "My first translation sounded like a legal document: 'The elderly gentleman subsequently remarked …' Chloe laughed out loud.",
                    ]
                },
                {
                    "sentences": [
                        "Some jokes are genuinely untranslatable, because they depend on a pun or a local custom.",
                        "In those cases, I add a short note — or I invent an English joke that does the same job.",
                    ]
                },
                {
                    "sentences": [
                        "Far from being a technical exercise, translation turned out to be an act of love.",
                        "Every choice I made was a question: what would Granny want a stranger to feel?",
                    ]
                },
            ],
            "highlight": [
                "dialect",
                "Translating",
                "connotation",
                "nuance",
                "register",
                "colloquial",
                "untranslatable",
                "Far from being",
            ],
        },
        "listening": [
            {
                "id": "c2-6-chloe",
                "title": "A call with Chloe",
                "transcript": [
                    {
                        "speaker": "Chloe",
                        "text": "I loved the story! But why does the old man talk like a lawyer?",
                    },
                    {
                        "speaker": "{teen}",
                        "text": "That was my first draft. I've made it much more colloquial now.",
                    },
                    {
                        "speaker": "Chloe",
                        "text": "Good. And what does 'the evening of the first frogs' mean?",
                    },
                    {
                        "speaker": "{teen}",
                        "text": "It's Granny's dialect. There's no English word, so I kept it and added a note.",
                    },
                ],
            },
            {
                "id": "c2-6-gran",
                "title": "Granny's opinion",
                "transcript": [
                    {"speaker": "Granny {gran2}", "text": "Read me the English version, love."},
                    {
                        "speaker": "{teen}",
                        "text": "'So the old fella turns round and says: you'll not catch me in a boat!'",
                    },
                    {
                        "speaker": "Granny {gran2}",
                        "text": "Ha! That's exactly how he'd have said it. You've kept the spirit.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Register shifts",
                "explanation": (
                    "The same idea can be expressed in different registers. "
                    "Colloquial: The kids loved it. / He found out what happened. / Loads of people came. "
                    "Neutral: The children really enjoyed it. / He learned what had happened. / Many people came. "
                    "Formal: The children were delighted. / He discovered the circumstances. / A considerable number of people attended. "
                    "Colloquial English uses phrasal verbs, contractions, vague words (stuff, loads) and direct speech. "
                    "Formal English uses single verbs (discover, attend), nominalisation and no contractions."
                ),
                "explanation_ru": (
                    "Один смысл — разные регистры: разговорный (phrasal verbs, loads, stuff), "
                    "нейтральный, официальный (discover, attend, номинализация)."
                ),
                "examples": [
                    "put up with → tolerate",
                    "get in touch → contact",
                    "a bit of a mess → somewhat disorganised",
                ],
            },
            {
                "title": "Connotation",
                "explanation": (
                    "Words with similar meanings can have different emotional colours (connotations). "
                    "slim (positive) / thin (neutral) / skinny (negative). "
                    "economical (positive) / cheap (often negative) / stingy (negative). "
                    "Translators must choose the word with the right connotation, not just the right dictionary meaning."
                ),
                "explanation_ru": "Коннотация — эмоциональный оттенок: slim (+), thin (нейтр.), skinny (−).",
                "examples": ["She is determined. (positive) / She is stubborn. (negative)"],
            },
        ],
    },
    "exercises": [
        matching(
            "translation-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("nuance", "a very small difference in meaning or feeling", None),
                ("connotation", "the feelings or ideas a word suggests", None),
                ("dialect", "a regional form of a language", None),
                ("colloquial", "used in informal conversation", None),
            ],
            ["vocab.nuance", "vocab.connotation", "vocab.dialect", "vocab.colloquial"],
            "A dialect belongs to a region.",
            "nuance = subtle difference; connotation = associated feelings; dialect = regional language; colloquial = conversational.",
        ),
        matching(
            "register-pairs",
            "VOCABULARY",
            "Match the colloquial phrase to its formal equivalent.",
            [
                ("find out", "discover", None),
                ("put up with", "tolerate", None),
                ("get in touch", "contact", None),
                ("loads of", "a considerable number of", None),
            ],
            ["grammar.register_shift"],
            "Formal English prefers single Latin-based verbs.",
            "find out → discover; put up with → tolerate; get in touch → contact; loads of → a considerable number of.",
        ),
        choice(
            "find-translate",
            "VOCABULARY",
            "Tap the right picture.",
            "Which picture best shows something untranslatable?",
            [(None, "🚧"), (None, "🔤"), (None, "📖")],
            "a",
            ["vocab.untranslatable", "vocab.translate"],
            "A barrier between languages.",
            "🚧 untranslatable — there's a barrier.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-register",
            "LISTENING",
            "Listen. Which version is the formal one?",
            "The formal version is …",
            [
                ("'A considerable number of residents attended the meeting.'", "👔"),
                ("'Loads of people turned up.'", "💬"),
                ("'Everyone and their dog came.'", "🐕"),
            ],
            "a",
            ["grammar.register_shift"],
            "Listen for single Latin-based verbs and no slang.",
            "A considerable number of residents attended = formal.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Version one: Loads of people turned up. Version two: A considerable number of residents attended the meeting.",
        ),
        true_false(
            "listen-frogs",
            "LISTENING",
            "Listen to Chloe and {teen}. True or false?",
            "{teen} found an exact English word for 'the evening of the first frogs'.",
            False,
            ["vocab.dialect", "vocab.untranslatable"],
            "What did she do instead?",
            "There's no English word, so she kept it and added a note.",
            listening_id="c2-6-chloe",
        ),
        true_false(
            "listen-spirit",
            "LISTENING",
            "Listen to Granny {gran2}. True or false?",
            "Granny thinks the translation has kept the spirit of the story.",
            True,
            ["vocab.colloquial", "vocab.nuance"],
            "Listen to Granny's last line.",
            "You've kept the spirit.",
            listening_id="c2-6-gran",
        ),
        blank(
            "register-blank",
            "GRAMMAR",
            "Make the sentence formal.",
            "He found out what happened. → He ___ the circumstances. Lots of people came. → Many people ___.",
            ["discovered", "attended"],
            ["discovered", "found", "attended", "turned up"],
            ["grammar.register_shift"],
            "Single formal verbs instead of phrasal verbs.",
            "He discovered the circumstances. Many people attended.",
        ),
        choice(
            "colloquial-version",
            "GRAMMAR",
            "Granny's story is colloquial. Which translation keeps her register?",
            "Choose the best translation.",
            [
                ("So the old fella turns round and says …", None),
                ("The elderly gentleman subsequently remarked …", None),
                ("It was stated by the aforementioned male …", None),
            ],
            "a",
            ["grammar.register_shift", "vocab.colloquial"],
            "Match the original register.",
            "So the old fella turns round and says … — colloquial, like Granny.",
        ),
        choice(
            "connotation-choice",
            "GRAMMAR",
            "Which word has the most positive connotation?",
            "Describe someone who spends little money.",
            [("economical", None), ("cheap", None), ("stingy", None)],
            "a",
            ["vocab.connotation"],
            "Which word is a compliment?",
            "economical (+), cheap (often −), stingy (−).",
        ),
        choice(
            "formal-rewrite",
            "GRAMMAR",
            "Choose the most formal version.",
            "We can't put up with this mess any more.",
            [
                ("This situation can no longer be tolerated.", None),
                ("We can't stand this mess no more.", None),
                ("This is a bit of a mess, innit.", None),
            ],
            "a",
            ["grammar.register_shift", "grammar.nominalisation"],
            "put up with → tolerate; passive; no contractions.",
            "This situation can no longer be tolerated.",
        ),
        build(
            "build-register",
            "GRAMMAR",
            "Put the words in order.",
            "Translation is not just a matter of words.",
            ["grammar.register_shift", "vocab.translate"],
            "Start with 'Translation is'.",
            "Translation is not just a matter of words.",
        ),
        choice(
            "read-nuance",
            "READING",
            "Read the text. Then answer.",
            "What is lost when Granny's word is translated as 'a warm evening'?",
            [
                ("its connotation of hope and childhood", "🌱"),
                ("its spelling", "✏️"),
                ("its grammar", "📐"),
            ],
            "a",
            ["vocab.nuance", "vocab.connotation"],
            "Look at paragraph 2.",
            "The connotation of hope, childhood and wet earth disappears.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-act-of-love",
            "READING",
            "Read the text. True or false?",
            "{teen} describes translation as a purely technical exercise.",
            False,
            ["grammar.fronting", "vocab.translate"],
            "Look at the last paragraph.",
            "Far from being a technical exercise, it was an act of love.",
        ),
        speak(
            "say-register",
            "Tell the same short event twice: first colloquially, as to a friend, then formally, as in a report.",
            "Colloquial: So … turned up and … Formal: A … attended …, and …",
            "Colloquial: So loads of people turned up and the music was awesome. Formal: A considerable number of guests attended, and the musical performance was outstanding.",
            ["grammar.register_shift", "vocab.colloquial"],
        ),
        blank(
            "quiz-far-from-translate",
            "QUIZ",
            "Complete the fronted sentence.",
            "Far ___ being simple, translation is an art.",
            ["from"],
            ["from", "of", "to"],
            ["grammar.fronting"],
            "Remember Lesson 5.",
            "Far from being simple, translation is an art.",
        ),
        choice(
            "quiz-figurative-translate",
            "QUIZ",
            "Why are idioms hard to translate?",
            "Choose the best answer.",
            [
                ("Their figurative meaning differs from the literal words.", None),
                ("They are always very long.", None),
                ("They are only used in writing.", None),
            ],
            "a",
            ["vocab.figurative", "vocab.literal", "grammar.idiom_form"],
            "Remember Unit 1, Lesson 1.",
            "Their figurative meaning differs from the literal words.",
        ),
        choice(
            "quiz-nominal-translation",
            "QUIZ",
            "Choose the academic version.",
            "{teen} translated the stories, so more people read them.",
            [
                ("The translation of the stories led to a wider readership.", None),
                ("{teen} translated stuff and loads more people read it.", None),
                ("Translating, readers increased.", None),
            ],
            "a",
            ["grammar.nominalisation"],
            "Remember Unit 1, Lesson 4.",
            "The translation of the stories led to a wider readership.",
        ),
    ],
}

LESSON_7 = {
    "slug": L7,
    "title": "Science for Everyone",
    "description": "{boy} explains black holes to {little}'s class. The simpler it sounds, the harder it is to do!",
    "minutes": 45,
    "objectives": [
        "Use vocabulary for explaining: jargon, analogy, accessible, misconception, layperson.",
        "Use advanced comparative structures: the more … the more …, just as … so …, not so much … as ….",
        "Explain a complex idea in simple, accurate language.",
    ],
    "review": [
        "grammar.register_shift",
        "vocab.nuance",
        "vocab.colloquial",
        "grammar.comparatives",
        "grammar.hedging",
        "grammar.second_conditional",
        "vocab.planet",
        "vocab.gravity",
        "vocab.galaxy",
        "vocab.scientist",
    ],
    "episode": (
        "The Black Hole in Room 4",
        "{boy} volunteers to explain black holes to {little}'s class of twelve-year-olds. They ask brilliant questions.",
    ),
    "content": {
        "story_intro": "{little}'s science teacher has invited {boy} to explain black holes to her class.",
        "reading": {
            "title": "How to Explain a Black Hole",
            "paragraphs": [
                {
                    "sentences": [
                        "I had prepared slides full of jargon: event horizon, singularity, spacetime curvature.",
                        "{little} looked at them and said: 'Nobody will understand a word. You have to make it accessible.'",
                    ]
                },
                {
                    "sentences": [
                        "So I started with an analogy. Just as water spirals faster and faster down a plughole, so everything near a black hole is pulled in faster and faster.",
                        "The closer you get, the harder it is to escape.",
                    ]
                },
                {
                    "sentences": [
                        "Then I tackled a misconception. Many people think a black hole is a 'hole'. It's not so much a hole as an enormous amount of mass squeezed into a tiny space.",
                        "Imagine the whole Earth squeezed into something the size of a marble.",
                    ]
                },
                {
                    "sentences": [
                        "The questions were wonderful. 'If you fell in, would you stretch like spaghetti?' Yes — scientists actually call it 'spaghettification'.",
                        "The more questions they asked, the more I realised how much I didn't know.",
                    ]
                },
                {
                    "sentences": [
                        "Explaining science to a layperson isn't about dumbing it down. It's about finding the right picture.",
                        "The simpler an explanation sounds, the more work it has usually taken.",
                    ]
                },
            ],
            "highlight": [
                "jargon",
                "accessible",
                "analogy",
                "Just as",
                "so",
                "The closer",
                "the harder",
                "misconception",
                "not so much a hole as",
                "The more",
                "the more",
                "layperson",
                "The simpler",
                "the more work",
            ],
        },
        "listening": [
            {
                "id": "c2-7-questions",
                "title": "Questions from the class",
                "transcript": [
                    {"speaker": "Student", "text": "Is a black hole twice as big as the Sun?"},
                    {
                        "speaker": "{boy}",
                        "text": "Some are smaller, some are millions of times heavier. It's not so much about size as about mass.",
                    },
                    {"speaker": "{little}", "text": "So the heavier it is, the stronger it pulls?"},
                    {
                        "speaker": "{boy}",
                        "text": "Exactly. You've just explained gravity better than my textbook.",
                    },
                ],
            },
            {
                "id": "c2-7-myth",
                "title": "A common misconception",
                "transcript": [
                    {
                        "speaker": "Teacher",
                        "text": "Is it true that black holes suck everything in, like a vacuum cleaner?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "That's a common misconception. If the Sun became a black hole of the same mass, the Earth would keep orbiting normally.",
                    },
                    {
                        "speaker": "Teacher",
                        "text": "Really? So it's not as dangerous as people think.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "Not from a distance, no. Just don't get too close!",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Advanced comparative structures",
                "explanation": (
                    "the + comparative …, the + comparative …: shows that two things change together. "
                    "The closer you get, the harder it is to escape. The more you read, the more you understand. "
                    "Just as …, so …: draws a parallel (an analogy). Just as water spirals down a plughole, so matter spirals into a black hole. "
                    "not so much A as B: B describes it better than A. It's not so much a hole as a huge mass. "
                    "twice / three times as … as: The Sun is about 109 times as wide as the Earth."
                ),
                "explanation_ru": (
                    "the more …, the more … — чем больше …, тем больше …; Just as …, so … — так же, как …, так и …; "
                    "not so much A as B — не столько A, сколько B."
                ),
                "examples": [
                    "The earlier you start, the better.",
                    "Just as a library stores books, so DNA stores information.",
                    "It's not so much difficult as unfamiliar.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "explaining-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("jargon", "special words used by experts that others find hard", None),
                ("analogy", "a comparison that explains something by showing a similarity", None),
                ("misconception", "a wrong idea that many people have", None),
                ("layperson", "someone who is not an expert", None),
            ],
            ["vocab.jargon", "vocab.analogy", "vocab.misconception", "vocab.layperson"],
            "An analogy compares two things.",
            "jargon = expert words; analogy = explanatory comparison; misconception = a wrong idea; layperson = non-expert.",
        ),
        matching(
            "explaining-pictures",
            "VOCABULARY",
            "Match the word to the picture.",
            [("accessible", None, "🚪"), ("analogy", None, "🔁"), ("misconception", None, "🤯")],
            ["vocab.accessible", "vocab.analogy", "vocab.misconception"],
            "Accessible = easy to enter or understand.",
            "accessible 🚪, analogy 🔁, misconception 🤯.",
        ),
        choice(
            "find-jargon",
            "VOCABULARY",
            "Tap the right picture.",
            "Which picture best represents scientific jargon?",
            [(None, "🧪"), (None, "🧸"), (None, "🍕")],
            "a",
            ["vocab.jargon"],
            "Specialist lab language.",
            "🧪 jargon belongs to the lab.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-the-more",
            "LISTENING",
            "Listen. What does the speaker say about practice?",
            "She says that …",
            [
                ("the more you practise, the more natural it feels", "🔁"),
                ("practice is a waste of time", "⌛"),
                ("you should only practise once", "1️⃣"),
            ],
            "a",
            ["grammar.comparative_structures"],
            "Listen for 'the more … the more'.",
            "The more you practise, the more natural it feels.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Explaining science is a skill. The more you practise, the more natural it feels, and the fewer notes you need.",
        ),
        true_false(
            "listen-size-mass",
            "LISTENING",
            "Listen to the class. True or false?",
            "{boy} says black holes are mainly about size, not mass.",
            False,
            ["grammar.comparative_structures"],
            "Listen for 'not so much … as …'.",
            "It's not so much about size as about mass.",
            listening_id="c2-7-questions",
        ),
        true_false(
            "listen-vacuum",
            "LISTENING",
            "Listen to the teacher and {boy}. True or false?",
            "The idea that black holes suck everything in like a vacuum cleaner is a misconception.",
            True,
            ["vocab.misconception"],
            "Listen to {boy}'s first answer.",
            "That's a common misconception.",
            listening_id="c2-7-myth",
        ),
        blank(
            "the-more-blank",
            "GRAMMAR",
            "Complete the comparative structure.",
            "The ___ you get, the ___ it is to escape.",
            ["closer", "harder"],
            ["closer", "close", "harder", "hard"],
            ["grammar.comparative_structures"],
            "the + comparative …, the + comparative …",
            "The closer you get, the harder it is to escape.",
        ),
        blank(
            "just-as-blank",
            "GRAMMAR",
            "Complete the analogy.",
            "___ as a library stores books, ___ DNA stores information.",
            ["Just", "so"],
            ["Just", "Such", "so", "then"],
            ["grammar.comparative_structures", "vocab.analogy"],
            "Just as …, so …",
            "Just as a library stores books, so DNA stores information.",
        ),
        choice(
            "not-so-much",
            "GRAMMAR",
            "Choose the correct sentence.",
            "A black hole is better described as a huge mass than as a hole.",
            [
                ("It's not so much a hole as a huge mass.", None),
                ("It's not so much a hole than a huge mass.", None),
                ("It's not as much hole so huge mass.", None),
            ],
            "a",
            ["grammar.comparative_structures"],
            "not so much A as B.",
            "It's not so much a hole as a huge mass.",
        ),
        choice(
            "times-as",
            "GRAMMAR",
            "Which sentence is correct?",
            "Compare Jupiter and the Earth.",
            [
                ("Jupiter is about eleven times as wide as the Earth.", None),
                ("Jupiter is about eleven times wider as the Earth.", None),
                ("Jupiter is about eleven times as wide than the Earth.", None),
            ],
            "a",
            ["grammar.comparative_structures", "vocab.planet"],
            "X times as + adjective + as.",
            "Jupiter is about eleven times as wide as the Earth.",
        ),
        build(
            "build-the-more",
            "GRAMMAR",
            "Put the words in order.",
            "The more you read, the more you understand.",
            ["grammar.comparative_structures"],
            "Start with 'The more you read'.",
            "The more you read, the more you understand.",
        ),
        choice(
            "read-plughole",
            "READING",
            "Read the text. Then answer.",
            "What analogy does {boy} use?",
            [
                ("water spiralling down a plughole", "🌀"),
                ("a vacuum cleaner", "🧹"),
                ("a library full of books", "📚"),
            ],
            "a",
            ["vocab.analogy"],
            "Look at paragraph 2.",
            "Water spiralling faster and faster down a plughole.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-dumbing",
            "READING",
            "Read the text. True or false?",
            "{boy} thinks explaining science to a layperson means dumbing it down.",
            False,
            ["vocab.layperson", "vocab.accessible"],
            "Look at the last paragraph.",
            "It isn't about dumbing it down. It's about finding the right picture.",
        ),
        speak(
            "say-explain",
            "Explain a scientific idea you know (for example gravity, photosynthesis or the internet) to a ten-year-old. Use an analogy and at least one advanced comparative.",
            "Just as …, so … The more …, the more … It's not so much … as …",
            "Just as a magnet pulls a paper clip, so the Earth pulls everything towards it. The heavier something is, the stronger it pulls. Gravity is not so much a thing as a force.",
            ["grammar.comparative_structures", "vocab.analogy"],
        ),
        choice(
            "quiz-register-science",
            "QUIZ",
            "Which version is best for a children's science book?",
            "Choose the right register.",
            [
                ("A black hole pulls things in very strongly.", None),
                ("The gravitational field of a singularity is of considerable magnitude.", None),
                ("BH = mega pull lol.", None),
            ],
            "a",
            ["grammar.register_shift", "vocab.accessible"],
            "Remember Lesson 6: match the reader.",
            "A black hole pulls things in very strongly.",
        ),
        choice(
            "quiz-second-fell",
            "QUIZ",
            "Choose the correct sentence.",
            "Imagine falling into a black hole.",
            [
                ("If you fell into a black hole, you would stretch like spaghetti.", None),
                ("If you fall into a black hole, you would stretch like spaghetti.", None),
                ("If you fell into a black hole, you will stretch like spaghetti.", None),
            ],
            "a",
            ["grammar.second_conditional"],
            "Remember B2.",
            "If you fell into a black hole, you would stretch.",
        ),
        blank(
            "quiz-nuance-science",
            "QUIZ",
            "Choose the right word.",
            "A good translator notices every ___ of meaning.",
            ["nuance"],
            ["nuance", "jargon", "dialect"],
            ["vocab.nuance"],
            "Remember Lesson 6.",
            "A good translator notices every nuance of meaning.",
        ),
    ],
}

LESSON_8 = {
    "slug": L8,
    "title": "The Negotiation",
    "description": "Where should the family spend Granny {gran1}'s ninetieth birthday? A delicate negotiation begins.",
    "minutes": 45,
    "objectives": [
        "Use negotiation vocabulary: compromise, concession, proposal, tactful, consensus.",
        "Use diplomatic language to soften requests and disagreement.",
        "Negotiate politely and reach a compromise.",
    ],
    "review": [
        "grammar.comparative_structures",
        "vocab.analogy",
        "vocab.misconception",
        "grammar.register_shift",
        "grammar.indirect_questions",
        "phrase.agree_disagree",
        "grammar.formal_register",
        "grammar.would_like",
        "vocab.birthday",
        "vocab.guest",
    ],
    "episode": (
        "Ninety Candles",
        "Every family member has a different plan for Granny {gran1}'s ninetieth birthday. {boy} becomes the reluctant mediator.",
    ),
    "content": {
        "story_intro": "Granny {gran1} turns ninety in June. Everyone has a different idea — and strong opinions.",
        "reading": {
            "title": "The Great Birthday Negotiation",
            "paragraphs": [
                {
                    "sentences": [
                        "Aunt {aunt} wanted a big party at a hotel. Dad wanted a quiet lunch at home. {little} wanted a picnic with a bouncy castle.",
                        "For the first twenty minutes, nobody was very tactful.",
                    ]
                },
                {
                    "sentences": [
                        "Then {teen} tried a different approach. 'I was wondering whether we might ask Granny what she'd prefer,' she said.",
                        "Everyone went quiet. It was, embarrassingly, the first time anyone had suggested it.",
                    ]
                },
                {
                    "sentences": [
                        "Granny's answer surprised us all: she wanted to go back to the village hall where she had danced as a girl.",
                        "Aunt {aunt} made the first concession: 'It might be worth looking at the hall, then. Perhaps the hotel could do the catering?'",
                    ]
                },
                {
                    "sentences": [
                        "Dad was slightly concerned about the cost. 'Wouldn't it be better to keep the guest list a little shorter?'",
                        "My proposal was a compromise: fifty guests, the village hall, Aunt {aunt}'s caterers — and one small bouncy castle in the garden.",
                    ]
                },
                {
                    "sentences": [
                        "Remarkably, we reached a consensus in under an hour.",
                        "The more we listened, the less we argued. Diplomacy, it turns out, begins at home.",
                    ]
                },
            ],
            "highlight": [
                "tactful",
                "I was wondering whether we might",
                "concession",
                "It might be worth",
                "slightly concerned",
                "Wouldn't it be better",
                "a little shorter",
                "proposal",
                "compromise",
                "consensus",
            ],
        },
        "listening": [
            {
                "id": "c2-8-hotel",
                "title": "Calling the hotel",
                "transcript": [
                    {
                        "speaker": "Aunt {aunt}",
                        "text": "I was wondering if you might be able to offer a slightly lower price for fifty guests.",
                    },
                    {
                        "speaker": "Manager",
                        "text": "I'm afraid that would be rather difficult. However, we could include the cake at no extra cost.",
                    },
                    {
                        "speaker": "Aunt {aunt}",
                        "text": "That sounds like a reasonable compromise. Could you send the proposal in writing?",
                    },
                    {"speaker": "Manager", "text": "Of course. You'll have it by this afternoon."},
                ],
            },
            {
                "id": "c2-8-dad",
                "title": "Dad and Aunt {aunt}",
                "transcript": [
                    {
                        "speaker": "Dad",
                        "text": "With respect, a hotel party seems a little excessive.",
                    },
                    {
                        "speaker": "Aunt {aunt}",
                        "text": "I take your point. Wouldn't it be nice, though, to make it really special?",
                    },
                    {
                        "speaker": "Dad",
                        "text": "Perhaps we could find a middle ground. The village hall, maybe?",
                    },
                    {"speaker": "Aunt {aunt}", "text": "That might actually work."},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Diplomatic language",
                "explanation": (
                    "In negotiations we soften what we say so that we don't sound rude or aggressive. "
                    "Past tenses for distance: I was wondering whether … / I wanted to ask … "
                    "Modals: It might be worth … / Could we perhaps …? / That would be rather difficult. "
                    "Negative questions as suggestions: Wouldn't it be better to …? / Shouldn't we …? "
                    "Softeners: slightly, a little, rather, a bit, perhaps. "
                    "Polite disagreement: With respect, … / I take your point, but … / I'm not entirely convinced."
                ),
                "explanation_ru": (
                    "Дипломатичный язык: прошедшее время для вежливости (I was wondering), модальные (might, could), "
                    "отрицательные вопросы (Wouldn't it be better …?), смягчители (slightly, a little)."
                ),
                "examples": [
                    "I was wondering whether we could postpone the meeting.",
                    "It might be worth considering a smaller venue.",
                    "That would be slightly difficult for us.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "negotiation-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("compromise", "an agreement where each side gives up something", None),
                ("concession", "something you agree to give up in a negotiation", None),
                ("consensus", "general agreement among a group", None),
                ("tactful", "careful not to upset people", None),
            ],
            ["vocab.compromise", "vocab.concession", "vocab.consensus", "vocab.tactful"],
            "A compromise is a middle way.",
            "compromise = a middle way; concession = something given up; consensus = general agreement; tactful = careful not to offend.",
        ),
        matching(
            "negotiation-pictures",
            "VOCABULARY",
            "Match the word to the picture.",
            [("proposal", None, "📝"), ("compromise", None, "🤝"), ("consensus", None, "✅")],
            ["vocab.proposal", "vocab.compromise", "vocab.consensus"],
            "A proposal is a written plan.",
            "proposal 📝, compromise 🤝, consensus ✅.",
        ),
        choice(
            "find-tactful",
            "VOCABULARY",
            "Tap the right picture.",
            "Which picture best represents being tactful?",
            [(None, "🕊️"), (None, "💣"), (None, "📢")],
            "a",
            ["vocab.tactful"],
            "Peaceful and gentle.",
            "🕊️ tactful.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-diplomatic",
            "LISTENING",
            "Listen. What is the woman actually saying?",
            "She means that …",
            [
                ("she doesn't really like the plan", "🙅"),
                ("she loves the plan", "😍"),
                ("she didn't hear the plan", "🙉"),
            ],
            "a",
            ["grammar.diplomatic_language"],
            "Diplomatic language hides strong disagreement.",
            "'I'm not entirely convinced' = I don't really like it.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="It's an interesting idea, and I can see you've worked hard on it. I'm just not entirely convinced it's right for us.",
        ),
        true_false(
            "listen-cake-free",
            "LISTENING",
            "Listen to Aunt {aunt} and the manager. True or false?",
            "The manager agrees to lower the price.",
            False,
            ["vocab.compromise", "grammar.diplomatic_language"],
            "What does he offer instead?",
            "He says a lower price would be difficult, but offers the cake at no extra cost.",
            listening_id="c2-8-hotel",
        ),
        true_false(
            "listen-middle-ground",
            "LISTENING",
            "Listen to Dad and Aunt {aunt}. True or false?",
            "Dad suggests the village hall as a middle ground.",
            True,
            ["vocab.compromise"],
            "Listen to Dad's second line.",
            "Perhaps we could find a middle ground. The village hall, maybe?",
            listening_id="c2-8-dad",
        ),
        blank(
            "diplomatic-blank",
            "GRAMMAR",
            "Make the requests more diplomatic.",
            "I was ___ whether we could change the date. It ___ be worth looking at the hall.",
            ["wondering", "might"],
            ["wondering", "wonder", "might", "must"],
            ["grammar.diplomatic_language"],
            "Past continuous for distance; might for a soft suggestion.",
            "I was wondering whether … It might be worth …",
        ),
        choice(
            "most-diplomatic",
            "GRAMMAR",
            "Which is the most diplomatic way to disagree?",
            "Your aunt suggests an expensive hotel.",
            [
                ("I take your point, but wouldn't it be better to keep it simple?", None),
                ("That's a ridiculous idea.", None),
                ("No. Too expensive.", None),
            ],
            "a",
            ["grammar.diplomatic_language", "vocab.tactful"],
            "Acknowledge, then use a negative question.",
            "I take your point, but wouldn't it be better to keep it simple?",
        ),
        choice(
            "softener",
            "GRAMMAR",
            "Choose the softened version.",
            "The price is too high.",
            [
                ("The price seems slightly higher than we expected.", None),
                ("The price is way too high!", None),
                ("Your price is a rip-off.", None),
            ],
            "a",
            ["grammar.diplomatic_language"],
            "Use seems and slightly.",
            "The price seems slightly higher than we expected.",
        ),
        blank(
            "negative-question-blank",
            "GRAMMAR",
            "Complete the diplomatic suggestion.",
            "___ it be better to keep the guest list a little ___?",
            ["Wouldn't", "shorter"],
            ["Wouldn't", "Won't", "shorter", "short"],
            ["grammar.diplomatic_language", "vocab.guest"],
            "Negative question + softener + comparative.",
            "Wouldn't it be better to keep the guest list a little shorter?",
        ),
        build(
            "build-diplomatic",
            "GRAMMAR",
            "Put the words in order.",
            "It might be worth considering another option.",
            ["grammar.diplomatic_language"],
            "Start with 'It might'.",
            "It might be worth considering another option.",
        ),
        choice(
            "read-granny-choice",
            "READING",
            "Read the text. Then answer.",
            "What did Granny {gran1} want for her birthday?",
            [
                ("a party at the village hall where she had danced as a girl", "💃"),
                ("a quiet lunch at home", "🍲"),
                ("a big hotel party", "🏨"),
            ],
            "a",
            ["vocab.proposal"],
            "Look at paragraph 3.",
            "She wanted to go back to the village hall where she had danced as a girl.",
            ex_type="READING_COMPREHENSION",
        ),
        order(
            "read-order",
            "READING",
            "Put the negotiation in order.",
            [
                "Everyone suggested a different plan.",
                "{teen} suggested asking Granny.",
                "Granny chose the village hall.",
                "Aunt {aunt} made the first concession.",
                "{boy} proposed a compromise.",
            ],
            ["vocab.concession", "vocab.compromise"],
            "The compromise comes at the end.",
            "Plans → ask Granny → village hall → concession → compromise.",
        ),
        speak(
            "say-negotiate",
            "Your class must choose between a museum trip and a beach day. Negotiate diplomatically: acknowledge the other view, make a concession and propose a compromise.",
            "I take your point … I was wondering whether … It might be worth … Wouldn't it be better …? How about a compromise: …",
            "I take your point about the beach. I was wondering whether we could do both. It might be worth visiting the museum in the morning. Wouldn't it be better to finish the day at the beach? That seems like a fair compromise.",
            ["grammar.diplomatic_language", "vocab.compromise"],
        ),
        blank(
            "quiz-the-more-listen",
            "QUIZ",
            "Complete the sentence.",
            "The more we listened, the ___ we argued.",
            ["less"],
            ["less", "fewer", "least"],
            ["grammar.comparative_structures"],
            "Remember Lesson 7.",
            "The more we listened, the less we argued.",
        ),
        choice(
            "quiz-register-hotel",
            "QUIZ",
            "Which sentence is formal enough for an email to the hotel?",
            "Choose one.",
            [
                ("We would be grateful if you could confirm the booking.", None),
                ("Can u confirm the booking thx", None),
                ("Sort out the booking, yeah?", None),
            ],
            "a",
            ["grammar.register_shift", "grammar.formal_register"],
            "Remember Lesson 6.",
            "We would be grateful if you could confirm the booking.",
        ),
        choice(
            "quiz-indirect-diplomatic",
            "QUIZ",
            "Choose the polite indirect question.",
            "How much does the hall cost?",
            [
                ("Could you tell me how much the hall costs?", None),
                ("Could you tell me how much does the hall cost?", None),
                ("Tell me how much costs the hall.", None),
            ],
            "a",
            ["grammar.indirect_questions"],
            "Remember B2.",
            "Could you tell me how much the hall costs?",
        ),
    ],
}

LESSON_9 = {
    "slug": L9,
    "title": "Poetry and Rhythm",
    "description": "{little} writes a poem for Granny {gran1}'s birthday. Rhyme, rhythm and stress — she DOES want it to be perfect.",
    "minutes": 40,
    "objectives": [
        "Use poetry vocabulary: rhyme, stanza, rhythm, alliteration, stress.",
        "Use emphatic structures: stressed do/does/did, the very, whatsoever.",
        "Read a poem aloud with natural stress and rhythm.",
    ],
    "review": [
        "grammar.diplomatic_language",
        "vocab.tactful",
        "vocab.compromise",
        "grammar.comparative_structures",
        "grammar.inversion",
        "grammar.cleft_sentences",
        "vocab.imagery",
        "vocab.metaphor",
        "vocab.song",
        "vocab.grandmother",
    ],
    "episode": (
        "Ninety Lines for Ninety Years",
        "{little} writes a poem for Granny {gran1}'s birthday and practises reading it aloud — again and again.",
    ),
    "content": {
        "story_intro": "{little} has decided to write a poem for Granny {gran1}'s ninetieth birthday and read it at the party.",
        "reading": {
            "title": "Writing the Poem",
            "paragraphs": [
                {
                    "sentences": [
                        "{little} spent a week on her poem. It had four stanzas, one for each part of Granny's life.",
                        "'Does it have to rhyme?' she asked. {teen} said no — but {little} did want it to rhyme, at least at the end of each stanza.",
                    ]
                },
                {
                    "sentences": [
                        "Her favourite line used alliteration: 'Dancing in the dusty dark of the village hall.'",
                        "Read it aloud, and the repeated d-sounds feel like footsteps on a wooden floor.",
                    ]
                },
                {
                    "sentences": [
                        "Then {boy} showed her how stress creates rhythm in English. 'Listen: da-DUM, da-DUM. Like a heartbeat.'",
                        "The very idea that a poem could have a heartbeat delighted her.",
                    ]
                },
                {
                    "sentences": [
                        "She practised reading it every evening. 'I do know it by heart,' she insisted, 'I just get nervous.'",
                        "Mum's advice: 'Do slow down. Let every word land.'",
                    ]
                },
                {
                    "sentences": [
                        "At the party, the hall went completely silent. When she finished, there was no doubt whatsoever who had given the best present.",
                        "Granny {gran1} didn't say anything for a long time. Then she did something none of us had ever seen: she asked for an encore.",
                    ]
                },
            ],
            "highlight": [
                "stanzas",
                "rhyme",
                "did want",
                "alliteration",
                "stress",
                "rhythm",
                "The very idea",
                "I do know",
                "Do slow down",
                "whatsoever",
                "she did something",
            ],
        },
        "listening": [
            {
                "id": "c2-9-practice",
                "title": "Practising the poem",
                "transcript": [
                    {
                        "speaker": "{little}",
                        "text": "'Ninety years of summers, ninety years of snow …' Is it too fast?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "A bit. Stress the important words: NINEty YEARS of SUMmers.",
                    },
                    {"speaker": "{little}", "text": "Oh! Now it does sound like music."},
                    {"speaker": "{boy}", "text": "That's rhythm. You've got it."},
                ],
            },
            {
                "id": "c2-9-stress",
                "title": "Stress changes meaning",
                "transcript": [
                    {
                        "speaker": "{teen}",
                        "text": "Listen to how stress changes the meaning. 'I didn't say she stole the cake.'",
                    },
                    {
                        "speaker": "{teen}",
                        "text": "'I didn't say SHE stole the cake' — someone else did.",
                    },
                    {
                        "speaker": "{teen}",
                        "text": "'I didn't say she stole the CAKE' — she stole something else!",
                    },
                    {"speaker": "{little}", "text": "That's the very thing I need for my poem!"},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Emphatic structures",
                "explanation": (
                    "Stressed auxiliary do / does / did: adds emphasis or contradicts: I DO know it by heart! She DID want it to rhyme. "
                    "Do + imperative: a warmer, stronger request: Do slow down. Do come in. "
                    "the very + noun: exactly that one: That's the very book I was looking for. "
                    "at all / whatsoever after a negative: There was no doubt whatsoever. I didn't understand it at all. "
                    "Also: Inversion, cleft sentences and fronting, which you have already learned."
                ),
                "explanation_ru": (
                    "Эмфаза: ударное do/does/did (I DO know!), Do + повелительное (Do come in!), "
                    "the very — именно тот; whatsoever / at all — совсем, абсолютно."
                ),
                "examples": [
                    "I did tell you — you weren't listening!",
                    "Do take a seat.",
                    "He had no idea whatsoever.",
                ],
            },
            {
                "title": "Stress and rhythm in speech",
                "explanation": (
                    "English is stress-timed: stressed syllables come at regular intervals, and unstressed ones are squeezed in between. "
                    "Content words (nouns, main verbs, adjectives) are usually stressed; grammar words (a, the, of, to) are usually not. "
                    "Moving the stress changes the meaning: I didn't say SHE took it vs I didn't say she TOOK it."
                ),
                "explanation_ru": "В английском ударные слоги идут ритмично; перенос ударения меняет смысл фразы.",
                "examples": ["NINEty YEARS of SUMmers", "I WANted to GO to the PARK."],
            },
        ],
    },
    "exercises": [
        matching(
            "poetry-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("rhyme", "words that end with the same sound", None),
                ("stanza", "a group of lines in a poem", None),
                ("alliteration", "repeating the same first sound in nearby words", None),
                ("rhythm", "a regular pattern of strong and weak beats", None),
            ],
            ["vocab.rhyme", "vocab.stanza", "vocab.alliteration", "vocab.rhythm"],
            "Moon / June = rhyme.",
            "rhyme = same end sound; stanza = group of lines; alliteration = same first sound; rhythm = beat pattern.",
        ),
        matching(
            "poetry-pictures",
            "VOCABULARY",
            "Match the word to the picture.",
            [("rhythm", None, "🥁"), ("stress (in words)", None, "🔊"), ("stanza", None, "🧱")],
            ["vocab.rhythm", "vocab.stress", "vocab.stanza"],
            "Stress = a louder, stronger syllable.",
            "rhythm 🥁, stress 🔊, stanza 🧱.",
        ),
        choice(
            "find-alliteration",
            "VOCABULARY",
            "Which phrase is an example of alliteration?",
            "Choose one.",
            [("big blue boats", "🅱️"), ("the moon in June", "🌙"), ("a long, sad song", "🎵")],
            "a",
            ["vocab.alliteration", "vocab.rhyme"],
            "Look at the first sounds.",
            "big blue boats — the same b-sound.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-emphatic",
            "LISTENING",
            "Listen. What is the boy insisting?",
            "He insists that he …",
            [
                ("did do his homework", "📘"),
                ("didn't do his homework", "🙈"),
                ("will do his homework later", "⏰"),
            ],
            "a",
            ["grammar.emphatic_structures"],
            "Listen for the stressed 'did'.",
            "I DID do my homework — the dog really ate it!",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="I know it sounds like an excuse, but I did do my homework. The dog really did eat it!",
        ),
        true_false(
            "listen-music",
            "LISTENING",
            "Listen to {little} and {boy}. True or false?",
            "When {little} stresses the important words, the poem sounds more like music.",
            True,
            ["vocab.stress", "vocab.rhythm", "grammar.emphatic_structures"],
            "Listen to {little}'s second line.",
            "Oh! Now it does sound like music.",
            listening_id="c2-9-practice",
        ),
        true_false(
            "listen-stress-meaning",
            "LISTENING",
            "Listen to {teen}. True or false?",
            "Moving the stress in a sentence never changes its meaning.",
            False,
            ["vocab.stress"],
            "Compare the two versions.",
            "Moving the stress changes the meaning: SHE vs CAKE.",
            listening_id="c2-9-stress",
        ),
        blank(
            "emphatic-blank",
            "GRAMMAR",
            "Complete the emphatic sentences.",
            "I ___ know it by heart! That's the ___ book I was looking for.",
            ["do", "very"],
            ["do", "am", "very", "same"],
            ["grammar.emphatic_structures"],
            "Stressed do; the very + noun.",
            "I do know it by heart! That's the very book I was looking for.",
        ),
        choice(
            "did-want",
            "GRAMMAR",
            "Choose the emphatic sentence that contradicts 'You didn't want it to rhyme.'",
            "Choose one.",
            [
                ("But I did want it to rhyme!", None),
                ("But I did wanted it to rhyme!", None),
                ("But I wanted do it to rhyme!", None),
            ],
            "a",
            ["grammar.emphatic_structures", "vocab.rhyme"],
            "did + base verb.",
            "But I did want it to rhyme!",
        ),
        choice(
            "whatsoever",
            "GRAMMAR",
            "Which sentence is correct?",
            "Emphasise that there was no doubt.",
            [
                ("There was no doubt whatsoever.", None),
                ("There was whatsoever no doubt.", None),
                ("There was a doubt whatsoever.", None),
            ],
            "a",
            ["grammar.emphatic_structures"],
            "whatsoever follows a negative noun phrase.",
            "There was no doubt whatsoever.",
        ),
        blank(
            "do-imperative-blank",
            "GRAMMAR",
            "Complete Mum's warm advice.",
            "___ slow down. Let every word land.",
            ["Do"],
            ["Do", "Does", "Did"],
            ["grammar.emphatic_structures"],
            "Do + imperative.",
            "Do slow down.",
        ),
        build(
            "build-emphatic",
            "GRAMMAR",
            "Put the words in order.",
            "She did ask for an encore.",
            ["grammar.emphatic_structures"],
            "Start with 'She did'.",
            "She did ask for an encore.",
        ),
        choice(
            "read-alliteration",
            "READING",
            "Read the text. Then answer.",
            "What effect does the alliteration in 'Dancing in the dusty dark' create?",
            [
                ("The d-sounds feel like footsteps on a wooden floor.", "👣"),
                ("It makes the poem rhyme.", "🎵"),
                ("It makes the line shorter.", "✂️"),
            ],
            "a",
            ["vocab.alliteration"],
            "Look at paragraph 2.",
            "The repeated d-sounds feel like footsteps.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-encore",
            "READING",
            "Read the text. True or false?",
            "Granny {gran1} asked {little} to read the poem again.",
            True,
            ["grammar.emphatic_structures"],
            "Look at the last sentence.",
            "She asked for an encore.",
        ),
        speak(
            "say-poem",
            "Write and read aloud a four-line poem about someone in your family. Use rhyme or alliteration, and stress the important words.",
            "Line 1 … / Line 2 … (rhyme) / Line 3 … / Line 4 … (rhyme)",
            "My grandad grows green beans in rows, / He hums old songs that no one knows. / His hands are hard, his heart is kind, / The gentlest man you'll ever find.",
            ["vocab.rhyme", "vocab.alliteration", "vocab.rhythm"],
        ),
        choice(
            "quiz-diplomatic-poem",
            "QUIZ",
            "Choose the most tactful feedback on {little}'s poem.",
            "The middle stanza is too long.",
            [
                ("It might be worth making the middle stanza slightly shorter.", None),
                ("The middle bit is boring. Cut it.", None),
                ("Your poem is too long.", None),
            ],
            "a",
            ["grammar.diplomatic_language", "vocab.stanza"],
            "Remember Lesson 8.",
            "It might be worth making the middle stanza slightly shorter.",
        ),
        blank(
            "quiz-the-slower",
            "QUIZ",
            "Complete the sentence.",
            "The ___ you read, the more the audience feels.",
            ["slower"],
            ["slower", "slow", "slowest"],
            ["grammar.comparative_structures"],
            "Remember Lesson 7.",
            "The slower you read, the more the audience feels.",
        ),
        choice(
            "quiz-inversion-poem",
            "QUIZ",
            "Choose the correct sentence.",
            "The hall had rarely been so silent.",
            [
                ("Rarely had the hall been so silent.", None),
                ("Rarely the hall had been so silent.", None),
                ("Rarely did the hall had been so silent.", None),
            ],
            "a",
            ["grammar.inversion"],
            "Remember C1.",
            "Rarely had the hall been so silent.",
        ),
    ],
}

LESSON_10 = {
    "slug": L10,
    "title": "The Family Film",
    "description": "{boy} turns the family's story into a film — from A1 to C2. The final review of the whole course!",
    "minutes": 50,
    "objectives": [
        "Use film vocabulary: screenplay, premiere, montage, legacy.",
        "Use the formal subjunctive: It is essential that she be …, I suggest that he go ….",
        "Review the whole course, from A1 to C2.",
    ],
    "review": [
        "grammar.emphatic_structures",
        "vocab.rhythm",
        "vocab.alliteration",
        "grammar.diplomatic_language",
        "grammar.comparative_structures",
        "grammar.register_shift",
        "grammar.fronting",
        "grammar.participle_clauses",
        "grammar.narrative_tenses",
        "grammar.third_conditional",
        "vocab.documentary",
        "vocab.family",
    ],
    "episode": (
        "Our Story",
        "At the premiere in the village hall, the whole family watches their own story on the big screen.",
    ),
    "content": {
        "story_intro": "For his final school project, {boy} has made a film about his family — the same family you met in your very first lesson.",
        "reading": {
            "title": "Our Story",
            "paragraphs": [
                {
                    "sentences": [
                        "The film opens with a montage of old photos: {little} as a baby with her first ball, {boy} with his little dog, {teen} with her guitar.",
                        "Hello, my name is {boy}. This is my family — that was the very first line I ever learned in English.",
                    ]
                },
                {
                    "sentences": [
                        "Writing the screenplay, I realised how much had happened. The family trip, the lost kitten, the science club, the debate final …",
                        "Had I not kept a diary, I would have forgotten half of it.",
                    ]
                },
                {
                    "sentences": [
                        "Granny {gran1} insisted that her letters be included. Granny {gran2} demanded that every idiom be subtitled 'for the young people'.",
                        "Mum suggested that the film end with the birthday poem. It was, she said, essential that {little} have the last word.",
                    ]
                },
                {
                    "sentences": [
                        "So moving was the premiere that even Dad — who never cries — had to leave the room 'to check the projector'.",
                        "{teen} called it 'not bad at all', which from her is the highest praise imaginable.",
                    ]
                },
                {
                    "sentences": [
                        "Stories, I've learned, are a family's legacy. The more we tell them, the longer they live.",
                        "This is our story. Thank you for learning English with us. Now — go and tell yours.",
                    ]
                },
            ],
            "highlight": [
                "montage",
                "screenplay",
                "Had I not kept",
                "insisted that her letters be included",
                "demanded that every idiom be subtitled",
                "suggested that the film end",
                "essential that {little} have",
                "So moving was the premiere",
                "legacy",
                "The more",
                "the longer",
            ],
        },
        "listening": [
            {
                "id": "c2-10-premiere",
                "title": "At the premiere",
                "transcript": [
                    {
                        "speaker": "Head teacher",
                        "text": "I propose that this film be shown to every new student. It is the best project we have ever had.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "Thank you. Having said that, it was a family collaboration — I just held the camera.",
                    },
                    {
                        "speaker": "Granny {gran1}",
                        "text": "Nonsense. He did all the hard work. I only insisted that my letters be in it!",
                    },
                    {"speaker": "{little}", "text": "And I insisted that my poem come last."},
                ],
            },
            {
                "id": "c2-10-future",
                "title": "What's next?",
                "transcript": [
                    {"speaker": "{teen}", "text": "So what's next, little brother? University?"},
                    {
                        "speaker": "{boy}",
                        "text": "Film school, if they'll have me. If I hadn't made this film, I wouldn't know what I want to do.",
                    },
                    {
                        "speaker": "{teen}",
                        "text": "Then it's vital that you send them this. Today.",
                    },
                    {"speaker": "{boy}", "text": "I already have. I sent it this morning."},
                ],
            },
        ],
        "grammar": [
            {
                "title": "The subjunctive",
                "explanation": (
                    "In formal English, after verbs and adjectives that express demands, suggestions or importance, we use the base form of the verb "
                    "for all persons — no -s, no past tense. "
                    "Verbs: insist, demand, suggest, propose, recommend, request. Granny insisted that her letters be included. Mum suggested that the film end with the poem. "
                    "Adjectives: essential, vital, important, crucial. It is essential that she have the last word. "
                    "Negative: It is vital that he not be late. "
                    "In less formal English we often use should instead: Mum suggested that the film should end with the poem. "
                    "The subjunctive also appears in fixed expressions: If I were you … / Be that as it may … / So be it."
                ),
                "explanation_ru": (
                    "Сослагательное наклонение в официальной речи: после insist, suggest, demand, essential, vital — "
                    "глагол в базовой форме для всех лиц: It is essential that she be there (не is). Менее формально — should."
                ),
                "examples": [
                    "The teacher recommended that he apply to film school.",
                    "It is crucial that everyone be on time.",
                    "I suggest that she take a break.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "film-terms",
            "VOCABULARY",
            "Match the term to its definition.",
            [
                ("screenplay", "the written text of a film, with dialogue and directions", None),
                ("premiere", "the first public showing of a film", None),
                ("montage", "a sequence of short shots edited together", None),
                ("legacy", "something passed on to future generations", None),
            ],
            ["vocab.screenplay", "vocab.premiere", "vocab.montage", "vocab.legacy"],
            "The premiere is the first showing.",
            "screenplay = film script; premiere = first showing; montage = edited sequence; legacy = what we pass on.",
        ),
        matching(
            "course-memories",
            "VOCABULARY",
            "Match each level to a memory from the family's story.",
            [
                ("A1", "Hello, my name is … This is my family.", None),
                ("B1", "The lost kitten and the school play", None),
                ("C1", "The documentary and Granny's memoir", None),
                ("C2", "Idioms at dinner and the family film", None),
            ],
            ["grammar.my_name_is", "vocab.kitten", "vocab.memoir", "vocab.screenplay"],
            "The story started with 'Hello'.",
            "A1: introductions; B1: kitten and play; C1: documentary and memoir; C2: idioms and the film.",
        ),
        choice(
            "find-premiere",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: premiere",
            [(None, "🎟️"), (None, "📄"), (None, "🌳")],
            "a",
            ["vocab.premiere"],
            "You need a ticket for the first showing.",
            "🎟️ premiere.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-subjunctive",
            "LISTENING",
            "Listen. What did the director recommend?",
            "She recommended that the actor …",
            [
                ("rest before filming", "😴"),
                ("leave the film", "🚪"),
                ("write the screenplay", "📄"),
            ],
            "a",
            ["grammar.subjunctive"],
            "Listen for 'recommended that'.",
            "She recommended that he rest before filming.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="The actor looked exhausted, so the director recommended that he rest for a day before filming the final scene.",
        ),
        true_false(
            "listen-poem-last",
            "LISTENING",
            "Listen to the premiere. True or false?",
            "{little} insisted that her poem come last.",
            True,
            ["grammar.subjunctive"],
            "Listen to {little}'s line.",
            "And I insisted that my poem come last.",
            listening_id="c2-10-premiere",
        ),
        true_false(
            "listen-film-school",
            "LISTENING",
            "Listen to {teen} and {boy}. True or false?",
            "{boy} hasn't sent the film to the film school yet.",
            False,
            ["grammar.subjunctive", "grammar.mixed_conditionals"],
            "Listen to his last line.",
            "I already have. I sent it this morning.",
            listening_id="c2-10-future",
        ),
        blank(
            "subjunctive-blank",
            "GRAMMAR",
            "Complete with the subjunctive.",
            "Granny insisted that her letters ___ included. It is essential that {little} ___ the last word.",
            ["be", "have"],
            ["be", "are", "have", "has"],
            ["grammar.subjunctive"],
            "Base form for all persons.",
            "… that her letters be included … that {little} have the last word.",
        ),
        choice(
            "subjunctive-correct",
            "GRAMMAR",
            "Which sentence uses the formal subjunctive correctly?",
            "Choose one.",
            [
                ("The teacher recommended that he apply to film school.", None),
                ("The teacher recommended that he applies to film school.", None),
                ("The teacher recommended that he applied to film school.", None),
            ],
            "a",
            ["grammar.subjunctive"],
            "No -s, no past: base form.",
            "The teacher recommended that he apply to film school.",
        ),
        choice(
            "subjunctive-should",
            "GRAMMAR",
            "Which is the less formal alternative?",
            "Mum suggested that the film end with the poem.",
            [
                ("Mum suggested that the film should end with the poem.", None),
                ("Mum suggested that the film ends with the poem yesterday.", None),
                ("Mum suggested the film to end with the poem.", None),
            ],
            "a",
            ["grammar.subjunctive"],
            "Use should + base form.",
            "Mum suggested that the film should end with the poem.",
        ),
        blank(
            "subjunctive-negative",
            "GRAMMAR",
            "Complete the formal sentence.",
            "It is vital that the audience ___ ___ told the ending.",
            ["not", "be"],
            ["not", "don't", "be", "is"],
            ["grammar.subjunctive"],
            "Negative subjunctive: not + base form.",
            "It is vital that the audience not be told the ending.",
        ),
        build(
            "build-subjunctive",
            "GRAMMAR",
            "Put the words in order.",
            "I suggest that she take a break.",
            ["grammar.subjunctive"],
            "Start with 'I suggest'.",
            "I suggest that she take a break.",
        ),
        choice(
            "read-montage",
            "READING",
            "Read the text. Then answer.",
            "How does the film begin?",
            [
                ("with a montage of old family photos", "🎞️"),
                ("with the birthday poem", "📜"),
                ("with the debate final", "🎤"),
            ],
            "a",
            ["vocab.montage"],
            "Look at paragraph 1.",
            "The film opens with a montage of old photos.",
            ex_type="READING_COMPREHENSION",
        ),
        order(
            "read-order",
            "READING",
            "Put the moments from the family's story in course order (A1 → C2).",
            [
                "{boy} introduced his family: 'This is my family.'",
                "The family went on a trip to Granny's village.",
                "The children searched for a lost kitten.",
                "{boy}'s team argued about homework at the debate club.",
                "{boy} made the family film.",
            ],
            ["vocab.family", "vocab.kitten", "vocab.debate", "vocab.screenplay"],
            "A1 → A2 → B1 → B2 → C2.",
            "Introductions (A1) → trip (A2) → kitten (B1) → debate (B2) → film (C2).",
        ),
        speak(
            "say-legacy",
            "Final task: Tell your own story in English. Who is in your family? What have you learned? What do you hope for? Use as many structures from the course as you can.",
            "Hello, my name is … This is my family … Having learned …, I … Never have I … The more I …, the more … It is essential that I …",
            "Hello, my name is Anna. This is my family. Having learned English for years, I can now read novels. Never have I felt so confident. The more I practise, the more I enjoy it. It is essential that I keep going.",
            [
                "grammar.subjunctive",
                "grammar.participle_clauses",
                "grammar.comparative_structures",
                "grammar.my_name_is",
            ],
        ),
        choice(
            "quiz-emphatic-final",
            "QUIZ",
            "Choose the emphatic sentence.",
            "Dad says he didn't cry. You know he did.",
            [
                ("But you did cry, Dad!", None),
                ("But you did cried, Dad!", None),
                ("But you cried did, Dad!", None),
            ],
            "a",
            ["grammar.emphatic_structures"],
            "Remember Lesson 9.",
            "But you did cry, Dad!",
        ),
        choice(
            "quiz-diplomatic-final",
            "QUIZ",
            "Choose the most diplomatic suggestion.",
            "The film is a little long.",
            [
                ("Wouldn't it be worth cutting a few minutes?", None),
                ("Cut it. It's too long.", None),
                ("Nobody wants to watch all that.", None),
            ],
            "a",
            ["grammar.diplomatic_language"],
            "Remember Lesson 8.",
            "Wouldn't it be worth cutting a few minutes?",
        ),
        blank(
            "quiz-the-longer",
            "QUIZ",
            "Complete the sentence.",
            "The more we tell our stories, the ___ they live.",
            ["longer"],
            ["longer", "long", "longest"],
            ["grammar.comparative_structures", "vocab.legacy"],
            "Remember Lesson 7.",
            "The more we tell our stories, the longer they live.",
        ),
        choice(
            "quiz-register-final",
            "QUIZ",
            "Choose the formal version.",
            "Loads of people came to the premiere.",
            [
                ("A considerable number of guests attended the premiere.", None),
                ("Tons of folks showed up.", None),
                ("Everyone and their dog came.", None),
            ],
            "a",
            ["grammar.register_shift", "vocab.premiere"],
            "Remember Lesson 6.",
            "A considerable number of guests attended the premiere.",
        ),
        blank(
            "quiz-so-moving",
            "QUIZ",
            "Complete the fronted sentence.",
            "So moving ___ the premiere that even Dad cried.",
            ["was"],
            ["was", "were", "did"],
            ["grammar.fronting"],
            "Remember Unit 1, Lesson 5.",
            "So moving was the premiere that even Dad cried.",
        ),
        choice(
            "quiz-third-diary",
            "QUIZ",
            "Choose the sentence with the same meaning.",
            "Had I not kept a diary, I would have forgotten half of it.",
            [
                ("If I hadn't kept a diary, I would have forgotten half of it.", None),
                ("If I didn't keep a diary, I forget half of it.", None),
                ("If I kept a diary, I will forget half of it.", None),
            ],
            "a",
            ["grammar.third_conditional"],
            "Remember B2: inverted third conditional.",
            "Had I not kept = If I hadn't kept.",
        ),
        blank(
            "quiz-participle-final",
            "QUIZ",
            "Choose the right participle.",
            "___ the screenplay, {boy} realised how much had happened.",
            ["Writing"],
            ["Writing", "Written", "Wrote"],
            ["grammar.participle_clauses", "vocab.screenplay"],
            "Remember Unit 1, Lesson 2.",
            "Writing the screenplay, {boy} realised how much had happened.",
        ),
        choice(
            "quiz-hello-final",
            "QUIZ",
            "Choose the very first sentence of the course.",
            "Where did it all begin?",
            [
                ("Hello, my name is {boy}.", None),
                ("Had I not kept a diary …", None),
                ("So moving was the premiere …", None),
            ],
            "a",
            ["grammar.my_name_is", "vocab.hello"],
            "Remember A1, Lesson 1!",
            "Hello, my name is {boy}. — where it all began.",
        ),
    ],
}

UNIT = {
    "slug": "our-story",
    "title": "Our Story",
    "description": "Translating Granny's tales, explaining science, a family negotiation, a birthday poem and the family film.",
    "lessons": [LESSON_6, LESSON_7, LESSON_8, LESSON_9, LESSON_10],
}
