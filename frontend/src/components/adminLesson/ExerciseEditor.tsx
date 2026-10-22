"use client";

import { useState } from "react";
import { Field, Input, Message, Select, SmallButton, TextArea } from "@/components/admin";
import { errorText, send } from "@/lib/api";
import type { ExerciseAdmin, LearningItemAdmin, MediaAdmin } from "@/lib/adminTypes";
import type { ExerciseType } from "@/lib/types";

export const TYPES: { value: ExerciseType; label: string }[] = [
  { value: "MULTIPLE_CHOICE", label: "Выбор ответа" },
  { value: "IMAGE_SELECTION", label: "Выбор картинки" },
  { value: "MATCHING", label: "Сопоставление" },
  { value: "SENTENCE_BUILDER", label: "Собрать предложение" },
  { value: "FILL_BLANK", label: "Заполнить пропуск" },
  { value: "READING_COMPREHENSION", label: "Понимание текста" },
  { value: "LISTENING_COMPREHENSION", label: "Аудирование" },
  { value: "TRUE_FALSE", label: "Верно / неверно" },
  { value: "ORDER_EVENTS", label: "Порядок событий" },
  { value: "SPEAKING", label: "Говорение (без автооценки)" },
];
const SECTIONS = ["VOCABULARY", "READING", "LISTENING", "GRAMMAR", "SPEAKING", "QUIZ"];

const choice = { prompt: { question: "Who is this? 👩", options: [{ id: "a", text: "mother" }, { id: "b", text: "father" }] }, answer: { correct: "a" } };
export const TEMPLATES: Record<ExerciseType, { prompt: object; answer: object }> = {
  MULTIPLE_CHOICE: choice,
  IMAGE_SELECTION: { prompt: { question: "Find: cat", options: [{ id: "a", emoji: "🐱" }, { id: "b", emoji: "🐶" }] }, answer: { correct: "a" } },
  READING_COMPREHENSION: choice,
  LISTENING_COMPREHENSION: { prompt: { question: "What is it?", listen_text: "It is a cat.", options: [{ id: "a", text: "a cat", emoji: "🐱" }, { id: "b", text: "a dog", emoji: "🐶" }] }, answer: { correct: "a" } },
  TRUE_FALSE: { prompt: { statement: "A cat is a pet." }, answer: { correct: true } },
  MATCHING: { prompt: { left: [{ id: "l0", text: "cat" }, { id: "l1", text: "dog" }], right: [{ id: "r0", emoji: "🐱" }, { id: "r1", emoji: "🐶" }] }, answer: { pairs: { l0: "r0", l1: "r1" } } },
  SENTENCE_BUILDER: { prompt: { tiles: ["I", "have", "a", "cat"] }, answer: { accepted: ["I have a cat."] } },
  FILL_BLANK: { prompt: { text: "I ___ a cat.", word_bank: ["have", "am"] }, answer: { blanks: [["have"]] } },
  ORDER_EVENTS: { prompt: { items: [{ id: "e0", text: "First" }, { id: "e1", text: "Then" }] }, answer: { order: ["e0", "e1"] } },
  SPEAKING: { prompt: { text: "Say: I have a cat.", model_answer: "I have a cat." }, answer: {} },
};

const pretty = (o: unknown) => JSON.stringify(o, null, 2);

