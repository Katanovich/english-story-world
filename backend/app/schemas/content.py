"""Structured lesson content stored in `lessons.content` (JSONB)."""

import uuid

from pydantic import BaseModel, ConfigDict, Field


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReadingParagraph(_Strict):
    sentences: list[str] = Field(min_length=1, max_length=20)
    image_id: uuid.UUID | None = None


class ReadingPassage(_Strict):
    title: str = Field(max_length=200)
    paragraphs: list[ReadingParagraph] = Field(min_length=1, max_length=20)
    # Words/phrases highlighted in the text (usually the lesson's target vocabulary).
    highlight: list[str] = Field(default_factory=list, max_length=40)


class TranscriptLine(_Strict):
    speaker: str = Field(max_length=40)
    text: str = Field(max_length=500)


class ListeningTrack(_Strict):
    id: str = Field(min_length=1, max_length=40)
    title: str = Field(max_length=200)
    # Audio is optional: without it the UI shows a "no audio yet" state + transcript.
    audio_id: uuid.UUID | None = None
    subtitle_id: uuid.UUID | None = None
    transcript: list[TranscriptLine] = Field(min_length=1, max_length=40)


class GrammarNote(_Strict):
    title: str = Field(max_length=200)
    explanation: str = Field(max_length=1000)
    explanation_ru: str | None = Field(default=None, max_length=1000)
    examples: list[str] = Field(default_factory=list, max_length=10)


class LessonContent(_Strict):
    story_intro: str | None = Field(default=None, max_length=1000)
    reading: ReadingPassage | None = None
    listening: list[ListeningTrack] = Field(default_factory=list, max_length=10)
    grammar: list[GrammarNote] = Field(default_factory=list, max_length=10)

    def media_ids(self) -> set[uuid.UUID]:
        ids: set[uuid.UUID] = set()
        if self.reading:
            ids |= {p.image_id for p in self.reading.paragraphs if p.image_id}
        for track in self.listening:
            ids |= {i for i in (track.audio_id, track.subtitle_id) if i}
        return ids
