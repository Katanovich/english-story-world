"use client";

/* Renderers for each exercise type. They are controlled: `value` is the response object
 * that will be sent to the API (shapes match backend app/exercises/definitions.py). */

import { useState } from "react";
import { Illustration, ListenButton, ListeningTrackPlayer } from "@/components/media";
import type { AttemptResult, Exercise, LessonContent, MediaRef, Option } from "@/lib/types";
import { Recorder } from "./Recorder";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Response = Record<string, any>;

export interface RendererProps {
  exercise: Exercise;
  media: Record<string, MediaRef>;
  content?: LessonContent;
  value: Response;
  setValue: (v: Response) => void;
  locked: boolean;
  result: AttemptResult | null;
  canRecord: boolean;
}

const tile =
  "min-h-14 rounded-2xl border-2 px-4 py-3 text-lg font-bold transition-colors " +
  "disabled:cursor-default";

function optionState(selected: boolean, result: AttemptResult | null, isRight: boolean | null) {
  if (result && isRight === true) return "border-leaf bg-ok-bg";
  if (result && selected && isRight === false) return "border-berry bg-err-bg";
  if (selected) return "border-sky bg-sky/10";
  return "border-line bg-surface hover:border-sky";
}

function OptionLabel({ option, media }: { option: Option; media: Record<string, MediaRef> }) {
  return (
    <span className="flex flex-col items-center gap-1">
      {option.text || option.image_id ? (
        <Illustration imageId={option.image_id} emoji={option.emoji} media={media} />
      ) : (
        // Picture-only option: let assistive tech read the emoji's own name.
        <span className="text-5xl">{option.emoji}</span>
      )}
      {option.text && <span>{option.text}</span>}
    </span>
  );
}

function PromptExtras({ exercise, content, media }: Pick<RendererProps, "exercise" | "content" | "media">) {
  const p = exercise.prompt;
  const track = p.listening_id ? content?.listening?.find((t) => t.id === p.listening_id) : undefined;
  return (
    <div className="space-y-4">
      {p.emoji && (
        <div className="text-center">
          <Illustration emoji={p.emoji} size="text-7xl" label="picture" />
        </div>
      )}
      {exercise.image_id && <Illustration imageId={exercise.image_id} media={media} />}
      {(p.listen_text || exercise.audio_id) && (
        <ListenButton text={p.listen_text ?? ""} audioId={exercise.audio_id} />
      )}
      {track && <ListeningTrackPlayer track={track} />}
      {p.context && <p className="rounded-2xl bg-bg p-4">{p.context}</p>}
    </div>
  );
}

export function ChoiceExercise(props: RendererProps) {
  const { exercise, media, value, setValue, locked, result } = props;
  const options: Option[] = exercise.prompt.options;
  const correct = result?.solution?.correct as string | undefined;
  const big = options.every((o) => !o.text);
  return (
    <div className="space-y-5">
      <PromptExtras {...props} />
      <p className="text-xl font-extrabold">{exercise.prompt.question}</p>
      <div role="radiogroup" aria-label={exercise.prompt.question} className={`grid gap-3 ${big ? "grid-cols-3" : "sm:grid-cols-2"}`}>
        {options.map((o) => {
          const selected = value.choice === o.id;
          const isRight = correct ? o.id === correct : result && selected ? result.is_correct : null;
          return (
            <button
              key={o.id}
              type="button"
              role="radio"
              aria-checked={selected}
              disabled={locked}
              onClick={() => setValue({ choice: o.id })}
              className={`${tile} ${optionState(selected, result, isRight)}`}
            >
              <OptionLabel option={o} media={media} />
            </button>
          );
        })}
      </div>
    </div>
  );
}

