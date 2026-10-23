"""B2 · Unit 2 "Around the World" (B2 lessons 6-10).

{teen} spends an exchange year in Canada while {boy} discovers other cultures from home.
Topics: pen friends, an exchange year, travel problems, festivals, a debate. Grammar:
contrast linkers, the third conditional and wish / if only, indirect questions, articles,
linking an argument. Lesson 10 closes B2 with a mixed review of both units.
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
    "pen-friends",
    "teens-exchange-year",
    "travel-troubles",
    "festivals-of-the-world",
    "the-debate-club",
)

ITEMS: dict[str, Item] = {
    # Lesson 6
    "vocab.pen_friend": (
        V,
        "pen friend",
        "✍️",
        "друг по переписке",
        L6,
        ["My pen friend lives in Japan."],
        None,
    ),
    "vocab.culture": (
        V,
        "culture",
        "🎎",
        "культура",
        L6,
        ["I'm interested in Japanese culture."],
        None,
    ),
    "vocab.custom": (V, "custom", "🙇", "обычай", L6, ["Bowing is a Japanese custom."], None),
    "vocab.abroad": (
        V,
        "abroad",
        "🧳",
        "за границей, за границу",
        L6,
        ["Have you ever lived abroad?"],
        None,
    ),
    "vocab.language": (V, "language", "🗣️", "язык", L6, ["She speaks three languages."], None),
    "vocab.similar": (
        V,
        "similar (to)",
        "🟰",
        "похожий (на)",
        L6,
        ["Our schools are similar in many ways."],
        None,
    ),
    "grammar.contrast_linkers": (
        G,
        "although / however / whereas / despite",
        None,
        "Союзы противопоставления: хотя, однако, тогда как, несмотря на",
        L6,
        [
            "Although it was late, we kept talking.",
            "Japanese school starts in April, whereas ours starts in September.",
        ],
        "although / whereas + clause; however at the start of a new sentence; despite + noun or -ing.",
    ),
    # Lesson 7
    "vocab.exchange": (
        V,
        "exchange",
        "🔄",
        "обмен (учебный)",
        L7,
        ["{teen} is on an exchange in Canada."],
        None,
    ),
    "vocab.host_family": (
        V,
        "host family",
        "🏠",
        "принимающая семья",
        L7,
        ["Her host family is very kind."],
        None,
    ),
    "vocab.homesick": (
        V,
        "homesick",
        "🥺",
        "тоскующий по дому",
        L7,
        ["She felt homesick in the first week."],
        None,
    ),
    "vocab.adapt": (
        V,
        "adapt (to)",
        "🦎",
        "приспособиться (к)",
        L7,
        ["It took a month to adapt to the cold."],
        None,
    ),
    "vocab.regret": (V, "regret", "😔", "сожалеть; сожаление", L7, ["I don't regret going."], None),
    "grammar.third_conditional": (
        G,
        "If I had known …, I would have …",
        None,
        "Условные предложения 3 типа: если бы (тогда) …, то …",
        L7,
        [
            "If I had packed a warmer coat, I wouldn't have been so cold.",
            "If she hadn't gone, she wouldn't have met Chloe.",
        ],
        "If + past perfect, would have + past participle. For imaginary situations in the past.",
    ),
    "grammar.wish": (
        G,
        "I wish … / If only …",
        None,
        "Жаль, что … / Если бы только …",
        L7,
        ["I wish you were here.", "I wish I had brought my gloves.", "If only it were summer!"],
        "wish + past simple = a wish about now; wish + past perfect = a regret about the past.",
    ),
    # Lesson 8
    "vocab.delay": (
        V,
        "delay",
        "⏳",
        "задержка; задерживать",
        L8,
        ["The flight was delayed by three hours."],
        None,
    ),
    "vocab.luggage": (V, "luggage", "🧳", "багаж", L8, ["Our luggage didn't arrive."], None),
    "vocab.passport": (V, "passport", "🛂", "паспорт", L8, ["Don't forget your passport!"], None),
    "vocab.cancel": (V, "cancel", "❌", "отменять", L8, ["The train was cancelled."], None),
    "vocab.refund": (V, "refund", "💸", "возврат денег", L8, ["Can I get a refund?"], None),
    "vocab.complaint": (V, "complaint", "📢", "жалоба", L8, ["Dad made a polite complaint."], None),
    "grammar.indirect_questions": (
        G,
        "Could you tell me where … is?",
        None,
        "Косвенные (вежливые) вопросы",
        L8,
        [
            "Could you tell me where the lost luggage office is?",
            "Do you know if the train is late?",
        ],
        "After Could you tell me / Do you know, use normal word order (subject + verb) and no do / does / did.",
    ),
    "phrase.polite_complaint": (
        P,
        "I'm afraid there's a problem with … / I'd like to complain about …",
        None,
        "Боюсь, есть проблема с … / Я хотел бы пожаловаться на …",
        L8,
        ["I'm afraid there's a problem with our booking.", "I'd like to complain about the delay."],
        "Polite ways to complain and ask for help.",
    ),
    # Lesson 9
    "vocab.festival": (
        V,
        "festival",
        "🎉",
        "фестиваль, праздник",
        L9,
        ["Diwali is a festival of light."],
        None,
    ),
    "vocab.tradition": (V, "tradition", "🪔", "традиция", L9, ["It's a family tradition."], None),
    "vocab.lantern": (
        V,
        "lantern",
        "🏮",
        "фонарь",
        L9,
        ["The streets were full of lanterns."],
        None,
    ),
    "vocab.parade": (
        V,
        "parade",
        "🎺",
        "парад, шествие",
        L9,
        ["We watched the parade from the balcony."],
        None,
    ),
    "vocab.fireworks": (
        V,
        "fireworks",
        "🎆",
        "фейерверк",
        L9,
        ["The fireworks started at midnight."],
        None,
    ),
    "vocab.celebrate": (
        V,
        "celebrate",
        "🥳",
        "праздновать",
        L9,
        ["How do you celebrate New Year?"],
        None,
    ),
    "grammar.articles": (
        G,
        "a / an / the / no article",
        None,
        "Артикли: a / an, the и нулевой артикль",
        L9,
        [
            "I saw a parade. The parade was amazing.",
            "The Moon is bright tonight.",
            "Children love festivals.",
        ],
        "a / an = one of many, mentioned for the first time; the = a specific or unique thing; no article = things in general.",
    ),
    # Lesson 10
    "vocab.debate": (V, "debate", "🎤", "дебаты", L10, ["We had a debate about homework."], None),
    "vocab.argument": (
        V,
        "argument",
        "🧩",
        "аргумент, довод",
        L10,
        ["That's a strong argument."],
        None,
    ),
    "vocab.opinion": (
        V,
        "opinion",
        "💭",
        "мнение",
        L10,
        ["In my opinion, school should start later."],
        None,
    ),
    "vocab.evidence": (
        V,
        "evidence",
        "📊",
        "доказательства, данные",
        L10,
        ["What evidence do you have?"],
        None,
    ),
    "vocab.persuade": (V, "persuade", "🤝", "убеждать", L10, ["She persuaded the judges."], None),
    "grammar.linking_arguments": (
        G,
        "Firstly … / Moreover … / On the other hand … / To sum up …",
        None,
        "Связки для аргументации",
        L10,
        [
            "Firstly, students need more sleep.",
            "On the other hand, parents work early.",
            "To sum up, …",
        ],
        "Use linkers to order points, add points, contrast and conclude.",
    ),
    "phrase.agree_disagree": (
        P,
        "I see your point, but … / I couldn't agree more.",
        None,
        "Понимаю твою точку зрения, но … / Полностью согласен.",
        L10,
        ["I see your point, but I'm not sure that's true.", "I couldn't agree more!"],
        "Polite ways to agree and disagree.",
    ),
}


LESSON_6 = {
    "slug": L6,
    "title": "Pen Friends",
    "description": "{boy} writes to his new pen friend in Japan. Their lives are similar — although some things are very different.",
    "minutes": 35,
    "objectives": [
        "Talk about cultures: culture, custom, language, abroad, similar.",
        "Contrast ideas with although, however, whereas and despite.",
        "Compare your life with life in another country.",
    ],
    "review": [
        "grammar.passive_all",
        "phrase.presenting",
        "vocab.invention",
        "grammar.gerund_infinitive",
        "grammar.relative_clauses",
        "grammar.present_perfect_continuous",
        "grammar.comparatives",
        "vocab.school",
        "grammar.prefer",
        "vocab.letter",
    ],
    "episode": (
        "Letters from Osaka",
        "{boy}'s class starts a pen-friend project with a school in Japan. {boy}'s pen friend is Haruto.",
    ),
    "content": {
        "story_intro": "{boy}'s school has started a pen-friend project with a school in Osaka, Japan.",
        "reading": {
            "title": "Dear Haruto",
            "paragraphs": [
                {
                    "sentences": [
                        "Thank you for your email! Although we live nine thousand kilometres apart, our lives are quite similar.",
                        "We both love football, robots and pizza.",
                    ]
                },
                {
                    "sentences": [
                        "However, our schools are very different. Your school year starts in April, whereas ours starts in September.",
                        "I was amazed that students clean their own classrooms in Japan. That's a custom we don't have!",
                    ]
                },
                {
                    "sentences": [
                        "Despite the long journey, my sister {teen} wants to visit Japan one day.",
                        "She has been learning Japanese for a year, although she says the writing is really hard.",
                    ]
                },
                {
                    "sentences": [
                        "I've never lived abroad, but I think learning about another culture is fascinating.",
                        "Could you tell me more about the festivals you celebrate?",
                    ]
                },
                {
                    "sentences": [
                        "By the way, the photo you sent of the cherry blossom is now on our classroom wall.",
                        "Write soon! Best wishes, {boy}",
                    ]
                },
            ],
            "highlight": [
                "Although",
                "However",
                "whereas",
                "Despite",
                "although",
                "similar",
                "custom",
                "abroad",
                "culture",
            ],
        },
        "listening": [
            {
                "id": "b2-6-call",
                "title": "A video call",
                "transcript": [
                    {
                        "speaker": "Haruto",
                        "text": "In Japan we usually eat lunch in the classroom, whereas you have a canteen, right?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "That's right. However, a lot of my friends bring their own lunch.",
                    },
                    {
                        "speaker": "Haruto",
                        "text": "Although I love Japanese food, I'd really like to try fish and chips!",
                    },
                    {"speaker": "{boy}", "text": "Ha! Despite the name, it's mostly potatoes."},
                ],
            },
            {
                "id": "b2-6-languages",
                "title": "Learning languages",
                "transcript": [
                    {
                        "speaker": "Teacher",
                        "text": "How many of you speak another language at home?",
                    },
                    {
                        "speaker": "Maya",
                        "text": "I do. I speak Spanish with my mum, although I'm not very good at writing it.",
                    },
                    {
                        "speaker": "Teacher",
                        "text": "That's still a great skill. Learning a language opens the door to a culture.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Contrast linkers",
                "explanation": (
                    "although + clause (in one sentence): Although it was late, we kept talking. "
                    "however + comma, at the start of a new sentence: Our lives are similar. However, our schools are different. "
                    "whereas compares two facts: Their year starts in April, whereas ours starts in September. "
                    "despite / in spite of + noun or -ing (not a clause): Despite the rain, we went out. Despite being tired, she finished."
                ),
                "explanation_ru": (
                    "although — хотя (+ предложение); however — однако (новое предложение); "
                    "whereas — тогда как; despite — несмотря на (+ существительное или -ing)."
                ),
                "examples": [
                    "Although Japanese is hard, I enjoy it.",
                    "It's expensive. However, it's worth it.",
                    "Despite the distance, we talk every week.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "culture-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("pen friend", None, "✍️"),
                ("custom", None, "🙇"),
                ("abroad", None, "🧳"),
                ("language", None, "🗣️"),
            ],
            ["vocab.pen_friend", "vocab.custom", "vocab.abroad", "vocab.language"],
            "A pen friend writes to you from another place.",
            "pen friend ✍️, custom 🙇, abroad 🧳, language 🗣️.",
        ),
        matching(
            "culture-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("culture", "the art, ideas and way of life of a group of people", None),
                ("custom", "a traditional way of doing something", None),
                ("similar", "almost the same", None),
            ],
            ["vocab.culture", "vocab.custom", "vocab.similar"],
            "Taking off your shoes at home is a custom in many countries.",
            "culture = way of life; custom = a traditional way of doing something; similar = almost the same.",
        ),
        choice(
            "find-abroad",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: something you need to travel abroad",
            [(None, "🛂"), (None, "🎒"), (None, "🚲")],
            "a",
            ["vocab.abroad"],
            "You show it at the border.",
            "🛂 You need a passport to travel abroad.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-whereas",
            "LISTENING",
            "Listen. How are the two sisters different?",
            "One sister …",
            [
                ("loves cities, whereas the other prefers the countryside", "🏙️"),
                ("speaks French, whereas the other speaks Japanese", "🗣️"),
                ("lives abroad, whereas the other lives at home", "✈️"),
            ],
            "a",
            ["grammar.contrast_linkers"],
            "Listen for 'whereas'.",
            "My sister loves big cities, whereas I prefer the countryside.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="My sister and I look very similar. However, she loves big cities, whereas I prefer the countryside.",
        ),
        true_false(
            "listen-fish-chips",
            "LISTENING",
            "Listen to Haruto and {boy}. True or false?",
            "Haruto would like to try fish and chips.",
            True,
            ["grammar.contrast_linkers"],
            "Listen to Haruto's second line.",
            "Although I love Japanese food, I'd really like to try fish and chips!",
            listening_id="b2-6-call",
        ),
        true_false(
            "listen-maya-spanish",
            "LISTENING",
            "Listen to the teacher and Maya. True or false?",
            "Maya is very good at writing Spanish.",
            False,
            ["grammar.contrast_linkers", "vocab.language"],
            "Listen for 'although'.",
            "She speaks Spanish, although she isn't very good at writing it.",
            listening_id="b2-6-languages",
        ),
        blank(
            "linker-blank",
            "GRAMMAR",
            "Choose the right linkers.",
            "___ the rain, we went to the festival. ___ it was cold, we stayed until midnight.",
            ["Despite", "Although"],
            ["Despite", "Although", "However"],
            ["grammar.contrast_linkers"],
            "despite + noun; although + clause.",
            "Despite the rain, we went. Although it was cold, we stayed.",
        ),
        blank(
            "whereas-blank",
            "GRAMMAR",
            "Choose the right linker.",
            "In Japan school starts in April, ___ in Britain it starts in September.",
            ["whereas"],
            ["whereas", "despite", "however"],
            ["grammar.contrast_linkers"],
            "Compare two facts in one sentence.",
            "…, whereas in Britain it starts in September.",
        ),
        choice(
            "however-position",
            "GRAMMAR",
            "Which is correct?",
            "Join the ideas: Japanese is difficult. I love learning it.",
            [
                ("Japanese is difficult. However, I love learning it.", None),
                ("Japanese is difficult, however I love learning it however.", None),
                ("However Japanese is difficult, I love learning it.", None),
            ],
            "a",
            ["grammar.contrast_linkers", "vocab.language"],
            "however starts a new sentence and is followed by a comma.",
            "Japanese is difficult. However, I love learning it.",
        ),
        choice(
            "despite-form",
            "GRAMMAR",
            "Which is correct?",
            "Talk about {teen}.",
            [
                ("Despite being tired, {teen} finished her Japanese homework.", None),
                ("Despite she was tired, {teen} finished her Japanese homework.", None),
                ("Despite of tired, {teen} finished her Japanese homework.", None),
            ],
            "a",
            ["grammar.contrast_linkers"],
            "despite + -ing or a noun.",
            "Despite being tired, she finished.",
        ),
        build(
            "build-although",
            "GRAMMAR",
            "Put the words in order.",
            "Although we live far apart, our lives are similar.",
            ["grammar.contrast_linkers", "vocab.similar"],
            "Start with 'Although we live'.",
            "Although we live far apart, our lives are similar.",
        ),
        choice(
            "read-clean",
            "READING",
            "Read the email. Then answer.",
            "Which Japanese custom surprised {boy}?",
            [
                ("Students clean their own classrooms.", "🧹"),
                ("School starts at six in the morning.", "⏰"),
                ("Students don't wear shoes outside.", "👟"),
            ],
            "a",
            ["vocab.custom", "vocab.culture"],
            "Look at paragraph 2.",
            "Students clean their own classrooms in Japan.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-teen-japanese",
            "READING",
            "Read the email. True or false?",
            "{teen} finds Japanese writing easy.",
            False,
            ["grammar.contrast_linkers", "vocab.language"],
            "Look at paragraph 3.",
            "She says the writing is really hard.",
        ),
        speak(
            "say-compare",
            "Compare your country with another country you know. Use although, however, whereas and despite.",
            "Although … , … In my country …, whereas in … However, … Despite …",
            "Although Britain and Japan are islands, they are very different. In Britain we drink a lot of tea, whereas in Japan green tea is more popular. However, both countries love football.",
            ["grammar.contrast_linkers", "vocab.culture"],
        ),
        choice(
            "quiz-passive-written",
            "QUIZ",
            "Choose the right passive form.",
            "Thousands of emails ___ by the students since the project started.",
            [("have been written", None), ("were being write", None), ("has written", None)],
            "a",
            ["grammar.passive_all"],
            "Remember Unit 1, Lesson 5: present perfect passive.",
            "Thousands of emails have been written.",
        ),
        blank(
            "quiz-enjoy-reading",
            "QUIZ",
            "Choose the right form.",
            "I really enjoy ___ your emails.",
            ["reading"],
            ["reading", "to read", "read"],
            ["grammar.gerund_infinitive"],
            "Remember Unit 1, Lesson 4: enjoy + -ing.",
            "I really enjoy reading your emails.",
        ),
        choice(
            "quiz-who-pen",
            "QUIZ",
            "Choose the right relative pronoun.",
            "Haruto is the boy ___ writes to me from Osaka.",
            [("who", None), ("which", None), ("whose", None)],
            "a",
            ["grammar.relative_clauses", "vocab.pen_friend"],
            "Remember Unit 1, Lesson 2.",
            "Haruto is the boy who writes to me.",
        ),
    ],
}

LESSON_7 = {
    "slug": L7,
    "title": "{teen}'s Exchange Year",
    "description": "{teen} spends a year with a host family in Canada. What would have happened if …?",
    "minutes": 35,
    "objectives": [
        "Talk about living abroad: exchange, host family, homesick, adapt, regret.",
        "Talk about the past with the third conditional.",
        "Express wishes and regrets with wish and if only.",
    ],
    "review": [
        "grammar.contrast_linkers",
        "vocab.abroad",
        "vocab.culture",
        "grammar.second_conditional",
        "grammar.present_perfect_continuous",
        "grammar.used_to",
        "grammar.past_continuous",
        "vocab.cold",
        "vocab.coat",
        "vocab.plane",
    ],
    "episode": (
        "Snow in October",
        "{teen} arrives in Canada for her exchange year. She didn't pack for the snow!",
    ),
    "content": {
        "story_intro": "{teen} is spending a year at a school in Canada. She is living with a host family, the Martins.",
        "reading": {
            "title": "{teen}'s Blog: Three Months in Canada",
            "paragraphs": [
                {
                    "sentences": [
                        "When I arrived in October, it was already snowing. If I had checked the weather, I would have packed a warmer coat!",
                        "I wish I had listened to Mum.",
                    ]
                },
                {
                    "sentences": [
                        "My host family, the Martins, are wonderful. Their daughter, Chloe, has become my best friend.",
                        "If I hadn't come on this exchange, I would never have met her.",
                    ]
                },
                {
                    "sentences": [
                        "In the first weeks I felt really homesick. I missed my family, and I wished I could understand the jokes at school.",
                        "But slowly I adapted. Now I even dream in English!",
                    ]
                },
                {
                    "sentences": [
                        "Last month we went skating on a frozen lake. I fell over about twenty times.",
                        "If Chloe hadn't held my hand, I would have fallen even more!",
                    ]
                },
                {
                    "sentences": [
                        "I don't regret coming here at all. The only thing I wish is that my family were here to see the snow.",
                        "If only {little} could build a snowman with me!",
                    ]
                },
            ],
            "highlight": [
                "If I had checked",
                "would have packed",
                "I wish I had listened",
                "If I hadn't come",
                "would never have met",
                "I wish",
                "If only",
                "homesick",
                "adapted",
                "host family",
            ],
        },
        "listening": [
            {
                "id": "b2-7-call",
                "title": "A call home",
                "transcript": [
                    {"speaker": "Mum", "text": "How are you, darling? Are you still homesick?"},
                    {
                        "speaker": "{teen}",
                        "text": "Not really. I wish you were here, though. It's so beautiful.",
                    },
                    {"speaker": "Mum", "text": "And the coat? I told you to take the big one!"},
                    {
                        "speaker": "{teen}",
                        "text": "I know. If I had taken it, I wouldn't have spent my first week shopping!",
                    },
                ],
            },
            {
                "id": "b2-7-chloe",
                "title": "Chloe and {teen}",
                "transcript": [
                    {"speaker": "Chloe", "text": "Do you ever wish you had stayed at home?"},
                    {
                        "speaker": "{teen}",
                        "text": "Never! If I hadn't come, I wouldn't have learned to ski.",
                    },
                    {"speaker": "Chloe", "text": "Or met me!"},
                    {
                        "speaker": "{teen}",
                        "text": "Exactly. The only thing I regret is not bringing my brother's camera.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "The third conditional",
                "explanation": (
                    "Use it to imagine a different past — something that didn't happen. "
                    "If + past perfect, would have + past participle. "
                    "If I had checked the weather, I would have packed a warmer coat. (I didn't check, so I didn't pack one.) "
                    "Negative: If I hadn't come, I wouldn't have met Chloe."
                ),
                "explanation_ru": (
                    "Нереальное прошлое: если бы тогда …, то … If + had + V3, would have + V3. "
                    "If I had known, I would have helped = Если бы я знал, я бы помог."
                ),
                "examples": [
                    "If we had left earlier, we wouldn't have missed the plane.",
                    "She would have won if she hadn't fallen.",
                    "What would you have done if you had been there?",
                ],
            },
            {
                "title": "wish / if only",
                "explanation": (
                    "wish + past simple = you want the present to be different: I wish you were here. (You aren't.) "
                    "wish + past perfect = a regret about the past: I wish I had listened to Mum. (I didn't.) "
                    "wish + could = an ability you don't have: I wish I could ski. "
                    "If only … is a stronger form: If only it were summer!"
                ),
                "explanation_ru": (
                    "wish + past simple — жаль, что сейчас не так; wish + past perfect — жаль, что тогда так случилось. "
                    "If only — «если бы только»."
                ),
                "examples": [
                    "I wish I spoke French.",
                    "I wish I hadn't eaten so much.",
                    "If only I had more time!",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "exchange-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("host family", None, "🏠"),
                ("homesick", None, "🥺"),
                ("exchange", None, "🔄"),
                ("regret", None, "😔"),
            ],
            ["vocab.host_family", "vocab.homesick", "vocab.exchange", "vocab.regret"],
            "When you miss home, you feel homesick.",
            "host family 🏠, homesick 🥺, exchange 🔄, regret 😔.",
        ),
        matching(
            "exchange-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("homesick", "sad because you are away from home", None),
                ("adapt", "change to suit a new situation", None),
                ("host family", "a family that a foreign student lives with", None),
            ],
            ["vocab.homesick", "vocab.adapt", "vocab.host_family"],
            "You adapt to a new school.",
            "homesick = missing home; adapt = change for a new situation; host family = a family you stay with.",
        ),
        choice(
            "find-homesick",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: homesick",
            [(None, "🥳"), (None, "🥺"), (None, "😡")],
            "b",
            ["vocab.homesick"],
            "Sad and missing home.",
            "🥺 homesick.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-third",
            "LISTENING",
            "Listen. Why did the boy miss the train?",
            "He missed it because …",
            [
                ("he got up late", "⏰"),
                ("the train was cancelled", "❌"),
                ("he lost his ticket", "🎫"),
            ],
            "a",
            ["grammar.third_conditional"],
            "Listen for 'If I had …'.",
            "If I had got up earlier, I wouldn't have missed the train.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="I can't believe it. If I had got up earlier, I wouldn't have missed the train. Now I have to wait an hour!",
        ),
        true_false(
            "listen-coat",
            "LISTENING",
            "Listen to Mum and {teen}. True or false?",
            "{teen} took the big coat to Canada.",
            False,
            ["grammar.third_conditional", "vocab.coat"],
            "What did she spend her first week doing?",
            "If I had taken it, I wouldn't have spent my first week shopping! (She didn't take it.)",
            listening_id="b2-7-call",
        ),
        true_false(
            "listen-camera",
            "LISTENING",
            "Listen to Chloe and {teen}. True or false?",
            "{teen} regrets not bringing her brother's camera.",
            True,
            ["vocab.regret", "grammar.wish"],
            "Listen to her last line.",
            "The only thing I regret is not bringing my brother's camera.",
            listening_id="b2-7-chloe",
        ),
        blank(
            "third-blank",
            "GRAMMAR",
            "Complete the third conditional.",
            "If I ___ checked the weather, I would ___ packed a warmer coat.",
            ["had", "have"],
            ["had", "have", "has", "would"],
            ["grammar.third_conditional"],
            "If + had + V3, would have + V3.",
            "If I had checked the weather, I would have packed a warmer coat.",
        ),
        blank(
            "wish-blank",
            "GRAMMAR",
            "Choose the right forms.",
            "I wish you ___ here now. I wish I ___ listened to Mum before I left.",
            ["were", "had"],
            ["are", "were", "had", "have"],
            ["grammar.wish"],
            "Now → past simple; before → past perfect.",
            "I wish you were here. I wish I had listened to Mum.",
        ),
        choice(
            "third-meaning",
            "GRAMMAR",
            "What does the sentence mean?",
            "If Chloe hadn't helped me, I would have fallen.",
            [
                ("Chloe helped me, so I didn't fall.", None),
                ("Chloe didn't help me, so I fell.", None),
                ("Chloe will help me so that I don't fall.", None),
            ],
            "a",
            ["grammar.third_conditional"],
            "The third conditional is the opposite of what really happened.",
            "In reality Chloe helped, so I didn't fall.",
        ),
        choice(
            "which-conditional",
            "GRAMMAR",
            "Choose the correct sentence.",
            "Last year {teen} didn't know about the snow, so she didn't pack boots.",
            [
                ("If she had known, she would have packed boots.", None),
                ("If she knew, she would pack boots.", None),
                ("If she will know, she packs boots.", None),
            ],
            "a",
            ["grammar.third_conditional", "grammar.second_conditional"],
            "The situation is in the past.",
            "Past → third conditional: If she had known, she would have packed boots.",
        ),
        build(
            "build-wish",
            "GRAMMAR",
            "Put the words in order.",
            "I wish I could speak French.",
            ["grammar.wish"],
            "Start with 'I wish'.",
            "I wish I could speak French.",
        ),
        order(
            "read-order",
            "READING",
            "Put {teen}'s experiences in order.",
            [
                "She arrived in October, and it was snowing.",
                "She felt homesick in the first weeks.",
                "She slowly adapted to life in Canada.",
                "She went skating on a frozen lake.",
                "She wrote that she doesn't regret coming.",
            ],
            ["vocab.homesick", "vocab.adapt", "vocab.regret"],
            "Homesick first, adapted later.",
            "Arrival → homesick → adapted → skating → no regrets.",
        ),
        choice(
            "read-chloe",
            "READING",
            "Read the blog. Then answer.",
            "Who is Chloe?",
            [
                ("the daughter of {teen}'s host family", "👧"),
                ("{teen}'s teacher in Canada", "🧑‍🏫"),
                ("{teen}'s pen friend from Japan", "✍️"),
            ],
            "a",
            ["vocab.host_family"],
            "Look at paragraph 2.",
            "Chloe is the Martins' daughter — {teen}'s host family.",
            ex_type="READING_COMPREHENSION",
        ),
        speak(
            "say-regrets",
            "Think about last year. Say one thing you wish you had done differently, and what would have happened.",
            "I wish I had … If I had …, I would have …",
            "I wish I had practised the piano more. If I had practised more, I would have played better at the concert.",
            ["grammar.third_conditional", "grammar.wish"],
        ),
        blank(
            "quiz-although-cold",
            "QUIZ",
            "Choose the right linker.",
            "___ it was minus twenty, {teen} went skating.",
            ["Although"],
            ["Although", "Despite", "However"],
            ["grammar.contrast_linkers"],
            "Remember Lesson 6: + a clause.",
            "Although it was minus twenty, {teen} went skating.",
        ),
        choice(
            "quiz-second-canada",
            "QUIZ",
            "Choose the right sentence.",
            "Imagine you are in Canada now.",
            [
                ("If I lived in Canada, I would learn to ski.", None),
                ("If I live in Canada, I would learn to ski.", None),
                ("If I lived in Canada, I will learn to ski.", None),
            ],
            "a",
            ["grammar.second_conditional"],
            "Remember Unit 1, Lesson 1.",
            "If I lived in Canada, I would learn to ski.",
        ),
        choice(
            "quiz-used-to-canada",
            "QUIZ",
            "Choose the right form.",
            "{teen} ___ feel homesick, but now she's fine.",
            [("used to", None), ("is used to", None), ("uses to", None)],
            "a",
            ["grammar.used_to", "vocab.homesick"],
            "Remember B1: past habits and states.",
            "{teen} used to feel homesick.",
        ),
    ],
}

LESSON_8 = {
    "slug": L8,
    "title": "Travel Troubles",
    "description": "The family flies to visit {teen} — and everything goes wrong. Could you tell me where our luggage is?",
    "minutes": 35,
    "objectives": [
        "Use travel vocabulary: delay, cancel, luggage, passport, refund, complaint.",
        "Ask polite indirect questions: Could you tell me …? Do you know if …?",
        "Make a polite complaint.",
    ],
    "review": [
        "grammar.third_conditional",
        "grammar.wish",
        "vocab.host_family",
        "grammar.contrast_linkers",
        "grammar.passive_all",
        "grammar.present_perfect_continuous",
        "vocab.ticket",
        "vocab.station",
        "vocab.suitcase",
        "vocab.plane",
    ],
    "episode": (
        "Lost in the Airport",
        "The family's flight to Canada is delayed and their luggage disappears. Dad stays polite — just.",
    ),
    "content": {
        "story_intro": "At the winter holidays, the family flies to Canada to visit {teen}. Not everything goes to plan.",
        "reading": {
            "title": "The Longest Journey",
            "paragraphs": [
                {
                    "sentences": [
                        "Our flight was delayed by four hours because of the snow.",
                        "Dad went to the desk and asked: Could you tell me when the plane will leave?",
                    ]
                },
                {
                    "sentences": [
                        "The assistant said she didn't know if the flight would be cancelled.",
                        "We had been waiting for so long that {little} fell asleep on the suitcases.",
                    ]
                },
                {
                    "sentences": [
                        "When we finally landed in Toronto, our luggage didn't arrive.",
                        "Mum stayed calm and said: I'm afraid there's a problem. Do you know where our bags are?",
                    ]
                },
                {
                    "sentences": [
                        "The man checked the computer and explained that the bags had been sent to Vancouver by mistake.",
                        "Dad asked whether we could get a refund for the delay, and he filled in a complaint form.",
                    ]
                },
                {
                    "sentences": [
                        "Our bags arrived two days later. {teen} laughed: If you had listened to me, you would have packed a toothbrush in your hand luggage!",
                        "Despite everything, it was wonderful to see her again.",
                    ]
                },
            ],
            "highlight": [
                "Could you tell me when the plane will leave",
                "if the flight would be cancelled",
                "Do you know where our bags are",
                "whether we could get a refund",
                "delayed",
                "luggage",
                "complaint",
                "refund",
            ],
        },
        "listening": [
            {
                "id": "b2-8-desk",
                "title": "At the information desk",
                "transcript": [
                    {
                        "speaker": "Dad",
                        "text": "Excuse me, could you tell me where the lost luggage office is?",
                    },
                    {"speaker": "Assistant", "text": "Of course. It's downstairs, next to exit B."},
                    {"speaker": "Dad", "text": "And do you know if it's open now?"},
                    {
                        "speaker": "Assistant",
                        "text": "I'm sorry, it closes at ten. You'll have to come back tomorrow morning.",
                    },
                ],
            },
            {
                "id": "b2-8-complaint",
                "title": "A polite complaint",
                "transcript": [
                    {
                        "speaker": "Mum",
                        "text": "I'd like to complain about our hotel room. I'm afraid the heating doesn't work.",
                    },
                    {
                        "speaker": "Receptionist",
                        "text": "I'm very sorry. We'll move you to another room immediately.",
                    },
                    {
                        "speaker": "Mum",
                        "text": "Thank you. Could you tell me what time breakfast is served?",
                    },
                    {
                        "speaker": "Receptionist",
                        "text": "From seven until ten. And it's free for you tomorrow, as an apology.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Indirect questions",
                "explanation": (
                    "Indirect questions are more polite. They start with Could you tell me …? / Do you know …? / I wonder … "
                    "After these phrases, use normal word order (subject + verb) and no do / does / did. "
                    "Where is the office? → Could you tell me where the office is? "
                    "When does the plane leave? → Do you know when the plane leaves? "
                    "For yes/no questions use if or whether: Is it open? → Do you know if it is open?"
                ),
                "explanation_ru": (
                    "Вежливые косвенные вопросы: после Could you tell me … — прямой порядок слов и без do/does/did. "
                    "Для вопросов «да/нет» — if / whether."
                ),
                "examples": [
                    "Could you tell me what time it is?",
                    "Do you know if the train has left?",
                    "I wonder whether they will give us a refund.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "travel-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("passport", None, "🛂"),
                ("luggage", None, "🧳"),
                ("delay", None, "⏳"),
                ("refund", None, "💸"),
            ],
            ["vocab.passport", "vocab.luggage", "vocab.delay", "vocab.refund"],
            "Luggage = your bags and suitcases.",
            "passport 🛂, luggage 🧳, delay ⏳, refund 💸.",
        ),
        matching(
            "travel-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("cancel", "decide that something will not happen", None),
                ("refund", "money that is given back to you", None),
                ("complaint", "a statement that you are not happy with something", None),
            ],
            ["vocab.cancel", "vocab.refund", "vocab.complaint"],
            "When a flight is cancelled, it doesn't fly.",
            "cancel = it won't happen; refund = money back; complaint = saying you're not happy.",
        ),
        choice(
            "find-cancel",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: cancelled",
            [(None, "⏳"), (None, "❌"), (None, "✅")],
            "b",
            ["vocab.cancel"],
            "The flight will not happen.",
            "❌ cancelled.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-indirect",
            "LISTENING",
            "Listen. What does the woman want to know?",
            "She wants to know …",
            [
                ("if the train to Paris is on time", "🚆"),
                ("where the toilets are", "🚻"),
                ("how much a ticket costs", "🎫"),
            ],
            "a",
            ["grammar.indirect_questions", "vocab.delay"],
            "Listen for 'Do you know if …'.",
            "Do you know if the train to Paris is on time?",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Excuse me, do you know if the train to Paris is on time? The board says there's a delay.",
        ),
        true_false(
            "listen-office-open",
            "LISTENING",
            "Listen to Dad and the assistant. True or false?",
            "The lost luggage office is open now.",
            False,
            ["grammar.indirect_questions", "vocab.luggage"],
            "What time does it close?",
            "It closes at ten. They have to come back tomorrow morning.",
            listening_id="b2-8-desk",
        ),
        true_false(
            "listen-breakfast",
            "LISTENING",
            "Listen to Mum and the receptionist. True or false?",
            "The family will get a free breakfast.",
            True,
            ["phrase.polite_complaint", "vocab.complaint"],
            "Listen to the last line.",
            "It's free for you tomorrow, as an apology.",
            listening_id="b2-8-complaint",
        ),
        blank(
            "indirect-blank",
            "GRAMMAR",
            "Complete the indirect question.",
            "Could you tell me where the gate ___? Do you know ___ the flight is delayed?",
            ["is", "if"],
            ["is", "does", "if", "that"],
            ["grammar.indirect_questions"],
            "Normal word order; yes/no → if.",
            "Could you tell me where the gate is? Do you know if the flight is delayed?",
        ),
        choice(
            "indirect-order",
            "GRAMMAR",
            "Choose the correct indirect question.",
            "When does the plane leave?",
            [
                ("Could you tell me when the plane leaves?", None),
                ("Could you tell me when does the plane leave?", None),
                ("Could you tell me when leaves the plane?", None),
            ],
            "a",
            ["grammar.indirect_questions"],
            "No does; subject + verb.",
            "Could you tell me when the plane leaves?",
        ),
        choice(
            "indirect-past",
            "GRAMMAR",
            "Choose the correct indirect question.",
            "Where did they send our bags?",
            [
                ("Do you know where they sent our bags?", None),
                ("Do you know where did they send our bags?", None),
                ("Do you know where they did send our bags?", None),
            ],
            "a",
            ["grammar.indirect_questions", "vocab.luggage"],
            "No did; the verb is in the past.",
            "Do you know where they sent our bags?",
        ),
        choice(
            "polite-complaint",
            "GRAMMAR",
            "Choose the most polite complaint.",
            "The heating in your room doesn't work.",
            [
                ("I'm afraid there's a problem with the heating in our room.", None),
                ("Your heating is terrible. Fix it!", None),
                ("Why your heating doesn't work?", None),
            ],
            "a",
            ["phrase.polite_complaint"],
            "Start with I'm afraid …",
            "I'm afraid there's a problem with the heating in our room.",
        ),
        build(
            "build-indirect",
            "GRAMMAR",
            "Put the words in order.",
            "Could you tell me where the lost luggage office is?",
            ["grammar.indirect_questions", "vocab.luggage"],
            "Start with 'Could you tell me'.",
            "Could you tell me where the lost luggage office is?",
        ),
        choice(
            "read-vancouver",
            "READING",
            "Read the text. Then answer.",
            "What happened to the family's bags?",
            [
                ("They were sent to Vancouver by mistake.", "🧳"),
                ("They were stolen at the airport.", "🕵️"),
                ("They were left at home.", "🏠"),
            ],
            "a",
            ["vocab.luggage", "grammar.passive_all"],
            "Look at paragraph 4.",
            "The bags had been sent to Vancouver by mistake.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-delay",
            "READING",
            "Read the text. True or false?",
            "The flight was delayed because of the snow.",
            True,
            ["vocab.delay"],
            "Look at the first sentence.",
            "Our flight was delayed by four hours because of the snow.",
        ),
        speak(
            "say-airport",
            "Your train has been cancelled. Ask the station assistant three polite indirect questions and make a polite complaint.",
            "Excuse me, could you tell me … ? Do you know if … ? I'm afraid … I'd like to …",
            "Excuse me, could you tell me when the next train leaves? Do you know if I can use my ticket on it? I'm afraid this is the second time this week. I'd like to ask for a refund.",
            ["grammar.indirect_questions", "phrase.polite_complaint", "vocab.refund"],
        ),
        blank(
            "quiz-if-had-packed",
            "QUIZ",
            "Complete the sentence.",
            "If we had ___ a toothbrush in our hand luggage, we wouldn't ___ bought a new one.",
            ["packed", "have"],
            ["packed", "pack", "have", "had"],
            ["grammar.third_conditional"],
            "Remember Lesson 7.",
            "If we had packed a toothbrush, we wouldn't have bought a new one.",
        ),
        choice(
            "quiz-despite-delay",
            "QUIZ",
            "Choose the right linker.",
            "___ the delay, we arrived in a good mood.",
            [("Despite", None), ("Although", None), ("Whereas", None)],
            "a",
            ["grammar.contrast_linkers", "vocab.delay"],
            "Remember Lesson 6: + a noun.",
            "Despite the delay, we arrived in a good mood.",
        ),
        choice(
            "quiz-being-checked",
            "QUIZ",
            "Choose the right passive form.",
            "Please wait. Your passport ___ at the moment.",
            [("is being checked", None), ("is checking", None), ("has being checked", None)],
            "a",
            ["grammar.passive_all", "vocab.passport"],
            "Remember Unit 1, Lesson 5.",
            "Your passport is being checked.",
        ),
    ],
}

LESSON_9 = {
    "slug": L9,
    "title": "Festivals of the World",
    "description": "From lanterns to fireworks: the class presents festivals from around the world. A, an, the — or nothing?",
    "minutes": 35,
    "objectives": [
        "Use festival vocabulary: festival, tradition, lantern, parade, fireworks, celebrate.",
        "Use a / an, the and no article correctly.",
        "Describe how a festival is celebrated.",
    ],
    "review": [
        "grammar.indirect_questions",
        "vocab.delay",
        "vocab.passport",
        "grammar.third_conditional",
        "grammar.contrast_linkers",
        "vocab.custom",
        "vocab.culture",
        "grammar.passive_all",
        "grammar.relative_clauses",
        "vocab.birthday",
    ],
    "episode": (
        "A Sky Full of Lanterns",
        "Haruto sends a video of a lantern festival. The class decides to hold its own festival day.",
    ),
    "content": {
        "story_intro": "For International Week, every student in {boy}'s class presents a festival from another country.",
        "reading": {
            "title": "International Week",
            "paragraphs": [
                {
                    "sentences": [
                        "Haruto sent us a video of a summer festival in Osaka. The festival is famous for its fireworks.",
                        "In the video, people in traditional clothes were walking along the river with lanterns.",
                    ]
                },
                {
                    "sentences": [
                        "Maya presented Day of the Dead, a Mexican festival. It is a happy tradition, not a sad one.",
                        "Families decorate the graves with orange flowers and remember the people they love.",
                    ]
                },
                {
                    "sentences": [
                        "Sam talked about Diwali, the festival of light, which is celebrated in India and around the world.",
                        "People light candles and lamps, and children get sweets and new clothes.",
                    ]
                },
                {
                    "sentences": [
                        "I chose Carnival in Brazil. There is a huge parade in Rio, with music, dancing and amazing costumes.",
                        "The parade lasts all night!",
                    ]
                },
                {
                    "sentences": [
                        "At the end, our teacher asked: What do all festivals have in common?",
                        "{little}, who had come to watch, shouted: Food! And everybody laughed — because it's true.",
                    ]
                },
            ],
            "highlight": [
                "a video",
                "The festival",
                "a Mexican festival",
                "the festival of light",
                "a huge parade",
                "The parade",
                "fireworks",
                "lanterns",
                "tradition",
                "celebrated",
            ],
        },
        "listening": [
            {
                "id": "b2-9-newyear",
                "title": "How do you celebrate?",
                "transcript": [
                    {
                        "speaker": "Haruto",
                        "text": "In Japan, New Year is the most important holiday. We eat special food and visit a temple.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "We have fireworks at midnight, and people sing a song called Auld Lang Syne.",
                    },
                    {"speaker": "Haruto", "text": "Do you visit your family?"},
                    {
                        "speaker": "{boy}",
                        "text": "Yes, usually the grandparents come to us. It's a family tradition.",
                    },
                ],
            },
            {
                "id": "b2-9-lanterns",
                "title": "The lantern festival",
                "transcript": [
                    {
                        "speaker": "Maya",
                        "text": "Look, there's a lantern festival in the park on Saturday!",
                    },
                    {"speaker": "{boy}", "text": "Is it the one with the parade?"},
                    {
                        "speaker": "Maya",
                        "text": "Yes. The parade starts at six, and the lanterns are lit at eight.",
                    },
                    {"speaker": "{boy}", "text": "Great. I'll ask if {little} can come too."},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Articles: a / an, the, no article",
                "explanation": (
                    "a / an: one thing, mentioned for the first time, or a job: I saw a parade. She's an engineer. "
                    "the: something specific, already mentioned, or unique: The parade lasted all night. The Sun. The river in Osaka. "
                    "Also with superlatives: the most important holiday. "
                    "No article: plural or uncountable nouns in general: Children love festivals. Music makes people happy. "
                    "Most countries and cities have no article (Japan, Brazil), but: the UK, the USA."
                ),
                "explanation_ru": (
                    "a / an — один из многих, впервые упомянутый; the — конкретный, уже известный или единственный; "
                    "без артикля — о вещах вообще (во множественном числе или неисчисляемых)."
                ),
                "examples": [
                    "I bought a lantern. The lantern was red.",
                    "Fireworks are beautiful. The fireworks last night were amazing.",
                    "Diwali is celebrated in India and the UK.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "festival-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("lantern", None, "🏮"),
                ("fireworks", None, "🎆"),
                ("parade", None, "🎺"),
                ("festival", None, "🎉"),
            ],
            ["vocab.lantern", "vocab.fireworks", "vocab.parade", "vocab.festival"],
            "Fireworks light up the sky.",
            "lantern 🏮, fireworks 🎆, parade 🎺, festival 🎉.",
        ),
        matching(
            "festival-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("tradition", "something people have done in the same way for a long time", None),
                ("parade", "a line of people walking or dancing through the streets", None),
                ("celebrate", "do something special for an important day", None),
            ],
            ["vocab.tradition", "vocab.parade", "vocab.celebrate"],
            "We celebrate birthdays.",
            "tradition = done the same way for a long time; parade = a procession; celebrate = mark a special day.",
        ),
        choice(
            "find-lantern",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: lantern",
            [(None, "🎆"), (None, "🏮"), (None, "🎺")],
            "b",
            ["vocab.lantern"],
            "A light inside paper or glass.",
            "🏮 lantern.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-festival",
            "LISTENING",
            "Listen. What is the most important part of the festival?",
            "The most important part is …",
            [("the parade", "🎺"), ("the fireworks", "🎆"), ("the food", "🍲")],
            "c",
            ["grammar.articles", "vocab.festival"],
            "Listen for 'the most important'.",
            "The most important part is the food.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="There is a parade and there are fireworks, but for my family the most important part of the festival is the food.",
        ),
        true_false(
            "listen-newyear",
            "LISTENING",
            "Listen to Haruto and {boy}. True or false?",
            "In Japan, people visit a temple at New Year.",
            True,
            ["vocab.celebrate", "vocab.tradition"],
            "Listen to Haruto's first line.",
            "We eat special food and visit a temple.",
            listening_id="b2-9-newyear",
        ),
        true_false(
            "listen-lanterns-time",
            "LISTENING",
            "Listen to Maya and {boy}. True or false?",
            "The lanterns are lit at six.",
            False,
            ["vocab.lantern", "vocab.parade"],
            "What starts at six?",
            "The parade starts at six; the lanterns are lit at eight.",
            listening_id="b2-9-lanterns",
        ),
        blank(
            "article-blank",
            "GRAMMAR",
            "Choose the right articles.",
            "Yesterday I saw ___ parade. ___ parade was two kilometres long!",
            ["a", "The"],
            ["a", "an", "The", "—"],
            ["grammar.articles", "vocab.parade"],
            "First mention → a; second mention → the.",
            "I saw a parade. The parade was two kilometres long!",
        ),
        choice(
            "zero-article",
            "GRAMMAR",
            "Which sentence talks about festivals in general?",
            "Choose the correct sentence.",
            [
                ("Children love festivals.", None),
                ("The children love the festivals in general.", None),
                ("A children love a festivals.", None),
            ],
            "a",
            ["grammar.articles", "vocab.festival"],
            "Plural nouns in general → no article.",
            "Children love festivals. (in general → no article)",
        ),
        choice(
            "article-unique",
            "GRAMMAR",
            "Which sentence is correct?",
            "Talk about the sky at night.",
            [
                ("The fireworks were brighter than the Moon.", None),
                ("A fireworks were brighter than Moon.", None),
                ("The fireworks were brighter than a Moon.", None),
            ],
            "a",
            ["grammar.articles", "vocab.fireworks"],
            "There is only one Moon.",
            "The fireworks were brighter than the Moon.",
        ),
        choice(
            "article-countries",
            "GRAMMAR",
            "Which sentence is correct?",
            "Talk about where Diwali is celebrated.",
            [
                ("It is celebrated in India and the UK.", None),
                ("It is celebrated in the India and UK.", None),
                ("It is celebrated in an India and the UK.", None),
            ],
            "a",
            ["grammar.articles"],
            "Most countries have no article, but the UK, the USA.",
            "in India and the UK.",
        ),
        build(
            "build-article",
            "GRAMMAR",
            "Put the words in order.",
            "New Year is the most important festival in Japan.",
            ["grammar.articles", "vocab.festival"],
            "Superlatives use the.",
            "New Year is the most important festival in Japan.",
        ),
        choice(
            "read-day-dead",
            "READING",
            "Read the text. Then answer.",
            "What is true about Day of the Dead?",
            [
                ("It is a happy tradition when families remember people they love.", "🌼"),
                ("It is a sad festival with no music.", "😢"),
                ("It is celebrated only in Brazil.", "🇧🇷"),
            ],
            "a",
            ["vocab.tradition", "vocab.festival"],
            "Look at paragraph 2.",
            "It is a happy tradition; families remember the people they love.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-carnival",
            "READING",
            "Read the text. True or false?",
            "The Carnival parade in Rio lasts all night.",
            True,
            ["vocab.parade"],
            "Look at paragraph 4.",
            "The parade lasts all night!",
        ),
        speak(
            "say-festival",
            "Describe a festival you love. When is it? How is it celebrated? What is the best part?",
            "My favourite festival is … It is celebrated … People … The best part is …",
            "My favourite festival is New Year. It is celebrated on the 31st of December. People decorate a tree and watch the fireworks. The best part is the family dinner.",
            ["grammar.articles", "vocab.celebrate", "grammar.passive_all"],
        ),
        choice(
            "quiz-indirect-parade",
            "QUIZ",
            "Choose the correct indirect question.",
            "What time does the parade start?",
            [
                ("Do you know what time the parade starts?", None),
                ("Do you know what time does the parade start?", None),
                ("Do you know what time starts the parade?", None),
            ],
            "a",
            ["grammar.indirect_questions", "vocab.parade"],
            "Remember Lesson 8.",
            "Do you know what time the parade starts?",
        ),
        blank(
            "quiz-wish-there",
            "QUIZ",
            "Choose the right form.",
            "I wish I ___ in Rio for the Carnival right now!",
            ["were"],
            ["am", "were", "had been"],
            ["grammar.wish"],
            "Remember Lesson 7: a wish about now.",
            "I wish I were in Rio right now!",
        ),
        choice(
            "quiz-whereas-festival",
            "QUIZ",
            "Choose the right linker.",
            "Diwali is in autumn, ___ Carnival is in February or March.",
            [("whereas", None), ("despite", None), ("however", None)],
            "a",
            ["grammar.contrast_linkers", "vocab.festival"],
            "Remember Lesson 6.",
            "Diwali is in autumn, whereas Carnival is in February or March.",
        ),
    ],
}

LESSON_10 = {
    "slug": L10,
    "title": "The Debate Club",
    "description": "Should students have homework? {boy} prepares for his first debate. Then a big B2 review!",
    "minutes": 40,
    "objectives": [
        "Use debate vocabulary: debate, argument, opinion, evidence, persuade.",
        "Structure an argument: firstly, moreover, on the other hand, to sum up.",
        "Agree and disagree politely, and review all of B2.",
    ],
    "review": [
        "grammar.articles",
        "vocab.tradition",
        "vocab.celebrate",
        "grammar.indirect_questions",
        "grammar.third_conditional",
        "grammar.wish",
        "grammar.contrast_linkers",
        "grammar.passive_all",
        "grammar.gerund_infinitive",
        "grammar.present_perfect_continuous",
        "grammar.relative_clauses",
        "grammar.second_conditional",
    ],
    "episode": (
        "The Great Homework Debate",
        "{boy}'s team argues that homework should be banned. Their opponents are the best debaters in the school.",
    ),
    "content": {
        "story_intro": "{boy} has joined the debate club. His first topic: Homework should be banned.",
        "reading": {
            "title": "Should Homework Be Banned?",
            "paragraphs": [
                {
                    "sentences": [
                        "Our team had to argue that homework should be banned. To be honest, I liked the topic!",
                        "We had been preparing for two weeks and had collected a lot of evidence.",
                    ]
                },
                {
                    "sentences": [
                        "Firstly, I said that students need time to rest, play sport and see their families.",
                        "Moreover, a study we found showed that too much homework can cause stress.",
                    ]
                },
                {
                    "sentences": [
                        "The other team was very strong. Their captain said: I see your point, but homework helps us remember what we learn.",
                        "On the other hand, she agreed that some homework is boring and not useful.",
                    ]
                },
                {
                    "sentences": [
                        "To sum up, I suggested a compromise: homework should be short, creative and optional at weekends.",
                        "Even the other team said: We couldn't agree more!",
                    ]
                },
                {
                    "sentences": [
                        "We didn't win — the judges were persuaded by the other team's arguments.",
                        "But our teacher said that if we had had more time, we might have won. Next time!",
                    ]
                },
            ],
            "highlight": [
                "Firstly",
                "Moreover",
                "On the other hand",
                "To sum up",
                "I see your point, but",
                "couldn't agree more",
                "evidence",
                "arguments",
                "persuaded",
            ],
        },
        "listening": [
            {
                "id": "b2-10-debate",
                "title": "In the debate",
                "transcript": [
                    {
                        "speaker": "{boy}",
                        "text": "In my opinion, school should start at ten. Firstly, teenagers need more sleep.",
                    },
                    {
                        "speaker": "Captain",
                        "text": "I see your point, but what about parents who start work at eight?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "That's a fair question. However, the evidence shows that students learn better later in the day.",
                    },
                    {
                        "speaker": "Captain",
                        "text": "I'm afraid I don't agree. Moreover, buses would be more crowded.",
                    },
                ],
            },
            {
                "id": "b2-10-after",
                "title": "After the debate",
                "transcript": [
                    {"speaker": "{teen}", "text": "So, did your team persuade the judges?"},
                    {
                        "speaker": "{boy}",
                        "text": "Not this time. I wish we had found more evidence.",
                    },
                    {
                        "speaker": "{teen}",
                        "text": "If I had been there, I would have voted for you!",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "Thanks! Next month's topic is: Should robots replace teachers?",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Linking an argument",
                "explanation": (
                    "Order your points: Firstly, … Secondly, … Finally, … "
                    "Add a point: Moreover, … / In addition, … / What's more, … "
                    "Contrast: On the other hand, … / However, … "
                    "Give an example: For example, … / such as … "
                    "Conclude: To sum up, … / In conclusion, … "
                    "Give your opinion: In my opinion, … / I believe that … / It seems to me that …"
                ),
                "explanation_ru": (
                    "Связки для аргументации: во-первых (Firstly), кроме того (Moreover), с другой стороны (On the other hand), "
                    "подводя итог (To sum up)."
                ),
                "examples": [
                    "Firstly, homework helps us to practise.",
                    "Moreover, it teaches us to organise our time.",
                    "On the other hand, too much homework causes stress.",
                    "To sum up, homework should be short and useful.",
                ],
            },
            {
                "title": "Agreeing and disagreeing politely",
                "explanation": (
                    "Agree: I couldn't agree more. / That's a good point. / Exactly! "
                    "Partly agree: I see your point, but … / That may be true, but … "
                    "Disagree: I'm afraid I don't agree. / I'm not sure about that."
                ),
                "explanation_ru": "Вежливо соглашаемся и не соглашаемся: I see your point, but … — «Понимаю, но …».",
                "examples": [
                    "I see your point, but I think there's another side.",
                    "I couldn't agree more!",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "debate-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("debate", None, "🎤"),
                ("evidence", None, "📊"),
                ("opinion", None, "💭"),
                ("persuade", None, "🤝"),
            ],
            ["vocab.debate", "vocab.evidence", "vocab.opinion", "vocab.persuade"],
            "Evidence = facts and data.",
            "debate 🎤, evidence 📊, opinion 💭, persuade 🤝.",
        ),
        matching(
            "debate-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("argument", "a reason you give to support an idea", None),
                ("evidence", "facts that show something is true", None),
                ("persuade", "make someone agree with you", None),
            ],
            ["vocab.argument", "vocab.evidence", "vocab.persuade"],
            "A good argument needs evidence.",
            "argument = a supporting reason; evidence = facts; persuade = make someone agree.",
        ),
        choice(
            "find-evidence",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: evidence",
            [(None, "💭"), (None, "📊"), (None, "🎉")],
            "b",
            ["vocab.evidence"],
            "Facts, numbers and data.",
            "📊 evidence.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-opinion",
            "LISTENING",
            "Listen. What is the girl's opinion?",
            "She thinks that …",
            [
                ("mobile phones should be allowed at break time", "📱"),
                ("mobile phones should be banned completely", "🚫"),
                ("students should have more homework", "📚"),
            ],
            "a",
            ["vocab.opinion", "grammar.linking_arguments"],
            "Listen for 'In my opinion'.",
            "In my opinion, phones should be allowed at break time.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="In my opinion, phones should be allowed at break time. Firstly, we can call our parents. On the other hand, they shouldn't be used in lessons.",
        ),
        true_false(
            "listen-buses",
            "LISTENING",
            "Listen to the debate. True or false?",
            "The captain agrees that school should start at ten.",
            False,
            ["phrase.agree_disagree", "vocab.debate"],
            "Listen to her last line.",
            "I'm afraid I don't agree. Moreover, buses would be more crowded.",
            listening_id="b2-10-debate",
        ),
        true_false(
            "listen-robots-topic",
            "LISTENING",
            "Listen to {teen} and {boy}. True or false?",
            "Next month's topic is about robots and teachers.",
            True,
            ["vocab.debate", "vocab.robot"],
            "Listen to {boy}'s last line.",
            "Should robots replace teachers?",
            listening_id="b2-10-after",
        ),
        blank(
            "linkers-blank",
            "GRAMMAR",
            "Choose the right linkers.",
            "___, students need sleep. ___, tired students can't concentrate.",
            ["Firstly", "Moreover"],
            ["Firstly", "Moreover", "To sum up"],
            ["grammar.linking_arguments"],
            "First point, then an extra point.",
            "Firstly, students need sleep. Moreover, tired students can't concentrate.",
        ),
        choice(
            "conclude",
            "GRAMMAR",
            "Choose the best way to finish your speech.",
            "You want to give a conclusion.",
            [
                ("To sum up, homework should be short and useful.", None),
                ("Moreover, homework should be short and useful.", None),
                ("For example, homework should be short and useful.", None),
            ],
            "a",
            ["grammar.linking_arguments"],
            "Conclusion → To sum up / In conclusion.",
            "To sum up, homework should be short and useful.",
        ),
        choice(
            "partly-agree",
            "GRAMMAR",
            "Choose the polite way to partly disagree.",
            "Your opponent says: Homework is always useless.",
            [
                ("I see your point, but some homework is useful.", None),
                ("You're wrong. Stop talking.", None),
                ("I couldn't agree more.", None),
            ],
            "a",
            ["phrase.agree_disagree"],
            "Show respect, then disagree.",
            "I see your point, but some homework is useful.",
        ),
        choice(
            "on-the-other-hand",
            "GRAMMAR",
            "Choose the best linker.",
            "Phones help us learn. ___, they can be a distraction.",
            [("On the other hand", None), ("Firstly", None), ("For example", None)],
            "a",
            ["grammar.linking_arguments"],
            "The second idea contrasts with the first.",
            "On the other hand, they can be a distraction.",
        ),
        build(
            "build-opinion",
            "GRAMMAR",
            "Put the words in order.",
            "In my opinion, school should start later.",
            ["grammar.linking_arguments", "vocab.opinion"],
            "Start with 'In my opinion'.",
            "In my opinion, school should start later.",
        ),
        choice(
            "read-compromise",
            "READING",
            "Read the text. Then answer.",
            "What compromise did {boy} suggest?",
            [
                ("Homework should be short, creative and optional at weekends.", "📝"),
                ("Homework should be banned completely.", "🚫"),
                ("Homework should only be given in maths.", "➗"),
            ],
            "a",
            ["vocab.argument", "grammar.linking_arguments"],
            "Look at paragraph 4.",
            "Short, creative and optional at weekends.",
            ex_type="READING_COMPREHENSION",
        ),
        order(
            "read-order",
            "READING",
            "Put {boy}'s debate in order.",
            [
                "The team prepared for two weeks and collected evidence.",
                "{boy} said that students need time to rest.",
                "The other team's captain disagreed politely.",
                "{boy} suggested a compromise.",
                "The judges chose the other team.",
            ],
            ["vocab.evidence", "vocab.debate"],
            "Preparation comes first; the result comes last.",
            "Preparation → first point → reply → compromise → result.",
        ),
        speak(
            "say-debate",
            "Give a short speech: Should students wear school uniforms? Give your opinion, two arguments, a contrasting point and a conclusion.",
            "In my opinion, … Firstly, … Moreover, … On the other hand, … To sum up, …",
            "In my opinion, students should wear uniforms. Firstly, they save time in the morning. Moreover, nobody feels poorer than others. On the other hand, uniforms can be expensive. To sum up, uniforms are a good idea if they are cheap.",
            ["grammar.linking_arguments", "phrase.agree_disagree"],
        ),
        choice(
            "quiz-if-had-time",
            "QUIZ",
            "Choose the correct sentence.",
            "The team didn't have enough time, so they lost.",
            [
                ("If they had had more time, they might have won.", None),
                ("If they had more time, they won.", None),
                ("If they have more time, they would have won.", None),
            ],
            "a",
            ["grammar.third_conditional"],
            "Remember Lesson 7: the past → third conditional.",
            "If they had had more time, they might have won.",
        ),
        blank(
            "quiz-wish-evidence",
            "QUIZ",
            "Choose the right form.",
            "I wish we ___ found more evidence.",
            ["had"],
            ["had", "have", "would"],
            ["grammar.wish", "vocab.evidence"],
            "Remember Lesson 7: a regret about the past.",
            "I wish we had found more evidence.",
        ),
        choice(
            "quiz-indirect-judges",
            "QUIZ",
            "Choose the correct indirect question.",
            "Why did the judges choose the other team?",
            [
                ("Could you tell me why the judges chose the other team?", None),
                ("Could you tell me why did the judges choose the other team?", None),
                ("Could you tell me why the judges did choose the other team?", None),
            ],
            "a",
            ["grammar.indirect_questions", "vocab.judge"],
            "Remember Lesson 8.",
            "Could you tell me why the judges chose the other team?",
        ),
        blank(
            "quiz-although-lost",
            "QUIZ",
            "Choose the right linker.",
            "___ we lost, it was a great experience.",
            ["Although"],
            ["Although", "Despite", "However"],
            ["grammar.contrast_linkers"],
            "Remember Lesson 6.",
            "Although we lost, it was a great experience.",
        ),
        blank(
            "quiz-article-debate",
            "QUIZ",
            "Choose the right articles.",
            "We had ___ debate yesterday. ___ debate was about homework.",
            ["a", "The"],
            ["a", "an", "The"],
            ["grammar.articles", "vocab.debate"],
            "Remember Lesson 9: first mention, then second mention.",
            "We had a debate yesterday. The debate was about homework.",
        ),
        choice(
            "quiz-passive-chosen",
            "QUIZ",
            "Choose the right passive form.",
            "The next topic ___ by the students next week.",
            [("will be chosen", None), ("will choose", None), ("is chose", None)],
            "a",
            ["grammar.passive_all"],
            "Remember Unit 1, Lesson 5.",
            "The next topic will be chosen by the students.",
        ),
        blank(
            "quiz-ppc-preparing",
            "QUIZ",
            "Complete the sentence.",
            "We have ___ preparing ___ two weeks.",
            ["been", "for"],
            ["been", "being", "for", "since"],
            ["grammar.present_perfect_continuous"],
            "Remember Unit 1, Lesson 3.",
            "We have been preparing for two weeks.",
        ),
        choice(
            "quiz-second-robots",
            "QUIZ",
            "Choose the correct sentence.",
            "Imagine robots were our teachers.",
            [
                ("If robots taught us, lessons would be very different.", None),
                ("If robots teach us, lessons would be very different.", None),
                ("If robots taught us, lessons will be very different.", None),
            ],
            "a",
            ["grammar.second_conditional", "vocab.robot"],
            "Remember Unit 1, Lesson 1.",
            "If robots taught us, lessons would be very different.",
        ),
        choice(
            "quiz-persuade",
            "QUIZ",
            "Choose the right word.",
            "The other team ___ the judges with strong arguments.",
            [("persuaded", None), ("celebrated", None), ("cancelled", None)],
            "a",
            ["vocab.persuade", "vocab.argument"],
            "They made the judges agree.",
            "The other team persuaded the judges.",
        ),
    ],
}

UNIT = {
    "slug": "around-the-world",
    "title": "Around the World",
    "description": "Pen friends in Japan, an exchange year in Canada, travel troubles, world festivals and a debate.",
    "lessons": [LESSON_6, LESSON_7, LESSON_8, LESSON_9, LESSON_10],
}
