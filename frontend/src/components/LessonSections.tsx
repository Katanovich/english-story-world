"use client";

import { Illustration, ListenButton, ListeningTrackPlayer } from "@/components/media";
import { Badge } from "@/components/ui";
import { speak } from "@/lib/speech";
import type { LessonDetail, Section } from "@/lib/types";

export const SECTION_INFO: Record<Section, { title: string; icon: string; intro: string }> = {
  VOCABULARY: { title: "Words", icon: "🔤", intro: "Look, listen and learn the new words." },
  READING: { title: "Reading", icon: "📖", intro: "Read the story. The new words are coloured." },
  LISTENING: { title: "Listening", icon: "🎧", intro: "Listen carefully. You can listen again." },
  GRAMMAR: { title: "Grammar", icon: "🧩", intro: "Learn the grammar rule, then practise it." },
  SPEAKING: { title: "Speaking", icon: "🎙️", intro: "Now it is your turn to talk!" },
  QUIZ: { title: "Quiz", icon: "🏆", intro: "Show what you remember — new words and old words!" },
};

function escapeRegExp(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function Highlighted({ text, words }: { text: string; words: string[] }) {
  if (!words.length) return <>{text}</>;
  const sorted = [...words].sort((a, b) => b.length - a.length).map(escapeRegExp);
  const re = new RegExp(`\\b(${sorted.join("|")})\\b`, "gi");
  const parts = text.split(re);
  return (
    <>
      {parts.map((p, i) =>
        i % 2 === 1 ? (
          <mark key={i} className="rounded-md bg-sun/50 px-1 font-extrabold text-ink">{p}</mark>
        ) : (
          <span key={i}>{p}</span>
        ),
      )}
    </>
  );
}

function Vocabulary({ lesson }: { lesson: LessonDetail }) {
  const newItems = lesson.items.filter((i) => i.role === "NEW");
  const review = lesson.items.filter((i) => i.role !== "NEW");
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        {newItems.map(({ item }) => (
          <button
            key={item.id}
            type="button"
            onClick={() => speak(item.text)}
            className="flex min-h-32 flex-col items-center justify-center gap-2 rounded-3xl border-2 border-line bg-surface p-4 hover:border-sky"
            aria-label={`${item.text}. Tap to listen.`}
          >
            <Illustration imageId={item.image_id} emoji={item.emoji ?? "💬"} media={lesson.media} />
            <span className="text-xl font-extrabold">{item.text}</span>
            {item.translation_ru && <span lang="ru" className="text-base font-bold text-muted">{item.translation_ru}</span>}
            <span aria-hidden className="text-sm text-muted">🔊</span>
          </button>
        ))}
      </div>
      {review.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-extrabold">Do you remember?</h3>
          <div className="flex flex-wrap gap-2">
            {review.map(({ item, role }) => (
              <span key={item.id} className="rounded-full border-2 border-line bg-surface px-3 py-1 font-bold">
                {item.emoji && <span aria-hidden>{item.emoji} </span>}
                {item.text}
                {item.translation_ru && <span lang="ru" className="font-normal text-muted"> — {item.translation_ru}</span>}
                {role === "RECENT_REVIEW" && <span className="sr-only"> (last lesson)</span>}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function Reading({ lesson }: { lesson: LessonDetail }) {
  const reading = lesson.content.reading;
  if (!reading) return <p className="text-muted">No reading in this lesson.</p>;
  return (
    <article className="space-y-4">
      <h3 className="text-2xl font-black">{reading.title}</h3>
      {reading.paragraphs.map((p, i) => (
        <div key={i} className="flex items-start gap-3 rounded-2xl bg-bg p-4">
          <div className="flex-1 space-y-1 text-xl leading-relaxed">
            {p.image_id && <Illustration imageId={p.image_id} media={lesson.media} />}
            {p.sentences.map((s, j) => (
              <p key={j}><Highlighted text={s} words={reading.highlight} /></p>
            ))}
          </div>
          <button
            type="button"
            onClick={() => speak(p.sentences.join(" "))}
            className="rounded-xl p-2 text-2xl hover:bg-line"
            aria-label="Read this part aloud"
          >
            🔈
          </button>
        </div>
      ))}
      <p className="text-xs text-muted">🔈 uses the computer voice until recordings are added.</p>
    </article>
  );
}

function Grammar({ lesson }: { lesson: LessonDetail }) {
  return (
    <div className="space-y-4">
      {(lesson.content.grammar ?? []).map((g) => (
        <div key={g.title} className="space-y-2 rounded-2xl bg-bg p-4">
          <h3 className="text-xl font-black">{g.title}</h3>
          <p>{g.explanation}</p>
          {g.explanation_ru && <p lang="ru" className="text-muted">{g.explanation_ru}</p>}
          <ul className="space-y-1">
            {g.examples.map((e) => (
              <li key={e} className="flex items-center gap-2 font-bold">
                <span aria-hidden>👉</span>{e}
                <button type="button" className="rounded-lg px-2 hover:bg-line" onClick={() => speak(e)} aria-label={`Listen: ${e}`}>🔈</button>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export function SectionIntro({ lesson, section }: { lesson: LessonDetail; section: Section }) {
  const info = SECTION_INFO[section];
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <span aria-hidden className="text-5xl">{info.icon}</span>
        <div>
          <Badge tone="brand">{info.title}</Badge>
          <p className="mt-1 text-lg font-bold">{info.intro}</p>
        </div>
      </div>
      {section === "VOCABULARY" && <Vocabulary lesson={lesson} />}
      {section === "READING" && <Reading lesson={lesson} />}
      {section === "LISTENING" &&
        (lesson.content.listening ?? []).map((t) => <ListeningTrackPlayer key={t.id} track={t} />)}
      {section === "GRAMMAR" && <Grammar lesson={lesson} />}
      {section === "SPEAKING" && (
        <ListenButton text="Now it is your turn. Listen, then say it out loud!" />
      )}
    </div>
  );
}
