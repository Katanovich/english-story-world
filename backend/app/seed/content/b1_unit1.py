"""B1 · Unit 1 "Clubs and Friends" (B1 lessons 1-5).

{boy} is twelve now and {little} has started school. Topics: the science club, {teen}'s band,
cooking with Aunt {aunt}, a lost kitten, the school play. Grammar: present perfect
(ever/never, just/already), would like / prefer, the first conditional, past continuous vs
past simple, must / have to / don't have to. Lesson 5 reviews the unit.
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
    "the-science-club",
    "teens-band",
    "cooking-with-aunt",
    "the-lost-kitten",
    "the-school-play",
)

ITEMS: dict[str, Item] = {
    # Lesson 1
    "vocab.experiment": (
        V,
        "experiment",
        "🧪",
        "эксперимент, опыт",
        L1,
        ["We have done an experiment with water."],
        None,
    ),
    "vocab.scientist": (V, "scientist", "🧑‍🔬", "учёный", L1, ["I want to be a scientist."], None),
    "vocab.magnet": (V, "magnet", "🧲", "магнит", L1, ["The magnet picks up the nails."], None),
    "vocab.goggles": (
        V,
        "safety goggles",
        "🥽",
        "защитные очки",
        L1,
        ["Put on your safety goggles!"],
        None,
    ),
    "vocab.microscope": (
        V,
        "microscope",
        "🔬",
        "микроскоп",
        L1,
        ["Look through the microscope."],
        None,
    ),
    "vocab.discover": (
        V,
        "discover",
        "💡",
        "открыть, обнаружить",
        L1,
        ["We have discovered something new!"],
        None,
    ),
    "grammar.present_perfect": (
        G,
        "I have done … / She has seen …",
        None,
        "Present perfect: опыт и результат к настоящему моменту",
        L1,
        ["I have seen a microscope.", "She has finished the experiment."],
        "have / has + past participle (done, seen, made, finished). No exact time in the past.",
    ),
    "grammar.ever_never": (
        G,
        "Have you ever …? — I have never …",
        None,
        "Ты когда-нибудь …? — Я никогда не …",
        L1,
        ["Have you ever used a magnet?", "I have never seen a volcano."],
        "Use ever in questions and never in answers about life experience.",
    ),
    "grammar.just_already": (
        G,
        "just / already / yet",
        None,
        "только что / уже / ещё (не)",
        L1,
        ["I have just finished.", "We have already started.", "Have you finished yet?"],
        "just = a moment ago; already = earlier than expected; yet = in questions and negatives.",
    ),
    # Lesson 2
    "vocab.band": (V, "band", "🎸", "музыкальная группа", L2, ["{teen} plays in a band."], None),
    "vocab.guitar": (V, "guitar", "🎸", "гитара", L2, ["She plays the guitar."], None),
    "vocab.drums": (V, "drums", "🥁", "барабаны", L2, ["The drums are very loud."], None),
    "vocab.piano": (V, "piano", "🎹", "пианино", L2, ["Granny plays the piano."], None),
    "vocab.concert": (V, "concert", "🎤", "концерт", L2, ["The concert is on Friday."], None),
    "vocab.practise": (
        V,
        "practise",
        "🔁",
        "репетировать, тренироваться",
        L2,
        ["They practise every day."],
        None,
    ),
    "vocab.song": (V, "song", "🎵", "песня", L2, ["This is my favourite song."], None),
    "grammar.would_like": (
        G,
        "I'd like to … / Would you like to …?",
        None,
        "Я бы хотел … / Не хочешь ли ты …?",
        L2,
        ["I'd like to play the drums.", "Would you like to come to the concert?"],
        "would like = a polite way to say want. I'd like + noun / to + verb.",
    ),
    "grammar.prefer": (
        G,
        "I prefer … to … / I'd rather …",
        None,
        "Я предпочитаю … (чему-то)",
        L2,
        ["I prefer rock to jazz.", "I prefer playing to listening."],
        "prefer A to B. After prefer you can use a noun or verb + -ing.",
    ),
    # Lesson 3
    "vocab.recipe": (V, "recipe", "📖", "рецепт", L3, ["This is Aunt {aunt}'s recipe."], None),
    "vocab.flour": (V, "flour", "🌾", "мука", L3, ["We need some flour."], None),
    "vocab.sugar": (V, "sugar", "🍬", "сахар", L3, ["Don't add too much sugar."], None),
    "vocab.butter": (V, "butter", "🧈", "сливочное масло", L3, ["Melt the butter."], None),
    "vocab.oven": (V, "oven", "🔥", "духовка", L3, ["Put the cake in the oven."], None),
    "vocab.mix": (V, "mix", "🥣", "смешивать", L3, ["Mix the eggs and the sugar."], None),
    "grammar.first_conditional": (
        G,
        "If + present, … will …",
        None,
        "Условные предложения 1 типа: если …, то …",
        L3,
        [
            "If you add too much sugar, the cake will be too sweet.",
            "If it burns, we'll make another one.",
        ],
        "If + present simple, will + verb. For real situations in the future.",
    ),
    "grammar.a_little_a_few": (
        G,
        "a little / a few / too much / too many",
        None,
        "немного / несколько / слишком много",
        L3,
        ["Add a little milk.", "We need a few eggs.", "There is too much sugar."],
        "a little / too much + uncountable (milk, sugar); a few / too many + countable (eggs).",
    ),
    # Lesson 4
    "vocab.kitten": (V, "kitten", "🐈", "котёнок", L4, ["The kitten was very small."], None),
    "vocab.neighbour": (
        V,
        "neighbour",
        "🏘️",
        "сосед, соседка",
        L4,
        ["Our neighbour has a kitten."],
        None,
    ),
    "vocab.search": (V, "search (for)", "🔎", "искать", L4, ["We searched for the kitten."], None),
    "vocab.suddenly": (
        V,
        "suddenly",
        "⚡",
        "вдруг, внезапно",
        L4,
        ["Suddenly we heard a noise."],
        None,
    ),
    "vocab.worried": (
        V,
        "worried",
        "😟",
        "обеспокоенный",
        L4,
        ["Mrs Hill was very worried."],
        None,
    ),
    "vocab.tree": (V, "tree", "🌳", "дерево", L4, ["The kitten was in a tree."], None),
    "grammar.past_continuous": (
        G,
        "I was doing … / They were doing …",
        None,
        "Past continuous: что происходило в момент в прошлом",
        L4,
        ["At six o'clock I was doing my homework.", "We were walking in the park."],
        "was / were + verb-ing for an action in progress in the past.",
    ),
    "grammar.when_while": (
        G,
        "I was … when … / While I was …",
        None,
        "Я делал …, когда … / Пока я …",
        L4,
        ["I was reading when the phone rang.", "While we were walking, we heard a noise."],
        "Long action: past continuous. Short action that interrupts it: past simple.",
    ),
    # Lesson 5
    "vocab.stage": (V, "stage", "🎭", "сцена", L5, ["We are on the stage!"], None),
    "vocab.costume": (V, "costume", "👑", "костюм", L5, ["My costume is a king's costume."], None),
    "vocab.audience": (V, "audience", "👏", "зрители", L5, ["The audience clapped."], None),
    "vocab.nervous": (
        V,
        "nervous",
        "😬",
        "нервный, волнующийся",
        L5,
        ["I feel nervous before the play."],
        None,
    ),
    "vocab.proud": (V, "proud", "🥹", "гордый", L5, ["Mum was proud of us."], None),
    "vocab.excited": (
        V,
        "excited",
        "🤩",
        "взволнованный (радостно)",
        L5,
        ["{little} is very excited."],
        None,
    ),
    "grammar.must_have_to": (
        G,
        "must / have to",
        None,
        "должен, нужно",
        L5,
        ["You must be quiet backstage.", "We have to learn our lines."],
        "must and have to = it is necessary. He has to … (he / she / it).",
    ),
    "grammar.dont_have_to": (
        G,
        "don't have to / mustn't",
        None,
        "не обязательно / нельзя",
        L5,
        ["You don't have to wear a costume.", "You mustn't touch the lights."],
        "don't have to = it isn't necessary; mustn't = it isn't allowed.",
    ),
    "phrase.break_a_leg": (
        P,
        "Good luck! / Break a leg!",
        None,
        "Удачи! (актёрам перед выходом)",
        L5,
        ["Break a leg, {boy}!"],
        "Actors say 'Break a leg!' to wish good luck. It is a friendly idiom.",
    ),
}


LESSON_1 = {
    "slug": L1,
    "title": "The Science Club",
    "description": "{boy} joins the science club. What has he discovered?",
    "minutes": 30,
    "objectives": [
        "Name science club things: experiment, magnet, microscope, safety goggles.",
        "Talk about experiences with the present perfect: Have you ever …?",
        "Use just, already and yet.",
    ],
    "review": [
        "grammar.comparatives",
        "phrase.postcard",
        "vocab.fast",
        "grammar.past_simple_irregular",
        "grammar.past_simple_regular",
        "vocab.saw",
        "vocab.went",
        "vocab.school",
        "vocab.teacher",
        "grammar.can_cant",
    ],
    "episode": (
        "The Magnet Mystery",
        "At the first science club meeting, {boy} and his friends find out what a magnet can do.",
    ),
    "content": {
        "story_intro": "{boy} is twelve now. On Wednesdays he goes to the school science club.",
        "reading": {
            "title": "My First Week at the Science Club",
            "paragraphs": [
                {
                    "sentences": [
                        "I have always loved science, so this year I have joined the science club.",
                        "Our teacher, Mrs Park, is a real scientist.",
                    ]
                },
                {
                    "sentences": [
                        "We have already done three experiments.",
                        "First we put on our safety goggles and mixed water and salt.",
                    ]
                },
                {
                    "sentences": [
                        "Then we looked at a leaf through a microscope.",
                        "I have never seen anything so beautiful!",
                    ]
                },
                {
                    "sentences": [
                        "Today we have just finished an experiment with a magnet.",
                        "We discovered that a magnet picks up nails, but not paper or wood.",
                    ]
                },
                {
                    "sentences": [
                        "We haven't built a volcano yet.",
                        "Mrs Park says we will do it next week. I can't wait!",
                    ]
                },
            ],
            "highlight": [
                "have joined",
                "have already done",
                "have never seen",
                "have just finished",
                "haven't built",
                "yet",
            ],
        },
        "listening": [
            {
                "id": "b1-1-ever",
                "title": "Have you ever …?",
                "transcript": [
                    {"speaker": "{teen}", "text": "Have you ever used a microscope, {boy}?"},
                    {"speaker": "{boy}", "text": "Yes, I have. We used one at the club yesterday."},
                    {"speaker": "{teen}", "text": "Have you ever made a volcano?"},
                    {
                        "speaker": "{boy}",
                        "text": "No, I haven't. Not yet! We're going to make one next week.",
                    },
                ],
            },
            {
                "id": "b1-1-just",
                "title": "Has she finished yet?",
                "transcript": [
                    {"speaker": "Mrs Park", "text": "Has everyone finished the magnet experiment?"},
                    {"speaker": "{boy}", "text": "I have just finished, Mrs Park."},
                    {"speaker": "Mrs Park", "text": "And Sam?"},
                    {
                        "speaker": "{boy}",
                        "text": "Sam has already finished. He's writing the results now.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "Present perfect: ever / never",
                "explanation": (
                    "Use have / has + past participle to talk about experiences, when the exact time is not important: "
                    "I have seen a microscope. Question: Have you ever made a volcano? — Yes, I have. / No, I haven't. "
                    "I have never … = not one time in my life."
                ),
                "explanation_ru": (
                    "Present perfect говорит об опыте «на сегодня», без точного времени: "
                    "I have never seen a volcano = Я никогда не видел вулкан. "
                    "Если есть точное время (yesterday, last week) — используй past simple."
                ),
                "examples": [
                    "Have you ever used a magnet? — Yes, I have.",
                    "She has never been to a science museum.",
                    "We used a microscope yesterday. (exact time → past simple)",
                ],
            },
            {
                "title": "just / already / yet",
                "explanation": (
                    "just = a very short time ago: I have just finished. "
                    "already = sooner than expected: We have already done three experiments. "
                    "yet = at the end of questions and negatives: Have you finished yet? We haven't built a volcano yet."
                ),
                "explanation_ru": "just — только что; already — уже; yet — в вопросах «уже?», в отрицаниях «ещё не».",
                "examples": [
                    "I've just seen Mrs Park.",
                    "Has the experiment started yet?",
                    "It hasn't started yet.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "science-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("magnet", None, "🧲"),
                ("microscope", None, "🔬"),
                ("safety goggles", None, "🥽"),
                ("scientist", None, "🧑‍🔬"),
            ],
            ["vocab.magnet", "vocab.microscope", "vocab.goggles", "vocab.scientist"],
            "You look through a microscope.",
            "magnet 🧲, microscope 🔬, safety goggles 🥽, scientist 🧑‍🔬.",
        ),
        matching(
            "science-meanings",
            "VOCABULARY",
            "Match the word to its meaning.",
            [
                ("experiment", "a test to find out something", None),
                ("discover", "find something new", None),
                ("scientist", "a person who studies science", None),
            ],
            ["vocab.experiment", "vocab.discover", "vocab.scientist"],
            "A scientist does experiments.",
            "experiment = a test; discover = find something new; scientist = a person who studies science.",
        ),
        choice(
            "find-goggles",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: safety goggles",
            [(None, "🧲"), (None, "🔬"), (None, "🥽")],
            "c",
            ["vocab.goggles"],
            "You wear them to protect your eyes.",
            "🥽 safety goggles.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-magnet",
            "LISTENING",
            "Listen. What has the girl just done?",
            "She has just …",
            [
                ("finished an experiment", "🧪"),
                ("seen a volcano", "🌋"),
                ("lost her goggles", "🥽"),
            ],
            "a",
            ["grammar.just_already", "vocab.experiment"],
            "Listen for 'just'.",
            "I have just finished the magnet experiment.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Look, Mrs Park! I have just finished the magnet experiment, and I've written the results.",
        ),
        true_false(
            "listen-volcano",
            "LISTENING",
            "Listen to {teen} and {boy}. True or false?",
            "{boy} has already made a volcano.",
            False,
            ["grammar.ever_never", "grammar.just_already"],
            "Listen to his answer: 'No, I haven't. Not yet!'",
            "{boy} hasn't made a volcano yet. They are going to make one next week.",
            listening_id="b1-1-ever",
        ),
        true_false(
            "listen-sam",
            "LISTENING",
            "Listen to Mrs Park and {boy}. True or false?",
            "Sam has already finished the experiment.",
            True,
            ["grammar.just_already"],
            "What is Sam doing now?",
            "Sam has already finished. He's writing the results.",
            listening_id="b1-1-just",
        ),
        blank(
            "pp-blank",
            "GRAMMAR",
            "Choose the missing words.",
            "I ___ never ___ a volcano.",
            ["have", "seen"],
            ["have", "has", "seen", "saw"],
            ["grammar.present_perfect", "grammar.ever_never"],
            "have + past participle (see → seen).",
            "I have never seen a volcano.",
        ),
        blank(
            "has-blank",
            "GRAMMAR",
            "Choose the missing word.",
            "Mrs Park ___ just started the experiment.",
            ["has"],
            ["have", "has", "is"],
            ["grammar.present_perfect", "grammar.just_already"],
            "Mrs Park = she → has.",
            "Mrs Park has just started the experiment.",
        ),
        choice(
            "yet-already",
            "GRAMMAR",
            "Choose the right sentence.",
            "The club starts at three. It's two o'clock now. 🕑",
            [
                ("The club hasn't started yet.", None),
                ("The club has already started.", None),
                ("The club hasn't started already.", None),
            ],
            "a",
            ["grammar.just_already"],
            "Use yet in negatives.",
            "It is not three o'clock, so the club hasn't started yet.",
        ),
        choice(
            "pp-or-past",
            "GRAMMAR",
            "Choose the right sentence.",
            "Yesterday …",
            [
                ("we used a microscope.", None),
                ("we have used a microscope.", None),
                ("we have use a microscope.", None),
            ],
            "a",
            ["grammar.present_perfect", "vocab.microscope", "grammar.past_simple_regular"],
            "Yesterday is an exact time.",
            "Exact time → past simple: Yesterday we used a microscope.",
        ),
        build(
            "build-ever",
            "GRAMMAR",
            "Put the words in order.",
            "Have you ever used a magnet?",
            ["grammar.ever_never", "vocab.magnet"],
            "Start with 'Have you ever'.",
            "Have you ever used a magnet?",
        ),
        choice(
            "read-microscope",
            "READING",
            "Read the text. Then answer.",
            "What did they look at through the microscope?",
            [("a leaf", "🍃"), ("a magnet", "🧲"), ("a volcano", "🌋")],
            "a",
            ["vocab.microscope"],
            "Look at paragraph 3.",
            "They looked at a leaf through a microscope.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-magnet-paper",
            "READING",
            "Read the text. True or false?",
            "A magnet picks up paper.",
            False,
            ["vocab.magnet", "vocab.discover"],
            "Look at paragraph 4.",
            "A magnet picks up nails, but not paper or wood.",
        ),
        speak(
            "say-experiences",
            "Tell a friend about three things you have done and one thing you have never done.",
            "I have … I have also … But I have never …",
            "I have been to a museum. I have used a microscope. I have also made a cake. But I have never seen a volcano.",
            ["grammar.present_perfect", "grammar.ever_never"],
        ),
        choice(
            "quiz-bigger",
            "QUIZ",
            "Choose the right word.",
            "A plane is ___ than a train.",
            [("faster", None), ("more fast", None), ("fastest", None)],
            "a",
            ["grammar.comparatives", "vocab.fast"],
            "Remember A2: short adjective + -er.",
            "A plane is faster than a train.",
        ),
        blank(
            "quiz-saw",
            "QUIZ",
            "Choose the missing word.",
            "Last summer we ___ a big fish in the lake.",
            ["saw"],
            ["see", "saw", "seen"],
            ["grammar.past_simple_irregular", "vocab.saw"],
            "Last summer = exact time → past simple.",
            "Last summer we saw a big fish.",
        ),
        choice(
            "quiz-goggles",
            "QUIZ",
            "Choose the right word.",
            "Put on your … before the experiment. 🥽",
            [("safety goggles", None), ("sunglasses", None), ("swimsuit", None)],
            "a",
            ["vocab.goggles", "vocab.experiment"],
            "They protect your eyes in the lab.",
            "Put on your safety goggles.",
        ),
    ],
}

LESSON_2 = {
    "slug": L2,
    "title": "{teen}'s Band",
    "description": "{teen} has started a band. Who would like to play what?",
    "minutes": 30,
    "objectives": [
        "Name instruments and music words: guitar, drums, piano, concert, song.",
        "Make polite offers and requests with would like.",
        "Talk about preferences with prefer … to ….",
    ],
    "review": [
        "grammar.present_perfect",
        "grammar.ever_never",
        "grammar.just_already",
        "vocab.discover",
        "vocab.sing",
        "vocab.dance",
        "grammar.i_like",
        "grammar.do_you_like",
        "grammar.frequency_adverbs",
        "vocab.always",
    ],
    "episode": (
        "Band Practice",
        "{teen}'s new band practises in the garage. Who will play the drums?",
    ),
    "content": {
        "story_intro": "{teen} and her friends have started a band. They practise in the garage on Saturdays.",
        "reading": {
            "title": "The Garage Band",
            "paragraphs": [
                {
                    "sentences": [
                        "{teen} has started a band with two friends from school.",
                        "She plays the guitar and sings.",
                    ]
                },
                {
                    "sentences": [
                        "Her friend Leo plays the piano, and Maya would like to play the drums.",
                        "But Maya hasn't got any drums yet.",
                    ]
                },
                {
                    "sentences": [
                        "Dad has an old drum kit in the garage. He says: Would you like to use my drums, Maya?",
                        "Maya is very happy. Yes, please! I'd love to!",
                    ]
                },
                {
                    "sentences": [
                        "{boy} would like to join the band too, but he prefers listening to playing.",
                        "So he is their first fan!",
                    ]
                },
                {
                    "sentences": [
                        "The band practises every Saturday. They have already written two songs.",
                        "Their first concert is at the school in May.",
                    ]
                },
            ],
            "highlight": [
                "would like",
                "Would you like",
                "I'd love to",
                "prefers",
                "guitar",
                "piano",
                "drums",
                "concert",
            ],
        },
        "listening": [
            {
                "id": "b1-2-offer",
                "title": "Would you like …?",
                "transcript": [
                    {"speaker": "Mum", "text": "Would you like some juice, everyone?"},
                    {"speaker": "Leo", "text": "Yes, please. I'd like orange juice."},
                    {"speaker": "Maya", "text": "No, thank you. I'd like some water, please."},
                    {"speaker": "Mum", "text": "Here you are."},
                ],
            },
            {
                "id": "b1-2-prefer",
                "title": "Rock or pop?",
                "transcript": [
                    {"speaker": "{boy}", "text": "What kind of music do you prefer, Leo?"},
                    {"speaker": "Leo", "text": "I prefer rock to pop. It's more exciting."},
                    {
                        "speaker": "{boy}",
                        "text": "Me too! But {little} prefers songs from cartoons.",
                    },
                    {
                        "speaker": "Leo",
                        "text": "Maybe we can play a cartoon song at the concert for her!",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "would like",
                "explanation": (
                    "would like is a polite way to say want. I'd like some water. I'd like to play the drums. "
                    "Offers: Would you like some juice? — Yes, please. / No, thank you. "
                    "Invitations: Would you like to come? — I'd love to!"
                ),
                "explanation_ru": "I'd like = I would like — вежливое «я бы хотел». Would you like …? — «Не хочешь ли …?»",
                "examples": [
                    "I'd like a new guitar.",
                    "Would you like to play the piano?",
                    "Yes, please. / I'd love to!",
                ],
            },
            {
                "title": "prefer",
                "explanation": (
                    "prefer = like something more. I prefer rock to pop. "
                    "With verbs use -ing: He prefers listening to playing. (he / she prefers)"
                ),
                "explanation_ru": "prefer A to B — предпочитать A, а не B. После prefer глагол часто с -ing.",
                "examples": [
                    "I prefer the guitar to the piano.",
                    "She prefers singing to dancing.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "music-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("guitar", None, "🎸"),
                ("drums", None, "🥁"),
                ("piano", None, "🎹"),
                ("concert", None, "🎤"),
            ],
            ["vocab.guitar", "vocab.drums", "vocab.piano", "vocab.concert"],
            "You hit the drums with sticks.",
            "guitar 🎸, drums 🥁, piano 🎹, concert 🎤.",
        ),
        matching(
            "music-meanings",
            "VOCABULARY",
            "Match the word to its meaning.",
            [
                ("band", "a group of people who play music", None),
                ("practise", "do something again and again to get better", None),
                ("song", "music with words", None),
            ],
            ["vocab.band", "vocab.practise", "vocab.song"],
            "You sing a song.",
            "band = a music group; practise = do again to get better; song = music with words.",
        ),
        choice(
            "find-piano",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: piano",
            [(None, "🥁"), (None, "🎹"), (None, "🎸")],
            "b",
            ["vocab.piano"],
            "It has black and white keys.",
            "🎹 piano.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-instrument",
            "LISTENING",
            "Listen. Which instrument would the boy like to play?",
            "He would like to play the …",
            [("drums", "🥁"), ("guitar", "🎸"), ("piano", "🎹")],
            "c",
            ["grammar.would_like", "vocab.piano"],
            "Listen for 'I'd like to'.",
            "I'd like to play the piano.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="I don't like the drums, they're too loud. I'd like to play the piano, like my granny.",
        ),
        true_false(
            "listen-maya-water",
            "LISTENING",
            "Listen to Mum and the band. True or false?",
            "Maya would like some orange juice.",
            False,
            ["grammar.would_like"],
            "Who would like orange juice?",
            "Leo would like orange juice. Maya would like some water.",
            listening_id="b1-2-offer",
        ),
        true_false(
            "listen-leo-rock",
            "LISTENING",
            "Listen to {boy} and Leo. True or false?",
            "Leo prefers rock to pop.",
            True,
            ["grammar.prefer"],
            "Listen to Leo's first answer.",
            "Leo: I prefer rock to pop.",
            listening_id="b1-2-prefer",
        ),
        choice(
            "would-answer",
            "GRAMMAR",
            "Choose the best answer.",
            "Would you like to come to our concert? 🎤",
            [("I'd love to!", None), ("Yes, I like.", None), ("Yes, I would like it to.", None)],
            "a",
            ["grammar.would_like", "vocab.concert"],
            "A happy answer to an invitation.",
            "Would you like to come? — I'd love to!",
        ),
        blank(
            "would-like-blank",
            "GRAMMAR",
            "Choose the missing words.",
            "I'd ___ ___ play the drums.",
            ["like", "to"],
            ["like", "likes", "to", "for"],
            ["grammar.would_like", "vocab.drums"],
            "I'd like + to + verb.",
            "I'd like to play the drums.",
        ),
        blank(
            "prefer-blank",
            "GRAMMAR",
            "Choose the missing words.",
            "{boy} ___ listening ___ playing.",
            ["prefers", "to"],
            ["prefer", "prefers", "to", "than"],
            ["grammar.prefer"],
            "He → prefers. prefer A to B.",
            "{boy} prefers listening to playing.",
        ),
        build(
            "build-prefer",
            "GRAMMAR",
            "Put the words in order.",
            "I prefer the guitar to the piano.",
            ["grammar.prefer", "vocab.guitar", "vocab.piano"],
            "Start with 'I prefer'.",
            "I prefer the guitar to the piano.",
        ),
        choice(
            "read-drums",
            "READING",
            "Read the text. Then answer.",
            "Where does Maya get drums?",
            [
                ("Dad lends her his old drums.", "🥁"),
                ("She buys them at a shop.", "🏪"),
                ("Leo gives them to her.", "🎹"),
            ],
            "a",
            ["vocab.drums", "grammar.would_like"],
            "Look at paragraph 3.",
            "Dad has an old drum kit and offers it to Maya.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-songs",
            "READING",
            "Read the text. True or false?",
            "The band hasn't written any songs yet.",
            False,
            ["vocab.song", "grammar.just_already"],
            "Look at the last paragraph.",
            "They have already written two songs.",
        ),
        speak(
            "say-music",
            "Talk about music. Which instrument would you like to play? What kind of music do you prefer?",
            "I'd like to play … I prefer … to …",
            "I'd like to play the guitar. I prefer rock to pop, and I prefer playing to listening.",
            ["grammar.would_like", "grammar.prefer"],
        ),
        blank(
            "quiz-ever",
            "QUIZ",
            "Choose the missing word.",
            "Have you ___ been to a concert?",
            ["ever"],
            ["ever", "never", "yet"],
            ["grammar.ever_never", "vocab.concert"],
            "Remember Lesson 1: questions about experience.",
            "Have you ever been to a concert?",
        ),
        choice(
            "quiz-already",
            "QUIZ",
            "Choose the right sentence.",
            "The band started at ten. Now it's eleven.",
            [
                ("They have already practised for an hour.", None),
                ("They haven't practised already.", None),
                ("They have practise yet.", None),
            ],
            "a",
            ["grammar.just_already", "vocab.practise"],
            "Remember Lesson 1: already in positive sentences.",
            "They have already practised for an hour.",
        ),
        blank(
            "quiz-always",
            "QUIZ",
            "Choose the missing word.",
            "{teen} ___ practises on Saturdays. She never misses it!",
            ["always"],
            ["always", "never", "sometimes"],
            ["grammar.frequency_adverbs", "vocab.always"],
            "Remember A2: she never misses it = every time.",
            "{teen} always practises on Saturdays.",
        ),
    ],
}

LESSON_3 = {
    "slug": L3,
    "title": "Cooking with Aunt {aunt}",
    "description": "Aunt {aunt} teaches {boy} and {little} to bake. What will happen if …?",
    "minutes": 30,
    "objectives": [
        "Name baking words: recipe, flour, sugar, butter, oven, mix.",
        "Use a little / a few / too much / too many.",
        "Talk about results with the first conditional: If …, … will ….",
    ],
    "review": [
        "grammar.would_like",
        "grammar.prefer",
        "vocab.practise",
        "grammar.present_perfect",
        "grammar.some_any",
        "grammar.how_much",
        "vocab.egg",
        "vocab.milk",
        "vocab.cake",
        "vocab.hot",
    ],
    "episode": (
        "The Flour Cloud",
        "Aunt {aunt} shows the children her famous apple cake recipe. {little} opens the flour too fast!",
    ),
    "content": {
        "story_intro": "Aunt {aunt} is a great cook. Today she is teaching {boy} and {little} her apple cake recipe.",
        "reading": {
            "title": "Aunt {aunt}'s Apple Cake",
            "paragraphs": [
                {
                    "sentences": [
                        "First, Aunt {aunt} turns on the oven. If the oven isn't hot, the cake won't rise.",
                        "Then she reads the recipe with the children.",
                    ]
                },
                {
                    "sentences": [
                        "{boy} mixes the butter and a little sugar.",
                        "Be careful! If you add too much sugar, the cake will be too sweet.",
                    ]
                },
                {
                    "sentences": [
                        "{little} adds a few eggs and some flour.",
                        "Oops! She opens the bag too fast, and there is a big white cloud in the kitchen!",
                    ]
                },
                {
                    "sentences": [
                        "Everybody laughs. Aunt {aunt} says: If we clean up now, the cake will be ready on time.",
                        "They cut a few apples and put them on top.",
                    ]
                },
                {
                    "sentences": [
                        "The cake is in the oven for forty minutes.",
                        "If you visit Aunt {aunt}, she will give you a piece!",
                    ]
                },
            ],
            "highlight": [
                "If",
                "will",
                "won't",
                "a little",
                "a few",
                "too much",
                "recipe",
                "oven",
                "flour",
            ],
        },
        "listening": [
            {
                "id": "b1-3-shopping",
                "title": "What do we need?",
                "transcript": [
                    {"speaker": "Aunt {aunt}", "text": "Have we got enough eggs?"},
                    {"speaker": "{boy}", "text": "We've only got a few. Three, I think."},
                    {"speaker": "Aunt {aunt}", "text": "That's fine. And is there any milk?"},
                    {
                        "speaker": "{boy}",
                        "text": "Only a little. If we need more, I'll go to the shop.",
                    },
                ],
            },
            {
                "id": "b1-3-if",
                "title": "If it rains …",
                "transcript": [
                    {"speaker": "{little}", "text": "Can we have a picnic with the cake tomorrow?"},
                    {"speaker": "Aunt {aunt}", "text": "If it's sunny, we'll go to the park."},
                    {"speaker": "{little}", "text": "And if it rains?"},
                    {
                        "speaker": "Aunt {aunt}",
                        "text": "If it rains, we'll eat it at home and watch a film.",
                    },
                ],
            },
        ],
        "grammar": [
            {
                "title": "The first conditional",
                "explanation": (
                    "Use it for real possibilities in the future. If + present simple, will / won't + verb. "
                    "If it rains, we'll stay at home. If you add too much sugar, the cake will be too sweet. "
                    "Don't use will after if: If it rains (NOT If it will rain)."
                ),
                "explanation_ru": (
                    "Если …, то … (реальное будущее). После if — настоящее время, в другой части — will: "
                    "If it rains, we will stay at home = Если пойдёт дождь, мы останемся дома."
                ),
                "examples": [
                    "If you hurry, you'll catch the bus.",
                    "If it's sunny, we'll go to the park.",
                    "The cake won't rise if the oven is cold.",
                ],
            },
            {
                "title": "a little / a few / too much / too many",
                "explanation": (
                    "Uncountable nouns (sugar, milk, flour): a little, too much, How much? "
                    "Countable nouns (eggs, apples): a few, too many, How many?"
                ),
                "explanation_ru": "a little / too much — с неисчисляемыми; a few / too many — с исчисляемыми.",
                "examples": ["a little milk", "a few apples", "too much sugar", "too many eggs"],
            },
        ],
    },
    "exercises": [
        matching(
            "baking-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("flour", None, "🌾"),
                ("butter", None, "🧈"),
                ("sugar", None, "🍬"),
                ("oven", None, "🔥"),
            ],
            ["vocab.flour", "vocab.butter", "vocab.sugar", "vocab.oven"],
            "Flour is made from wheat.",
            "flour 🌾, butter 🧈, sugar 🍬, oven 🔥.",
        ),
        matching(
            "baking-meanings",
            "VOCABULARY",
            "Match the word to its meaning.",
            [
                ("recipe", "instructions for cooking something", None),
                ("mix", "put things together and stir", None),
                ("oven", "a hot box for baking", None),
            ],
            ["vocab.recipe", "vocab.mix", "vocab.oven"],
            "You follow a recipe.",
            "recipe = cooking instructions; mix = stir together; oven = a hot box for baking.",
        ),
        choice(
            "find-butter",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: butter",
            [(None, "🧈"), (None, "🌾"), (None, "🥣")],
            "a",
            ["vocab.butter"],
            "It is yellow and soft.",
            "🧈 butter.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-if-late",
            "LISTENING",
            "Listen. What will happen if they don't hurry?",
            "If they don't hurry, …",
            [("they will miss the bus", "🚌"), ("the cake will burn", "🔥"), ("it will rain", "🌧️")],
            "b",
            ["grammar.first_conditional", "vocab.oven"],
            "Listen for 'If we don't hurry'.",
            "If we don't hurry, the cake will burn!",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="Quick, take it out of the oven! If we don't hurry, the cake will burn!",
        ),
        true_false(
            "listen-eggs",
            "LISTENING",
            "Listen to Aunt {aunt} and {boy}. True or false?",
            "They have got a lot of eggs.",
            False,
            ["grammar.a_little_a_few", "vocab.egg"],
            "How many eggs have they got?",
            "They have only got a few eggs — three.",
            listening_id="b1-3-shopping",
        ),
        true_false(
            "listen-rain-film",
            "LISTENING",
            "Listen to {little} and Aunt {aunt}. True or false?",
            "If it rains, they will watch a film at home.",
            True,
            ["grammar.first_conditional", "vocab.rainy"],
            "Listen to the last line.",
            "If it rains, we'll eat it at home and watch a film.",
            listening_id="b1-3-if",
        ),
        blank(
            "if-blank",
            "GRAMMAR",
            "Choose the missing words.",
            "If you ___ too much sugar, the cake ___ be too sweet.",
            ["add", "will"],
            ["add", "will add", "will", "is"],
            ["grammar.first_conditional", "vocab.sugar"],
            "If + present, … will …",
            "If you add too much sugar, the cake will be too sweet.",
        ),
        choice(
            "if-right",
            "GRAMMAR",
            "Choose the right sentence.",
            "Tomorrow, maybe it will be sunny.",
            [
                ("If it is sunny, we will go to the park.", None),
                ("If it will be sunny, we go to the park.", None),
                ("If it is sunny, we go to the park yesterday.", None),
            ],
            "a",
            ["grammar.first_conditional", "vocab.sunny"],
            "No will after if.",
            "If it is sunny, we will go to the park.",
        ),
        blank(
            "few-little-blank",
            "GRAMMAR",
            "Choose the missing words.",
            "Add a ___ milk and a ___ eggs.",
            ["little", "few"],
            ["little", "few", "many"],
            ["grammar.a_little_a_few", "vocab.milk", "vocab.egg"],
            "milk = uncountable; eggs = countable.",
            "Add a little milk and a few eggs.",
        ),
        build(
            "build-if",
            "GRAMMAR",
            "Put the words in order.",
            "If the oven is cold, the cake won't rise.",
            ["grammar.first_conditional", "vocab.oven"],
            "Start with 'If the oven'.",
            "If the oven is cold, the cake won't rise.",
        ),
        order(
            "read-order",
            "READING",
            "Put the recipe in order.",
            [
                "Aunt {aunt} turns on the oven.",
                "{boy} mixes the butter and sugar.",
                "{little} adds eggs and flour.",
                "They put apples on top.",
                "The cake bakes for forty minutes.",
            ],
            ["vocab.recipe", "vocab.mix", "vocab.oven"],
            "The oven needs to get hot first.",
            "Oven on → butter and sugar → eggs and flour → apples → bake.",
        ),
        choice(
            "read-cloud",
            "READING",
            "Read the text. Then answer.",
            "Why is there a white cloud in the kitchen?",
            [
                ("{little} opened the flour too fast.", "🌾"),
                ("The cake burned in the oven.", "🔥"),
                ("{boy} added too much sugar.", "🍬"),
            ],
            "a",
            ["vocab.flour"],
            "Look at paragraph 3.",
            "{little} opened the bag of flour too fast.",
            ex_type="READING_COMPREHENSION",
        ),
        speak(
            "say-if",
            "Finish these sentences about your weekend: If it's sunny, … If it rains, … If I have time, …",
            "If it's sunny, I'll … If it rains, I'll … If I have time, I'll …",
            "If it's sunny, I'll play football. If it rains, I'll read a book. If I have time, I'll bake a cake.",
            ["grammar.first_conditional"],
        ),
        choice(
            "quiz-would-like",
            "QUIZ",
            "Choose the best answer.",
            "Would you like a piece of cake? 🍰",
            [("Yes, please!", None), ("Yes, I like.", None), ("Yes, I would like to cake.", None)],
            "a",
            ["grammar.would_like", "vocab.cake"],
            "Remember Lesson 2: offers.",
            "Would you like …? — Yes, please!",
        ),
        blank(
            "quiz-prefer",
            "QUIZ",
            "Choose the missing word.",
            "{little} prefers cake ___ soup.",
            ["to"],
            ["to", "than", "of"],
            ["grammar.prefer", "vocab.soup"],
            "Remember Lesson 2: prefer A to B.",
            "{little} prefers cake to soup.",
        ),
        choice(
            "quiz-how-much",
            "QUIZ",
            "Choose the right question.",
            "You need to know the amount of flour.",
            [
                ("How much flour do we need?", None),
                ("How many flour do we need?", None),
                ("How flour do we need?", None),
            ],
            "a",
            ["grammar.how_much", "vocab.flour"],
            "Flour is uncountable.",
            "How much flour do we need?",
        ),
        blank(
            "quiz-has-made",
            "QUIZ",
            "Choose the missing word.",
            "Aunt {aunt} has ___ this cake a hundred times!",
            ["made"],
            ["make", "made", "making"],
            ["grammar.present_perfect"],
            "Remember Lesson 1: has + past participle.",
            "She has made this cake a hundred times.",
        ),
    ],
}

LESSON_4 = {
    "slug": L4,
    "title": "The Lost Kitten",
    "description": "The neighbour's kitten is missing. What were the children doing when they heard it?",
    "minutes": 30,
    "objectives": [
        "Use story words: kitten, neighbour, search, suddenly, worried.",
        "Describe actions in progress with the past continuous.",
        "Tell a story with when and while.",
    ],
    "review": [
        "grammar.first_conditional",
        "grammar.a_little_a_few",
        "vocab.recipe",
        "grammar.would_like",
        "grammar.past_simple_irregular",
        "grammar.was_were",
        "vocab.cat",
        "vocab.where",
        "vocab.under",
        "grammar.present_continuous",
    ],
    "episode": (
        "Where Is Whiskers?",
        "The family helps their neighbour Mrs Hill to search for her lost kitten.",
    ),
    "content": {
        "story_intro": "Last Sunday something exciting happened in our street.",
        "reading": {
            "title": "Where Is Whiskers?",
            "paragraphs": [
                {
                    "sentences": [
                        "Last Sunday it was raining. {boy} was doing his homework and {little} was drawing a picture.",
                        "Suddenly somebody knocked on the door.",
                    ]
                },
                {
                    "sentences": [
                        "It was our neighbour, Mrs Hill. She was very worried.",
                        "Her kitten, Whiskers, was lost!",
                    ]
                },
                {
                    "sentences": [
                        "We put on our coats and searched for Whiskers everywhere.",
                        "We looked under the cars and in the gardens, but we didn't find her.",
                    ]
                },
                {
                    "sentences": [
                        "While we were walking past the park, {little} heard a small sound: Miaow!",
                        "Whiskers was sitting high up in a tree.",
                    ]
                },
                {
                    "sentences": [
                        "Dad got a ladder and carried the kitten down.",
                        "Mrs Hill was so happy that she gave us a big box of chocolates!",
                    ]
                },
            ],
            "highlight": [
                "was raining",
                "was doing",
                "was drawing",
                "were walking",
                "was sitting",
                "Suddenly",
                "While",
            ],
        },
        "listening": [
            {
                "id": "b1-4-doing",
                "title": "What were you doing?",
                "transcript": [
                    {"speaker": "Mrs Hill", "text": "When did you last see Whiskers?"},
                    {"speaker": "{boy}", "text": "This morning. She was playing in your garden."},
                    {"speaker": "Mrs Hill", "text": "And what were you doing?"},
                    {"speaker": "{boy}", "text": "I was riding my bike in the street."},
                ],
            },
            {
                "id": "b1-4-found",
                "title": "We found her!",
                "transcript": [
                    {
                        "speaker": "{little}",
                        "text": "Mum! While we were walking past the park, I heard a kitten!",
                    },
                    {"speaker": "Mum", "text": "Where was it?"},
                    {
                        "speaker": "{little}",
                        "text": "It was sitting in a tree. Dad is getting it down now.",
                    },
                    {"speaker": "Mum", "text": "Well done, {little}!"},
                ],
            },
        ],
        "grammar": [
            {
                "title": "Past continuous",
                "explanation": (
                    "Use was / were + verb-ing for an action in progress at a time in the past. "
                    "At five o'clock I was doing my homework. They were playing in the garden. "
                    "Question: What were you doing? Negative: She wasn't sleeping."
                ),
                "explanation_ru": (
                    "Past continuous — «что происходило» в какой-то момент в прошлом: "
                    "I was reading = Я читал (в тот момент)."
                ),
                "examples": [
                    "It was raining all day.",
                    "What were you doing at six?",
                    "We weren't watching TV.",
                ],
            },
            {
                "title": "Past continuous and past simple: when / while",
                "explanation": (
                    "A long action (past continuous) is interrupted by a short action (past simple). "
                    "I was doing my homework when somebody knocked on the door. "
                    "While we were walking, we heard a sound."
                ),
                "explanation_ru": "Длинное действие — was/were + -ing; короткое, которое его прервало, — past simple.",
                "examples": [
                    "I was sleeping when the phone rang.",
                    "While Dad was cooking, the kitten came in.",
                ],
            },
        ],
    },
    "exercises": [
        matching(
            "story-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("kitten", None, "🐈"),
                ("tree", None, "🌳"),
                ("worried", None, "😟"),
                ("neighbour", None, "🏘️"),
            ],
            ["vocab.kitten", "vocab.tree", "vocab.worried", "vocab.neighbour"],
            "A kitten is a baby cat.",
            "kitten 🐈, tree 🌳, worried 😟, neighbour 🏘️.",
        ),
        matching(
            "story-meanings",
            "VOCABULARY",
            "Match the word to its meaning.",
            [
                ("search", "look carefully for something", None),
                ("suddenly", "quickly and unexpectedly", None),
                ("neighbour", "a person who lives near you", None),
            ],
            ["vocab.search", "vocab.suddenly", "vocab.neighbour"],
            "You search for something you have lost.",
            "search = look for; suddenly = quickly and unexpectedly; neighbour = a person who lives near you.",
        ),
        choice(
            "find-worried",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: worried",
            [(None, "😀"), (None, "😟"), (None, "😴")],
            "b",
            ["vocab.worried"],
            "Mrs Hill's face when her kitten was lost.",
            "😟 worried.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-interrupt",
            "LISTENING",
            "Listen. What was the girl doing when the kitten came in?",
            "She was …",
            [("watching TV", "📺"), ("eating breakfast", "🥣"), ("reading a book", "📖")],
            "c",
            ["grammar.when_while", "vocab.kitten"],
            "Listen for 'I was … when …'.",
            "I was reading a book when the kitten came in.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="I was reading a book in the garden when a little kitten came in and sat on my feet!",
        ),
        true_false(
            "listen-bike",
            "LISTENING",
            "Listen to Mrs Hill and {boy}. True or false?",
            "{boy} was riding his bike in the morning.",
            True,
            ["grammar.past_continuous", "vocab.bike"],
            "What was {boy} doing?",
            "I was riding my bike in the street.",
            listening_id="b1-4-doing",
        ),
        true_false(
            "listen-house",
            "LISTENING",
            "Listen to {little} and Mum. True or false?",
            "The kitten was sitting in a car.",
            False,
            ["grammar.past_continuous", "vocab.tree"],
            "Where was the kitten?",
            "It was sitting in a tree.",
            listening_id="b1-4-found",
        ),
        blank(
            "pc-blank",
            "GRAMMAR",
            "Choose the missing words.",
            "At six o'clock {boy} ___ doing his homework and the girls ___ drawing.",
            ["was", "were"],
            ["was", "were", "did"],
            ["grammar.past_continuous"],
            "he → was; they → were.",
            "{boy} was doing his homework and the girls were drawing.",
        ),
        blank(
            "when-blank",
            "GRAMMAR",
            "Choose the missing words.",
            "I was sleeping when the phone ___. While Dad was ___, the kitten ran in.",
            ["rang", "cooking"],
            ["rang", "was ringing", "cooking", "cooked"],
            ["grammar.when_while"],
            "Short action → past simple; long action → -ing.",
            "I was sleeping when the phone rang. While Dad was cooking, the kitten ran in.",
        ),
        choice(
            "pc-question",
            "GRAMMAR",
            "Choose the right question.",
            "You want to know about yesterday at 7 pm.",
            [
                ("What were you doing at seven yesterday?", None),
                ("What you were doing at seven yesterday?", None),
                ("What did you doing at seven yesterday?", None),
            ],
            "a",
            ["grammar.past_continuous"],
            "What + were + you + -ing?",
            "What were you doing at seven yesterday?",
        ),
        build(
            "build-while",
            "GRAMMAR",
            "Put the words in order.",
            "While we were walking, we heard a kitten.",
            ["grammar.when_while", "vocab.kitten"],
            "Start with 'While we were'.",
            "While we were walking, we heard a kitten.",
        ),
        order(
            "read-order",
            "READING",
            "Put the story in order.",
            [
                "Mrs Hill knocked on the door.",
                "The family searched under cars and in gardens.",
                "{little} heard a sound near the park.",
                "Dad carried the kitten down from the tree.",
                "Mrs Hill gave them chocolates.",
            ],
            ["vocab.search", "vocab.neighbour"],
            "The story starts with a knock on the door.",
            "Knock → search → sound → Dad and the ladder → chocolates.",
        ),
        choice(
            "read-weather",
            "READING",
            "Read the text. Then answer.",
            "What was the weather like last Sunday?",
            [("It was raining.", "🌧️"), ("It was sunny.", "☀️"), ("It was snowing.", "❄️")],
            "a",
            ["grammar.past_continuous"],
            "Look at the first sentence.",
            "Last Sunday it was raining.",
            ex_type="READING_COMPREHENSION",
        ),
        speak(
            "say-story",
            "Tell a short story: What were you doing yesterday at five o'clock? Then what happened suddenly?",
            "Yesterday at five o'clock I was … Suddenly …",
            "Yesterday at five o'clock I was playing in the garden. Suddenly it started to rain, so I ran inside.",
            ["grammar.past_continuous", "grammar.when_while", "vocab.suddenly"],
        ),
        choice(
            "quiz-if-find",
            "QUIZ",
            "Choose the right ending.",
            "If we find Whiskers, …",
            [
                ("Mrs Hill will be very happy.", None),
                ("Mrs Hill is happy yesterday.", None),
                ("Mrs Hill will happy.", None),
            ],
            "a",
            ["grammar.first_conditional"],
            "Remember Lesson 3: If …, … will + verb.",
            "If we find Whiskers, Mrs Hill will be very happy.",
        ),
        blank(
            "quiz-few",
            "QUIZ",
            "Choose the missing word.",
            "We only looked in a ___ gardens.",
            ["few"],
            ["few", "little", "much"],
            ["grammar.a_little_a_few"],
            "Remember Lesson 3: gardens are countable.",
            "We only looked in a few gardens.",
        ),
        choice(
            "quiz-ladder-under",
            "QUIZ",
            "Choose the right word.",
            "The kitten wasn't ___ the car. It was in the tree.",
            [("under", None), ("into", None), ("at", None)],
            "a",
            ["vocab.under", "vocab.car"],
            "Remember A1: in, on, under.",
            "The kitten wasn't under the car.",
        ),
    ],
}

LESSON_5 = {
    "slug": L5,
    "title": "The School Play",
    "description": "{boy} is in the school play. What must he do? Then a review of the unit.",
    "minutes": 35,
    "objectives": [
        "Talk about feelings: nervous, excited, proud.",
        "Talk about rules with must, have to, don't have to and mustn't.",
        "Review Unit 1: present perfect, would like, first conditional, past continuous.",
    ],
    "review": [
        "grammar.past_continuous",
        "grammar.when_while",
        "vocab.suddenly",
        "grammar.first_conditional",
        "grammar.would_like",
        "grammar.present_perfect",
        "vocab.concert",
        "vocab.sing",
    ],
    "episode": (
        "The King Who Forgot His Lines",
        "{boy} plays the king in the school play. He is nervous, but his family is in the audience.",
    ),
    "content": {
        "story_intro": "It's the night of the school play. {boy} is the king, and {little} is a little star.",
        "reading": {
            "title": "Backstage",
            "paragraphs": [
                {
                    "sentences": [
                        "Our teacher, Mr Brown, gave us the rules: You must be quiet backstage. You mustn't touch the lights.",
                        "We have to be on the stage at seven o'clock.",
                    ]
                },
                {
                    "sentences": [
                        "I play the king, so I have to wear a big costume with a gold crown.",
                        "{little} is a star. She doesn't have to say anything, she only has to dance.",
                    ]
                },
                {
                    "sentences": [
                        "Before the play I felt very nervous. My hands were cold!",
                        "{teen} came backstage and said: Break a leg!",
                    ]
                },
                {
                    "sentences": [
                        "While I was saying my lines, I suddenly forgot a word.",
                        "But my friend whispered it, and nobody in the audience noticed.",
                    ]
                },
                {
                    "sentences": [
                        "At the end the audience clapped and clapped.",
                        "Mum and Dad were very proud, and {little} was so excited that she couldn't sleep!",
                    ]
                },
            ],
            "highlight": [
                "must",
                "mustn't",
                "have to",
                "has to",
                "doesn't have to",
                "nervous",
                "proud",
                "excited",
            ],
        },
        "listening": [
            {
                "id": "b1-5-rules",
                "title": "The rules",
                "transcript": [
                    {
                        "speaker": "Mr Brown",
                        "text": "Remember, everybody: you must be here at half past six.",
                    },
                    {"speaker": "{boy}", "text": "Do we have to bring our costumes?"},
                    {
                        "speaker": "Mr Brown",
                        "text": "No, you don't have to. They're already here at school.",
                    },
                    {"speaker": "Mr Brown", "text": "And you mustn't eat in your costumes!"},
                ],
            },
            {
                "id": "b1-5-feelings",
                "title": "How do you feel?",
                "transcript": [
                    {"speaker": "Mum", "text": "How do you feel, {boy}?"},
                    {"speaker": "{boy}", "text": "I'm a bit nervous. What if I forget my lines?"},
                    {"speaker": "Mum", "text": "If you forget a word, your friends will help you."},
                    {"speaker": "{little}", "text": "I'm not nervous. I'm excited!"},
                ],
            },
        ],
        "grammar": [
            {
                "title": "must / have to",
                "explanation": (
                    "must and have to both mean it is necessary. You must be quiet. We have to be on stage at seven. "
                    "he / she / it has to. Questions: Do we have to …? Past: had to."
                ),
                "explanation_ru": "must / have to — «должен, нужно». He has to …; в прошлом — had to.",
                "examples": [
                    "We must learn our lines.",
                    "She has to wear a costume.",
                    "Do I have to sing?",
                ],
            },
            {
                "title": "don't have to / mustn't",
                "explanation": (
                    "Be careful! They are different. don't have to = it isn't necessary, you can choose. "
                    "mustn't = it is not allowed, don't do it! "
                    "You don't have to bring a costume. You mustn't touch the lights."
                ),
                "explanation_ru": "don't have to — «не обязательно»; mustn't — «нельзя».",
                "examples": ["{little} doesn't have to speak.", "You mustn't run on the stage."],
            },
        ],
    },
    "exercises": [
        matching(
            "play-words",
            "VOCABULARY",
            "Match each word to the picture.",
            [
                ("stage", None, "🎭"),
                ("costume", None, "👑"),
                ("audience", None, "👏"),
                ("nervous", None, "😬"),
            ],
            ["vocab.stage", "vocab.costume", "vocab.audience", "vocab.nervous"],
            "The audience claps.",
            "stage 🎭, costume 👑, audience 👏, nervous 😬.",
        ),
        matching(
            "feelings",
            "VOCABULARY",
            "Match the feeling to the situation.",
            [
                ("nervous", "before a big test", None),
                ("proud", "when your child does something great", None),
                ("excited", "the night before your birthday", None),
            ],
            ["vocab.nervous", "vocab.proud", "vocab.excited"],
            "Parents feel proud of their children.",
            "nervous before a test; proud of your child; excited before your birthday.",
        ),
        choice(
            "find-excited",
            "VOCABULARY",
            "Tap the right picture.",
            "Find: excited",
            [(None, "😬"), (None, "😟"), (None, "🤩")],
            "c",
            ["vocab.excited"],
            "A very happy face, waiting for something great.",
            "🤩 excited.",
            ex_type="IMAGE_SELECTION",
        ),
        choice(
            "listen-rule",
            "LISTENING",
            "Listen to the teacher. What mustn't the children do?",
            "They mustn't …",
            [("run on the stage", "🏃"), ("sing", "🎤"), ("wear costumes", "👑")],
            "a",
            ["grammar.dont_have_to", "vocab.stage"],
            "Listen for 'mustn't'.",
            "You mustn't run on the stage.",
            ex_type="LISTENING_COMPREHENSION",
            listen_text="You can sing as loudly as you like, but you mustn't run on the stage. It's dangerous.",
        ),
        true_false(
            "listen-costumes",
            "LISTENING",
            "Listen to Mr Brown. True or false?",
            "The children have to bring their costumes.",
            False,
            ["grammar.dont_have_to", "vocab.costume"],
            "Where are the costumes?",
            "They don't have to bring them. The costumes are already at school.",
            listening_id="b1-5-rules",
        ),
        true_false(
            "listen-little-excited",
            "LISTENING",
            "Listen to Mum and the children. True or false?",
            "{little} is nervous.",
            False,
            ["vocab.nervous", "vocab.excited"],
            "Listen to {little}'s answer.",
            "{little}: I'm not nervous. I'm excited!",
            listening_id="b1-5-feelings",
        ),
        blank(
            "has-to-blank",
            "GRAMMAR",
            "Choose the missing words.",
            "{boy} ___ to wear a crown. {little} ___ have to speak.",
            ["has", "doesn't"],
            ["has", "have", "doesn't", "mustn't"],
            ["grammar.must_have_to", "grammar.dont_have_to"],
            "he / she → has to, doesn't have to.",
            "{boy} has to wear a crown. {little} doesn't have to speak.",
        ),
        choice(
            "mustnt-or-dont",
            "GRAMMAR",
            "Choose the right sentence.",
            "It's dangerous to touch the stage lights. 💡",
            [
                ("You mustn't touch the lights.", None),
                ("You don't have to touch the lights.", None),
                ("You must touch the lights.", None),
            ],
            "a",
            ["grammar.dont_have_to"],
            "It is not allowed.",
            "You mustn't touch the lights.",
        ),
        choice(
            "dont-have-to-meaning",
            "GRAMMAR",
            "What does it mean?",
            "You don't have to wear a costume.",
            [
                ("You can wear a costume, but it isn't necessary.", None),
                ("You are not allowed to wear a costume.", None),
                ("You must wear a costume.", None),
            ],
            "a",
            ["grammar.dont_have_to", "vocab.costume"],
            "don't have to = not necessary.",
            "don't have to = it isn't necessary, you can choose.",
        ),
        build(
            "build-must",
            "GRAMMAR",
            "Put the words in order.",
            "We must be quiet backstage.",
            ["grammar.must_have_to"],
            "Start with 'We must'.",
            "We must be quiet backstage.",
        ),
        choice(
            "read-forgot",
            "READING",
            "Read the text. Then answer.",
            "What happened while {boy} was saying his lines?",
            [
                ("He forgot a word.", "😳"),
                ("His crown fell off.", "👑"),
                ("The lights went out.", "💡"),
            ],
            "a",
            ["grammar.when_while", "vocab.suddenly"],
            "Look at paragraph 4.",
            "While I was saying my lines, I suddenly forgot a word.",
            ex_type="READING_COMPREHENSION",
        ),
        true_false(
            "read-audience",
            "READING",
            "Read the text. True or false?",
            "The audience noticed that {boy} forgot a word.",
            False,
            ["vocab.audience"],
            "Look at paragraph 4.",
            "His friend whispered the word, and nobody in the audience noticed.",
        ),
        speak(
            "say-rules",
            "Tell a new student the rules at your school. What must you do? What don't you have to do? What mustn't you do?",
            "You must … You have to … You don't have to … You mustn't …",
            "You must be on time. You have to wear a uniform. You don't have to bring lunch. You mustn't run in the corridors.",
            ["grammar.must_have_to", "grammar.dont_have_to"],
        ),
        blank(
            "quiz-pp-never",
            "QUIZ",
            "Choose the missing words.",
            "I have ___ ___ in a play before!",
            ["never", "been"],
            ["never", "ever", "been", "was"],
            ["grammar.present_perfect", "grammar.ever_never"],
            "Remember Lesson 1.",
            "I have never been in a play before!",
        ),
        choice(
            "quiz-scientist",
            "QUIZ",
            "Choose the right word.",
            "Mrs Park studies science. She is a …",
            [("scientist", None), ("neighbour", None), ("band", None)],
            "a",
            ["vocab.scientist"],
            "Remember Lesson 1.",
            "She is a scientist.",
        ),
        choice(
            "quiz-band",
            "QUIZ",
            "Choose the best answer.",
            "Would you like to sing in our band? 🎸",
            [("I'd love to!", None), ("Yes, I'd like.", None), ("I prefer to sing than.", None)],
            "a",
            ["grammar.would_like", "vocab.band"],
            "Remember Lesson 2.",
            "Would you like to …? — I'd love to!",
        ),
        blank(
            "quiz-prefer-dance",
            "QUIZ",
            "Choose the missing word.",
            "{little} prefers dancing ___ speaking.",
            ["to"],
            ["to", "than", "for"],
            ["grammar.prefer"],
            "Remember Lesson 2.",
            "{little} prefers dancing to speaking.",
        ),
        blank(
            "quiz-if-forget",
            "QUIZ",
            "Choose the missing words.",
            "If you ___ a word, your friend ___ help you.",
            ["forget", "will"],
            ["forget", "will forget", "will", "does"],
            ["grammar.first_conditional"],
            "Remember Lesson 3.",
            "If you forget a word, your friend will help you.",
        ),
        choice(
            "quiz-sugar",
            "QUIZ",
            "Choose the right word.",
            "Don't put ___ sugar in the tea. It's too sweet!",
            [("too much", None), ("too many", None), ("a few", None)],
            "a",
            ["grammar.a_little_a_few", "vocab.sugar"],
            "Remember Lesson 3: sugar is uncountable.",
            "Don't put too much sugar in the tea.",
        ),
        blank(
            "quiz-was-sitting",
            "QUIZ",
            "Choose the missing words.",
            "The kitten ___ sitting in the tree when {little} ___ it.",
            ["was", "heard"],
            ["was", "were", "heard", "was hearing"],
            ["grammar.past_continuous", "grammar.when_while", "vocab.kitten"],
            "Remember Lesson 4.",
            "The kitten was sitting in the tree when {little} heard it.",
        ),
        choice(
            "quiz-proud",
            "QUIZ",
            "Choose the right word.",
            "Mum and Dad watched the play. They were very ___ of us.",
            [("proud", None), ("nervous", None), ("worried", None)],
            "a",
            ["vocab.proud", "vocab.worried"],
            "How do parents feel when their children do well?",
            "They were very proud of us.",
        ),
    ],
}

UNIT = {
    "slug": "clubs-and-friends",
    "title": "Clubs and Friends",
    "description": "A science club, a garage band, an apple cake, a lost kitten and the school play.",
    "lessons": [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5],
}
