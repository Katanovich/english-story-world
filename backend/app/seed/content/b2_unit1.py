"""B2 · Unit 1 "Explorers of Science" (B2 lessons 1-5).

{boy} is fourteen and his school runs a science fortnight. Topics: space, robots, climate
and weather, health, an invention fair. Grammar: the second conditional, defining and
non-defining relative clauses, the present perfect continuous, gerunds vs infinitives,
the passive in all tenses. Lesson 5 reviews the unit.
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
    "space-week",
    "robots-and-us",
    "the-weather-station",
    "healthy-choices",
    "the-invention-fair",
)

ITEMS: dict[str, Item] = {
    # Lesson 1
    "vocab.planet": (
        V,
        "planet",
        "🪐",
        "планета",
        L1,
        ["Mars is the fourth planet from the Sun."],
        None,
    ),
    "vocab.astronaut": (
        V,
        "astronaut",
        "🧑‍🚀",
        "космонавт, астронавт",
        L1,
        ["If I were an astronaut, I'd go to Mars."],
        None,
    ),
    "vocab.telescope": (
        V,
        "telescope",
        "🔭",
        "телескоп",
        L1,
        ["We looked at the Moon through a telescope."],
        None,
    ),
    "vocab.orbit": (
        V,
        "orbit",
        "🛰️",
        "орбита; вращаться по орбите",
        L1,
        ["The Moon orbits the Earth."],
        None,
    ),
    "vocab.gravity": (
        V,
        "gravity",
        "🍎",
        "гравитация",
        L1,
        ["Gravity keeps us on the ground."],
        None,
    ),
    "vocab.galaxy": (
        V,
        "galaxy",
        "🌌",
        "галактика",
        L1,
        ["Our galaxy is called the Milky Way."],
        None,
    ),
    "grammar.second_conditional": (
        G,
        "If I had …, I would …",
        None,
        "Условные предложения 2 типа: если бы …, то …",
        L1,
        [
            "If I had a telescope, I would watch the stars every night.",
            "If I were an astronaut, I'd visit Mars.",
        ],
        "If + past simple, would + verb. For imaginary or unlikely situations in the present or future.",
    ),
    # Lesson 2
    "vocab.robot": (V, "robot", "🤖", "робот", L2, ["The robot can clean the floor."], None),
    "vocab.device": (V, "device", "📱", "устройство", L2, ["A phone is a small device."], None),
    "vocab.battery": (
        V,
        "battery",
        "🔋",
        "аккумулятор, батарейка",
        L2,
        ["The battery is almost empty."],
        None,
    ),
    "vocab.ai": (
        V,
        "artificial intelligence (AI)",
        "🧠",
        "искусственный интеллект",
        L2,
        ["AI helps doctors find illnesses."],
        None,
    ),
    "vocab.program": (
        V,
        "program",
        "💻",
        "программировать; программа",
        L2,
        ["We programmed the robot to dance."],
        None,
    ),
    "vocab.sensor": (
        V,
        "sensor",
        "📡",
        "датчик",
        L2,
        ["The sensor notices when someone comes in."],
        None,
    ),
    "grammar.relative_clauses": (
        G,
        "who / which / that / where / whose",
        None,
        "Придаточные определительные: который, где, чей",
        L2,
        ["This is the robot that cleans the floor.", "Mr Lee, who teaches IT, built it."],
        "Defining clauses give necessary information (no commas). Non-defining clauses add extra information (with commas, no that).",
    ),
    # Lesson 3
    "vocab.climate": (V, "climate", "🌡️", "климат", L3, ["The climate is getting warmer."], None),
    "vocab.temperature": (
        V,
        "temperature",
        "🌡️",
        "температура",
        L3,
        ["The temperature has been rising all week."],
        None,
    ),
    "vocab.forecast": (
        V,
        "forecast",
        "📺",
        "прогноз",
        L3,
        ["The forecast says it will snow."],
        None,
    ),
    "vocab.flood": (V, "flood", "🌊", "наводнение", L3, ["The flood damaged many houses."], None),
    "vocab.drought": (
        V,
        "drought",
        "🏜️",
        "засуха",
        L3,
        ["There has been a drought for months."],
        None,
    ),
    "vocab.measure": (
        V,
        "measure",
        "📏",
        "измерять",
        L3,
        ["We measure the rain every morning."],
        None,
    ),
    "grammar.present_perfect_continuous": (
        G,
        "I have been doing … (for / since)",
        None,
        "Present perfect continuous: делаю уже какое-то время",
        L3,
        [
            "It has been raining for three days.",
            "We have been measuring the temperature since May.",
        ],
        "have / has been + verb-ing for an action that started in the past and is still going on (or has just stopped).",
    ),
    # Lesson 4
    "vocab.diet": (
        V,
        "diet",
        "🥗",
        "питание, рацион",
        L4,
        ["A balanced diet keeps you healthy."],
        None,
    ),
    "vocab.habit": (V, "habit", "🔁", "привычка", L4, ["Going to bed late is a bad habit."], None),
    "vocab.vitamins": (
        V,
        "vitamins",
        "💊",
        "витамины",
        L4,
        ["Oranges are full of vitamins."],
        None,
    ),
    "vocab.fitness": (
        V,
        "fitness",
        "🏋️",
        "физическая форма",
        L4,
        ["Swimming is great for fitness."],
        None,
    ),
    "vocab.avoid": (
        V,
        "avoid",
        "🚫",
        "избегать",
        L4,
        ["Try to avoid eating too much sugar."],
        None,
    ),
    "vocab.balanced": (
        V,
        "balanced",
        "⚖️",
        "сбалансированный",
        L4,
        ["Eat a balanced breakfast."],
        None,
    ),
    "grammar.gerund_infinitive": (
        G,
        "enjoy doing / decide to do",
        None,
        "Герундий или инфинитив после глаголов",
        L4,
        ["I enjoy swimming.", "She decided to eat more vegetables.", "Stop eating sweets!"],
        "Some verbs take -ing (enjoy, avoid, finish, mind); others take to + verb (decide, want, hope, plan).",
    ),
    # Lesson 5
    "vocab.invention": (
        V,
        "invention",
        "💡",
        "изобретение",
        L5,
        ["The wheel is an old invention."],
        None,
    ),
    "vocab.prototype": (V, "prototype", "🛠️", "прототип", L5, ["This is only a prototype."], None),
    "vocab.judge": (
        V,
        "judge",
        "🧑‍⚖️",
        "судья, член жюри",
        L5,
        ["The judges liked our project."],
        None,
    ),
    "vocab.solar_panel": (
        V,
        "solar panel",
        "☀️",
        "солнечная панель",
        L5,
        ["The solar panel charges the battery."],
        None,
    ),
    "vocab.prize": (V, "prize", "🏆", "приз", L5, ["We won first prize!"], None),
    "grammar.passive_all": (
        G,
        "is being made / has been made / will be made",
        None,
        "Страдательный залог во всех временах",
        L5,
        [
            "The robot is being tested.",
            "The prize has been won by Class 9B.",
            "The winners will be announced at five.",
        ],
        "be (in any tense) + past participle: is being built, has been built, will be built, can be built.",
    ),
    "phrase.presenting": (
        P,
        "Let me show you … / As you can see, …",
        None,
        "Позвольте показать … / Как вы видите, …",
        L5,
        ["Let me show you how it works.", "As you can see, the light turns on."],
        "Useful phrases for presenting a project.",
    ),
}


LESSON_1 = {
    "slug": L1,
    "title": "Space Week",
    "description": "It's Space Week at school. What would you do if you were an astronaut?",
    "minutes": 35,
    "objectives": [
        "Use space vocabulary: planet, orbit, gravity, galaxy, telescope, astronaut.",
        "Talk about imaginary situations with the second conditional.",
        "Compare the first and second conditionals.",
    ],
    "review": [
        "grammar.reported_speech",
        "vocab.newspaper",
        "vocab.article",
        "grammar.first_conditional",
        "grammar.present_perfect",
        "grammar.will_going_to",
        "vocab.scientist",
        "vocab.discover",
        "grammar.comparatives",
        "grammar.would_like",
    ],
    "episode": (
        "A Night Under the Stars",
        "{boy}'s class spends an evening at the observatory. Through a telescope, Saturn is real!",
    ),
    "content": {
        "story_intro": "{boy} is fourteen now. This week his school is celebrating Space Week.",
        "reading": {
            "title": "If I Were an Astronaut …",
            "paragraphs": [
                {
                    "sentences": [
                        "On Monday a real astronaut visited our school and told us about life in orbit.",
                        "Because there is almost no gravity, she slept in a sleeping bag tied to the wall!",
                    ]
                },
                {
                    "sentences": [
                        "Then our teacher asked us to write an essay: What would you do if you were an astronaut?",
                        "Most of my friends said they would go to Mars.",
                    ]
                },
                {
                    "sentences": [
                        "I wrote that if I went into space, I would take a powerful telescope.",
                        "If I had one up there, I could see other galaxies much more clearly.",
                    ]
                },
                {
                    "sentences": [
                        "My friend Sam was more practical. He wrote: If I lived on the space station, I would miss my mum's pizza.",
                        "Everybody laughed, but the astronaut said she had felt exactly the same!",
                    ]
                },
                {
                    "sentences": [
                        "On Friday night we visited the observatory and looked at Saturn.",
                        "The sky was perfectly clear, so we could see its rings.",
                    ]
                },
            ],
            "highlight": [
                "would",
                "if you were",
                "If I went",
                "If I had",
                "If I lived",
                "orbit",
                "gravity",
                "telescope",
                "galaxies",
            ],
        },
        "listening": [
            {
                "id": "b2-1-mars",
                "title": "Would you go to Mars?",
                "transcript": [
                    {
                        "speaker": "{teen}",
                        "text": "If someone offered you a ticket to Mars, would you go?",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "Only if I could come back! The journey takes about seven months.",
                    },
                    {
                        "speaker": "{teen}",
                        "text": "I wouldn't go. If I were on Mars, I'd be bored without my friends.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "You could video-call them — but the messages would take twenty minutes!",
                    },
                ],
            },
            {
                "id": "b2-1-real",
                "title": "Real or imaginary?",
                "transcript": [
                    {
                        "speaker": "Teacher",
                        "text": "If the weather is clear tonight, we will go to the observatory.",
                    },
                    {"speaker": "{boy}", "text": "And if it's cloudy?"},
                    {
                        "speaker": "Teacher",
                        "text": "Then we'll watch a film about the planets instead.",
                    },
                    {
                        "speaker": "{boy}",
                        "text": "If I had my own observatory, I'd never watch films about stars!",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "The second conditional",
                "explanation": (
                    "Use it for imaginary, impossible or unlikely situations now or in the future. "
                    "If + past simple, would / could + verb. If I had a telescope, I would watch the stars. "
                    "With be we often use were for all persons: If I were an astronaut … "
                    "The past tense here does not mean the past — it means 'not real'."
                ),
                "explanation_ru": (
                    "Если бы …, то … (воображаемая ситуация). If + past simple, would + глагол: "
                    "If I had a telescope, I would watch the stars = Если бы у меня был телескоп, я бы смотрел на звёзды."
                ),
                "examples": [
                    "If I were you, I'd study astronomy.",
                    "What would you do if you met an alien?",
                    "If we lived on the Moon, we could jump very high.",
                ],
            },
            {
                "title": "First or second conditional?",
                "explanation": (
                    "First conditional = a real possibility: If it is clear tonight, we will see Saturn. "
                    "Second conditional = imaginary or very unlikely: If I lived on Saturn, I would have very long winters."
                ),
                "explanation_ru": "1 тип — реально возможно; 2 тип — нереально или маловероятно.",
                "examples": [
                    "If I finish early, I'll call you. (real)",
                    "If I won a million, I'd buy a spaceship. (imaginary)",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "space-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("planet", None, "🪐"),
                ("astronaut", None, "🧑‍🚀"),
                ("telescope", None, "🔭"),
                ("galaxy", None, "🌌"),
            ],
            ["vocab.planet", "vocab.astronaut", "vocab.telescope", "vocab.galaxy"],
            "Saturn is a planet with rings.",
            "planet 🪐, astronaut 🧑‍🚀, telescope 🔭, galaxy 🌌.",
        ),
        matching(
            "space-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("gravity", "the force that pulls things towards the ground", None),
                ("orbit", "the path of an object moving around a planet or star", None),
                ("galaxy", "a huge group of stars", None),
            ],
            ["vocab.gravity", "vocab.orbit", "vocab.galaxy"],
            "An apple falls because of gravity.",
            "gravity = the force that pulls things down; orbit = a path around a planet; galaxy = a huge group of stars.",
        ),
        choice(
            "find-orbit",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: something in orbit around the Earth",
            [(None, "🛰️"), (None, "🔭"), (None, "🌋")],
            "a",
            ["vocab.orbit"],
            "Satellites travel around the Earth.",
            "🛰️ a satellite in orbit.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-would-do",
            "LISTENING",
            "Listen. What would the girl do if she could travel into space?",
            "She would …",
            [("take photos of the Earth", "📸"), ("live on Mars", "🔴"), ("become a pilot", "✈️")],
            "a",
            ["grammar.second_conditional"],
            "Listen for 'I would'.",
            "If I could travel into space, I would take photos of the Earth.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="If I could travel into space, I wouldn't want to land anywhere. I would just take photos of the Earth from orbit.",
        ),
        true_false(
            "listen-teen-mars",
            "LISTENING",
            "Listen to {teen} and {boy}. True or false?",
            "{teen} would like to go to Mars.",
            False,
            ["grammar.second_conditional", "vocab.planet"],
            "Why wouldn't she go?",
            "{teen}: I wouldn't go. If I were on Mars, I'd be bored without my friends.",
            listening_id="b2-1-mars",
        ),
        true_false(
            "listen-cloudy",
            "LISTENING",
            "Listen to the teacher and {boy}. True or false?",
            "If it's cloudy, the class will watch a film.",
            True,
            ["grammar.first_conditional"],
            "Listen to the teacher's second answer.",
            "Then we'll watch a film about the planets instead.",
            listening_id="b2-1-real",
        ),
        blank(
            "second-cond-blank",
            "GRAMMAR",
            "Complete the second conditional.",
            "If I ___ a telescope, I ___ look at the stars every night.",
            ["had", "would"],
            ["have", "had", "will", "would"],
            ["grammar.second_conditional", "vocab.telescope"],
            "If + past simple, would + verb.",
            "If I had a telescope, I would look at the stars every night.",
        ),
        blank(
            "were-blank",
            "GRAMMAR",
            "Choose the best form.",
            "If I ___ you, I'd study physics.",
            ["were"],
            ["am", "were", "will be"],
            ["grammar.second_conditional"],
            "Advice: If I were you …",
            "If I were you, I'd study physics.",
        ),
        choice(
            "first-or-second",
            "GRAMMAR",
            "Which sentence is about an imaginary situation?",
            "Choose the second conditional.",
            [
                ("If I lived on the Moon, I would weigh much less.", None),
                ("If it is clear tonight, we will see Saturn.", None),
                ("If you heat ice, it melts.", None),
            ],
            "a",
            ["grammar.second_conditional", "grammar.first_conditional", "vocab.gravity"],
            "Nobody really lives on the Moon.",
            "If I lived on the Moon, I would weigh much less. (imaginary → second conditional)",
        ),
        choice(
            "cond-meaning",
            "GRAMMAR",
            "What does the sentence mean?",
            "If I had more time, I would join the astronomy club.",
            [
                ("I don't have much time, so I'm not joining.", None),
                ("I have a lot of time and I'm joining.", None),
                ("I joined the club last year.", None),
            ],
            "a",
            ["grammar.second_conditional"],
            "The past simple after if means 'not real'.",
            "In reality I don't have enough time, so I'm not joining.",
        ),
        build(
            "build-second",
            "GRAMMAR",
            "Put the words in order.",
            "What would you do if you met an alien?",
            ["grammar.second_conditional"],
            "Start with 'What would you do'.",
            "What would you do if you met an alien?",
        ),
        choice(
            "read-sleep",
            "READING",
            "Read the text. Then answer.",
            "Why did the astronaut sleep in a bag tied to the wall?",
            [
                ("Because there is almost no gravity in orbit.", "🍎"),
                ("Because the beds were too small.", "🛏️"),
                ("Because it was very cold.", "🥶"),
            ],
            "a",
            ["vocab.gravity", "vocab.orbit"],
            "Look at paragraph 1.",
            "There is almost no gravity, so she would float away!",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-saturn",
            "READING",
            "Read the text. True or false?",
            "The class couldn't see Saturn's rings because of the clouds.",
            False,
            ["vocab.planet", "vocab.telescope"],
            "Look at the last paragraph.",
            "The sky was clear and perfect, so they saw the rings.",
        ),
        speak(
            "say-imagine",
            "Answer the questions: What would you do if you were an astronaut? Where would you go if you could travel anywhere in the universe?",
            "If I were an astronaut, I would … If I could go anywhere, I'd …",
            "If I were an astronaut, I would live on the space station and do experiments. If I could go anywhere, I'd visit another galaxy.",
            ["grammar.second_conditional", "vocab.astronaut"],
        ),
        choice(
            "quiz-reported-astronaut",
            "QUIZ",
            "Report the astronaut's words.",
            "'I miss pizza in space.'",
            [
                ("She said that she missed pizza in space.", None),
                ("She said that I miss pizza in space.", None),
                ("She told that she misses pizza in space.", None),
            ],
            "a",
            ["grammar.reported_speech"],
            "Remember B1, Lesson 10: miss → missed.",
            "She said that she missed pizza in space.",
        ),
        blank(
            "quiz-pp-been-space",
            "QUIZ",
            "Choose the missing words.",
            "Only about six hundred people have ___ ___ into space.",
            ["ever", "been"],
            ["ever", "yet", "been", "went"],
            ["grammar.ever_never", "grammar.present_perfect"],
            "Remember B1: have ever been.",
            "Only about six hundred people have ever been into space.",
        ),
        choice(
            "quiz-farther",
            "QUIZ",
            "Choose the right word.",
            "Mars is ___ from the Sun than the Earth.",
            [("farther", None), ("more far", None), ("farer", None)],
            "a",
            ["grammar.comparatives", "vocab.planet"],
            "Remember: far → farther / further.",
            "Mars is farther from the Sun than the Earth.",
        ),
    ],
}

LESSON_2 = {
    "slug": L2,
    "title": "Robots and Us",
    "description": "The IT club builds a robot. Who, which, that, whose — let's describe it!",
    "minutes": 35,
    "objectives": [
        "Use technology vocabulary: robot, device, sensor, battery, program, AI.",
        "Use defining relative clauses: the robot that cleans the floor.",
        "Add extra information with non-defining clauses and commas.",
    ],
    "review": [
        "grammar.second_conditional",
        "vocab.astronaut",
        "vocab.telescope",
        "grammar.passive_present",
        "grammar.used_to",
        "vocab.nowadays",
        "vocab.experiment",
        "grammar.should",
        "vocab.museum",
        "grammar.prefer",
    ],
    "episode": (
        "Robo-Rex",
        "The IT club builds a small robot dog. It works perfectly — until it meets the real dog next door.",
    ),
    "content": {
        "story_intro": "{boy} has joined the IT club. This term the club is building a robot.",
        "reading": {
            "title": "Meet Robo-Rex",
            "paragraphs": [
                {
                    "sentences": [
                        "Robo-Rex is a robot dog that our IT club has built.",
                        "Mr Lee, who teaches computer science, helped us with the difficult parts.",
                    ]
                },
                {
                    "sentences": [
                        "It has a sensor which notices people and objects in front of it.",
                        "When the battery is low, it walks back to the place where it charges.",
                    ]
                },
                {
                    "sentences": [
                        "Maya, whose dad is an engineer, programmed it to bark and wag its tail.",
                        "The program that she wrote uses simple AI, so Robo-Rex learns our voices.",
                    ]
                },
                {
                    "sentences": [
                        "Last week we took it to my house, where our neighbour's real dog, Biscuit, lives.",
                        "Biscuit, who is usually very friendly, barked at Robo-Rex for ten minutes!",
                    ]
                },
                {
                    "sentences": [
                        "Robots used to be something people only saw in films.",
                        "Nowadays they are devices that we use every day — but Biscuit doesn't agree yet.",
                    ]
                },
            ],
            "highlight": [
                "that",
                "who",
                "which",
                "where",
                "whose",
                "robot",
                "sensor",
                "battery",
                "programmed",
                "AI",
            ],
        },
        "listening": [
            {
                "id": "b2-2-club",
                "title": "In the IT club",
                "transcript": [
                    {"speaker": "Mr Lee", "text": "Who's the student who wrote this program?"},
                    {"speaker": "Maya", "text": "That's me. It's the program that makes Rex bark."},
                    {"speaker": "Mr Lee", "text": "Excellent. And which sensor did you use?"},
                    {
                        "speaker": "Maya",
                        "text": "The one which my dad gave me. It can see up to two metres.",
                    },
                ],
            },
            {
                "id": "b2-2-future",
                "title": "Robots at home",
                "transcript": [
                    {"speaker": "{boy}", "text": "Would you like a robot that does your homework?"},
                    {"speaker": "{teen}", "text": "No! I'd like a robot which cleans my room."},
                    {
                        "speaker": "{boy}",
                        "text": "Granny {gran1}, who hates cooking, wants a robot chef.",
                    },
                    {"speaker": "{teen}", "text": "And Dad wants one that finds his keys!"},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Defining relative clauses",
                "explanation": (
                    "They tell us exactly which person or thing we mean. No commas. "
                    "who / that for people, which / that for things, where for places, whose for possession. "
                    "This is the robot that cleans the floor. She's the girl whose dad is an engineer. "
                    "You can leave out who / which / that when it is the object: the program (that) she wrote."
                ),
                "explanation_ru": (
                    "Определительные придаточные (без запятых): который (who/that — люди, which/that — вещи), "
                    "где (where), чей (whose)."
                ),
                "examples": [
                    "A sensor is a device that notices movement.",
                    "That's the room where we charge the robot.",
                    "The boy who built it is my brother.",
                ],
            },
            {
                "title": "Non-defining relative clauses",
                "explanation": (
                    "They add extra information about someone or something we already know. Use commas. "
                    "You cannot use that, and you cannot leave out the pronoun. "
                    "Mr Lee, who teaches IT, helped us. Robo-Rex, which cost £50, is our best project."
                ),
                "explanation_ru": "Неопределительные придаточные — дополнительная информация, выделяется запятыми; that нельзя.",
                "examples": [
                    "My sister, who is sixteen, loves robots.",
                    "Paris, where my aunt lives, is beautiful.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "tech-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("robot", None, "🤖"),
                ("battery", None, "🔋"),
                ("sensor", None, "📡"),
                ("device", None, "📱"),
            ],
            ["vocab.robot", "vocab.battery", "vocab.sensor", "vocab.device"],
            "A battery gives a device power.",
            "robot 🤖, battery 🔋, sensor 📡, device 📱.",
        ),
        matching(
            "tech-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("sensor", "a part that notices light, heat or movement", None),
                ("program", "give a computer instructions", None),
                (
                    "artificial intelligence (AI)",
                    "computers that can learn and make decisions",
                    None,
                ),
            ],
            ["vocab.sensor", "vocab.program", "vocab.ai"],
            "You write code to program a robot.",
            "sensor = notices things; program = give instructions; AI = computers that learn.",
        ),
        choice(
            "find-battery",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: battery",
            [(None, "📡"), (None, "🔋"), (None, "🤖")],
            "b",
            ["vocab.battery"],
            "It stores energy.",
            "🔋 battery.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-whose",
            "LISTENING",
            "Listen. Who is Tom?",
            "Tom is the boy …",
            [
                ("whose robot won the competition", "🏆"),
                ("who broke the robot", "💥"),
                ("who teaches IT", "🧑‍🏫"),
            ],
            "a",
            ["grammar.relative_clauses", "vocab.robot"],
            "Listen for 'whose'.",
            "Tom is the boy whose robot won the competition.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Do you see the tall boy over there? That's Tom, the boy whose robot won the city competition last year.",
        ),
        true_false(
            "listen-maya-program",
            "LISTENING",
            "Listen to Mr Lee and Maya. True or false?",
            "Maya wrote the program that makes Rex bark.",
            True,
            ["grammar.relative_clauses", "vocab.program"],
            "Who says 'That's me'?",
            "Maya: It's the program that makes Rex bark.",
            listening_id="b2-2-club",
        ),
        true_false(
            "listen-teen-robot",
            "LISTENING",
            "Listen to {boy} and {teen}. True or false?",
            "{teen} wants a robot that does her homework.",
            False,
            ["grammar.relative_clauses", "vocab.robot"],
            "What kind of robot would {teen} like?",
            "She'd like a robot which cleans her room.",
            listening_id="b2-2-future",
        ),
        blank(
            "relative-blank",
            "GRAMMAR",
            "Choose the right relative pronouns.",
            "Maya, ___ dad is an engineer, built a robot ___ can dance.",
            ["whose", "that"],
            ["who", "whose", "that", "where"],
            ["grammar.relative_clauses"],
            "Her dad → whose; a thing → that / which.",
            "Maya, whose dad is an engineer, built a robot that can dance.",
        ),
        blank(
            "where-blank",
            "GRAMMAR",
            "Choose the right relative pronoun.",
            "This is the lab ___ we test our robots.",
            ["where"],
            ["where", "which", "who"],
            ["grammar.relative_clauses"],
            "A place → where.",
            "This is the lab where we test our robots.",
        ),
        choice(
            "non-defining",
            "GRAMMAR",
            "Which sentence is correct?",
            "Add extra information about Mr Lee.",
            [
                ("Mr Lee, who teaches IT, helped us.", None),
                ("Mr Lee, that teaches IT, helped us.", None),
                ("Mr Lee who teaches IT, helped us.", None),
            ],
            "a",
            ["grammar.relative_clauses"],
            "Non-defining: commas and no that.",
            "Mr Lee, who teaches IT, helped us.",
        ),
        choice(
            "leave-out",
            "GRAMMAR",
            "In which sentence can you leave out the relative pronoun?",
            "Choose one.",
            [
                ("The program that she wrote is clever.", None),
                ("The robot that cleans the floor is new.", None),
                ("Mr Lee, who teaches IT, is kind.", None),
            ],
            "a",
            ["grammar.relative_clauses", "vocab.program"],
            "You can leave it out when it is the object of the clause.",
            "The program (that) she wrote is clever — 'she' is the subject, so 'that' can go.",
        ),
        build(
            "build-relative",
            "GRAMMAR",
            "Put the words in order.",
            "A sensor is a device that notices movement.",
            ["grammar.relative_clauses", "vocab.sensor", "vocab.device"],
            "Start with 'A sensor is'.",
            "A sensor is a device that notices movement.",
        ),
        choice(
            "read-battery",
            "READING",
            "Read the text. Then answer.",
            "What does Robo-Rex do when its battery is low?",
            [
                ("It walks back to the place where it charges.", "🔌"),
                ("It barks until someone helps.", "🐕"),
                ("It switches off immediately.", "📴"),
            ],
            "a",
            ["vocab.battery", "grammar.relative_clauses"],
            "Look at paragraph 2.",
            "It walks back to the place where it charges.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-biscuit",
            "READING",
            "Read the text. True or false?",
            "Biscuit, the neighbour's dog, liked Robo-Rex immediately.",
            False,
            ["vocab.neighbour", "vocab.robot"],
            "Look at paragraph 4.",
            "Biscuit barked at Robo-Rex for ten minutes!",
        ),
        speak(
            "say-robot",
            "Describe a robot you would like to have. Use who, which, that or whose.",
            "I'd like a robot that … It would have a sensor which … It would help people who …",
            "I'd like a robot that cooks dinner. It would have a sensor which notices when the food is ready. It would help people who are too busy to cook.",
            ["grammar.relative_clauses", "grammar.second_conditional"],
        ),
        blank(
            "quiz-if-had-robot",
            "QUIZ",
            "Complete the sentence.",
            "If I ___ a robot, it ___ tidy my room.",
            ["had", "would"],
            ["had", "have", "would", "will"],
            ["grammar.second_conditional", "vocab.robot"],
            "Remember Lesson 1: imaginary situation.",
            "If I had a robot, it would tidy my room.",
        ),
        choice(
            "quiz-used-to-films",
            "QUIZ",
            "Choose the right sentence.",
            "Fifty years ago …",
            [
                ("people used to see robots only in films.", None),
                ("people use to see robots only in films.", None),
                ("people were used see robots only in films.", None),
            ],
            "a",
            ["grammar.used_to"],
            "Remember B1, Lesson 7.",
            "People used to see robots only in films.",
        ),
        choice(
            "quiz-made-in",
            "QUIZ",
            "Choose the right sentence.",
            "Factories in Japan make many robots.",
            [
                ("Many robots are made in Japan.", None),
                ("Many robots make in Japan.", None),
                ("Many robots are make in Japan.", None),
            ],
            "a",
            ["grammar.passive_present", "vocab.robot"],
            "Remember B1, Lesson 8: are + past participle.",
            "Many robots are made in Japan.",
        ),
    ],
}

LESSON_3 = {
    "slug": L3,
    "title": "The Weather Station",
    "description": "The school weather station has been collecting data for months. What has been happening?",
    "minutes": 35,
    "objectives": [
        "Use climate words: climate, temperature, forecast, flood, drought, measure.",
        "Use the present perfect continuous with for and since.",
        "Choose between the present perfect simple and continuous.",
    ],
    "review": [
        "grammar.relative_clauses",
        "vocab.sensor",
        "vocab.device",
        "grammar.second_conditional",
        "vocab.environment",
        "vocab.pollution",
        "grammar.present_perfect",
        "grammar.just_already",
        "vocab.rainy",
        "vocab.hot",
    ],
    "episode": (
        "Storm Warning",
        "The school weather station shows that a big storm is coming. {boy}'s team has to warn the town.",
    ),
    "content": {
        "story_intro": "The science club has a weather station on the school roof. {boy} is in the team that looks after it.",
        "reading": {
            "title": "Our Weather Station Diary",
            "paragraphs": [
                {
                    "sentences": [
                        "We have been running the school weather station since September.",
                        "Every morning we measure the temperature, the wind and the rain.",
                    ]
                },
                {
                    "sentences": [
                        "This summer has been very strange. It hasn't rained for six weeks, and farmers have been talking about a drought.",
                        "The temperature has been rising every year since we started.",
                    ]
                },
                {
                    "sentences": [
                        "Our teacher says that the climate has been changing all over the world.",
                        "Some places have more floods, and others have less water than before.",
                    ]
                },
                {
                    "sentences": [
                        "Yesterday our sensors showed that the air pressure has been falling fast.",
                        "We checked the forecast, which said that a big storm was coming.",
                    ]
                },
                {
                    "sentences": [
                        "We have written a warning for the school website. Two hundred people have already read it!",
                        "I've been checking the data all afternoon, and my eyes are tired — but it feels important.",
                    ]
                },
            ],
            "highlight": [
                "have been running",
                "has been rising",
                "has been changing",
                "has been falling",
                "have been talking",
                "I've been checking",
                "since",
                "for",
            ],
        },
        "listening": [
            {
                "id": "b2-3-tired",
                "title": "Why are you so wet?",
                "transcript": [
                    {"speaker": "Mum", "text": "{boy}, why are you so wet?"},
                    {
                        "speaker": "{boy}",
                        "text": "I've been fixing the rain sensor on the roof. It's been raining all afternoon!",
                    },
                    {"speaker": "Mum", "text": "How long have you been doing that?"},
                    {"speaker": "{boy}", "text": "For about two hours. But I've fixed it now!"},
                ],
            },
            {
                "id": "b2-3-forecast",
                "title": "The forecast",
                "transcript": [
                    {
                        "speaker": "Forecaster",
                        "text": "It has been snowing in the mountains since early this morning.",
                    },
                    {
                        "speaker": "Forecaster",
                        "text": "Temperatures have been falling all day, and tonight it will be minus ten.",
                    },
                    {
                        "speaker": "Forecaster",
                        "text": "Drivers should be very careful on the roads.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Present perfect continuous",
                "explanation": (
                    "Form: have / has been + verb-ing. Use it for an activity that started in the past and is still "
                    "continuing: We have been running the station since September. "
                    "Also for an activity that has just stopped and has a result now: I'm wet because I've been fixing the sensor. "
                    "for + a period of time (for two hours); since + a starting point (since May). Question: How long have you been …?"
                ),
                "explanation_ru": (
                    "Делаю уже какое-то время (и продолжаю) или только что закончил, и виден результат. "
                    "for — в течение (for 2 hours), since — с (since May)."
                ),
                "examples": [
                    "It has been raining for three days.",
                    "How long have you been waiting?",
                    "She's tired because she's been running.",
                ],
            },
            {
                "title": "Present perfect simple or continuous?",
                "explanation": (
                    "Simple focuses on the result or how many: I have written two reports. "
                    "Continuous focuses on the activity and how long: I have been writing reports all day. "
                    "Some verbs are not used in the continuous: know, like, believe, own (I've known him for years)."
                ),
                "explanation_ru": "Simple — результат, количество; continuous — процесс, длительность.",
                "examples": [
                    "I've read three books this week.",
                    "I've been reading all afternoon.",
                    "We've known Mr Lee since 2020.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "weather-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("flood", None, "🌊"),
                ("drought", None, "🏜️"),
                ("temperature", None, "🌡️"),
                ("forecast", None, "📺"),
            ],
            ["vocab.flood", "vocab.drought", "vocab.temperature", "vocab.forecast"],
            "A drought is a long time without rain.",
            "flood 🌊, drought 🏜️, temperature 🌡️, forecast 📺.",
        ),
        matching(
            "weather-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("climate", "the usual weather in a place over many years", None),
                ("forecast", "a prediction of the weather", None),
                ("measure", "find the exact size or amount of something", None),
            ],
            ["vocab.climate", "vocab.forecast", "vocab.measure"],
            "Weather = today; climate = over many years.",
            "climate = usual weather over years; forecast = a prediction; measure = find the exact amount.",
        ),
        choice(
            "find-drought",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: drought",
            [(None, "🌊"), (None, "❄️"), (None, "🏜️")],
            "c",
            ["vocab.drought"],
            "Dry land, no rain for a long time.",
            "🏜️ drought.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-how-long",
            "LISTENING",
            "Listen. How long has the girl been waiting for the bus?",
            "She has been waiting …",
            [("for forty minutes", "⏳"), ("since yesterday", "📅"), ("for five minutes", "⏱️")],
            "a",
            ["grammar.present_perfect_continuous"],
            "Listen for 'for'.",
            "I've been waiting for forty minutes.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="This is terrible! I've been waiting for this bus for forty minutes, and it's been raining the whole time.",
        ),
        true_false(
            "listen-wet",
            "LISTENING",
            "Listen to Mum and {boy}. True or false?",
            "{boy} has been fixing the sensor for about two hours.",
            True,
            ["grammar.present_perfect_continuous", "vocab.sensor"],
            "Listen to his last answer.",
            "For about two hours. But I've fixed it now!",
            listening_id="b2-3-tired",
        ),
        true_false(
            "listen-snow",
            "LISTENING",
            "Listen to the forecast. True or false?",
            "Temperatures have been rising all day.",
            False,
            ["grammar.present_perfect_continuous", "vocab.temperature", "vocab.forecast"],
            "Are they going up or down?",
            "Temperatures have been falling all day.",
            listening_id="b2-3-forecast",
        ),
        blank(
            "ppc-blank",
            "GRAMMAR",
            "Complete the sentence.",
            "It has ___ raining ___ three days.",
            ["been", "for"],
            ["been", "being", "for", "since"],
            ["grammar.present_perfect_continuous"],
            "has been + -ing; for + a period of time.",
            "It has been raining for three days.",
        ),
        blank(
            "for-since-blank",
            "GRAMMAR",
            "Choose for or since.",
            "We've been measuring the rain ___ September and the wind ___ two months.",
            ["since", "for"],
            ["for", "since"],
            ["grammar.present_perfect_continuous", "vocab.measure"],
            "since + a starting point; for + a period.",
            "since September; for two months.",
        ),
        choice(
            "simple-or-cont",
            "GRAMMAR",
            "Choose the best sentence.",
            "You want to say how many reports you finished.",
            [
                ("I've written three weather reports today.", None),
                ("I've been writing three weather reports today.", None),
                ("I've been written three weather reports today.", None),
            ],
            "a",
            ["grammar.present_perfect_continuous", "grammar.present_perfect"],
            "How many → present perfect simple.",
            "I've written three weather reports today. (result, number)",
        ),
        choice(
            "know-state",
            "GRAMMAR",
            "Which sentence is correct?",
            "Talk about your friendship with Sam.",
            [
                ("I've known Sam since I was six.", None),
                ("I've been knowing Sam since I was six.", None),
                ("I know Sam since I was six.", None),
            ],
            "a",
            ["grammar.present_perfect_continuous", "grammar.present_perfect"],
            "know is not used in the continuous.",
            "I've known Sam since I was six.",
        ),
        build(
            "build-ppc",
            "GRAMMAR",
            "Put the words in order.",
            "How long have you been working on the project?",
            ["grammar.present_perfect_continuous"],
            "Start with 'How long'.",
            "How long have you been working on the project?",
        ),
        choice(
            "read-drought",
            "READING",
            "Read the text. Then answer.",
            "Why have farmers been talking about a drought?",
            [
                ("It hasn't rained for six weeks.", "🏜️"),
                ("There has been a big flood.", "🌊"),
                ("The forecast said it would snow.", "❄️"),
            ],
            "a",
            ["vocab.drought"],
            "Look at paragraph 2.",
            "It hasn't rained for six weeks.",
            ex_type="READING_COMPREHENSION",
        ),
        order(
            "read-order",
            "READING",
            "Put the events in the order of the text.",
            [
                "The team started the weather station in September.",
                "There was no rain for six weeks.",
                "The sensors showed that the air pressure was falling.",
                "The forecast said a storm was coming.",
                "The team wrote a warning for the website.",
            ],
            ["vocab.forecast", "vocab.sensor"],
            "The warning comes at the end.",
            "Start → dry summer → pressure falling → forecast → warning.",
        ),
        speak(
            "say-how-long",
            "Talk about three things you have been doing for a long time (a hobby, a language, a sport). Say how long.",
            "I've been … for … / since … I've also been …",
            "I've been learning English for five years. I've been playing the piano since I was eight. I've also been reading a great book this week.",
            ["grammar.present_perfect_continuous"],
        ),
        choice(
            "quiz-who-which",
            "QUIZ",
            "Choose the right relative pronoun.",
            "A meteorologist is a scientist ___ studies the weather.",
            [("who", None), ("which", None), ("where", None)],
            "a",
            ["grammar.relative_clauses", "vocab.scientist"],
            "Remember Lesson 2: people → who.",
            "A meteorologist is a scientist who studies the weather.",
        ),
        blank(
            "quiz-if-were-rain",
            "QUIZ",
            "Complete the sentence.",
            "If I ___ the weather, I ___ make it sunny every weekend.",
            ["controlled", "would"],
            ["control", "controlled", "will", "would"],
            ["grammar.second_conditional"],
            "Remember Lesson 1: imaginary situation.",
            "If I controlled the weather, I would make it sunny every weekend.",
        ),
        choice(
            "quiz-should-floods",
            "QUIZ",
            "Choose the best advice.",
            "There is a flood warning.",
            [
                ("You should stay at home.", None),
                ("You should to stay at home.", None),
                ("You should staying at home.", None),
            ],
            "a",
            ["grammar.should", "vocab.flood"],
            "Remember B1, Lesson 6.",
            "You should stay at home.",
        ),
    ],
}

LESSON_4 = {
    "slug": L4,
    "title": "Healthy Choices",
    "description": "Health Week at school: {boy} decides to change some habits. Enjoy doing or decide to do?",
    "minutes": 35,
    "objectives": [
        "Use health vocabulary: diet, habit, fitness, vitamins, balanced, avoid.",
        "Use verbs followed by -ing (enjoy, avoid, finish).",
        "Use verbs followed by to + infinitive (decide, hope, plan).",
    ],
    "review": [
        "grammar.present_perfect_continuous",
        "vocab.measure",
        "vocab.temperature",
        "grammar.relative_clauses",
        "grammar.should",
        "grammar.must_have_to",
        "grammar.prefer",
        "grammar.a_little_a_few",
        "vocab.sugar",
        "vocab.football",
    ],
    "episode": (
        "The 30-Day Challenge",
        "{boy} and {teen} start a 30-day health challenge. Will {boy} really stop eating crisps?",
    ),
    "content": {
        "story_intro": "It's Health Week at school. {boy} and {teen} have decided to take a 30-day challenge.",
        "reading": {
            "title": "The 30-Day Challenge",
            "paragraphs": [
                {
                    "sentences": [
                        "Our PE teacher asked us to look at our habits for one week.",
                        "I was surprised to see how much time I spent sitting in front of a screen.",
                    ]
                },
                {
                    "sentences": [
                        "So {teen} and I decided to try a 30-day challenge.",
                        "We agreed to go for a run three times a week and to avoid eating crisps and sweets.",
                    ]
                },
                {
                    "sentences": [
                        "At first it wasn't easy. I really missed having chocolate after dinner!",
                        "But I started to enjoy running, especially in the morning.",
                    ]
                },
                {
                    "sentences": [
                        "Mum helped us to plan a balanced diet with lots of fruit and vegetables, which are full of vitamins.",
                        "{teen} stopped drinking fizzy drinks and now prefers water.",
                    ]
                },
                {
                    "sentences": [
                        "After 30 days, my fitness has improved a lot, and I sleep better.",
                        "I hope to keep going — although I haven't stopped dreaming about chocolate!",
                    ]
                },
            ],
            "highlight": [
                "decided to",
                "agreed to",
                "avoid eating",
                "missed having",
                "enjoy running",
                "stopped drinking",
                "hope to",
                "habits",
                "balanced diet",
                "vitamins",
                "fitness",
            ],
        },
        "listening": [
            {
                "id": "b2-4-coach",
                "title": "The coach's advice",
                "transcript": [
                    {
                        "speaker": "Coach",
                        "text": "Remember to drink water before you start running.",
                    },
                    {"speaker": "{boy}", "text": "I keep getting tired after ten minutes."},
                    {
                        "speaker": "Coach",
                        "text": "Try running more slowly. And avoid eating just before training.",
                    },
                    {"speaker": "{boy}", "text": "OK. I'll practise running slowly every day."},
                ],
            },
            {
                "id": "b2-4-teen",
                "title": "{teen}'s new habit",
                "transcript": [
                    {"speaker": "Mum", "text": "You've stopped buying fizzy drinks, {teen}!"},
                    {
                        "speaker": "{teen}",
                        "text": "Yes. I decided to give them up. I don't miss them at all.",
                    },
                    {
                        "speaker": "Mum",
                        "text": "And are you going to keep going after the challenge?",
                    },
                    {
                        "speaker": "{teen}",
                        "text": "I hope to. I'd like to run a 10K race in the spring.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Verb + -ing or verb + to",
                "explanation": (
                    "After some verbs we use -ing: enjoy, avoid, finish, mind, miss, keep, practise, suggest. "
                    "I enjoy running. Avoid eating late. "
                    "After other verbs we use to + infinitive: decide, agree, hope, plan, want, learn, promise, refuse, would like. "
                    "We decided to try a challenge. "
                    "After prepositions we always use -ing: I'm good at swimming. Thanks for helping."
                ),
                "explanation_ru": (
                    "После одних глаголов — форма -ing (enjoy, avoid, finish), после других — to + глагол (decide, hope, plan). "
                    "После предлогов всегда -ing."
                ),
                "examples": [
                    "I've finished doing my homework.",
                    "She refused to eat the cake.",
                    "He's interested in learning Chinese.",
                ],
            },
            {
                "title": "stop / remember / try + -ing or to",
                "explanation": (
                    "Some verbs change their meaning. stop doing = not do it any more: I stopped eating sweets. "
                    "stop to do = stop in order to do something: We stopped to drink water. "
                    "remember to do = not forget a task: Remember to drink water. "
                    "remember doing = have a memory: I remember running my first race."
                ),
                "explanation_ru": "stop doing — перестать; stop to do — остановиться, чтобы. remember to do — не забыть; remember doing — помнить, как делал.",
                "examples": [
                    "He stopped playing video games at night.",
                    "We stopped to look at the view.",
                    "Remember to bring your trainers.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "health-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("diet", None, "🥗"),
                ("vitamins", None, "💊"),
                ("fitness", None, "🏋️"),
                ("balanced", None, "⚖️"),
            ],
            ["vocab.diet", "vocab.vitamins", "vocab.fitness", "vocab.balanced"],
            "A diet is what you usually eat.",
            "diet 🥗, vitamins 💊, fitness 🏋️, balanced ⚖️.",
        ),
        matching(
            "health-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("habit", "something you do regularly, often without thinking", None),
                ("avoid", "try not to do or meet something", None),
                ("fitness", "how strong and healthy your body is", None),
            ],
            ["vocab.habit", "vocab.avoid", "vocab.fitness"],
            "Brushing your teeth is a good habit.",
            "habit = something you do regularly; avoid = try not to do; fitness = how fit you are.",
        ),
        choice(
            "find-balanced",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: a healthy meal",
            [(None, "🥗"), (None, "🍟"), (None, "🍭")],
            "a",
            ["vocab.diet", "vocab.balanced"],
            "Which one is full of vegetables?",
            "🥗 a salad is part of a balanced diet.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-give-up",
            "LISTENING",
            "Listen. What has the man decided to do?",
            "He has decided …",
            [("to cycle to work", "🚲"), ("to stop running", "🛑"), ("to eat more sugar", "🍬")],
            "a",
            ["grammar.gerund_infinitive", "vocab.habit"],
            "Listen for 'decided to'.",
            "I've decided to cycle to work every day.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="I used to drive everywhere, but I've decided to cycle to work every day. I really enjoy being outside.",
        ),
        true_false(
            "listen-coach-eat",
            "LISTENING",
            "Listen to the coach and {boy}. True or false?",
            "The coach says {boy} should eat just before training.",
            False,
            ["grammar.gerund_infinitive", "vocab.avoid"],
            "Listen for 'avoid'.",
            "The coach: avoid eating just before training.",
            listening_id="b2-4-coach",
        ),
        true_false(
            "listen-teen-race",
            "LISTENING",
            "Listen to Mum and {teen}. True or false?",
            "{teen} would like to run a race in the spring.",
            True,
            ["grammar.gerund_infinitive", "vocab.fitness"],
            "Listen to her last line.",
            "I'd like to run a 10K race in the spring.",
            listening_id="b2-4-teen",
        ),
        blank(
            "ger-inf-blank",
            "GRAMMAR",
            "Choose the right forms.",
            "I enjoy ___ in the morning, so I've decided ___ every day.",
            ["running", "to run"],
            ["running", "to run", "run"],
            ["grammar.gerund_infinitive", "vocab.fitness"],
            "enjoy + -ing; decide + to.",
            "I enjoy running, so I've decided to run every day.",
        ),
        blank(
            "avoid-hope-blank",
            "GRAMMAR",
            "Choose the right forms.",
            "Try to avoid ___ fizzy drinks. I hope ___ healthier this year.",
            ["drinking", "to be"],
            ["drinking", "to drink", "being", "to be"],
            ["grammar.gerund_infinitive", "vocab.avoid"],
            "avoid + -ing; hope + to.",
            "Try to avoid drinking fizzy drinks. I hope to be healthier this year.",
        ),
        choice(
            "stop-meaning",
            "GRAMMAR",
            "What does the sentence mean?",
            "We stopped to drink some water.",
            [
                ("We stopped running so that we could drink water.", None),
                ("We don't drink water any more.", None),
                ("We forgot to drink water.", None),
            ],
            "a",
            ["grammar.gerund_infinitive"],
            "stop to do = stop in order to do.",
            "stop to drink = stop (running) in order to drink.",
        ),
        choice(
            "preposition-ing",
            "GRAMMAR",
            "Which sentence is correct?",
            "Talk about {teen}'s talent.",
            [
                ("{teen} is good at running long distances.", None),
                ("{teen} is good at run long distances.", None),
                ("{teen} is good at to run long distances.", None),
            ],
            "a",
            ["grammar.gerund_infinitive"],
            "After a preposition → -ing.",
            "{teen} is good at running long distances.",
        ),
        build(
            "build-ger",
            "GRAMMAR",
            "Put the words in order.",
            "He has stopped eating sweets after dinner.",
            ["grammar.gerund_infinitive", "vocab.habit"],
            "Start with 'He has stopped'.",
            "He has stopped eating sweets after dinner.",
        ),
        choice(
            "read-hard",
            "READING",
            "Read the text. Then answer.",
            "What did {boy} find difficult at first?",
            [
                ("He missed having chocolate after dinner.", "🍫"),
                ("He didn't like vegetables.", "🥦"),
                ("He couldn't wake up early.", "⏰"),
            ],
            "a",
            ["grammar.gerund_infinitive"],
            "Look at paragraph 3.",
            "I really missed having chocolate after dinner!",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-results",
            "READING",
            "Read the text. True or false?",
            "After 30 days {boy} sleeps better and is fitter.",
            True,
            ["vocab.fitness"],
            "Look at the last paragraph.",
            "My fitness has improved a lot, and I sleep better.",
        ),
        speak(
            "say-habits",
            "Talk about your habits. What do you enjoy doing? What do you want to stop doing? What have you decided to do?",
            "I enjoy … I'd like to stop … I've decided to … I'm trying to avoid …",
            "I enjoy playing basketball. I'd like to stop using my phone in bed. I've decided to go to sleep earlier, and I'm trying to avoid eating crisps.",
            ["grammar.gerund_infinitive", "vocab.habit"],
        ),
        blank(
            "quiz-ppc-running",
            "QUIZ",
            "Complete the sentence.",
            "{boy} is hot because he ___ ___ running.",
            ["has", "been"],
            ["has", "have", "been", "being"],
            ["grammar.present_perfect_continuous"],
            "Remember Lesson 3: a result of an activity.",
            "{boy} is hot because he has been running.",
        ),
        choice(
            "quiz-which-vitamins",
            "QUIZ",
            "Choose the right relative pronoun.",
            "Oranges, ___ are full of vitamin C, are good for you.",
            [("which", None), ("that", None), ("who", None)],
            "a",
            ["grammar.relative_clauses", "vocab.vitamins"],
            "Remember Lesson 2: a non-defining clause with commas → no that.",
            "Oranges, which are full of vitamin C, are good for you.",
        ),
        choice(
            "quiz-dont-have-to",
            "QUIZ",
            "Choose the right word.",
            "You ___ go to the gym to be fit. Walking is great too.",
            [("don't have to", None), ("mustn't", None), ("must", None)],
            "a",
            ["grammar.dont_have_to", "vocab.fitness"],
            "Remember B1: not necessary.",
            "You don't have to go to the gym.",
        ),
    ],
}

LESSON_5 = {
    "slug": L5,
    "title": "The Invention Fair",
    "description": "{boy}'s team presents an invention. Has it been tested? Will it be chosen? Then a review of the unit.",
    "minutes": 40,
    "objectives": [
        "Use invention vocabulary: invention, prototype, solar panel, judge, prize.",
        "Use the passive in all tenses: is being tested, has been built, will be announced.",
        "Present a project and review Unit 1.",
    ],
    "review": [
        "grammar.gerund_infinitive",
        "vocab.avoid",
        "vocab.habit",
        "grammar.present_perfect_continuous",
        "grammar.relative_clauses",
        "grammar.second_conditional",
        "vocab.battery",
        "vocab.sensor",
        "grammar.passive_past",
        "grammar.passive_present",
    ],
    "episode": (
        "The Smart Umbrella",
        "{boy}'s team builds a smart umbrella for the invention fair. The judges are coming!",
    ),
    "content": {
        "story_intro": "The science fortnight ends with an invention fair. {boy}'s team has a surprising idea.",
        "reading": {
            "title": "The Smart Umbrella",
            "paragraphs": [
                {
                    "sentences": [
                        "Our invention is a smart umbrella. It was designed by Maya, Sam and me.",
                        "A small solar panel has been fitted on the top, and it charges a battery inside the handle.",
                    ]
                },
                {
                    "sentences": [
                        "The umbrella has a sensor which checks the weather forecast.",
                        "If rain is expected, you are warned by a little light before you leave home.",
                    ]
                },
                {
                    "sentences": [
                        "The prototype was built in the school lab, and it has been tested in real rain — by me, unfortunately!",
                        "At the moment a second version is being made with a stronger frame.",
                    ]
                },
                {
                    "sentences": [
                        "At the fair, I said: Let me show you how it works. As you can see, the light turns blue when rain is coming.",
                        "The judges asked a lot of questions, which we had practised answering.",
                    ]
                },
                {
                    "sentences": [
                        "The results will be announced on Monday. The winning invention will be shown at the city science museum.",
                        "Whatever happens, we have learned a lot — and I will never forget my umbrella again!",
                    ]
                },
            ],
            "highlight": [
                "was designed",
                "has been fitted",
                "are warned",
                "was built",
                "has been tested",
                "is being made",
                "will be announced",
                "will be shown",
                "Let me show you",
                "As you can see",
            ],
        },
        "listening": [
            {
                "id": "b2-5-judges",
                "title": "The judges",
                "transcript": [
                    {"speaker": "Judge", "text": "Has the umbrella been tested outside?"},
                    {
                        "speaker": "{boy}",
                        "text": "Yes, it has. It was tested in the rain for two weeks.",
                    },
                    {"speaker": "Judge", "text": "And could it be sold in shops one day?"},
                    {
                        "speaker": "{boy}",
                        "text": "We hope so! A cheaper version is being designed right now.",
                    },
                ],
            },
            {
                "id": "b2-5-results",
                "title": "The results",
                "transcript": [
                    {
                        "speaker": "Head teacher",
                        "text": "This year forty inventions have been presented.",
                    },
                    {
                        "speaker": "Head teacher",
                        "text": "First prize has been won by the Smart Umbrella team!",
                    },
                    {
                        "speaker": "Head teacher",
                        "text": "Their invention will be shown at the city science museum next month.",
                    },
                    {"speaker": "{boy}", "text": "Wow, I can't believe it!"},
                ],
            },
        ],
        "grammar": [
            {
                "title": "The passive in all tenses",
                "explanation": (
                    "Form: the right form of be + past participle. "
                    "Present simple: is made. Present continuous: is being made. "
                    "Past simple: was made. Present perfect: has been made. "
                    "Future: will be made. Modal: can / could / must be made. "
                    "Use it when the action or the result is more important than who did it. Add by + agent only when it is useful."
                ),
                "explanation_ru": (
                    "Пассив в любом времени: форма be + третья форма глагола. "
                    "is being tested — сейчас тестируется; has been tested — уже протестирован; will be tested — будет протестирован."
                ),
                "examples": [
                    "The umbrella is being tested right now.",
                    "Forty inventions have been presented.",
                    "The winner will be announced on Monday.",
                    "This problem can be solved.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "invention-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("solar panel", None, "☀️"),
                ("prize", None, "🏆"),
                ("judge", None, "🧑‍⚖️"),
                ("invention", None, "💡"),
            ],
            ["vocab.solar_panel", "vocab.prize", "vocab.judge", "vocab.invention"],
            "A solar panel uses energy from the Sun.",
            "solar panel ☀️, prize 🏆, judge 🧑‍⚖️, invention 💡.",
        ),
        matching(
            "invention-meanings",
            "VOCABULARY",
            "Match the word to its definition.",
            [
                ("prototype", "the first model of a new machine or product", None),
                ("invention", "something that has never been made before", None),
                ("judge", "a person who decides who wins a competition", None),
            ],
            ["vocab.prototype", "vocab.invention", "vocab.judge"],
            "A prototype comes before the final product.",
            "prototype = a first model; invention = something new; judge = decides the winner.",
        ),
        choice(
            "find-prize",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: prize",
            [(None, "💡"), (None, "🏆"), (None, "🛠️")],
            "b",
            ["vocab.prize"],
            "The winners get it.",
            "🏆 prize.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-passive",
            "LISTENING",
            "Listen. What is happening to the robot now?",
            "The robot …",
            [
                ("is being repaired", "🔧"),
                ("has been sold", "💰"),
                ("will be built next year", "📅"),
            ],
            "a",
            ["grammar.passive_all"],
            "Listen for 'is being'.",
            "It is being repaired at the moment.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Sorry, you can't see our robot today. It was damaged yesterday, and it is being repaired at the moment.",
        ),
        true_false(
            "listen-tested",
            "LISTENING",
            "Listen to the judge and {boy}. True or false?",
            "The umbrella has never been tested outside.",
            False,
            ["grammar.passive_all", "vocab.judge"],
            "How long was it tested?",
            "It was tested in the rain for two weeks.",
            listening_id="b2-5-judges",
        ),
        true_false(
            "listen-museum",
            "LISTENING",
            "Listen to the head teacher. True or false?",
            "The Smart Umbrella will be shown at the city science museum.",
            True,
            ["grammar.passive_all", "vocab.prize"],
            "Listen to the last sentence.",
            "Their invention will be shown at the city science museum next month.",
            listening_id="b2-5-results",
        ),
        blank(
            "passive-tenses-blank",
            "GRAMMAR",
            "Complete with the passive.",
            "Right now a new version is ___ made. The results will ___ announced on Monday.",
            ["being", "be"],
            ["be", "been", "being"],
            ["grammar.passive_all"],
            "Present continuous passive: is being; future passive: will be.",
            "A new version is being made. The results will be announced.",
        ),
        blank(
            "has-been-blank",
            "GRAMMAR",
            "Complete with the present perfect passive.",
            "A solar panel ___ ___ fitted on the top.",
            ["has", "been"],
            ["has", "have", "been", "being"],
            ["grammar.passive_all", "vocab.solar_panel"],
            "has + been + past participle.",
            "A solar panel has been fitted on the top.",
        ),
        choice(
            "passive-transform",
            "GRAMMAR",
            "Choose the passive sentence with the same meaning.",
            "They will announce the winners at five.",
            [
                ("The winners will be announced at five.", None),
                ("The winners will announced at five.", None),
                ("The winners are announcing at five.", None),
            ],
            "a",
            ["grammar.passive_all"],
            "will + be + past participle.",
            "The winners will be announced at five.",
        ),
        choice(
            "presenting-phrase",
            "GRAMMAR",
            "Choose the best phrase to start a demonstration.",
            "You are presenting your invention to the judges.",
            [
                ("Let me show you how it works.", None),
                ("Let me to show you how it works.", None),
                ("I show you how does it work.", None),
            ],
            "a",
            ["phrase.presenting", "grammar.gerund_infinitive"],
            "let + person + verb (no to).",
            "Let me show you how it works.",
        ),
        build(
            "build-passive-all",
            "GRAMMAR",
            "Put the words in order.",
            "The prototype has been tested in real rain.",
            ["grammar.passive_all", "vocab.prototype"],
            "Start with 'The prototype has'.",
            "The prototype has been tested in real rain.",
        ),
        choice(
            "read-light",
            "READING",
            "Read the text. Then answer.",
            "How does the umbrella warn you about rain?",
            [
                ("A little light turns blue.", "💡"),
                ("It plays music.", "🎵"),
                ("It opens by itself.", "☂️"),
            ],
            "a",
            ["vocab.sensor", "vocab.invention"],
            "Look at paragraphs 2 and 4.",
            "A little light turns blue when rain is coming.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-results-monday",
            "READING",
            "Read the text. True or false?",
            "The results were announced at the fair.",
            False,
            ["grammar.passive_all"],
            "Look at the last paragraph.",
            "The results will be announced on Monday.",
        ),
        speak(
            "say-present",
            "Present an invention (real or imaginary) to the judges. Say how it was made, what has been tested, and what will be done next.",
            "Let me show you … It was made … It has been tested … As you can see, … Next, it will be …",
            "Let me show you our smart bin. It was made from recycled plastic. It has been tested at school. As you can see, it sorts the rubbish. Next, it will be made smaller.",
            ["grammar.passive_all", "phrase.presenting"],
        ),
        blank(
            "quiz-if-won",
            "QUIZ",
            "Complete the sentence.",
            "If we ___ first prize, we ___ build a better version.",
            ["won", "would"],
            ["win", "won", "would", "will"],
            ["grammar.second_conditional", "vocab.prize"],
            "Remember Lesson 1: imagine.",
            "If we won first prize, we would build a better version.",
        ),
        choice(
            "quiz-galaxy",
            "QUIZ",
            "Choose the right word.",
            "The Milky Way is our ___.",
            [("galaxy", None), ("planet", None), ("orbit", None)],
            "a",
            ["vocab.galaxy", "vocab.planet", "vocab.orbit"],
            "Remember Lesson 1.",
            "The Milky Way is our galaxy.",
        ),
        choice(
            "quiz-whose",
            "QUIZ",
            "Choose the right relative pronoun.",
            "Maya, ___ dad is an engineer, designed the battery.",
            [("whose", None), ("who", None), ("that", None)],
            "a",
            ["grammar.relative_clauses", "vocab.battery"],
            "Remember Lesson 2: possession → whose.",
            "Maya, whose dad is an engineer, designed the battery.",
        ),
        blank(
            "quiz-ppc-climate",
            "QUIZ",
            "Complete the sentence.",
            "The climate has been ___ ___ more than a hundred years.",
            ["changing", "for"],
            ["changing", "changed", "for", "since"],
            ["grammar.present_perfect_continuous", "vocab.climate"],
            "Remember Lesson 3.",
            "The climate has been changing for more than a hundred years.",
        ),
        blank(
            "quiz-avoid",
            "QUIZ",
            "Choose the right form.",
            "The judges advised us to avoid ___ too much technical language.",
            ["using"],
            ["using", "to use", "use"],
            ["grammar.gerund_infinitive", "vocab.avoid"],
            "Remember Lesson 4: avoid + -ing.",
            "Avoid using too much technical language.",
        ),
        choice(
            "quiz-prototype",
            "QUIZ",
            "Choose the right word.",
            "Before you make a thousand umbrellas, you build one ___.",
            [("prototype", None), ("prize", None), ("judge", None)],
            "a",
            ["vocab.prototype"],
            "The first model.",
            "You build a prototype first.",
        ),
    ],
}

UNIT = {
    "slug": "explorers-of-science",
    "title": "Explorers of Science",
    "description": "Space, robots, the school weather station, healthy habits and an invention fair.",
    "lessons": [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5],
}