export function ExerciseEditor({
  lessonId,
  exercise,
  items,
  media,
  nextPosition,
  onSaved,
  onCancel,
}: {
  lessonId: string;
  exercise?: ExerciseAdmin;
  items: LearningItemAdmin[];
  media: MediaAdmin[];
  nextPosition: number;
  onSaved: () => void;
  onCancel: () => void;
}) {
  const startType: ExerciseType = exercise?.type ?? "MULTIPLE_CHOICE";
  const [f, setF] = useState({
    key: exercise?.key ?? "",
    type: startType,
    section: exercise?.section ?? "VOCABULARY",
    recall_mode: exercise?.recall_mode ?? "RECOGNITION",
    position: exercise?.position ?? nextPosition,
    instructions: exercise?.instructions ?? "",
    points: exercise?.points ?? 1,
    prompt: pretty(exercise?.prompt ?? TEMPLATES[startType].prompt),
    answer: pretty(exercise?.answer ?? TEMPLATES[startType].answer),
    hint: exercise?.feedback.hint ?? "",
    explanation: exercise?.feedback.explanation ?? "",
    correct: exercise?.feedback.correct ?? "",
    incorrect: exercise?.feedback.incorrect ?? "",
    image_id: exercise?.image_id ?? "",
    audio_id: exercise?.audio_id ?? "",
    items: new Set(exercise?.learning_item_ids ?? []),
  });
  const [itemFilter, setItemFilter] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const set = (k: keyof typeof f) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
    setF({ ...f, [k]: e.target.type === "number" ? Number(e.target.value) : e.target.value });

  function changeType(t: ExerciseType) {
    const keep = exercise && exercise.type === t;
    setF({ ...f, type: t, prompt: pretty(keep ? exercise.prompt : TEMPLATES[t].prompt), answer: pretty(keep ? exercise.answer : TEMPLATES[t].answer), recall_mode: ["SENTENCE_BUILDER", "FILL_BLANK", "SPEAKING"].includes(t) ? "RECALL" : "RECOGNITION" });
  }

  async function save(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    let prompt, answer;
    try {
      prompt = JSON.parse(f.prompt);
      answer = JSON.parse(f.answer);
    } catch {
      setErr("Prompt или answer — некорректный JSON.");
      return;
    }
    const feedback = Object.fromEntries(
      (["hint", "explanation", "correct", "incorrect"] as const).filter((k) => f[k].trim()).map((k) => [k, f[k].trim()]),
    );
    const body = {
      key: f.key, type: f.type, section: f.section, recall_mode: f.recall_mode, position: f.position,
      instructions: f.instructions, points: f.points, prompt, answer, feedback,
      image_id: f.image_id || null, audio_id: f.audio_id || null, learning_item_ids: [...f.items],
    };
    setBusy(true);
    try {
      if (exercise) await send("PATCH", `/admin/exercises/${exercise.id}`, body);
      else await send("POST", `/admin/lessons/${lessonId}/exercises`, body);
      onSaved();
    } catch (e2) {
      setErr(errorText(e2));
    } finally {
      setBusy(false);
    }
  }

  const visibleItems = items.filter((i) => f.items.has(i.id) || !itemFilter || `${i.text} ${i.key}`.toLowerCase().includes(itemFilter.toLowerCase()));

  return (
    <form onSubmit={save} className="space-y-3 rounded-lg border border-sky bg-bg p-3">
      {exercise && exercise.attempt_count > 0 && (
        <Message kind="ok" text={`На это упражнение уже ответили ${exercise.attempt_count} раз(а). Изменение вопроса/ответа создаст новую версию (v${exercise.version + 1}); старые ответы сохранят свою версию.`} />
      )}
      <div className="grid gap-3 sm:grid-cols-3 lg:grid-cols-6">
        <Field label="Ключ *"><Input value={f.key} onChange={set("key")} required pattern="[a-z0-9_.\-]+" /></Field>
        <Field label="Тип"><Select value={f.type} onChange={(e) => changeType(e.target.value as ExerciseType)}>{TYPES.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}</Select></Field>
        <Field label="Раздел"><Select value={f.section} onChange={set("section")}>{SECTIONS.map((s) => <option key={s}>{s}</option>)}</Select></Field>
        <Field label="Режим" hint="узнавание / воспроизведение"><Select value={f.recall_mode} onChange={set("recall_mode")}><option value="RECOGNITION">Узнавание</option><option value="RECALL">Воспроизведение</option></Select></Field>
        <Field label="Порядок"><Input type="number" min={0} value={f.position} onChange={set("position")} /></Field>
        <Field label="Баллы"><Input type="number" min={0} max={20} value={f.points} onChange={set("points")} /></Field>
      </div>
      <Field label="Инструкция для ученика (англ.) *"><Input value={f.instructions} onChange={set("instructions")} required /></Field>
      <div className="grid gap-3 lg:grid-cols-2">
        <Field label="Prompt (видит ученик), JSON" hint="option: {id, text?, emoji?, image_id?}; listen_text — текст для озвучки; listening_id — диалог из контента">
          <TextArea rows={10} value={f.prompt} onChange={set("prompt")} spellCheck={false} />
        </Field>
        <Field label="Answer (ключ ответа, не отправляется ученику), JSON">
          <TextArea rows={10} value={f.answer} onChange={set("answer")} spellCheck={false} />
        </Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Field label="Подсказка (после ошибки)"><Input value={f.hint} onChange={set("hint")} /></Field>
        <Field label="Объяснение (после верного ответа)"><Input value={f.explanation} onChange={set("explanation")} /></Field>
        <Field label="Текст при верном ответе"><Input value={f.correct} onChange={set("correct")} placeholder="Great job!" /></Field>
        <Field label="Текст при ошибке"><Input value={f.incorrect} onChange={set("incorrect")} placeholder="Not yet. Have another try!" /></Field>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Изображение"><Select value={f.image_id} onChange={set("image_id")}><option value="">—</option>{media.filter((m) => m.media_type === "IMAGE").map((m) => <option key={m.id} value={m.id}>{m.original_filename}</option>)}</Select></Field>
        <Field label="Аудио"><Select value={f.audio_id} onChange={set("audio_id")}><option value="">— (озвучка браузером по listen_text)</option>{media.filter((m) => m.media_type === "AUDIO").map((m) => <option key={m.id} value={m.id}>{m.original_filename}</option>)}</Select></Field>
      </div>
      <fieldset className="space-y-2">
        <legend className="text-sm font-bold">Связанные слова и грамматика (для повторения и освоения): {f.items.size}</legend>
        <Input placeholder="фильтр…" value={itemFilter} onChange={(e) => setItemFilter(e.target.value)} aria-label="Фильтр элементов" />
        <div className="flex max-h-40 flex-wrap gap-1 overflow-y-auto">
          {visibleItems.map((i) => (
            <label key={i.id} className={`cursor-pointer rounded-full border px-2 py-0.5 text-xs ${f.items.has(i.id) ? "border-sky bg-sky/20 font-bold" : "border-line bg-surface"}`}>
              <input type="checkbox" className="sr-only" checked={f.items.has(i.id)} onChange={() => { const s = new Set(f.items); if (s.has(i.id)) s.delete(i.id); else s.add(i.id); setF({ ...f, items: s }); }} />
              {i.emoji} {i.text}
            </label>
          ))}
        </div>
      </fieldset>
      {err && <Message kind="err" text={err} />}
      <div className="flex gap-2">
        <SmallButton type="submit" variant="primary" disabled={busy}>{busy ? "Сохранение…" : "Сохранить упражнение"}</SmallButton>
        <SmallButton onClick={onCancel}>Отмена</SmallButton>
      </div>
    </form>
  );
}