export function TrueFalseExercise(props: RendererProps) {
  const { exercise, value, setValue, locked, result } = props;
  const correct = result?.solution?.correct as boolean | undefined;
  return (
    <div className="space-y-5">
      <PromptExtras {...props} />
      <p className="text-xl font-extrabold">“{exercise.prompt.statement}”</p>
      <div role="radiogroup" aria-label="True or false" className="grid grid-cols-2 gap-3">
        {[true, false].map((v) => {
          const selected = value.value === v;
          const isRight = correct !== undefined ? v === correct : result && selected ? result.is_correct : null;
          return (
            <button
              key={String(v)}
              type="button"
              role="radio"
              aria-checked={selected}
              disabled={locked}
              onClick={() => setValue({ value: v })}
              className={`${tile} ${optionState(selected, result, isRight)}`}
            >
              <span aria-hidden className="mr-2">{v ? "👍" : "👎"}</span>
              {v ? "True" : "False"}
            </button>
          );
        })}
      </div>
    </div>
  );
}

const PAIR_COLORS = ["bg-sky/20", "bg-sun/40", "bg-leaf/20", "bg-berry/20", "bg-brand/20", "bg-line"];

export function MatchingExercise({ exercise, media, value, setValue, locked, result }: RendererProps) {
  const left: Option[] = exercise.prompt.left;
  const right: Option[] = exercise.prompt.right;
  const pairs: Record<string, string> = value.pairs ?? {};
  const [active, setActive] = useState<string | null>(null);
  const perItem: Record<string, boolean> | undefined = result?.details?.pairs;

  const pairIndex = (leftId: string) => left.findIndex((l) => l.id === leftId);
  const leftFor = (rightId: string) => Object.keys(pairs).find((k) => pairs[k] === rightId);

  function chooseRight(rightId: string) {
    if (!active) return;
    const next = { ...pairs };
    const previousOwner = leftFor(rightId);
    if (previousOwner) delete next[previousOwner];
    next[active] = rightId;
    setValue({ pairs: next });
    setActive(null);
  }

  return (
    <div className="space-y-4">
      <p className="text-muted">Tap a word, then tap its picture.</p>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-3">
          {left.map((l) => {
            const paired = pairs[l.id] !== undefined;
            const mark = perItem ? (perItem[l.id] ? " ✅" : " ❌") : "";
            return (
              <button
                key={l.id}
                type="button"
                disabled={locked}
                aria-pressed={active === l.id}
                onClick={() => setActive(active === l.id ? null : l.id)}
                className={`${tile} w-full ${active === l.id ? "border-sky" : "border-line"} ${paired ? PAIR_COLORS[pairIndex(l.id) % PAIR_COLORS.length] : "bg-surface"}`}
              >
                {l.text}
                {mark}
              </button>
            );
          })}
        </div>
        <div className="space-y-3">
          {right.map((r) => {
            const owner = leftFor(r.id);
            const ownerText = owner ? left.find((l) => l.id === owner)?.text : undefined;
            return (
              <button
                key={r.id}
                type="button"
                disabled={locked || !active}
                onClick={() => chooseRight(r.id)}
                aria-label={`${r.text ?? r.emoji ?? "picture"}${ownerText ? `, matched with ${ownerText}` : ""}`}
                className={`${tile} w-full border-line ${owner ? PAIR_COLORS[pairIndex(owner) % PAIR_COLORS.length] : "bg-surface"} ${active ? "hover:border-sky" : ""}`}
              >
                <OptionLabel option={r} media={media} />
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export function SentenceBuilderExercise({ exercise, value, setValue, locked }: RendererProps) {
  const tiles: string[] = exercise.prompt.tiles;
  const chosen: number[] = value._order ?? [];
  const update = (order: number[]) => setValue({ _order: order, tiles: order.map((i) => tiles[i]) });
  return (
    <div className="space-y-5">
      {exercise.prompt.hint && <p className="text-muted">💡 {exercise.prompt.hint}</p>}
      <div
        aria-label="Your sentence"
        className="flex min-h-20 flex-wrap items-center gap-2 rounded-2xl border-2 border-dashed border-line bg-bg p-3"
      >
        {chosen.length === 0 && <span className="text-muted">Tap the words below.</span>}
        {chosen.map((i, pos) => (
          <button
            key={`${i}-${pos}`}
            type="button"
            disabled={locked}
            onClick={() => update(chosen.filter((_, p) => p !== pos))}
            className={`${tile} border-sky bg-surface`}
            aria-label={`Remove ${tiles[i]}`}
          >
            {tiles[i]}
          </button>
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {tiles.map((t, i) =>
          chosen.includes(i) ? (
            <span key={i} className={`${tile} border-line bg-line/40 text-transparent`} aria-hidden>
              {t}
            </span>
          ) : (
            <button
              key={i}
              type="button"
              disabled={locked}
              onClick={() => update([...chosen, i])}
              className={`${tile} border-line bg-surface hover:border-sky`}
            >
              {t}
            </button>
          ),
        )}
      </div>
    </div>
  );
}

export function FillBlankExercise({ exercise, value, setValue, locked, result }: RendererProps) {
  const parts: string[] = String(exercise.prompt.text).split("___");
  const blanks = parts.length - 1;
  const answers: string[] = value.answers ?? Array(blanks).fill("");
  const bank: string[] = exercise.prompt.word_bank ?? [];
  const marks: Record<string, boolean> | undefined = result?.details?.blanks;

  function setAnswer(i: number, text: string) {
    const next = [...answers];
    next[i] = text;
    setValue({ answers: next });
  }
  function fillNext(word: string) {
    const i = answers.findIndex((a) => !a);
    setAnswer(i === -1 ? blanks - 1 : i, word);
  }

  return (
    <div className="space-y-5">
      {exercise.prompt.hint_ru && <p className="text-muted">Подсказка: {exercise.prompt.hint_ru}</p>}
      <p className="flex flex-wrap items-center gap-2 text-2xl font-bold leading-loose">
        {parts.map((part, i) => (
          <span key={i} className="contents">
            {part && <span>{part}</span>}
            {i < blanks &&
              (bank.length ? (
                <button
                  type="button"
                  disabled={locked || !answers[i]}
                  onClick={() => setAnswer(i, "")}
                  aria-label={answers[i] ? `Blank ${i + 1}: ${answers[i]}. Tap to clear.` : `Blank ${i + 1}: empty`}
                  className={`min-h-12 min-w-24 rounded-xl border-b-4 px-3 ${marks ? (marks[String(i)] ? "border-leaf bg-ok-bg" : "border-berry bg-err-bg") : "border-sky bg-sky/10"}`}
                >
                  {answers[i] || " "}
                </button>
              ) : (
                <input
                  aria-label={`Blank ${i + 1}`}
                  value={answers[i]}
                  disabled={locked}
                  onChange={(e) => setAnswer(i, e.target.value)}
                  autoCapitalize="none"
                  className="min-h-12 w-36 rounded-xl border-2 border-line px-3"
                />
              ))}
          </span>
        ))}
      </p>
      {bank.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {bank.map((w) => (
            <button
              key={w}
              type="button"
              disabled={locked}
              onClick={() => fillNext(w)}
              className={`${tile} border-line bg-surface hover:border-sky`}
            >
              {w}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export function OrderEventsExercise({ exercise, value, setValue, locked }: RendererProps) {
  const items: Option[] = exercise.prompt.items;
  const order: string[] = value.order ?? items.map((i) => i.id);
  const byId = Object.fromEntries(items.map((i) => [i.id, i]));
  function move(index: number, delta: number) {
    const next = [...order];
    const [moved] = next.splice(index, 1);
    next.splice(index + delta, 0, moved);
    setValue({ order: next });
  }
  return (
    <ol className="space-y-3">
      {order.map((id, i) => (
        <li key={id} className="flex items-center gap-3 rounded-2xl border-2 border-line bg-surface p-3">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-sun font-extrabold">
            {i + 1}
          </span>
          <span className="flex-1 text-lg font-semibold">{byId[id]?.text}</span>
          <button
            type="button"
            className="h-11 w-11 rounded-xl border-2 border-line text-xl disabled:opacity-30"
            disabled={locked || i === 0}
            onClick={() => move(i, -1)}
            aria-label={`Move up: ${byId[id]?.text}`}
          >
            ↑
          </button>
          <button
            type="button"
            className="h-11 w-11 rounded-xl border-2 border-line text-xl disabled:opacity-30"
            disabled={locked || i === order.length - 1}
            onClick={() => move(i, 1)}
            aria-label={`Move down: ${byId[id]?.text}`}
          >
            ↓
          </button>
        </li>
      ))}
    </ol>
  );
}

export function SpeakingExercise({ exercise, value, setValue, locked, canRecord }: RendererProps) {
  const p = exercise.prompt;
  return (
    <div className="space-y-5">
      <p className="text-2xl font-bold">{p.text}</p>
      {p.model_answer && (
        <div className="space-y-3 rounded-2xl bg-bg p-4">
          <p>
            <span className="font-extrabold">Example: </span>
            {p.model_answer}
          </p>
          <ListenButton text={p.model_answer} audioId={p.model_audio_id} />
        </div>
      )}
      {canRecord ? (
        <Recorder
          disabled={locked}
          onSaved={(id) => setValue({ ...value, recording_asset_id: id, self_check: true })}
        />
      ) : (
        <p className="text-sm text-muted">Recording is not available in preview.</p>
      )}
      <p className="text-sm text-muted">
        Say it out loud. Nobody grades your voice automatically — this is practice for you.
      </p>
    </div>
  );
}

export const RENDERERS: Record<string, (p: RendererProps) => React.ReactElement> = {
  MULTIPLE_CHOICE: ChoiceExercise,
  IMAGE_SELECTION: ChoiceExercise,
  READING_COMPREHENSION: ChoiceExercise,
  LISTENING_COMPREHENSION: ChoiceExercise,
  TRUE_FALSE: TrueFalseExercise,
  MATCHING: MatchingExercise,
  SENTENCE_BUILDER: SentenceBuilderExercise,
  FILL_BLANK: FillBlankExercise,
  ORDER_EVENTS: OrderEventsExercise,
  SPEAKING: SpeakingExercise,
};

export function initialValue(exercise: Exercise): Response {
  switch (exercise.type) {
    case "ORDER_EVENTS":
      return { order: (exercise.prompt.items as Option[]).map((i) => i.id) };
    case "SPEAKING":
      return { self_check: true };
    default:
      return {};
  }
}

export function isReady(exercise: Exercise, value: Response): boolean {
  switch (exercise.type) {
    case "TRUE_FALSE":
      return typeof value.value === "boolean";
    case "MATCHING":
      return Object.keys(value.pairs ?? {}).length === exercise.prompt.left.length;
    case "SENTENCE_BUILDER":
      return (value.tiles ?? []).length === exercise.prompt.tiles.length;
    case "FILL_BLANK":
      return (value.answers ?? []).length > 0 && value.answers.every((a: string) => a.trim());
    case "ORDER_EVENTS":
    case "SPEAKING":
      return true;
    default:
      return typeof value.choice === "string";
  }
}

/** Strip UI-only keys (prefixed with _) before sending. */
export function toResponse(value: Response): Response {
  return Object.fromEntries(Object.entries(value).filter(([k]) => !k.startsWith("_")));
}

export function describeSolution(exercise: Exercise, solution: Response): string {
  const p = exercise.prompt;
  const optionText = (opts: Option[], id: string) => {
    const o = opts.find((x) => x.id === id);
    return o?.text ?? o?.emoji ?? id;
  };
  switch (exercise.type) {
    case "TRUE_FALSE":
      return solution.correct ? "True" : "False";
    case "SENTENCE_BUILDER":
      return solution.sentence;
    case "FILL_BLANK":
      return solution.blanks.join(", ");
    case "ORDER_EVENTS":
      return (solution.order as string[]).map((id, i) => `${i + 1}. ${optionText(p.items, id)}`).join("  ");
    case "MATCHING":
      return Object.entries(solution.pairs as Record<string, string>)
        .map(([l, r]) => `${optionText(p.left, l)} → ${optionText(p.right, r)}`)
        .join(", ");
    default:
      return optionText(p.options, solution.correct);
  }
}
