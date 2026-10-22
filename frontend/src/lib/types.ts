// Mirrors backend Pydantic schemas (app/schemas/*.py).

export type Role = "ADMIN" | "STUDENT";
export type AccountStatus = "INVITED" | "ACTIVE" | "SUSPENDED" | "INACTIVE";
export type Cefr = "A1" | "A2" | "B1" | "B2" | "C1" | "C2";
export type ProgressStatus = "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED";
export type ItemRole = "NEW" | "RECENT_REVIEW" | "OLDER_REVIEW";
export type Section = "VOCABULARY" | "READING" | "LISTENING" | "GRAMMAR" | "SPEAKING" | "QUIZ";
export type ExerciseType =
  | "MULTIPLE_CHOICE"
  | "IMAGE_SELECTION"
  | "MATCHING"
  | "SENTENCE_BUILDER"
  | "FILL_BLANK"
  | "READING_COMPREHENSION"
  | "LISTENING_COMPREHENSION"
  | "TRUE_FALSE"
  | "ORDER_EVENTS"
  | "SPEAKING";

export interface User {
  id: string;
  username: string;
  email: string | null;
  display_name: string;
  role: Role;
  status: AccountStatus;
}

export interface MediaRef {
  id: string;
  media_type: "IMAGE" | "AUDIO" | "VIDEO" | "SUBTITLE";
  mime_type: string;
  status: string;
  url: string;
  alt_text: string | null;
  duration_seconds: number | null;
  subtitle_asset_id: string | null;
  transcript: string | null;
}

export interface LearningItem {
  id: string;
  key: string;
  kind: string;
  text: string;
  emoji: string | null;
  translation_ru: string | null;
  explanation: string | null;
  examples: string[];
  image_id: string | null;
  audio_id: string | null;
}

export interface Option {
  id: string;
  text?: string;
  emoji?: string;
  image_id?: string;
}

export interface Exercise {
  id: string;
  key: string;
  type: ExerciseType;
  section: Section;
  recall_mode: "RECOGNITION" | "RECALL";
  position: number;
  instructions: string;
  // Shape depends on `type` (see backend app/exercises/definitions.py).
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  prompt: Record<string, any>;
  points: number;
  is_scored: boolean;
  image_id: string | null;
  audio_id: string | null;
  version: number;
}

export interface Episode {
  id: string;
  title: string;
  synopsis: string;
  position: number;
  video_asset_id: string | null;
  subtitle_asset_id: string | null;
  poster_image_id: string | null;
  has_video: boolean;
}

export interface EpisodeListItem extends Episode {
  lesson_id: string;
  lesson_title: string;
  lesson_position: number;
}

export interface LessonProgress {
  status: ProgressStatus;
  score: number;
  max_score: number;
  best_quiz_percent: number | null;
  lesson_version: number;
  started_at: string | null;
  completed_at: string | null;
  attempted_exercise_ids: string[];
}

export interface TranscriptLine {
  speaker: string;
  text: string;
}

export interface ListeningTrack {
  id: string;
  title: string;
  audio_id?: string;
  subtitle_id?: string;
  transcript: TranscriptLine[];
}

export interface LessonContent {
  story_intro?: string;
  reading?: {
    title: string;
    paragraphs: { sentences: string[]; image_id?: string }[];
    highlight: string[];
  };
  listening?: ListeningTrack[];
  grammar?: { title: string; explanation: string; explanation_ru?: string; examples: string[] }[];
}

export interface LessonDetail {
  id: string;
  course_id: string;
  unit_id: string;
  unit_title: string;
  slug: string;
  title: string;
  description: string;
  objectives: string[];
  cefr_level: Cefr;
  position: number;
  estimated_minutes: number;
  content_version: number;
  is_published: boolean;
  content: LessonContent;
  items: { role: ItemRole; item: LearningItem }[];
  exercises: Exercise[];
  episodes: Episode[];
  media: Record<string, MediaRef>;
  progress: LessonProgress | null;
  previous_lesson_id: string | null;
  next_lesson_id: string | null;
}

export interface LessonSummary {
  id: string;
  slug: string;
  title: string;
  description: string;
  position: number;
  estimated_minutes: number;
  cefr_level: Cefr;
  cover_image_id: string | null;
  progress_status: ProgressStatus;
}

export interface CourseTree {
  id: string;
  slug: string;
  title: string;
  description: string;
  current_level: Cefr | null;
  current_lesson_id: string | null;
  levels: {
    id: string;
    cefr_level: Cefr;
    title: string;
    units: { id: string; title: string; description: string; lessons: LessonSummary[] }[];
  }[];
}

export interface Dashboard {
  display_name: string;
  course: CourseTree | null;
  current_lesson: LessonSummary | null;
  lessons_completed: number;
  lessons_total: number;
  items_practiced: number;
  items_mastered: number;
  reviews_due: number;
  last_activity_at: string | null;
  achievements: { key: string; title: string; earned: boolean }[];
}

export interface AttemptResult {
  attempt_id: string;
  is_correct: boolean | null;
  score: number;
  max_score: number;
  message: string | null;
  explanation: string | null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  details: Record<string, any>;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  solution: Record<string, any> | null;
  counted_for_mastery: boolean;
  lesson_progress: LessonProgress;
}

export interface Mastery {
  item: LearningItem;
  attempts: number;
  correct: number;
  incorrect: number;
  recognition_correct: number;
  recall_correct: number;
  mastery: number;
  mastered: boolean;
  last_practiced_at: string | null;
  next_review_at: string | null;
}

export interface ProgressReport {
  lessons: (LessonProgress & { lesson_id: string; lesson_title: string })[];
  mastery: Mastery[];
}

export interface ReviewEntry {
  item: LearningItem;
  due_at: string;
  exercise: Exercise | null;
  lesson_id: string | null;
}

export interface Page<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}
