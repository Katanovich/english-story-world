"""Mastery estimation and spaced-repetition scheduling.

Scheduling (a simplified SM-2):
- Correct:   repetitions += 1; interval = 1 day (1st), 3 days (2nd), then interval * ease;
             ease += 0.1 (max 3.0).
- Incorrect: repetitions = 0; review again in 10 minutes; ease -= 0.2 (min 1.3).

Mastery (0..1) needs evidence of both kinds of knowledge:
- Recognition (choose/match) contributes at most 0.4, recall (build/type) at most 0.6;
  each saturates after 3 correct answers.
- The sum is multiplied by overall accuracy (correct / attempts).
So one correct picture choice gives ~0.13, and 0.8 ("mastered") is impossible without
productive recall.

Immediate retries (same exercise within RETRY_WINDOW) are stored as attempts but do not
count as new evidence, so retrying after seeing feedback cannot inflate mastery.
"""

import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LearnerMastery, ReviewQueue
from app.models.enums import RecallMode

MASTERED_THRESHOLD = 0.8
RETRY_WINDOW = timedelta(minutes=10)
RELEARN_DELAY = timedelta(minutes=10)
MIN_EASE, MAX_EASE, START_EASE = 1.3, 3.0, 2.3


def estimate_mastery(m: LearnerMastery) -> float:
    if m.attempts == 0:
        return 0.0
    recognition = min(m.recognition_correct, 3) / 3 * 0.4
    recall = min(m.recall_correct, 3) / 3 * 0.6
    accuracy = m.correct / m.attempts
    return round(min(1.0, (recognition + recall) * accuracy), 3)


def next_schedule(entry: ReviewQueue, correct: bool, now: datetime) -> None:
    if correct:
        entry.repetitions += 1
        if entry.repetitions == 1:
            entry.interval_days = 1.0
        elif entry.repetitions == 2:
            entry.interval_days = 3.0
        else:
            entry.interval_days = round(entry.interval_days * entry.ease, 2)
        entry.ease = min(MAX_EASE, entry.ease + 0.1)
        entry.due_at = now + timedelta(days=entry.interval_days)
        entry.last_result = "correct"
    else:
        entry.repetitions = 0
        entry.interval_days = 0.0
        entry.ease = max(MIN_EASE, entry.ease - 0.2)
        entry.due_at = now + RELEARN_DELAY
        entry.last_result = "incorrect"


def record_evidence(
    db: Session,
    user_id: uuid.UUID,
    item_ids: list[uuid.UUID],
    correct: bool,
    mode: RecallMode,
    now: datetime,
) -> None:
    for item_id in item_ids:
        mastery = db.scalar(
            select(LearnerMastery).where(
                LearnerMastery.user_id == user_id, LearnerMastery.learning_item_id == item_id
            )
        )
        if mastery is None:
            mastery = LearnerMastery(
                user_id=user_id,
                learning_item_id=item_id,
                attempts=0,
                correct=0,
                incorrect=0,
                recognition_correct=0,
                recall_correct=0,
            )
            db.add(mastery)
        mastery.attempts += 1
        if correct:
            mastery.correct += 1
            if mode == RecallMode.RECALL:
                mastery.recall_correct += 1
            else:
                mastery.recognition_correct += 1
        else:
            mastery.incorrect += 1
        mastery.last_practiced_at = now
        mastery.mastery = estimate_mastery(mastery)

        entry = db.scalar(
            select(ReviewQueue).where(
                ReviewQueue.user_id == user_id, ReviewQueue.learning_item_id == item_id
            )
        )
        if entry is None:
            entry = ReviewQueue(
                user_id=user_id,
                learning_item_id=item_id,
                due_at=now,
                interval_days=0.0,
                ease=START_EASE,
                repetitions=0,
            )
            db.add(entry)
        next_schedule(entry, correct, now)
