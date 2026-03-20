export type Level = "Beginner" | "Intermediate" | "Advanced";

export interface Lesson {
  id: string;
  topic: string;
  level: Level;
  title: string;
  content: string;
  key_terms: Record<string, string>;
}

export interface MapNode {
  id: string;
  title: string;
  topic: string;
  level: Level;
  icon: string;
}

export interface Unit {
  id: string;
  title: string;
  description: string;
  level: Level;
  nodes: MapNode[];
}

export interface QuizQuestion {
  q: string;
  options: string[];
  answer: string;
  explanation: string;
}

export interface Scenario {
  scenario: string;
  situation: string;
  question: string;
  answer: string;
  key_concept: string;
}

export interface HistoryEvent {
  year: string;
  event: string;
  description: string;
  lesson: string;
  era: string;
}

export interface FillInBlank {
  sentence: string;
  answer: string;
  hint: string;
  level: Level;
}

export interface ConceptChain {
  title: string;
  concepts: string[];
  description: string;
  level: Level;
}
