"""C1 · Unit 1 "Media and Projects" (C1 lessons 1-5).

{boy} is sixteen and works on media and school projects; {little} writes her first story.
Topics: a documentary, fake news, an eco project, creative writing, a charity run. Grammar:
narrative tenses for effect, hedging, cleft sentences, mixed conditionals, inversion after
negative adverbials. Lesson 5 reviews the unit.
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

L1, L2, L3, L4, L5 = (
    "the-documentary",
    "fact-or-fake",
    "the-eco-project",
    "littles-first-story",
    "the-charity-run",
)

ITEMS: dict[str, Item] = {
    # Lesson 1
    "vocab.documentary": (
        V,
        "documentary",
        "🎬",
        "документальный фильм",
        L1,
        ["We're making a documentary about the river."],
        None,
    ),
    "vocab.footage": (
        V,
        "footage",
        "📹",
        "отснятый материал",
        L1,
        ["The footage of the otters was incredible."],
        None,
    ),
    "vocab.director": (
        V,
        "director",
        "🎥",
        "режиссёр",
        L1,
        ["{boy} was the director of the film."],
        None,
    ),
    "vocab.edit": (
        V,
        "edit",
        "✂️",
        "монтировать, редактировать",
        L1,
        ["It took weeks to edit the film."],
        None,
    ),
    "vocab.wildlife": (
        V,
        "wildlife",
        "🦦",
        "дикая природа",
        L1,
        ["The river is full of wildlife."],
        None,
    ),
    "vocab.crew": (
        V,
        "crew",
        "👥",
        "съёмочная группа, команда",
        L1,
        ["The crew had been waiting since dawn."],
        None,
    ),
    "grammar.narrative_tenses": (
        G,
        "had done / had been doing / was doing / did",
        None,
        "Повествовательные времена для эффекта",
        L1,
        [
            "We had been waiting for hours when the otter finally appeared.",
            "By the time we arrived, the sun had set.",
        ],
        "Past simple moves the story on; past continuous sets the scene; past perfect (continuous) goes further back.",
    ),
    # Lesson 2
    "vocab.source": (V, "source", "📚", "источник", L2, ["Always check your sources."], None),
    "vocab.reliable": (
        V,
        "reliable",
        "✅",
        "надёжный, достоверный",
        L2,
        ["Is this website reliable?"],
        None,
    ),
    "vocab.misleading": (
        V,
        "misleading",
        "🌀",
        "вводящий в заблуждение",
        L2,
        ["The headline was misleading."],
        None,
    ),
    "vocab.claim": (
        V,
        "claim",
        "📣",
        "утверждение; утверждать",
        L2,
        ["The article claims that chocolate cures colds."],
        None,
    ),
    "vocab.verify": (
        V,
        "verify",
        "🔍",
        "проверять, подтверждать",
        L2,
        ["Journalists must verify the facts."],
        None,
    ),
    "vocab.bias": (V, "bias", "⚖️", "предвзятость", L2, ["The report shows a clear bias."], None),
    "grammar.hedging": (
        G,
        "It seems that … / appears to … / is likely to …",
        None,
        "Осторожные формулировки (хеджирование)",
        L2,
        [
            "It seems that the photo has been edited.",
            "The story appears to be false.",
            "This is likely to be an advert.",
        ],
        "Hedging makes a claim less certain: seem / appear, may / might, tend to, be likely to, it is possible that.",
    ),
    # Lesson 3
    "vocab.sustainable": (
        V,
        "sustainable",
        "🌿",
        "устойчивый, экологичный",
        L3,
        ["We need a more sustainable lifestyle."],
        None,
    ),
    "vocab.waste": (
        V,
        "waste",
        "🚮",
        "отходы; тратить впустую",
        L3,
        ["The canteen produces a lot of food waste."],
        None,
    ),
    "vocab.renewable": (
        V,
        "renewable energy",
        "🌬️",
        "возобновляемая энергия",
        L3,
        ["Wind is a renewable energy source."],
        None,
    ),
    "vocab.carbon_footprint": (
        V,
        "carbon footprint",
        "👣",
        "углеродный след",
        L3,
        ["Flying increases your carbon footprint."],
        None,
    ),
    "vocab.campaign": (
        V,
        "campaign",
        "📢",
        "кампания",
        L3,
        ["The students started a campaign."],
        None,
    ),
    "vocab.reduce": (V, "reduce", "📉", "сокращать", L3, ["We reduced plastic by half."], None),
    "grammar.cleft_sentences": (
        G,
        "It was … that … / What … is …",
        None,
        "Выделительные конструкции (cleft sentences)",
        L3,
        [
            "It was the canteen that produced the most waste.",
            "What surprised us was the amount of plastic.",
        ],
        "Cleft sentences put emphasis on one part: It is/was + focus + that/who …; What + clause + is/was + focus.",
    ),
    # Lesson 4
    "vocab.plot": (V, "plot", "🗺️", "сюжет", L4, ["The plot has a surprising twist."], None),
    "vocab.character": (
        V,
        "character",
        "🧚",
        "персонаж",
        L4,
        ["The main character is a brave fox."],
        None,
    ),
    "vocab.setting": (
        V,
        "setting",
        "🏞️",
        "место и время действия",
        L4,
        ["The setting is a forest in winter."],
        None,
    ),
    "vocab.twist": (
        V,
        "twist",
        "🔀",
        "неожиданный поворот",
        L4,
        ["Nobody expected the twist at the end."],
        None,
    ),
    "vocab.draft": (V, "draft", "📝", "черновик", L4, ["This is only my first draft."], None),
    "vocab.imagination": (
        V,
        "imagination",
        "🌈",
        "воображение",
        L4,
        ["{little} has a wonderful imagination."],
        None,
    ),
    "grammar.mixed_conditionals": (
        G,
        "If I had …, I would be … / If I were …, I would have …",
        None,
        "Смешанные условные предложения",
        L4,
        [
            "If she hadn't read so much, she wouldn't be such a good writer now.",
            "If I were braver, I would have entered the competition.",
        ],
        "Mix the times: a past condition with a present result, or a present situation with a past result.",
    ),
    # Lesson 5
    "vocab.charity": (
        V,
        "charity",
        "🎗️",
        "благотворительная организация",
        L5,
        ["We ran for a children's charity."],
        None,
    ),
    "vocab.donate": (V, "donate", "💝", "жертвовать", L5, ["Hundreds of people donated."], None),
    "vocab.sponsor": (
        V,
        "sponsor",
        "🤝",
        "спонсировать; спонсор",
        L5,
        ["Granny sponsored me £10 a kilometre!"],
        None,
    ),
    "vocab.raise_money": (
        V,
        "raise money",
        "💷",
        "собирать деньги",
        L5,
        ["We raised money for the hospital."],
        None,
    ),
    "vocab.cause": (
        V,
        "cause",
        "❤️",
        "дело, цель (благое)",
        L5,
        ["It's a really good cause."],
        None,
    ),
    "vocab.exhausted": (
        V,
        "exhausted",
        "🥵",
        "измученный, обессиленный",
        L5,
        ["I was exhausted after the race."],
        None,
    ),
    "grammar.inversion": (
        G,
        "Never have I … / Not only did we … / Rarely …",
        None,
        "Инверсия после отрицательных наречий",
        L5,
        ["Never have I felt so tired!", "Not only did we finish, but we also raised £2,000."],
        "After negative or limiting adverbials at the start (Never, Rarely, Not only, Little, No sooner), use question word order.",
    ),
}


LESSON_1 = {
    "slug": L1,
    "title": "The Documentary",
    "description": "{boy}'s film crew waits all night by the river. Had the otters really come back?",
    "minutes": 40,
    "objectives": [
        "Use film vocabulary: documentary, footage, director, crew, edit, wildlife.",
        "Combine narrative tenses to tell a story with tension.",
        "Use the past perfect continuous to show a long earlier action.",
    ],
    "review": [
        "grammar.linking_arguments",
        "phrase.agree_disagree",
        "vocab.evidence",
        "grammar.articles",
        "grammar.third_conditional",
        "grammar.past_continuous",
        "grammar.when_while",
        "grammar.present_perfect_continuous",
        "vocab.environment",
        "vocab.camera",
    ],
    "episode": (
        "Night of the Otters",
        "{boy} directs a short documentary for a national competition. The star of the film refuses to appear.",
    ),
    "content": {
        "story_intro": "{boy} is sixteen now. With three friends he is making a wildlife documentary for a national competition.",
        "reading": {
            "title": "Waiting for the Otters",
            "paragraphs": [
                {
                    "sentences": [
                        "For years nobody had seen an otter in our river. Then, last spring, a fisherman told us he had spotted one near the old mill.",
                        "We decided that this would be the subject of our documentary.",
                    ]
                },
                {
                    "sentences": [
                        "On the first night the crew arrived at the river at nine. It was freezing, and a thin mist was rising from the water.",
                        "We had been waiting for over four hours, and Sam was starting to fall asleep, when we heard a splash.",
                    ]
                },
                {
                    "sentences": [
                        "I switched on the camera. Something dark was moving across the water — but it was only a duck.",
                        "By the time we packed up, the sun had already risen, and we hadn't filmed a single otter.",
                    ]
                },
                {
                    "sentences": [
                        "Five nights later our luck changed. Two otters had been playing on the bank for several minutes before we even noticed them.",
                        "The footage we got that night was better than anything we had planned.",
                    ]
                },
                {
                    "sentences": [
                        "Editing the film took three weeks. As the director, I had to cut hours of footage down to ten minutes.",
                        "When we finally watched it on the big screen, I realised the waiting had been worth every cold minute.",
                    ]
                },
            ],
            "highlight": [
                "had seen",
                "had spotted",
                "had been waiting",
                "was starting",
                "was moving",
                "had already risen",
                "had been playing",
                "footage",
                "crew",
                "director",
                "Editing",
            ],
        },
        "listening": [
            {
                "id": "c1-1-interview",
                "title": "An interview with the director",
                "transcript": [
                    {
                        "speaker": "Presenter",
                        "text": "So, {boy}, what was the hardest part of making the film?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "Honestly, the waiting. We'd been sitting by the river for five nights before we saw anything.",
                    },
                    {
                        "speaker": "Presenter",
                        "text": "And how did you feel when the otters finally appeared?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "I was shaking. I'd dreamed about that moment for weeks, and suddenly it was happening.",
                    },
                ],
            },
            {
                "id": "c1-1-edit",
                "title": "In the editing room",
                "transcript": [
                    {
                        "speaker": "Maya",
                        "text": "Why did you cut the scene with the duck? It was funny.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "It was funny, but it slowed everything down. The audience had already been waiting too long.",
                    },
                    {
                        "speaker": "Maya",
                        "text": "Fair enough. But keep the shot of the mist — it sets the scene perfectly.",
                    },
                    {"speaker": "{boy}", "text": "Agreed. That's where the story really begins."},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Narrative tenses",
                "explanation": (
                    "Good stories mix past tenses. Past simple moves the main events forward: I switched on the camera. "
                    "Past continuous sets the scene or describes an action in progress: A mist was rising from the water. "
                    "Past perfect goes back to an earlier moment: Nobody had seen an otter for years. "
                    "Past perfect continuous stresses the duration of an earlier activity: We had been waiting for four hours when we heard a splash."
                ),
                "explanation_ru": (
                    "В рассказе: past simple — основные события; past continuous — фон; "
                    "past perfect — то, что случилось раньше; past perfect continuous — как долго что-то длилось до момента в прошлом."
                ),
                "examples": [
                    "By the time we arrived, the otters had gone.",
                    "It had been raining all day, and the path was muddy.",
                    "While we were filming, a fox walked past.",
                ],
            },
            {
                "title": "Narrative tenses for effect",
                "explanation": (
                    "Writers use the past perfect continuous and time expressions to build tension: "
                    "We had been waiting for hours. Then, suddenly, … "
                    "Useful linkers: by the time, as soon as, no sooner … than, just as, it was only when …"
                ),
                "explanation_ru": "Чтобы создать напряжение, сочетают длительные времена с резкими короткими событиями: Then, suddenly …",
                "examples": [
                    "Just as we were leaving, the otter appeared.",
                    "It was only when I watched the footage that I saw the second otter.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "film-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("documentary", None, "🎬"),
                ("footage", None, "📹"),
                ("wildlife", None, "🦦"),
                ("edit", None, "✂️"),
            ],
            ["vocab.documentary", "vocab.footage", "vocab.wildlife", "vocab.edit"],
            "Footage = what you have filmed.",
            "documentary 🎬, footage 📹, wildlife 🦦, edit ✂️.",
        ),
        matching(
            "film-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("director", "the person who controls how a film is made", None),
                ("crew", "a group of people who work together on a film", None),
                ("footage", "film that has been recorded", None),
            ],
            ["vocab.director", "vocab.crew", "vocab.footage"],
            "The director gives instructions to the crew.",
            "director = controls the film; crew = the team; footage = recorded film.",
        ),
        choice(
            "find-wildlife",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: an example of wildlife",
            [(None, "🦦"), (None, "🎥"), (None, "🏙️")],
            "a",
            ["vocab.wildlife"],
            "Wild animals living in nature.",
            "🦦 an otter is wildlife.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-narrative",
            "LISTENING",
            "Listen. Why was the camerawoman so tired?",
            "She was tired because …",
            [
                ("she had been filming since five in the morning", "⏰"),
                ("she had run to catch the bus", "🏃"),
                ("she was ill", "🤒"),
            ],
            "a",
            ["grammar.narrative_tenses", "vocab.crew"],
            "Listen for 'had been'.",
            "She had been filming since five in the morning.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="By the time the sun set, our camerawoman was exhausted. She had been filming since five in the morning without a break.",
        ),
        true_false(
            "listen-five-nights",
            "LISTENING",
            "Listen to the interview. True or false?",
            "The crew saw the otters on the first night.",
            False,
            ["grammar.narrative_tenses"],
            "How long had they been sitting there?",
            "They'd been sitting by the river for five nights before they saw anything.",
            listening_id="c1-1-interview",
        ),
        true_false(
            "listen-mist-shot",
            "LISTENING",
            "Listen to Maya and {boy}. True or false?",
            "Maya thinks the shot of the mist should stay in the film.",
            True,
            ["vocab.edit", "vocab.director"],
            "Listen to Maya's second line.",
            "Keep the shot of the mist — it sets the scene perfectly.",
            listening_id="c1-1-edit",
        ),
        blank(
            "narrative-blank",
            "GRAMMAR",
            "Choose the best tenses.",
            "We ___ been waiting for hours when we finally ___ a splash.",
            ["had", "heard"],
            ["had", "have", "heard", "were hearing"],
            ["grammar.narrative_tenses"],
            "A long earlier action + a short event.",
            "We had been waiting for hours when we finally heard a splash.",
        ),
        blank(
            "by-the-time-blank",
            "GRAMMAR",
            "Choose the best tense.",
            "By the time we packed up, the sun ___ already risen.",
            ["had"],
            ["had", "has", "was"],
            ["grammar.narrative_tenses"],
            "The sun rose before we packed up.",
            "By the time we packed up, the sun had already risen.",
        ),
        choice(
            "scene-setting",
            "GRAMMAR",
            "Which sentence best sets the scene at the start of a story?",
            "Choose one.",
            [
                ("A thin mist was rising from the water, and an owl was calling somewhere.", None),
                ("A thin mist rose from the water and then we went home.", None),
                ("A thin mist has risen from the water.", None),
            ],
            "a",
            ["grammar.narrative_tenses"],
            "Background actions → past continuous.",
            "Past continuous describes the background: A thin mist was rising …",
        ),
        choice(
            "ppc-meaning",
            "GRAMMAR",
            "What does the sentence tell us?",
            "The otters had been playing on the bank for several minutes before we noticed them.",
            [
                ("The otters were playing for some time before we saw them.", None),
                ("We saw the otters, and then they started playing.", None),
                ("The otters played after we left.", None),
            ],
            "a",
            ["grammar.narrative_tenses"],
            "had been + -ing = an activity in progress before another past moment.",
            "They were already playing for several minutes before we noticed.",
        ),
        build(
            "build-narrative",
            "GRAMMAR",
            "Put the words in order.",
            "Just as we were leaving, the otter appeared.",
            ["grammar.narrative_tenses"],
            "Start with 'Just as'.",
            "Just as we were leaving, the otter appeared.",
        ),
        order(
            "read-order",
            "READING",
            "Put the events of the story in order.",
            [
                "A fisherman spotted an otter near the old mill.",
                "The crew waited by the river all night.",
                "They filmed a duck by mistake.",
                "Two otters appeared on the bank.",
                "{boy} edited the footage down to ten minutes.",
            ],
            ["vocab.footage", "vocab.crew", "grammar.narrative_tenses"],
            "The editing happens at the end.",
            "Fisherman → waiting → duck → otters → editing.",
        ),
        choice(
            "read-worth",
            "READING",
            "Read the text. Then answer.",
            "How did {boy} feel when he watched the finished film?",
            [
                ("He felt that the long wait had been worth it.", "🎬"),
                ("He regretted cutting the duck scene.", "🦆"),
                ("He thought the film was too short.", "⏱️"),
            ],
            "a",
            ["vocab.documentary"],
            "Look at the last sentence.",
            "The waiting had been worth every cold minute.",
            ex_type="READING_COMPREHENSION",
        ),
        speak(
            "say-story",
            "Tell the story of a moment when you had been waiting for something for a long time. Use at least three different past tenses.",
            "I had been … for … It was … and … was … Suddenly … By the time …",
            "I had been waiting for my exam results all summer. It was a hot morning and my phone was buzzing. Suddenly the email arrived. By the time I opened it, my hands were shaking.",
            ["grammar.narrative_tenses"],
        ),
        choice(
            "quiz-linking-film",
            "QUIZ",
            "Choose the best linker.",
            "The film was expensive to make. ___, it won two prizes.",
            [("On the other hand", None), ("Firstly", None), ("To sum up", None)],
            "a",
            ["grammar.linking_arguments"],
            "Remember B2: contrast.",
            "On the other hand, it won two prizes.",
        ),
        blank(
            "quiz-third-film",
            "QUIZ",
            "Complete the sentence.",
            "If we hadn't waited so long, we wouldn't ___ ___ the otters.",
            ["have", "filmed"],
            ["have", "had", "filmed", "film"],
            ["grammar.third_conditional"],
            "Remember B2: would have + past participle.",
            "If we hadn't waited so long, we wouldn't have filmed the otters.",
        ),
        choice(
            "quiz-article-otter",
            "QUIZ",
            "Choose the right articles.",
            "We saw ___ otter last night. ___ otter was eating a fish.",
            [("an … The", None), ("a … An", None), ("the … A", None)],
            "a",
            ["grammar.articles"],
            "Remember B2: first mention, then second mention. otter starts with a vowel sound.",
            "We saw an otter. The otter was eating a fish.",
        ),
    ],
}

LESSON_2 = {
    "slug": L2,
    "title": "Fact or Fake?",
    "description": "A viral photo shows a shark on a motorway. Is it real? {boy}'s class learns to check — and to hedge.",
    "minutes": 40,
    "objectives": [
        "Use media literacy vocabulary: source, reliable, misleading, claim, verify, bias.",
        "Use hedging to make careful claims: It seems that …, appears to …, is likely to ….",
        "Evaluate how reliable a news story is.",
    ],
    "review": [
        "grammar.narrative_tenses",
        "vocab.footage",
        "vocab.edit",
        "grammar.reported_speech",
        "grammar.passive_all",
        "grammar.indirect_questions",
        "vocab.journalist",
        "vocab.headline",
        "vocab.evidence",
        "vocab.opinion",
    ],
    "episode": (
        "The Shark on the Motorway",
        "A shocking photo goes viral at school. {boy} and Maya investigate where it really came from.",
    ),
    "content": {
        "story_intro": "On Monday morning everybody at school was sharing the same photo: a shark swimming on a flooded motorway.",
        "reading": {
            "title": "Fact or Fake?",
            "paragraphs": [
                {
                    "sentences": [
                        "The photo appeared to show a shark swimming along a flooded motorway after a storm.",
                        "By lunchtime it had been shared thousands of times, and a news website claimed it was genuine.",
                    ]
                },
                {
                    "sentences": [
                        "Our media teacher, Ms Okafor, asked us to verify it before we believed it.",
                        "First, we looked for the original source. It seems that the same shark had appeared in several other 'floods' over the last ten years!",
                    ]
                },
                {
                    "sentences": [
                        "A reverse image search suggested that the shark had been copied from a diving photo and edited into the picture.",
                        "In other words, the image is very likely to be fake.",
                    ]
                },
                {
                    "sentences": [
                        "Ms Okafor explained that misleading stories tend to spread faster than true ones, because they make us feel strong emotions.",
                        "She also warned us about bias: we may be more likely to believe stories that match what we already think.",
                    ]
                },
                {
                    "sentences": [
                        "We wrote a short report. Instead of saying 'This is 100% fake', we said: 'The evidence suggests that the photo has been manipulated.'",
                        "Ms Okafor said that was exactly how a reliable journalist should write.",
                    ]
                },
            ],
            "highlight": [
                "appeared to",
                "It seems that",
                "suggested that",
                "is very likely to",
                "tend to",
                "may be more likely to",
                "The evidence suggests",
                "source",
                "verify",
                "misleading",
                "bias",
                "reliable",
                "claimed",
            ],
        },
        "listening": [
            {
                "id": "c1-2-radio",
                "title": "A radio report",
                "transcript": [
                    {
                        "speaker": "Reporter",
                        "text": "A new study appears to show that teenagers are reading more books than ten years ago.",
                    },
                    {
                        "speaker": "Reporter",
                        "text": "However, the researchers point out that the sample was relatively small.",
                    },
                    {
                        "speaker": "Reporter",
                        "text": "It is possible that the results would be different in other countries.",
                    },
                ],
            },
            {
                "id": "c1-2-check",
                "title": "Checking a claim",
                "transcript": [
                    {
                        "speaker": "Maya",
                        "text": "This website says chocolate makes you smarter. Should I put it in my essay?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "Who wrote it? It seems to be a chocolate company's blog.",
                    },
                    {
                        "speaker": "Maya",
                        "text": "Oh. So it's probably not the most reliable source.",
                    },
                    {"speaker": "{boy}", "text": "Exactly. Let's look for a proper study instead."},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Hedging: making careful claims",
                "explanation": (
                    "In academic and media writing we often avoid sounding 100% certain. "
                    "Verbs: seem / appear (+ to + verb): The story appears to be false. It seems that … "
                    "Modals: may, might, could: This may be an advert. "
                    "Adjectives and adverbs: likely / unlikely, probably, possibly: It is likely to be fake. "
                    "Other phrases: tend to, suggest, indicate: Misleading stories tend to spread faster. The evidence suggests that …"
                ),
                "explanation_ru": (
                    "Хеджирование — осторожные формулировки, чтобы не звучать слишком категорично: "
                    "seems to, appears to, is likely to, may, tend to, the evidence suggests."
                ),
                "examples": [
                    "It appears that the photo was edited.",
                    "The results seem to suggest a link.",
                    "This is unlikely to be true.",
                    "People tend to share shocking news.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "media-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("source", None, "📚"),
                ("reliable", None, "✅"),
                ("verify", None, "🔍"),
                ("claim", None, "📣"),
            ],
            ["vocab.source", "vocab.reliable", "vocab.verify", "vocab.claim"],
            "You verify facts with a magnifying glass — in theory!",
            "source 📚, reliable ✅, verify 🔍, claim 📣.",
        ),
        matching(
            "media-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("misleading", "giving the wrong idea or impression", None),
                ("bias", "an unfair preference for one side", None),
                ("verify", "check that something is true", None),
            ],
            ["vocab.misleading", "vocab.bias", "vocab.verify"],
            "A misleading headline makes you believe something false.",
            "misleading = gives a wrong impression; bias = unfair preference; verify = check it is true.",
        ),
        choice(
            "find-verify",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: verify",
            [(None, "📣"), (None, "🔍"), (None, "🌀")],
            "b",
            ["vocab.verify"],
            "Look closely to check.",
            "🔍 verify.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-hedge",
            "LISTENING",
            "Listen. How certain is the scientist?",
            "The scientist …",
            [
                ("thinks it is probably true but isn't completely sure", "🤔"),
                ("is completely sure it is true", "💯"),
                ("is sure it is false", "❌"),
            ],
            "a",
            ["grammar.hedging"],
            "Listen for 'seems' and 'likely'.",
            "It seems likely … but we can't be certain yet.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="It seems likely that the bird uses the Earth's magnetic field to navigate, but we can't be certain yet. More research is needed.",
        ),
        true_false(
            "listen-sample",
            "LISTENING",
            "Listen to the radio report. True or false?",
            "The reporter says the study proves that all teenagers read more.",
            False,
            ["grammar.hedging", "vocab.claim"],
            "What do the researchers point out?",
            "The study only 'appears to show' this, and the sample was small.",
            listening_id="c1-2-radio",
        ),
        true_false(
            "listen-chocolate-blog",
            "LISTENING",
            "Listen to Maya and {boy}. True or false?",
            "The claim about chocolate comes from a chocolate company's blog.",
            True,
            ["vocab.source", "vocab.reliable"],
            "Who wrote it?",
            "It seems to be a chocolate company's blog — not a reliable source.",
            listening_id="c1-2-check",
        ),
        blank(
            "hedge-blank",
            "GRAMMAR",
            "Complete the hedged sentences.",
            "The photo appears ___ have been edited. It is ___ to be a fake.",
            ["to", "likely"],
            ["to", "that", "likely", "sure"],
            ["grammar.hedging"],
            "appear + to; be likely + to.",
            "The photo appears to have been edited. It is likely to be a fake.",
        ),
        choice(
            "most-careful",
            "GRAMMAR",
            "Which sentence is the most careful (hedged)?",
            "Report the results of a small study.",
            [
                ("The results suggest that sleep may improve memory.", None),
                ("The results prove that sleep improves memory.", None),
                ("Sleep improves memory. Everyone knows that.", None),
            ],
            "a",
            ["grammar.hedging", "vocab.evidence"],
            "Look for suggest and may.",
            "The results suggest that sleep may improve memory.",
        ),
        choice(
            "tend-to",
            "GRAMMAR",
            "Choose the correct sentence.",
            "Talk about a general pattern.",
            [
                ("People tend to share shocking stories quickly.", None),
                ("People tend sharing shocking stories quickly.", None),
                ("People are tend to share shocking stories quickly.", None),
            ],
            "a",
            ["grammar.hedging"],
            "tend + to + verb.",
            "People tend to share shocking stories quickly.",
        ),
        blank(
            "seems-blank",
            "GRAMMAR",
            "Complete the sentence.",
            "It ___ that the same shark has appeared in many 'floods'.",
            ["seems"],
            ["seems", "is seeming", "seem"],
            ["grammar.hedging"],
            "It seems that + clause.",
            "It seems that the same shark has appeared in many 'floods'.",
        ),
        build(
            "build-hedge",
            "GRAMMAR",
            "Put the words in order.",
            "The evidence suggests that the photo is fake.",
            ["grammar.hedging", "vocab.evidence"],
            "Start with 'The evidence suggests'.",
            "The evidence suggests that the photo is fake.",
        ),
        choice(
            "read-why-fast",
            "READING",
            "Read the text. Then answer.",
            "Why do misleading stories spread faster, according to Ms Okafor?",
            [
                ("They make us feel strong emotions.", "😱"),
                ("They are written by professionals.", "🧑‍💼"),
                ("They are always shorter.", "✂️"),
            ],
            "a",
            ["vocab.misleading"],
            "Look at paragraph 4.",
            "They make us feel strong emotions.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-report",
            "READING",
            "Read the text. True or false?",
            "The students wrote that the photo was '100% fake'.",
            False,
            ["grammar.hedging", "vocab.reliable"],
            "Look at the last paragraph.",
            "They wrote: 'The evidence suggests that the photo has been manipulated.'",
        ),
        speak(
            "say-evaluate",
            "Someone shares a news story claiming that a new app can make you fluent in English in one week. Explain, using hedging, why you are not sure it's true and how you would check it.",
            "It seems that … The claim appears to … It's unlikely that … I would check the source by …",
            "It seems that the story comes from the app's own website, so it may be biased. It's unlikely that anyone can become fluent in a week. I would check the source and look for independent reviews.",
            ["grammar.hedging", "vocab.source", "vocab.verify"],
        ),
        choice(
            "quiz-had-been-shared",
            "QUIZ",
            "Choose the best tense.",
            "By lunchtime the photo ___ thousands of times.",
            [("had been shared", None), ("has shared", None), ("was sharing", None)],
            "a",
            ["grammar.narrative_tenses", "grammar.passive_all"],
            "Remember Lesson 1: before a past moment, passive.",
            "By lunchtime the photo had been shared thousands of times.",
        ),
        choice(
            "quiz-reported-claim",
            "QUIZ",
            "Report the statement.",
            "The website: 'The photo is genuine.'",
            [
                ("The website claimed that the photo was genuine.", None),
                ("The website claimed that the photo is being genuine.", None),
                ("The website told that the photo was genuine.", None),
            ],
            "a",
            ["grammar.reported_speech", "vocab.claim"],
            "Remember B1: is → was.",
            "The website claimed that the photo was genuine.",
        ),
        choice(
            "quiz-indirect-source",
            "QUIZ",
            "Choose the correct indirect question.",
            "Where did the photo come from?",
            [
                ("Do you know where the photo came from?", None),
                ("Do you know where did the photo come from?", None),
                ("Do you know where came the photo from?", None),
            ],
            "a",
            ["grammar.indirect_questions", "vocab.source"],
            "Remember B2: no did, normal word order.",
            "Do you know where the photo came from?",
        ),
    ],
}

LESSON_3 = {
    "slug": L3,
    "title": "The Eco Project",
    "description": "The school wants to cut its waste. What really made the difference? Cleft sentences put the focus where it belongs.",
    "minutes": 40,
    "objectives": [
        "Use sustainability vocabulary: sustainable, waste, renewable energy, carbon footprint, campaign, reduce.",
        "Emphasise information with It is/was … that … .",
        "Emphasise information with What … is/was … .",
    ],
    "review": [
        "grammar.hedging",
        "vocab.claim",
        "vocab.reliable",
        "grammar.narrative_tenses",
        "grammar.passive_all",
        "grammar.contrast_linkers",
        "grammar.should",
        "vocab.recycle",
        "vocab.rubbish",
        "vocab.climate",
    ],
    "episode": (
        "Zero Waste Week",
        "{boy}'s eco team measures how much rubbish the school throws away — and the results shock everyone.",
    ),
    "content": {
        "story_intro": "The school has asked students to plan a campaign that will make the school more sustainable.",
        "reading": {
            "title": "How We Halved Our Waste",
            "paragraphs": [
                {
                    "sentences": [
                        "When our eco team started, we assumed it was plastic bottles that caused the most waste.",
                        "We were wrong. What we discovered after a week of weighing the bins was far more surprising.",
                    ]
                },
                {
                    "sentences": [
                        "It was food from the canteen that filled most of the bins — around forty kilograms a day.",
                        "What shocked us most was that much of it hadn't even been touched.",
                    ]
                },
                {
                    "sentences": [
                        "So we launched a campaign called 'Take What You'll Eat'. The canteen started offering smaller portions, and students could come back for more.",
                        "We also persuaded the head teacher to install solar panels, which reduced the school's carbon footprint.",
                    ]
                },
                {
                    "sentences": [
                        "After three months, our food waste had fallen by more than half.",
                        "It wasn't the posters that made the difference, though. It was the conversations in the lunch queue.",
                    ]
                },
                {
                    "sentences": [
                        "What I've learned is that sustainable change doesn't need to be dramatic.",
                        "It's the small daily habits that matter most.",
                    ]
                },
            ],
            "highlight": [
                "it was plastic bottles that",
                "What we discovered",
                "It was food from the canteen that",
                "What shocked us most was",
                "It wasn't the posters that",
                "What I've learned is",
                "It's the small daily habits that",
                "campaign",
                "carbon footprint",
                "sustainable",
                "waste",
            ],
        },
        "listening": [
            {
                "id": "c1-3-head",
                "title": "Meeting the head teacher",
                "transcript": [
                    {
                        "speaker": "Head teacher",
                        "text": "So, what do you think is the biggest problem?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "What surprised us was the canteen. It's food, not plastic, that makes up most of our waste.",
                    },
                    {
                        "speaker": "Head teacher",
                        "text": "Interesting. And what do you need from me?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "What we'd really like is permission to change the portion sizes for a month.",
                    },
                ],
            },
            {
                "id": "c1-3-energy",
                "title": "Solar panels",
                "transcript": [
                    {"speaker": "Maya", "text": "Did the solar panels make a big difference?"},
                    {
                        "speaker": "{boy}",
                        "text": "They did. The school now gets about a third of its electricity from renewable energy.",
                    },
                    {"speaker": "Maya", "text": "That's impressive. Was it your idea?"},
                    {
                        "speaker": "{boy}",
                        "text": "No — it was Sam who found the government grant. He deserves the credit.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Cleft sentences: It is / was … that / who …",
                "explanation": (
                    "Use a cleft sentence to put emphasis on one piece of information, often to correct someone. "
                    "Neutral: Food caused most of the waste. "
                    "Cleft: It was food that caused most of the waste (not plastic). "
                    "Use who for people: It was Sam who found the grant."
                ),
                "explanation_ru": (
                    "Выделительная конструкция It is/was … that … подчёркивает одну часть: "
                    "It was Sam who found the grant = Именно Сэм нашёл грант."
                ),
                "examples": [
                    "It's the small habits that matter.",
                    "It was in March that the campaign started.",
                    "It wasn't me who broke it!",
                ],
            },
            {
                "title": "Cleft sentences: What … is / was …",
                "explanation": (
                    "A What-clause builds up to the important information at the end. "
                    "Neutral: The amount of food surprised us. "
                    "Cleft: What surprised us was the amount of food. "
                    "Also: What I need is … / What we did was (to) + verb: What we did was weigh the bins."
                ),
                "explanation_ru": "What … is/was … — «То, что …, — это …»: What surprised us was the food = Что нас удивило, так это еда.",
                "examples": [
                    "What I love about this project is the teamwork.",
                    "What we did was talk to every class.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "eco-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("renewable energy", None, "🌬️"),
                ("carbon footprint", None, "👣"),
                ("campaign", None, "📢"),
                ("reduce", None, "📉"),
            ],
            ["vocab.renewable", "vocab.carbon_footprint", "vocab.campaign", "vocab.reduce"],
            "Wind turbines produce renewable energy.",
            "renewable energy 🌬️, carbon footprint 👣, campaign 📢, reduce 📉.",
        ),
        matching(
            "eco-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("sustainable", "able to continue without harming the environment", None),
                ("carbon footprint", "the amount of CO₂ caused by a person or organisation", None),
                ("campaign", "organised actions to achieve a goal", None),
            ],
            ["vocab.sustainable", "vocab.carbon_footprint", "vocab.campaign"],
            "Flying increases your carbon footprint.",
            "sustainable = can continue without harm; carbon footprint = CO₂ you cause; campaign = organised actions.",
        ),
        choice(
            "find-waste",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: waste",
            [(None, "🌬️"), (None, "🚮"), (None, "📢")],
            "b",
            ["vocab.waste"],
            "Things that are thrown away.",
            "🚮 waste.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-cleft",
            "LISTENING",
            "Listen. What made the biggest difference, according to the speaker?",
            "The biggest difference came from …",
            [("changing the lights", "💡"), ("the new bins", "🗑️"), ("the posters", "📰")],
            "a",
            ["grammar.cleft_sentences", "vocab.reduce"],
            "Listen for 'It was … that …'.",
            "It was changing the lights that made the biggest difference.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Everyone thinks the new bins reduced our energy bill. Actually, it was changing the lights that made the biggest difference.",
        ),
        true_false(
            "listen-plastic",
            "LISTENING",
            "Listen to the head teacher and {boy}. True or false?",
            "{boy} says plastic makes up most of the school's waste.",
            False,
            ["grammar.cleft_sentences", "vocab.waste"],
            "Food or plastic?",
            "It's food, not plastic, that makes up most of our waste.",
            listening_id="c1-3-head",
        ),
        true_false(
            "listen-sam-grant",
            "LISTENING",
            "Listen to Maya and {boy}. True or false?",
            "It was Sam who found the money for the solar panels.",
            True,
            ["grammar.cleft_sentences", "vocab.renewable"],
            "Listen to {boy}'s last line.",
            "It was Sam who found the government grant.",
            listening_id="c1-3-energy",
        ),
        blank(
            "it-was-blank",
            "GRAMMAR",
            "Complete the cleft sentences.",
            "It was food ___ filled the bins. It was Sam ___ found the grant.",
            ["that", "who"],
            ["that", "who", "what"],
            ["grammar.cleft_sentences"],
            "Things → that; people → who (or that).",
            "It was food that filled the bins. It was Sam who found the grant.",
        ),
        blank(
            "what-blank",
            "GRAMMAR",
            "Complete the cleft sentence.",
            "___ shocked us most ___ the amount of untouched food.",
            ["What", "was"],
            ["What", "It", "was", "that"],
            ["grammar.cleft_sentences"],
            "What + clause + was + focus.",
            "What shocked us most was the amount of untouched food.",
        ),
        choice(
            "cleft-correct",
            "GRAMMAR",
            "Someone says: 'The posters reduced the waste.' Correct them with emphasis.",
            "Choose the best answer.",
            [
                ("Actually, it was the conversations in the queue that reduced it.", None),
                ("Actually, the conversations reduced it, it was.", None),
                ("Actually, what reduced it the conversations.", None),
            ],
            "a",
            ["grammar.cleft_sentences"],
            "It was + focus + that …",
            "It was the conversations in the queue that reduced it.",
        ),
        choice(
            "what-we-did",
            "GRAMMAR",
            "Which sentence is correct?",
            "Explain your method with emphasis.",
            [
                ("What we did was weigh the bins every day.", None),
                ("What we did it was weigh the bins every day.", None),
                ("That we did was weigh the bins every day.", None),
            ],
            "a",
            ["grammar.cleft_sentences"],
            "What we did was + verb.",
            "What we did was weigh the bins every day.",
        ),
        build(
            "build-cleft",
            "GRAMMAR",
            "Put the words in order.",
            "It's the small daily habits that matter most.",
            ["grammar.cleft_sentences"],
            "Start with 'It's the small'.",
            "It's the small daily habits that matter most.",
        ),
        choice(
            "read-canteen",
            "READING",
            "Read the text. Then answer.",
            "How did the canteen help to reduce food waste?",
            [
                ("It offered smaller portions, and students could come back for more.", "🍽️"),
                ("It stopped serving lunch on Fridays.", "🚫"),
                ("It banned plastic bottles.", "🧴"),
            ],
            "a",
            ["vocab.waste", "vocab.reduce"],
            "Look at paragraph 3.",
            "Smaller portions; students could come back for more.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-halved",
            "READING",
            "Read the text. True or false?",
            "After three months the food waste had fallen by more than half.",
            True,
            ["vocab.reduce", "vocab.waste"],
            "Look at paragraph 4.",
            "Our food waste had fallen by more than half.",
        ),
        speak(
            "say-cleft",
            "Talk about an environmental problem in your town or school. Use at least two cleft sentences to emphasise the main cause and the best solution.",
            "What worries me most is … It's … that … What we should do is …",
            "What worries me most is the traffic outside our school. It's the parents' cars that cause most of the pollution. What we should do is create a safe cycling route.",
            ["grammar.cleft_sentences", "vocab.sustainable"],
        ),
        choice(
            "quiz-hedge-results",
            "QUIZ",
            "Choose the most careful sentence.",
            "Report your eco team's findings.",
            [
                ("Our data suggests that smaller portions may reduce waste.", None),
                ("Our data proves that portions always cause waste.", None),
                ("Smaller portions definitely solve everything.", None),
            ],
            "a",
            ["grammar.hedging"],
            "Remember Lesson 2.",
            "Our data suggests that smaller portions may reduce waste.",
        ),
        choice(
            "quiz-past-perfect-bins",
            "QUIZ",
            "Choose the best tense.",
            "When we opened the bins, we saw that much of the food ___ touched.",
            [("hadn't been", None), ("haven't been", None), ("wasn't being", None)],
            "a",
            ["grammar.narrative_tenses"],
            "Remember Lesson 1: an earlier past.",
            "Much of the food hadn't been touched.",
        ),
        blank(
            "quiz-despite-cost",
            "QUIZ",
            "Choose the right linker.",
            "___ the high cost, the school installed solar panels.",
            ["Despite"],
            ["Despite", "Although", "However"],
            ["grammar.contrast_linkers"],
            "Remember B2: + noun.",
            "Despite the high cost, the school installed solar panels.",
        ),
    ],
}

LESSON_4 = {
    "slug": L4,
    "title": "{little}'s First Story",
    "description": "{little} enters a writing competition. If she hadn't found Granny's old notebook, would she be a writer now?",
    "minutes": 40,
    "objectives": [
        "Use creative writing vocabulary: plot, character, setting, twist, draft, imagination.",
        "Use mixed conditionals (past → present, present → past).",
        "Talk about perspective and voice in a story.",
    ],
    "review": [
        "grammar.cleft_sentences",
        "vocab.campaign",
        "vocab.sustainable",
        "grammar.hedging",
        "grammar.narrative_tenses",
        "grammar.third_conditional",
        "grammar.second_conditional",
        "grammar.wish",
        "vocab.prize",
        "vocab.judge",
    ],
    "episode": (
        "The Fox Who Couldn't Sleep",
        "{little} writes a story for a national competition. Her brother helps her edit it — a little too much.",
    ),
    "content": {
        "story_intro": "{little} is ten now and loves writing. She has entered a national story competition for children.",
        "reading": {
            "title": "A Writer Is Born",
            "paragraphs": [
                {
                    "sentences": [
                        "Last summer {little} found an old notebook in Granny {gran1}'s attic, full of stories Granny had written as a girl.",
                        "If she hadn't found it, she probably wouldn't be so passionate about writing now.",
                    ]
                },
                {
                    "sentences": [
                        "Her competition story is about a fox who can't sleep. The setting is a snowy forest, and the story is told from the fox's point of view.",
                        "The plot seems simple, but there is a clever twist at the end: the fox has been dreaming the whole time.",
                    ]
                },
                {
                    "sentences": [
                        "She wrote four drafts. {boy} offered to help, but he changed so much that it didn't sound like her any more.",
                        "If he were a better listener, he would have noticed that the story needed her voice, not his.",
                    ]
                },
                {
                    "sentences": [
                        "Granny {gran1} gave the best advice: Keep the characters you love, and cut everything else.",
                        "What makes a story special, she said, is the writer's imagination — not perfect grammar.",
                    ]
                },
                {
                    "sentences": [
                        "{little}'s story was shortlisted out of three thousand entries.",
                        "If she had given up after the second draft, she wouldn't be going to the award ceremony next week!",
                    ]
                },
            ],
            "highlight": [
                "If she hadn't found it",
                "wouldn't be",
                "If he were",
                "would have noticed",
                "If she had given up",
                "wouldn't be going",
                "setting",
                "point of view",
                "plot",
                "twist",
                "drafts",
                "characters",
                "imagination",
            ],
        },
        "listening": [
            {
                "id": "c1-4-interview",
                "title": "{little} on the radio",
                "transcript": [
                    {
                        "speaker": "Presenter",
                        "text": "{little}, where did the idea for the sleepless fox come from?",
                    },
                    {
                        "speaker": "{little}",
                        "text": "I couldn't sleep one night, and I imagined who else might be awake in the forest.",
                    },
                    {
                        "speaker": "Presenter",
                        "text": "Do you think you'd be a writer if you hadn't found your granny's notebook?",
                    },
                    {
                        "speaker": "{little}",
                        "text": "Maybe — but I wouldn't be writing about foxes! Granny's stories were full of animals.",
                    },
                ],
            },
            {
                "id": "c1-4-feedback",
                "title": "Granny's feedback",
                "transcript": [
                    {
                        "speaker": "Granny {gran1}",
                        "text": "I love the fox. But the middle of the story is a bit slow.",
                    },
                    {"speaker": "{little}", "text": "Should I cut the part with the owl?"},
                    {
                        "speaker": "Granny {gran1}",
                        "text": "No, keep the owl — he's a wonderful character. Just make that scene shorter.",
                    },
                    {"speaker": "{little}", "text": "OK. I'll write another draft tonight."},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Mixed conditionals",
                "explanation": (
                    "Mixed conditionals connect different times. "
                    "1) Past condition → present result: If + past perfect, would + verb. "
                    "If she hadn't found the notebook, she wouldn't be a writer now. "
                    "2) Present situation → past result: If + past simple, would have + past participle. "
                    "If he were a better listener, he would have noticed the problem. (He isn't a good listener, so he didn't notice.)"
                ),
                "explanation_ru": (
                    "Смешанные условные: прошлое условие → результат сейчас (If I had …, I would be …); "
                    "постоянная ситуация сейчас → результат в прошлом (If I were …, I would have …)."
                ),
                "examples": [
                    "If I had studied harder, I would be at university now.",
                    "If she weren't so talented, she wouldn't have been shortlisted.",
                    "If we had left earlier, we would be there by now.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "story-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("character", None, "🧚"),
                ("setting", None, "🏞️"),
                ("twist", None, "🔀"),
                ("draft", None, "📝"),
            ],
            ["vocab.character", "vocab.setting", "vocab.twist", "vocab.draft"],
            "A twist is a surprising change in the story.",
            "character 🧚, setting 🏞️, twist 🔀, draft 📝.",
        ),
        matching(
            "story-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("plot", "the series of events in a story", None),
                ("setting", "where and when a story happens", None),
                ("draft", "an early version of a piece of writing", None),
            ],
            ["vocab.plot", "vocab.setting", "vocab.draft"],
            "The plot is what happens.",
            "plot = the events; setting = where and when; draft = an early version.",
        ),
        choice(
            "find-imagination",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: imagination",
            [(None, "📝"), (None, "🌈"), (None, "🗺️")],
            "b",
            ["vocab.imagination"],
            "Colourful ideas in your head.",
            "🌈 imagination.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-mixed",
            "LISTENING",
            "Listen. Why is the speaker not living in Paris now?",
            "He isn't living in Paris because …",
            [
                ("he didn't accept a job there years ago", "💼"),
                ("he doesn't like French food", "🥐"),
                ("his family moved to Canada", "🍁"),
            ],
            "a",
            ["grammar.mixed_conditionals"],
            "Listen for 'If I had …, I would be …'.",
            "If I had accepted that job, I would be living in Paris now.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Ten years ago I was offered a job in Paris, but I said no. If I had accepted it, I would be living in Paris now.",
        ),
        true_false(
            "listen-animals",
            "LISTENING",
            "Listen to {little} on the radio. True or false?",
            "{little} says Granny's stories were full of animals.",
            True,
            ["grammar.mixed_conditionals", "vocab.character"],
            "Listen to her last line.",
            "I wouldn't be writing about foxes! Granny's stories were full of animals.",
            listening_id="c1-4-interview",
        ),
        true_false(
            "listen-owl",
            "LISTENING",
            "Listen to Granny and {little}. True or false?",
            "Granny tells {little} to cut the owl from the story.",
            False,
            ["vocab.character", "vocab.draft"],
            "What does Granny say about the owl?",
            "Keep the owl — just make that scene shorter.",
            listening_id="c1-4-feedback",
        ),
        blank(
            "mixed-past-present",
            "GRAMMAR",
            "Complete the mixed conditional (past → present).",
            "If she hadn't ___ the notebook, she wouldn't ___ a writer now.",
            ["found", "be"],
            ["found", "find", "be", "have been"],
            ["grammar.mixed_conditionals"],
            "Past condition (had + V3) → present result (would + verb).",
            "If she hadn't found the notebook, she wouldn't be a writer now.",
        ),
        blank(
            "mixed-present-past",
            "GRAMMAR",
            "Complete the mixed conditional (present → past).",
            "If he ___ a better listener, he would ___ noticed the problem.",
            ["were", "have"],
            ["were", "had been", "have", "be"],
            ["grammar.mixed_conditionals"],
            "Present situation (past simple) → past result (would have + V3).",
            "If he were a better listener, he would have noticed the problem.",
        ),
        choice(
            "mixed-meaning",
            "GRAMMAR",
            "What does the sentence mean?",
            "If I had gone to bed earlier, I wouldn't be so tired now.",
            [
                ("I went to bed late, and I'm tired now.", None),
                ("I went to bed early, and I'm not tired.", None),
                ("I'm going to bed early tonight.", None),
            ],
            "a",
            ["grammar.mixed_conditionals"],
            "Both parts are the opposite of reality.",
            "In reality I went to bed late, so I'm tired now.",
        ),
        choice(
            "which-mixed",
            "GRAMMAR",
            "Which sentence is a correct mixed conditional?",
            "Choose one.",
            [
                ("If we had left earlier, we would be there by now.", None),
                ("If we left earlier, we would have been there by now yesterday.", None),
                ("If we have left earlier, we will be there now.", None),
            ],
            "a",
            ["grammar.mixed_conditionals", "grammar.third_conditional"],
            "Past action → present result.",
            "If we had left earlier, we would be there by now.",
        ),
        build(
            "build-mixed",
            "GRAMMAR",
            "Put the words in order.",
            "If I had studied harder, I would be happier now.",
            ["grammar.mixed_conditionals"],
            "Start with 'If I had'.",
            "If I had studied harder, I would be happier now.",
        ),
        choice(
            "read-twist",
            "READING",
            "Read the text. Then answer.",
            "What is the twist at the end of {little}'s story?",
            [
                ("The fox has been dreaming the whole time.", "💤"),
                ("The fox is really a dog.", "🐕"),
                ("The forest is on another planet.", "🪐"),
            ],
            "a",
            ["vocab.twist", "vocab.plot"],
            "Look at paragraph 2.",
            "The fox has been dreaming the whole time.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-boy-help",
            "READING",
            "Read the text. True or false?",
            "{boy}'s changes made the story sound more like {little}.",
            False,
            ["vocab.draft", "grammar.mixed_conditionals"],
            "Look at paragraph 3.",
            "He changed so much that it didn't sound like her any more.",
        ),
        speak(
            "say-mixed",
            "Think about a decision you made in the past. Say how your life would be different now if you had made a different choice.",
            "If I hadn't …, I wouldn't … now. If I had …, I would be … now.",
            "If I hadn't joined the drama club, I wouldn't have so many friends now. If I had chosen the football team instead, I would be much fitter now.",
            ["grammar.mixed_conditionals"],
        ),
        choice(
            "quiz-cleft-idea",
            "QUIZ",
            "Choose the sentence that emphasises Granny.",
            "Granny gave {little} the best advice.",
            [
                ("It was Granny who gave {little} the best advice.", None),
                ("What Granny gave {little} the best advice.", None),
                ("It was Granny that she gave the best advice.", None),
            ],
            "a",
            ["grammar.cleft_sentences"],
            "Remember Lesson 3.",
            "It was Granny who gave {little} the best advice.",
        ),
        blank(
            "quiz-wish-shorter",
            "QUIZ",
            "Choose the right form.",
            "{boy} wishes he ___ changed so much of her story.",
            ["hadn't"],
            ["hadn't", "didn't", "wouldn't"],
            ["grammar.wish"],
            "Remember B2: a regret about the past.",
            "{boy} wishes he hadn't changed so much of her story.",
        ),
        choice(
            "quiz-seems-shortlist",
            "QUIZ",
            "Choose the best hedged sentence.",
            "You think the judges probably liked the twist.",
            [
                ("The judges seem to have liked the twist.", None),
                ("The judges seem liking the twist.", None),
                ("The judges are seem to like the twist.", None),
            ],
            "a",
            ["grammar.hedging", "vocab.judge"],
            "Remember Lesson 2: seem + to have + V3 for the past.",
            "The judges seem to have liked the twist.",
        ),
    ],
}

LESSON_5 = {
    "slug": L5,
    "title": "The Charity Run",
    "description": "Never had {boy} run so far! The family runs a half marathon for charity. Then a review of the unit.",
    "minutes": 45,
    "objectives": [
        "Use charity vocabulary: charity, donate, sponsor, raise money, cause, exhausted.",
        "Use inversion after negative adverbials for emphasis: Never have I …, Not only did we ….",
        "Persuade people to support a cause, and review Unit 1.",
    ],
    "review": [
        "grammar.mixed_conditionals",
        "vocab.imagination",
        "vocab.draft",
        "grammar.cleft_sentences",
        "grammar.hedging",
        "grammar.narrative_tenses",
        "grammar.linking_arguments",
        "vocab.persuade",
        "vocab.volunteer",
        "vocab.fitness",
    ],
    "episode": (
        "Twenty-One Kilometres",
        "{boy}, {teen} and Dad run a half marathon to raise money for the children's hospital.",
    ),
    "content": {
        "story_intro": "{teen} is home from university for the spring. She, {boy} and Dad have signed up for a charity half marathon.",
        "reading": {
            "title": "Never Have I Been So Tired",
            "paragraphs": [
                {
                    "sentences": [
                        "When the children's hospital asked for volunteers to run the city half marathon, {teen} signed us up immediately.",
                        "Little did I know how hard the training would be.",
                    ]
                },
                {
                    "sentences": [
                        "For three months we ran four times a week. Not only did we have to run in the rain, but we also had to get up at six on Sundays.",
                        "Rarely have I complained so much — ask Mum!",
                    ]
                },
                {
                    "sentences": [
                        "We asked friends and family to sponsor us. Granny {gran2} promised to donate a pound for every kilometre, and then doubled it.",
                        "Not until the night before the race did we check the total: we had raised over three thousand pounds for a great cause.",
                    ]
                },
                {
                    "sentences": [
                        "The race itself was a blur. At kilometre eighteen, I was exhausted and wanted to stop.",
                        "No sooner had I slowed down than I heard {little} shouting my name from the crowd.",
                    ]
                },
                {
                    "sentences": [
                        "Never have I been so happy to see a finish line. Dad crossed it holding {teen}'s hand and mine.",
                        "Under no circumstances will I run another half marathon … at least not until next year.",
                    ]
                },
            ],
            "highlight": [
                "Little did I know",
                "Not only did we",
                "Rarely have I",
                "Not until … did we",
                "No sooner had I",
                "Never have I",
                "Under no circumstances will I",
                "sponsor",
                "donate",
                "raised",
                "cause",
                "exhausted",
                "charity",
            ],
        },
        "listening": [
            {
                "id": "c1-5-appeal",
                "title": "A charity appeal",
                "transcript": [
                    {
                        "speaker": "Nurse",
                        "text": "Not only does the money buy new equipment, but it also pays for a play room for the children.",
                    },
                    {
                        "speaker": "Nurse",
                        "text": "Rarely do we receive such generous support from a single family.",
                    },
                    {"speaker": "Nurse", "text": "Every pound you donate makes a real difference."},
                ],
            },
            {
                "id": "c1-5-finish",
                "title": "At the finish line",
                "transcript": [
                    {"speaker": "Mum", "text": "You did it! How do you feel?"},
                    {"speaker": "{boy}", "text": "Exhausted. Never have my legs hurt so much."},
                    {
                        "speaker": "{teen}",
                        "text": "But we raised more than three thousand pounds. It was worth it.",
                    },
                    {"speaker": "Dad", "text": "Next year, it's your turn, {little}!"},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Inversion after negative adverbials",
                "explanation": (
                    "In formal or dramatic English, we can put a negative or limiting expression at the start of the sentence for emphasis. "
                    "Then the subject and auxiliary change places, like in a question. "
                    "I have never been so tired. → Never have I been so tired. "
                    "We not only ran in the rain … → Not only did we run in the rain, but we also … "
                    "Other expressions: Rarely / Seldom, Little did I know, No sooner had … than, Not until … did, Under no circumstances."
                ),
                "explanation_ru": (
                    "Инверсия для эмфазы: после Never, Rarely, Not only, Little, No sooner в начале предложения — "
                    "вопросительный порядок слов: Never have I seen … = Никогда я не видел …"
                ),
                "examples": [
                    "Rarely do we see such generosity.",
                    "Little did she know that she would win.",
                    "No sooner had we arrived than it started to rain.",
                    "Under no circumstances should you run without water.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "charity-words",
            "VOCABULARY",
            "Match the word to the picture.",
            [
                ("charity", None, "🎗️"),
                ("donate", None, "💝"),
                ("sponsor", None, "🤝"),
                ("exhausted", None, "🥵"),
            ],
            ["vocab.charity", "vocab.donate", "vocab.sponsor", "vocab.exhausted"],
            "Exhausted = extremely tired.",
            "charity 🎗️, donate 💝, sponsor 🤝, exhausted 🥵.",
        ),
        matching(
            "charity-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("raise money", "collect money for a purpose", None),
                ("sponsor", "promise money if someone completes a challenge", None),
                ("cause", "an aim or organisation that people support", None),
            ],
            ["vocab.raise_money", "vocab.sponsor", "vocab.cause"],
            "You sponsor a friend who runs a race.",
            "raise money = collect money; sponsor = promise money for a challenge; cause = an aim people support.",
        ),
        choice(
            "find-exhausted",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: exhausted",
            [(None, "🥵"), (None, "🤩"), (None, "😌")],
            "a",
            ["vocab.exhausted"],
            "How {boy} felt at kilometre eighteen.",
            "🥵 exhausted.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-inversion",
            "LISTENING",
            "Listen. What happened as soon as the race started?",
            "As soon as the race started, …",
            [("it began to rain", "🌧️"), ("a runner fell over", "🤕"), ("the music stopped", "🔇")],
            "a",
            ["grammar.inversion"],
            "Listen for 'No sooner … than'.",
            "No sooner had the race started than it began to rain.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="It was sunny all morning. But no sooner had the race started than it began to rain — heavily!",
        ),
        true_false(
            "listen-playroom",
            "LISTENING",
            "Listen to the nurse. True or false?",
            "The money will also pay for a play room.",
            True,
            ["grammar.inversion", "vocab.donate"],
            "Listen for 'Not only … but also'.",
            "Not only does the money buy equipment, but it also pays for a play room.",
            listening_id="c1-5-appeal",
        ),
        true_false(
            "listen-total",
            "LISTENING",
            "Listen to the family at the finish line. True or false?",
            "They raised less than a thousand pounds.",
            False,
            ["vocab.raise_money"],
            "Listen to {teen}.",
            "We raised more than three thousand pounds.",
            listening_id="c1-5-finish",
        ),
        blank(
            "never-blank",
            "GRAMMAR",
            "Complete the inversion.",
            "Never ___ I been so tired! Not only ___ we run in the rain, but we also trained at six.",
            ["have", "did"],
            ["have", "had", "did", "do"],
            ["grammar.inversion"],
            "Never + have + I + V3; Not only + did + we + verb.",
            "Never have I been so tired! Not only did we run in the rain …",
        ),
        choice(
            "inversion-correct",
            "GRAMMAR",
            "Which sentence is correct?",
            "Emphasise that you rarely complain.",
            [
                ("Rarely do I complain.", None),
                ("Rarely I complain do.", None),
                ("Rarely I do complain.", None),
            ],
            "a",
            ["grammar.inversion"],
            "Rarely + auxiliary + subject + verb.",
            "Rarely do I complain.",
        ),
        choice(
            "little-did",
            "GRAMMAR",
            "Choose the sentence with the same meaning.",
            "I didn't know how hard the training would be.",
            [
                ("Little did I know how hard the training would be.", None),
                ("Little I knew how hard the training would be.", None),
                ("Little did I knew how hard the training would be.", None),
            ],
            "a",
            ["grammar.inversion"],
            "Little + did + subject + base verb.",
            "Little did I know how hard the training would be.",
        ),
        blank(
            "no-sooner-blank",
            "GRAMMAR",
            "Complete the sentence.",
            "No sooner ___ I slowed down ___ I heard my sister shouting.",
            ["had", "than"],
            ["had", "did", "than", "when"],
            ["grammar.inversion"],
            "No sooner + had + subject + V3 + than.",
            "No sooner had I slowed down than I heard my sister shouting.",
        ),
        build(
            "build-inversion",
            "GRAMMAR",
            "Put the words in order.",
            "Never have I seen so many runners.",
            ["grammar.inversion"],
            "Start with 'Never have I'.",
            "Never have I seen so many runners.",
        ),
        choice(
            "read-granny-donate",
            "READING",
            "Read the text. Then answer.",
            "What did Granny {gran2} do?",
            [
                ("She promised a pound per kilometre and then doubled it.", "💷"),
                ("She ran the half marathon too.", "🏃"),
                ("She organised the race.", "📋"),
            ],
            "a",
            ["vocab.donate", "vocab.sponsor"],
            "Look at paragraph 3.",
            "She promised a pound per kilometre and then doubled it.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-km18",
            "READING",
            "Read the text. True or false?",
            "Hearing {little} in the crowd helped {boy} to keep going.",
            True,
            ["grammar.inversion", "vocab.exhausted"],
            "Look at paragraph 4.",
            "As soon as he slowed down, he heard {little} shouting his name.",
        ),
        speak(
            "say-appeal",
            "Persuade your class to support a charity you care about. Use at least two inversions for emphasis.",
            "Never have I … Not only does this charity …, but it also … Rarely do we have the chance to …",
            "Never have I seen a charity that does so much with so little. Not only does it feed hungry families, but it also teaches cooking. Rarely do we have the chance to help so directly — so please donate!",
            ["grammar.inversion", "vocab.charity", "vocab.persuade"],
        ),
        choice(
            "quiz-narrative-race",
            "QUIZ",
            "Choose the best tense.",
            "We ___ for three months when the big day finally came.",
            [("had been training", None), ("have been training", None), ("are training", None)],
            "a",
            ["grammar.narrative_tenses"],
            "Remember Lesson 1.",
            "We had been training for three months when the day came.",
        ),
        blank(
            "quiz-hedge-donations",
            "QUIZ",
            "Complete the hedged sentence.",
            "Donations ___ to rise before big races.",
            ["tend"],
            ["tend", "tends", "are tend"],
            ["grammar.hedging"],
            "Remember Lesson 2.",
            "Donations tend to rise before big races.",
        ),
        choice(
            "quiz-cleft-cause",
            "QUIZ",
            "Choose the correct cleft sentence.",
            "Emphasise the reason you ran.",
            [
                ("What made us run was the children's hospital.", None),
                ("What made us run it was the children's hospital.", None),
                ("It was the children's hospital what made us run.", None),
            ],
            "a",
            ["grammar.cleft_sentences", "vocab.cause"],
            "Remember Lesson 3.",
            "What made us run was the children's hospital.",
        ),
        blank(
            "quiz-mixed-trained",
            "QUIZ",
            "Complete the mixed conditional.",
            "If we hadn't trained so hard, we wouldn't ___ so proud now.",
            ["be"],
            ["be", "have been", "being"],
            ["grammar.mixed_conditionals"],
            "Remember Lesson 4: past → present.",
            "If we hadn't trained so hard, we wouldn't be so proud now.",
        ),
        choice(
            "quiz-footage-race",
            "QUIZ",
            "Choose the right word.",
            "{boy} filmed the race and ___ the footage into a short video for the hospital.",
            [("edited", None), ("verified", None), ("donated", None)],
            "a",
            ["vocab.edit", "vocab.footage"],
            "Remember Lesson 1.",
            "He edited the footage into a short video.",
        ),
        choice(
            "quiz-source-reliable",
            "QUIZ",
            "Choose the right word.",
            "Before you donate online, check that the charity's website is ___.",
            [("reliable", None), ("misleading", None), ("exhausted", None)],
            "a",
            ["vocab.reliable", "vocab.charity"],
            "Remember Lesson 2.",
            "Check that the website is reliable.",
        ),
        choice(
            "quiz-carbon",
            "QUIZ",
            "Choose the right phrase.",
            "Walking to the race instead of driving reduced our ___.",
            [("carbon footprint", None), ("twist", None), ("draft", None)],
            "a",
            ["vocab.carbon_footprint", "vocab.reduce"],
            "Remember Lesson 3.",
            "It reduced our carbon footprint.",
        ),
        choice(
            "quiz-plot",
            "QUIZ",
            "Choose the right word.",
            "{little} wants to write a story about the race. First she plans the ___: what happens and in what order.",
            [("plot", None), ("setting", None), ("cause", None)],
            "a",
            ["vocab.plot", "vocab.setting"],
            "Remember Lesson 4.",
            "First she plans the plot.",
        ),
    ],
}

UNIT = {
    "slug": "media-and-projects",
    "title": "Media and Projects",
    "description": "A wildlife documentary, fake news, an eco campaign, {little}'s first story and a charity half marathon.",
    "lessons": [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5],
}
