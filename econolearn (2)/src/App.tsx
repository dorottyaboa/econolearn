import React, { useState, useEffect } from "react";
import { 
  TrendingUp, 
  BookOpen, 
  HelpCircle, 
  Target, 
  Edit3, 
  Link as LinkIcon, 
  History, 
  BarChart3, 
  ChevronRight, 
  Moon, 
  Sun, 
  Award, 
  Zap, 
  Flame,
  CheckCircle2,
  XCircle,
  Search
} from "lucide-react";
import { motion, AnimatePresence } from "motion/react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { 
  LEVELS, 
  TOPICS, 
  LESSONS, 
  QUIZ_QUESTIONS, 
  SCENARIO_EXERCISES, 
  HISTORY_EVENTS, 
  FILL_IN_BLANKS, 
  CONCEPT_CONNECTIONS 
} from "./constants";
import { Level, Lesson, QuizQuestion, Scenario, HistoryEvent, FillInBlank, ConceptChain } from "./types";

type Page = "Home" | "Daily Lesson" | "Quiz" | "Scenarios" | "Fill in the Blanks" | "Concept Chains" | "Economic History" | "My Progress";

export default function App() {
  const [level, setLevel] = useState<Level>(() => {
    try {
      return (localStorage.getItem("econ_level") as Level) || "Beginner";
    } catch (e) {
      return "Beginner";
    }
  });
  const [topic, setTopic] = useState<string>(() => {
    try {
      return localStorage.getItem("econ_topic") || "Supply & Demand";
    } catch (e) {
      return "Supply & Demand";
    }
  });
  const [page, setPage] = useState<Page>("Home");
  const [xp, setXp] = useState(() => {
    try {
      return Number(localStorage.getItem("econ_xp")) || 0;
    } catch (e) {
      return 0;
    }
  });
  const [streak, setStreak] = useState(() => {
    try {
      return Number(localStorage.getItem("econ_streak")) || 0;
    } catch (e) {
      return 0;
    }
  });
  const [darkMode, setDarkMode] = useState(() => {
    try {
      return localStorage.getItem("econ_darkMode") === "true";
    } catch (e) {
      return false;
    }
  });
  const [totalAnswered, setTotalAnswered] = useState(() => {
    try {
      return Number(localStorage.getItem("econ_totalAnswered")) || 0;
    } catch (e) {
      return 0;
    }
  });
  const [correctAnswered, setCorrectAnswered] = useState(() => {
    try {
      return Number(localStorage.getItem("econ_correctAnswered")) || 0;
    } catch (e) {
      return 0;
    }
  });
  const [dailyDone, setDailyDone] = useState<string[]>(() => {
    try {
      return JSON.parse(localStorage.getItem("econ_dailyDone") || "[]");
    } catch (e) {
      return [];
    }
  });
  const [quizAnswers, setQuizAnswers] = useState<Record<string, { chosen: string; correct: boolean }>>(() => {
    try {
      return JSON.parse(localStorage.getItem("econ_quizAnswers") || "{}");
    } catch (e) {
      return {};
    }
  });
  const [scenarioRevealed, setScenarioRevealed] = useState<Record<string, boolean>>(() => {
    try {
      return JSON.parse(localStorage.getItem("econ_scenarioRevealed") || "{}");
    } catch (e) {
      return {};
    }
  });
  const [fibAnswers, setFibAnswers] = useState<Record<string, string>>({});
  const [fibSubmitted, setFibSubmitted] = useState<Record<string, string>>(() => {
    try {
      return JSON.parse(localStorage.getItem("econ_fibSubmitted") || "{}");
    } catch (e) {
      return {};
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem("econ_level", level);
      localStorage.setItem("econ_topic", topic);
      localStorage.setItem("econ_xp", xp.toString());
      localStorage.setItem("econ_streak", streak.toString());
      localStorage.setItem("econ_darkMode", darkMode.toString());
      localStorage.setItem("econ_totalAnswered", totalAnswered.toString());
      localStorage.setItem("econ_correctAnswered", correctAnswered.toString());
      localStorage.setItem("econ_dailyDone", JSON.stringify(dailyDone));
      localStorage.setItem("econ_quizAnswers", JSON.stringify(quizAnswers));
      localStorage.setItem("econ_scenarioRevealed", JSON.stringify(scenarioRevealed));
      localStorage.setItem("econ_fibSubmitted", JSON.stringify(fibSubmitted));
    } catch (e) {
      console.warn("localStorage not available", e);
    }
  }, [level, topic, xp, streak, darkMode, totalAnswered, correctAnswered, dailyDone, quizAnswers, scenarioRevealed, fibSubmitted]);

  useEffect(() => {
    // Mock streak logic - in a real app this would check the last login date
    if (streak === 0) setStreak(3);
  }, []);

  const awardXp = (amount: number) => {
    setXp(prev => prev + amount);
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);

  const renderSidebar = () => (
    <div className={`w-64 flex-shrink-0 border-r transition-colors duration-300 ${darkMode ? "bg-[#16142a] border-[#514d86]" : "bg-[#6aa08f] border-[#b8c4a4]"} flex flex-col h-screen sticky top-0`}>
      <div className="p-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold text-[#FDF6E3] flex items-center gap-2">
          <TrendingUp size={24} /> EconoLearn
        </h2>
        <button 
          onClick={toggleDarkMode}
          className={`p-2 rounded-full transition-all ${darkMode ? "bg-[#514d86] text-yellow-400" : "bg-[#4a7a6e] text-white"} hover:scale-110`}
        >
          {darkMode ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </div>

      <div className="px-6 mb-6">
        <div className="flex justify-between items-end mb-1">
          <span className="text-xs font-bold text-[#FDF6E3]">Level {Math.floor(xp / 100)} Explorer ✨</span>
          <span className="text-xs font-bold text-[#FDF6E3]">{xp} XP</span>
        </div>
        <div className={`h-3 w-full rounded-full overflow-hidden ${darkMode ? "bg-[#16142a] border border-[#816cb1]" : "bg-[#4a7a6e] border border-[#b8c4a4]"}`}>
          <motion.div 
            initial={{ width: 0 }}
            animate={{ width: `${xp % 100}%` }}
            className={`h-full ${darkMode ? "bg-[#d289ae]" : "bg-[#e8ae7d]"}`}
          />
        </div>
        <div className="mt-2 flex items-center gap-1">
          {streak > 0 && Array.from({ length: Math.min(streak, 5) }).map((_, i) => (
            <Flame key={i} size={16} className="text-orange-400 fill-orange-400" />
          ))}
          <span className="text-xs font-bold text-[#FDF6E3] ml-1">Streak: {streak} days</span>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-4 space-y-1">
        {[
          { icon: <TrendingUp size={18} />, label: "Home", id: "Home" },
          { icon: <BookOpen size={18} />, label: "Daily Lesson", id: "Daily Lesson" },
          { icon: <HelpCircle size={18} />, label: "Quiz", id: "Quiz" },
          { icon: <Target size={18} />, label: "Scenarios", id: "Scenarios" },
          { icon: <Edit3 size={18} />, label: "Fill in the Blanks", id: "Fill in the Blanks" },
          { icon: <LinkIcon size={18} />, label: "Concept Chains", id: "Concept Chains" },
          { icon: <History size={18} />, label: "Economic History", id: "Economic History" },
          { icon: <BarChart3 size={18} />, label: "My Progress", id: "My Progress" },
        ].map((item) => (
          <button
            key={item.id}
            onClick={() => setPage(item.id as Page)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-bold transition-all ${
              page === item.id 
                ? (darkMode ? "bg-[#2a2840] text-[#d289ae] border border-[#816cb1]" : "bg-[#4a7a6e] text-white shadow-inner")
                : "text-[#FDF6E3] hover:bg-white/10"
            }`}
          >
            {item.icon} {item.label}
          </button>
        ))}
      </nav>

      <div className="p-6 border-t border-white/10">
        <div className="mb-4">
          <label className="text-xs font-bold text-[#FDF6E3] uppercase tracking-wider block mb-2">Difficulty</label>
          <div className="flex gap-1">
            {LEVELS.map(lvl => (
              <button
                key={lvl}
                onClick={() => setLevel(lvl)}
                className={`flex-1 py-1 text-[10px] rounded-lg font-black uppercase transition-all ${
                  level === lvl
                    ? (lvl === "Beginner" ? "bg-green-500 text-white" : lvl === "Intermediate" ? "bg-orange-500 text-white" : "bg-red-500 text-white")
                    : "bg-white/10 text-white/50 hover:bg-white/20"
                }`}
              >
                {lvl.substring(0, 3)}
              </button>
            ))}
          </div>
        </div>
        <div>
          <label className="text-xs font-bold text-[#FDF6E3] uppercase tracking-wider block mb-2">Topic</label>
          <select 
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className={`w-full p-2 rounded-xl text-sm font-bold border-none focus:ring-2 focus:ring-white/20 ${darkMode ? "bg-[#2a2840] text-white" : "bg-[#4a7a6e] text-white"}`}
          >
            {Object.keys(TOPICS).map(t => (
              <option key={t} value={t}>{TOPICS[t]} {t}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );

  const renderHome = () => (
    <div className="space-y-8">
      <div className="text-center space-y-2">
        <h1 className={`text-6xl font-black tracking-tight ${darkMode ? "text-[#e2d6fa] drop-shadow-[3px_3px_0_#816cb1]" : "text-[#7f4a4f] drop-shadow-[3px_3px_0_#b8c4a4]"}`}>
          EconoLearn
        </h1>
        <p className={`text-xl font-bold ${darkMode ? "text-[#c5c5ff]" : "text-[#6aa08f]"}`}>
          Master economics — from supply & demand to financial crises.
        </p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {[
          { label: "Your XP", value: `${xp} XP`, icon: <Award className="text-yellow-500" /> },
          { label: "Accuracy", value: totalAnswered > 0 ? `${Math.round((correctAnswered / totalAnswered) * 100)}%` : "—", icon: <CheckCircle2 className="text-green-500" /> },
          { label: "Streak", value: `${streak} days`, icon: <Flame className="text-orange-500" /> },
        ].map((stat, i) => (
          <div key={i} className={`p-6 rounded-3xl border-4 flex flex-col items-center gap-2 transition-all hover:scale-105 ${darkMode ? "bg-[#514d86] border-[#816cb1] shadow-[5px_5px_0_#16142a]" : "bg-[#dbe8cd] border-[#b8c4a4] shadow-[5px_5px_0_#8b82a8]"}`}>
            <div className="p-3 rounded-full bg-white/10">{stat.icon}</div>
            <span className="text-xs font-black uppercase tracking-widest opacity-60">{stat.label}</span>
            <span className="text-3xl font-black">{stat.value}</span>
          </div>
        ))}
      </div>

      <div className={`p-8 rounded-[2rem] border-4 ${darkMode ? "bg-[#2a2840] border-[#816cb1]" : "bg-white border-[#b8c4a4]"} shadow-xl`}>
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-black flex items-center gap-2">
            <Zap className="text-yellow-500" /> Today's Topic: {TOPICS[topic]} {topic}
          </h3>
          <span className={`px-4 py-1 rounded-full text-xs font-black uppercase ${level === "Beginner" ? "bg-green-100 text-green-700" : level === "Intermediate" ? "bg-orange-100 text-orange-700" : "bg-red-100 text-red-700"}`}>
            {level}
          </span>
        </div>
        
        {LESSONS[topic]?.[level] ? (
          <div className="space-y-4">
            <button 
              onClick={() => setPage("Daily Lesson")}
              className={`w-full py-4 rounded-2xl font-black text-lg transition-all flex items-center justify-center gap-2 ${
                darkMode ? "bg-[#d289ae] text-[#16142a] shadow-[0_4px_0_#8a4a6e] hover:translate-y-1 hover:shadow-[0_2px_0_#8a4a6e]" : "bg-[#e8ae7d] text-[#2d2020] shadow-[0_4px_0_#a56066] hover:translate-y-1 hover:shadow-[0_2px_0_#a56066]"
              }`}
            >
              Start Today's Lesson <ChevronRight size={20} />
            </button>
          </div>
        ) : (
          <p className="text-center py-10 opacity-50 italic">No lesson available for this topic and level yet.</p>
        )}
      </div>

      <div className="grid grid-cols-3 gap-4">
        {[
          { icon: <HelpCircle />, label: "Take a Quiz", page: "Quiz" },
          { icon: <Target />, label: "Scenario Exercise", page: "Scenarios" },
          { icon: <History />, label: "Economic History", page: "Economic History" },
        ].map((action, i) => (
          <button
            key={i}
            onClick={() => setPage(action.page as Page)}
            className={`p-4 rounded-2xl border-2 font-bold flex items-center gap-3 transition-all hover:scale-105 ${
              darkMode ? "bg-[#514d86] border-[#816cb1] text-white" : "bg-[#dbe8cd] border-[#b8c4a4] text-[#2d2020]"
            }`}
          >
            {action.icon} {action.label}
          </button>
        ))}
      </div>
    </div>
  );

  const renderLesson = () => {
    const lesson = LESSONS[topic]?.[level];
    if (!lesson) return <div className="text-center py-20 opacity-50 italic">No lesson available for this topic and level.</div>;

    return (
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <div className="flex justify-center gap-2">
            <span className={`px-4 py-1 rounded-full text-xs font-black uppercase ${level === "Beginner" ? "bg-green-100 text-green-700" : level === "Intermediate" ? "bg-orange-100 text-orange-700" : "bg-red-100 text-red-700"}`}>
              {level}
            </span>
            <span className="px-4 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-black uppercase">{topic}</span>
          </div>
          <h2 className="text-4xl font-black">{lesson.title}</h2>
        </div>

        <div className={`p-8 rounded-[2rem] border-4 prose prose-lg max-w-none ${darkMode ? "bg-[#2a2840] border-[#816cb1] text-white" : "bg-white border-[#b8c4a4] text-[#2d2020]"} markdown-content`}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {lesson.content}
          </ReactMarkdown>
        </div>

        <div className="space-y-4">
          <h3 className="text-2xl font-black flex items-center gap-2">
            <Zap className="text-yellow-500" /> Key Terms
          </h3>
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(lesson.key_terms).map(([term, def], i) => (
              <div key={i} className={`p-4 rounded-2xl border-2 ${darkMode ? "bg-[#514d86] border-[#816cb1]" : "bg-[#f9f6e3] border-[#b8c4a4]"}`}>
                <h4 className="font-black mb-1">{term}</h4>
                <p className="text-sm opacity-70">{def}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-4 pt-8">
          <button onClick={() => setPage("Quiz")} className="flex-1 py-4 bg-blue-500 text-white rounded-2xl font-black shadow-[0_4px_0_#2563eb] hover:translate-y-1 hover:shadow-[0_2px_0_#2563eb] transition-all">Take Quiz</button>
          <button onClick={() => setPage("Scenarios")} className="flex-1 py-4 bg-purple-500 text-white rounded-2xl font-black shadow-[0_4px_0_#7c3aed] hover:translate-y-1 hover:shadow-[0_2px_0_#7c3aed] transition-all">Try Scenario</button>
        </div>
      </div>
    );
  };

  const renderQuiz = () => {
    const questions = QUIZ_QUESTIONS[level] || [];
    if (questions.length === 0) return <div className="text-center py-20 opacity-50 italic">No quiz questions available for this level.</div>;

    return (
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="text-center">
          <h2 className="text-4xl font-black mb-2">Quiz Time!</h2>
          <p className="opacity-60 font-bold">Level: {level}</p>
        </div>

        {questions.map((q, i) => {
          const answerKey = `${level}_${i}`;
          const result = quizAnswers[answerKey];

          return (
            <div key={i} className={`p-8 rounded-[2rem] border-4 ${darkMode ? "bg-[#2a2840] border-[#816cb1]" : "bg-white border-[#b8c4a4]"} shadow-xl space-y-6`}>
              <h3 className="text-xl font-black">Q{i + 1}: {q.q}</h3>
              
              <div className="space-y-3">
                {q.options.map((opt, j) => {
                  const optLetter = opt[0];
                  const isSelected = result?.chosen === optLetter;
                  const isCorrect = q.answer === optLetter;
                  
                  let btnClass = darkMode ? "bg-[#514d86] border-[#816cb1] hover:bg-[#5e5a9a]" : "bg-[#f9f6e3] border-[#b8c4a4] hover:bg-[#f0ecd0]";
                  if (result) {
                    if (isCorrect) btnClass = "bg-green-500 text-white border-green-600";
                    else if (isSelected) btnClass = "bg-red-500 text-white border-red-600";
                    else btnClass = "opacity-40 bg-gray-100 border-gray-200";
                  }

                  return (
                    <button
                      key={j}
                      disabled={!!result}
                      onClick={() => {
                        const correct = optLetter === q.answer;
                        setQuizAnswers(prev => ({ ...prev, [answerKey]: { chosen: optLetter, correct } }));
                        setTotalAnswered(prev => prev + 1);
                        if (correct) {
                          setCorrectAnswered(prev => prev + 1);
                          awardXp(15);
                        } else {
                          awardXp(2);
                        }
                      }}
                      className={`w-full p-4 rounded-xl border-2 text-left font-bold transition-all ${btnClass}`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>

              <AnimatePresence>
                {result && (
                  <motion.div 
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`p-4 rounded-2xl border-2 ${result.correct ? "bg-green-50 border-green-200 text-green-800" : "bg-red-50 border-red-200 text-red-800"}`}
                  >
                    <p className="font-black mb-1">{result.correct ? "✅ Correct! +15 XP" : `❌ Answer: ${q.answer}`}</p>
                    <p className="text-sm opacity-80">{q.explanation}</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          );
        })}

        {Object.keys(quizAnswers).length >= questions.length && (
          <button 
            onClick={() => setQuizAnswers({})}
            className="w-full py-4 bg-gray-800 text-white rounded-2xl font-black transition-all hover:bg-black"
          >
            Reset Quiz
          </button>
        )}
      </div>
    );
  };

  const renderScenarios = () => {
    const scenarios = SCENARIO_EXERCISES[level] || [];
    if (scenarios.length === 0) return <div className="text-center py-20 opacity-50 italic">No scenarios available for this level.</div>;

    return (
      <div className="max-w-3xl mx-auto space-y-12">
        <div className="text-center">
          <h2 className="text-4xl font-black mb-2">Real-World Scenarios</h2>
          <p className="opacity-60 font-bold">Apply your knowledge to solve economic puzzles.</p>
        </div>

        {scenarios.map((s, i) => {
          const revealed = scenarioRevealed[`${level}_${i}`];
          return (
            <div key={i} className="space-y-6">
              <div className={`p-8 rounded-[2rem] border-4 ${darkMode ? "bg-[#2a2840] border-[#816cb1]" : "bg-white border-[#b8c4a4]"} shadow-xl space-y-6`}>
                <h3 className="text-2xl font-black text-blue-500">{s.scenario}</h3>
                <div className={`p-6 rounded-2xl border-2 ${darkMode ? "bg-[#514d86] border-[#816cb1]" : "bg-[#f9f6e3] border-[#b8c4a4]"}`}>
                  <p className="font-bold leading-relaxed">{s.situation}</p>
                </div>
                <p className="text-lg font-black italic">❓ {s.question}</p>
                
                {!revealed ? (
                  <button 
                    onClick={() => {
                      setScenarioRevealed(prev => ({ ...prev, [`${level}_${i}`]: true }));
                      awardXp(5);
                    }}
                    className="w-full py-4 bg-blue-500 text-white rounded-2xl font-black shadow-[0_4px_0_#2563eb] hover:translate-y-1 hover:shadow-[0_2px_0_#2563eb] transition-all"
                  >
                    Reveal Answer
                  </button>
                ) : (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="space-y-4"
                  >
                    <div className="p-6 rounded-2xl bg-green-50 border-2 border-green-200 text-green-900">
                      <h4 className="font-black mb-2">Answer & Analysis:</h4>
                      <div className="prose prose-sm max-w-none">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {s.answer}
                        </ReactMarkdown>
                      </div>
                    </div>
                    <div className="p-6 rounded-2xl bg-yellow-50 border-2 border-yellow-200 text-yellow-900">
                      <h4 className="font-black mb-2 flex items-center gap-2"><Zap size={18} /> Key Concept:</h4>
                      <p className="opacity-90">{s.key_concept}</p>
                    </div>
                  </motion.div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  const renderHistory = () => {
    return (
      <div className="max-w-4xl mx-auto space-y-12">
        <div className="text-center">
          <h2 className="text-4xl font-black mb-2">Economic History</h2>
          <p className="opacity-60 font-bold">The events that shaped the global economy.</p>
        </div>

        <div className="space-y-8 relative before:absolute before:left-8 before:top-0 before:bottom-0 before:w-1 before:bg-gray-200 before:hidden md:before:block">
          {HISTORY_EVENTS.map((event, i) => (
            <div key={i} className="md:pl-20 relative">
              <div className="hidden md:flex absolute left-6 top-10 w-5 h-5 rounded-full bg-blue-500 border-4 border-white z-10" />
              <div className={`p-8 rounded-[2rem] border-4 ${darkMode ? "bg-[#2a2840] border-[#816cb1]" : "bg-white border-[#b8c4a4]"} shadow-xl space-y-4`}>
                <div className="flex items-center justify-between">
                  <span className="text-3xl font-black text-blue-500">{event.year}</span>
                  <span className={`px-3 py-1 rounded-lg text-[10px] font-black uppercase ${darkMode ? "bg-[#514d86] text-white" : "bg-gray-100 text-gray-600"}`}>
                    {event.era}
                  </span>
                </div>
                <h3 className="text-2xl font-black">{event.event}</h3>
                <p className="opacity-80 leading-relaxed">{event.description}</p>
                <div className={`p-4 rounded-xl border-2 ${darkMode ? "bg-[#514d86] border-[#816cb1]" : "bg-yellow-50 border-yellow-100"}`}>
                  <p className="text-sm font-bold italic">💡 Lesson: {event.lesson}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderProgress = () => (
    <div className="max-w-4xl mx-auto space-y-12">
      <div className="text-center">
        <h2 className="text-4xl font-black mb-2">My Progress</h2>
        <p className="opacity-60 font-bold">Track your journey to economic mastery.</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {[
          { label: "Total XP", value: xp, color: "text-yellow-500" },
          { label: "Accuracy", value: totalAnswered > 0 ? `${Math.round((correctAnswered / totalAnswered) * 100)}%` : "N/A", color: "text-green-500" },
          { label: "Answered", value: totalAnswered, color: "text-blue-500" },
          { label: "Streak", value: `${streak} days`, color: "text-orange-500" },
        ].map((stat, i) => (
          <div key={i} className={`p-6 rounded-3xl border-4 text-center ${darkMode ? "bg-[#2a2840] border-[#816cb1]" : "bg-white border-[#b8c4a4]"}`}>
            <p className="text-xs font-black uppercase tracking-widest opacity-50 mb-1">{stat.label}</p>
            <p className={`text-3xl font-black ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="space-y-6">
        <h3 className="text-2xl font-black">Badges Earned</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { id: "starter", label: "First 100 XP", icon: "🥉", unlocked: xp >= 100 },
            { id: "club", label: "500 XP Club", icon: "🥇", unlocked: xp >= 500 },
            { id: "quiz", label: "Quiz Starter", icon: "📝", unlocked: correctAnswered >= 5 },
            { id: "master", label: "Quiz Master", icon: "🎓", unlocked: correctAnswered >= 20 },
          ].map((badge) => (
            <div key={badge.id} className={`p-6 rounded-3xl border-4 text-center transition-all ${
              badge.unlocked 
                ? (darkMode ? "bg-[#514d86] border-[#d289ae]" : "bg-white border-[#e8ae7d] shadow-lg scale-105") 
                : "bg-gray-100 border-gray-200 opacity-40 grayscale"
            }`}>
              <div className="text-4xl mb-2">{badge.icon}</div>
              <p className="font-black text-sm">{badge.label}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="pt-8 border-t border-gray-200">
        <button 
          onClick={() => {
            if (confirm("Are you sure you want to reset all progress?")) {
              localStorage.clear();
              setXp(0);
              setTotalAnswered(0);
              setCorrectAnswered(0);
              setQuizAnswers({});
              setScenarioRevealed({});
              setFibSubmitted({});
              setDailyDone([]);
              setStreak(0);
            }
          }}
          className="px-6 py-3 bg-red-100 text-red-600 rounded-xl font-bold hover:bg-red-200 transition-all"
        >
          Reset All Progress
        </button>
      </div>
    </div>
  );

  const renderFillInBlanks = () => {
    const levelQs = FILL_IN_BLANKS.filter(q => q.level === level);
    if (levelQs.length === 0) return <div className="text-center py-20 opacity-50 italic">No fill-in-the-blank exercises for {level} yet.</div>;

    return (
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="text-center">
          <h2 className="text-4xl font-black mb-2">Fill in the Blanks</h2>
          <p className="opacity-60 font-bold">Test your terminology knowledge.</p>
        </div>

        {levelQs.map((q, i) => {
          const answerKey = `${level}_${i}`;
          const submitted = fibSubmitted[answerKey];
          const currentInput = fibAnswers[answerKey] || "";

          return (
            <div key={i} className={`p-8 rounded-[2rem] border-4 ${darkMode ? "bg-[#2a2840] border-[#816cb1]" : "bg-white border-[#b8c4a4]"} shadow-xl space-y-6`}>
              <h3 className="text-xl font-bold leading-relaxed">{i + 1}. {q.sentence}</h3>
              
              {!submitted ? (
                <div className="space-y-4">
                  <input 
                    type="text"
                    value={currentInput}
                    onChange={(e) => setFibAnswers(prev => ({ ...prev, [answerKey]: e.target.value }))}
                    placeholder="Type your answer here..."
                    className={`w-full p-4 rounded-xl border-2 font-bold transition-all focus:ring-2 focus:ring-blue-500 outline-none ${darkMode ? "bg-[#16142a] border-[#514d86] text-white" : "bg-gray-50 border-gray-200"}`}
                  />
                  <div className="flex items-center justify-between">
                    <p className="text-xs font-bold opacity-50 italic">💡 Hint: {q.hint}</p>
                    <button 
                      onClick={() => {
                        if (!currentInput.trim()) return;
                        setFibSubmitted(prev => ({ ...prev, [answerKey]: currentInput }));
                        setTotalAnswered(prev => prev + 1);
                        const isCorrect = currentInput.toLowerCase().includes(q.answer.toLowerCase()) || q.answer.toLowerCase().includes(currentInput.toLowerCase());
                        if (isCorrect) {
                          setCorrectAnswered(prev => prev + 1);
                          awardXp(10);
                        } else {
                          awardXp(2);
                        }
                      }}
                      className="px-8 py-2 bg-blue-500 text-white rounded-xl font-black shadow-[0_4px_0_#2563eb] hover:translate-y-1 hover:shadow-[0_2px_0_#2563eb] transition-all"
                    >
                      Check
                    </button>
                  </div>
                </div>
              ) : (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`p-6 rounded-2xl border-2 ${
                    submitted.toLowerCase().includes(q.answer.toLowerCase()) || q.answer.toLowerCase().includes(submitted.toLowerCase())
                      ? "bg-green-50 border-green-200 text-green-800"
                      : "bg-red-50 border-red-200 text-red-800"
                  }`}
                >
                  <p className="font-black mb-1">
                    {submitted.toLowerCase().includes(q.answer.toLowerCase()) || q.answer.toLowerCase().includes(submitted.toLowerCase())
                      ? "✅ Correct! +10 XP" 
                      : `❌ Your answer: "${submitted}"`}
                  </p>
                  <p className="font-bold">Correct Answer: <span className="underline">{q.answer}</span></p>
                </motion.div>
              )}
            </div>
          );
        })}

        {Object.keys(fibSubmitted).length > 0 && (
          <button 
            onClick={() => {
              setFibSubmitted({});
              setFibAnswers({});
            }}
            className="w-full py-4 bg-gray-800 text-white rounded-2xl font-black transition-all hover:bg-black"
          >
            Reset Exercises
          </button>
        )}
      </div>
    );
  };

  const renderConceptChains = () => {
    return (
      <div className="max-w-4xl mx-auto space-y-12">
        <div className="text-center">
          <h2 className="text-4xl font-black mb-2">Concept Chains</h2>
          <p className="opacity-60 font-bold">See how economic forces cascade through the system.</p>
        </div>

        <div className="space-y-12">
          {CONCEPT_CONNECTIONS.map((chain, i) => (
            <div key={i} className={`p-8 rounded-[2rem] border-4 ${darkMode ? "bg-[#2a2840] border-[#816cb1]" : "bg-white border-[#b8c4a4]"} shadow-xl space-y-6`}>
              <div className="flex items-center justify-between">
                <h3 className="text-2xl font-black">{chain.title}</h3>
                <span className={`px-3 py-1 rounded-lg text-[10px] font-black uppercase ${level === "Beginner" ? "bg-green-100 text-green-700" : level === "Intermediate" ? "bg-orange-100 text-orange-700" : "bg-red-100 text-red-700"}`}>
                  {chain.level}
                </span>
              </div>
              <p className="opacity-70 italic font-bold">"{chain.description}"</p>
              
              <div className="flex flex-wrap items-center gap-3">
                {chain.concepts.map((concept, j) => (
                  <React.Fragment key={j}>
                    <div className={`px-4 py-2 rounded-xl border-2 font-bold text-sm ${darkMode ? "bg-[#514d86] border-[#816cb1]" : "bg-[#fff6ae] border-[#e8ae7d]"}`}>
                      {concept}
                    </div>
                    {j < chain.concepts.length - 1 && (
                      <ChevronRight className="text-gray-400" size={20} />
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderContent = () => {
    switch (page) {
      case "Home": return renderHome();
      case "Daily Lesson": return renderLesson();
      case "Quiz": return renderQuiz();
      case "Scenarios": return renderScenarios();
      case "Fill in the Blanks": return renderFillInBlanks();
      case "Concept Chains": return renderConceptChains();
      case "Economic History": return renderHistory();
      case "My Progress": return renderProgress();
      default: return <div className="text-center py-20 opacity-50 italic">Page "{page}" is under construction.</div>;
    }
  };

  return (
    <div className={`min-h-screen flex transition-colors duration-300 ${darkMode ? "bg-[#1e1c2e] text-[#e3e1c8]" : "bg-[#f9f6e3] text-[#2d2020]"}`}>
      {renderSidebar()}
      <main className="flex-1 p-12 overflow-y-auto">
        <AnimatePresence mode="wait">
          <motion.div
            key={page + topic + level}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {renderContent()}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
}
