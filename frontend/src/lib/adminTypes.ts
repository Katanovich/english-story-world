import type { Cefr, ExerciseType, ItemRole, Section } from "./types";

export type PubStatus = "DRAFT" | "PUBLISHED";

export interface AdminUser {
  id: string;
  username: string;
  email: string | null;
  display_name: string;
  role: "ADMIN" | "STUDENT";
  status: "INVITED" | "ACTIVE" | "SUSPENDED" | "INACTIVE";
  created_at: string;
  updated_at: string;
  last_login_at: string | null;
  last_activity_at: string | null;
}

export interface CourseNode {
  id: string;
  slug: string;
  title: string;
  description: string;
  status: PubStatus;
  levels: {
    id: string;
    cefr_level: Cefr;
    title: string;
    description: string;
    position: number;
    units: {
      id: string;
      slug: string;
      title: string;
      description: string;
      position: number;
      lessons: { id: string; slug: string; title: string; status: PubStatus; position: number; content_version: number; exercise_count: number }[];
    }[];
  }[];
}

export interface ExerciseAdmin {
  id: string;
  lesson_id: string;
  key: string;
  type: ExerciseType;
  section: Section;
  recall_mode: "RECOGNITION" | "RECALL";
  position: number;
  instructions: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  prompt: Record<string, any>;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  answer: Record<string, any>;
  feedback: Record<string, string>;
  points: number;
  is_scored: boolean;
  image_id: string | null;
  audio_id: string | null;
  version: number;
  learning_item_ids: string[];
  attempt_count: number;
}

export interface EpisodeAdmin {
  id: string;
  title: string;
  synopsis: string;
  position: number;
  status: PubStatus;
  video_asset_id: string | null;
  subtitle_asset_id: string | null;
  poster_image_id: string | null;
}

export interface LessonAdmin {
  id: string;
  unit_id: string;
  course_id: string;
  slug: string;
  title: string;
  description: string;
  objectives: string[];
  cefr_level: Cefr;
  position: number;
  estimated_minutes: number;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  content: Record<string, any>;
  status: PubStatus;
  content_version: number;
  cover_image_id: string | null;
  updated_at: string;
  items: { learning_item_id: string; role: ItemRole }[];
  exercises: ExerciseAdmin[];
  episodes: EpisodeAdmin[];
}

export interface LearningItemAdmin {
  id: string;
  key: string;
  kind: string;
  text: string;
  emoji: string | null;
  translation_ru: string | null;
  explanation: string | null;
  cefr_level: Cefr;
  examples: string[];
  introduced_in_lesson_id: string | null;
  image_id: string | null;
  audio_id: string | null;
}

export interface MediaAdmin {
  id: string;
  media_type: "IMAGE" | "AUDIO" | "VIDEO" | "SUBTITLE";
  mime_type: string;
  status: string;
  url: string;
  alt_text: string | null;
  original_filename: string;
  size_bytes: number;
  created_at: string;
}

export interface ValidationReport {
  errors: string[];
  warnings: string[];
}

export const STATUS_RU: Record<AdminUser["status"], string> = {
  INVITED: "Приглашён",
  ACTIVE: "Активен",
  SUSPENDED: "Приостановлен",
  INACTIVE: "Отключён",
};

export const fmtDate = (d: string | null) => (d ? new Date(d).toLocaleString("ru-RU") : "—");
