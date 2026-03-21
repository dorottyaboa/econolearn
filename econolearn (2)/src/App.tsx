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
  CONCEPT_CONNECTIONS,
  UNITS
} from "./constants";
import { Level, Lesson, QuizQuestion, Scenario, HistoryEvent, FillInBlank, ConceptChain, Unit, MapNode } from "./types";

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

  const [completedNodes, setCompletedNodes] = useState<string[]>(() => {
    try {
      return JSON.parse(localStorage.getItem("econ_completedNodes") || "[]");
    } catch (e) {
      return [];
    }
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

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
      localStorage.setItem("econ_completedNodes", JSON.stringify(completedNodes));
    } catch (e) {
      console.warn("localStorage not available", e);
    }
  }, [level, topic, xp, streak, darkMode, totalAnswered, correctAnswered, dailyDone, quizAnswers, scenarioRevealed, fibSubmitted, completedNodes]);

  useEffect(() => {
    // Mock streak logic - in a real app this would check the last login date
    if (streak === 0) setStreak(3);
  }, []);

  const awardXp = (amount: number) => {
    setXp(prev => prev + amount);
  };

  const toggleDarkMode = () => setDarkMode(!darkMode);

  const renderTopBar = () => (
    <div className={`fixed top-0 left-0 right-0 h-16 border-b-4 z-50 transition-colors duration-300 ${darkMode ? "bg-app-sidebar border-app-sidebar-border" : "bg-app-sidebar border-app-sidebar-border"} flex items-center justify-between px-6`}>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1 bg-white/10 px-3 py-1 rounded-full border-2 border-white/20">
          <Flame size={18} className="text-orange-400 fill-orange-400" />
          <span className="text-sm font-black text-white">{streak}</span>
        </div>
        <div className="flex items-center gap-1 bg-white/10 px-3 py-1 rounded-full border-2 border-white/20">
          <Award size={18} className="text-yellow-400" />
          <span className="text-sm font-black text-white">{xp}</span>
        </div>
      </div>
      
      <h2 className="text-xl font-black text-white flex items-center gap-2 tracking-tighter absolute left-1/2 -translate-x-1/2">
        <TrendingUp size={24} strokeWidth={3} /> ECONO
      </h2>

      <div className="flex items-center gap-3">
        <button 
          onClick={toggleDarkMode}
          className={`p-2 rounded-xl transition-all ${darkMode ? "bg-app-card-border text-yellow-400" : "bg-app-xp-bg text-white"} hover:scale-110 shadow-lg`}
        >
          {darkMode ? <Sun size={18} /> : <Moon size={18} />}
        </button>
      </div>
    </div>
  );

  const renderBottomNav = () => (
    <div className={`fixed bottom-0 left-0 right-0 h-20 border-t-4 z-50 transition-colors duration-300 ${darkMode ? "bg-app-sidebar border-app-sidebar-border" : "bg-app-sidebar border-app-sidebar-border"} flex items-center justify-around px-4`}>
      {[
        { icon: <TrendingUp size={24} />, label: "Map", id: "Home" },
        { icon: <HelpCircle size={24} />, label: "Quiz", id: "Quiz" },
        { icon: <Target size={24} />, label: "Scenarios", id: "Scenarios" },
        { icon: <History size={24} />, label: "History", id: "Economic History" },
        { icon: <BarChart3 size={24} />, label: "Stats", id: "My Progress" },
      ].map((item) => (
        <button
          key={item.id}
          onClick={() => setPage(item.id as Page)}
          className={`flex flex-col items-center gap-1 transition-all ${
            page === item.id 
              ? "text-white scale-110" 
              : "text-white/40 hover:text-white/60"
          }`}
        >
          <div className={`p-2 rounded-xl ${page === item.id ? "bg-white/20 border-2 border-white/30" : ""}`}>
            {item.icon}
          </div>
          <span className="text-[10px] font-black uppercase tracking-widest">{item.label}</span>
        </button>
      ))}
    </div>
  );

  const renderMap = () => {
    const isNodeUnlocked = (nodeId: string) => {
      const allNodes = UNITS.flatMap(u => u.nodes);
      const nodeIndex = allNodes.findIndex(n => n.id === nodeId);
      if (nodeIndex === 0) return true;
      const prevNode = allNodes[nodeIndex - 1];
      return completedNodes.includes(prevNode.id);
    };

    return (
      <div className="max-w-md mx-auto py-24 px-4 space-y-32">
        {UNITS.map((unit, unitIdx) => (
          <div key={unit.id} className="space-y-16">
            <div className={`p-6 rounded-[2rem] border-4 ${darkMode ? "bg-app-card border-app-card-border text-white" : "bg-app-sidebar border-app-text text-[#FDF6E3]"} shadow-[8px_8px_0_rgba(0,0,0,0.1)] relative overflow-hidden`}>
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <BookOpen size={80} />
              </div>
              <h3 className="text-[10px] font-black uppercase tracking-[0.3em] opacity-70 mb-1">Unit {unitIdx + 1}</h3>
              <h2 className="text-2xl font-black tracking-tighter mb-2">{unit.title}</h2>
              <p className="text-sm font-medium opacity-90 leading-tight">{unit.description}</p>
            </div>

            <div className="flex flex-col items-center gap-16 relative">
              {/* Path line */}
              <div className={`absolute top-0 bottom-0 w-3 ${darkMode ? "bg-app-sidebar" : "bg-app-text/10"} -z-10 rounded-full`} />
              
              {unit.nodes.map((node, nodeIdx) => {
                const unlocked = isNodeUnlocked(node.id);
                const completed = completedNodes.includes(node.id);
                // S-curve logic: alternate left, center, right
                const positions = [0, 70, 0, -70];
                const offset = positions[nodeIdx % 4];

                return (
                  <div key={node.id} className="relative">
                    <motion.button
                      whileHover={unlocked ? { scale: 1.1 } : {}}
                      whileTap={unlocked ? { scale: 0.95 } : {}}
                      onClick={() => {
                        if (unlocked) {
                          setTopic(node.topic);
                          setLevel(node.level);
                          setPage("Daily Lesson");
                        }
                      }}
                      style={{ x: offset }}
                      className={`relative w-20 h-20 rounded-full border-b-8 flex items-center justify-center text-3xl shadow-xl transition-all ${
                        completed 
                          ? "bg-app-btn border-app-btn-shadow text-white" 
                          : unlocked 
                            ? "bg-white border-gray-300 text-gray-700"
                            : "bg-gray-200 border-gray-300 text-gray-400 opacity-50 cursor-not-allowed"
                      }`}
                    >
                      {node.icon}
                      {completed && (
                        <div className="absolute -top-1 -right-1 bg-green-500 text-white rounded-full p-1 border-2 border-white shadow-lg">
                          <CheckCircle2 size={14} strokeWidth={4} />
                        </div>
                      )}
                      {!unlocked && (
                        <div className="absolute inset-0 flex items-center justify-center bg-black/5 rounded-full">
                          <Zap size={20} className="text-gray-400" />
                        </div>
                      )}
                    </motion.button>
                    
                    {/* Label */}
                    <div 
                      style={{ x: offset }}
                      className={`absolute top-full mt-4 left-1/2 -translate-x-1/2 whitespace-nowrap px-3 py-1 rounded-xl border-2 font-black uppercase text-[9px] tracking-widest ${
                        unlocked 
                          ? (darkMode ? "bg-app-card border-app-card-border text-white" : "bg-white border-gray-200 text-gray-600")
                          : "bg-gray-100 border-gray-200 text-gray-400"
                      }`}
                    >
                      {node.title}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
        <div className="h-20" /> {/* Spacer for bottom nav */}
      </div>
    );
  };

  const renderHome = () => renderMap();

  const renderDailyLesson = () => {
    const lesson = LESSONS[topic]?.[level];
    if (!lesson) return <div className="text-center py-20 opacity-50 italic">No lesson available for this topic and level.</div>;

    const markAsComplete = () => {
      const node = UNITS.flatMap(u => u.nodes).find(n => n.topic === topic && n.level === level);
      if (node && !completedNodes.includes(node.id)) {
        setCompletedNodes(prev => [...prev, node.id]);
        awardXp(50);
      }
      setPage("Home");
    };

    return (
      <div className="max-w-3xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <div className="flex justify-center gap-2">
            <span className={`px-4 py-1 rounded-full text-xs font-black uppercase ${level === "Beginner" ? "bg-green-100 text-green-700" : level === "Intermediate" ? "bg-orange-100 text-orange-700" : "bg-red-100 text-red-700"}`}>
              {level}
            </span>
            <span className="px-4 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-black uppercase">{topic}</span>
          </div>
          <h2 className="text-4xl font-black text-app-text">{lesson.title}</h2>
        </div>

        <div className={`p-8 rounded-[2rem] border-4 prose prose-lg max-w-none bg-app-card border-app-card-border text-app-text markdown-content`}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {lesson.content}
          </ReactMarkdown>
        </div>

        <div className="space-y-4">
          <h3 className="text-2xl font-black flex items-center gap-2 text-app-text">
            <Zap className="text-yellow-500" /> Key Terms
          </h3>
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(lesson.key_terms).map(([term, def], i) => (
              <div key={i} className={`p-4 rounded-2xl border-2 bg-app-sidebar border-app-sidebar-border text-white`}>
                <h4 className="font-black mb-1">{term}</h4>
                <p className="text-sm opacity-70">{def}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-4 pt-8">
          <button 
            onClick={markAsComplete}
            className={`flex-1 py-6 rounded-2xl font-black transition-all hover:scale-[1.02] active:scale-[0.98] bg-app-btn text-white shadow-[0_8px_0_var(--app-btn-shadow)]`}
          >
            Complete Lesson & Return to Map
          </button>
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
          <h2 className="text-4xl font-black mb-2 text-app-text">Quiz Time!</h2>
          <p className="opacity-60 font-bold text-app-text">Level: {level}</p>
        </div>

        {questions.map((q, i) => {
          const answerKey = `${level}_${i}`;
          const result = quizAnswers[answerKey];

          return (
            <div key={i} className={`p-8 rounded-[2rem] border-4 bg-app-card border-app-card-border shadow-xl space-y-6`}>
              <h3 className="text-xl font-black text-app-text">Q{i + 1}: {q.q}</h3>
              
              <div className="space-y-3">
                {q.options.map((opt, j) => {
                  const optLetter = opt[0];
                  const isSelected = result?.chosen === optLetter;
                  const isCorrect = q.answer === optLetter;
                  
                  let btnClass = "bg-app-sidebar border-app-sidebar-border text-white hover:opacity-90";
                  if (result) {
                    if (isCorrect) btnClass = "bg-green-500 text-white border-green-600";
                    else if (isSelected) btnClass = "bg-red-500 text-white border-red-600";
                    else btnClass = "opacity-40 bg-gray-100 border-gray-200 text-gray-500";
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
            className="w-full py-4 bg-app-sidebar text-white rounded-2xl font-black transition-all hover:opacity-90"
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
          <h2 className="text-4xl font-black mb-2 text-app-text">Real-World Scenarios</h2>
          <p className="opacity-60 font-bold text-app-text">Apply your knowledge to solve economic puzzles.</p>
        </div>

        {scenarios.map((s, i) => {
          const revealed = scenarioRevealed[`${level}_${i}`];
          return (
            <div key={i} className="space-y-6">
              <div className={`p-8 rounded-[2rem] border-4 bg-app-card border-app-card-border shadow-xl space-y-6`}>
                <h3 className="text-2xl font-black text-app-btn">{s.scenario}</h3>
                <div className={`p-6 rounded-2xl border-2 bg-app-sidebar border-app-sidebar-border text-white`}>
                  <p className="font-bold leading-relaxed">{s.situation}</p>
                </div>
                <p className="text-lg font-black italic text-app-text">❓ {s.question}</p>
                
                {!revealed ? (
                  <button 
                    onClick={() => {
                      setScenarioRevealed(prev => ({ ...prev, [`${level}_${i}`]: true }));
                      awardXp(5);
                    }}
                    className="w-full py-4 bg-app-btn text-white rounded-2xl font-black shadow-[0_4px_0_var(--app-btn-shadow)] hover:translate-y-1 hover:shadow-none transition-all"
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
          <h2 className="text-4xl font-black mb-2 text-app-text">Economic History</h2>
          <p className="opacity-60 font-bold text-app-text">The events that shaped the global economy.</p>
        </div>

        <div className="space-y-8 relative before:absolute before:left-8 before:top-0 before:bottom-0 before:w-1 before:bg-app-text/10 before:hidden md:before:block">
          {HISTORY_EVENTS.map((event, i) => (
            <div key={i} className="md:pl-20 relative">
              <div className="hidden md:flex absolute left-6 top-10 w-5 h-5 rounded-full bg-app-btn border-4 border-app-card-border z-10" />
              <div className={`p-8 rounded-[2rem] border-4 bg-app-card border-app-card-border shadow-xl space-y-4`}>
                <div className="flex items-center justify-between">
                  <span className="text-3xl font-black text-app-btn">{event.year}</span>
                  <span className={`px-3 py-1 rounded-lg text-[10px] font-black uppercase bg-app-sidebar text-white`}>
                    {event.era}
                  </span>
                </div>
                <h3 className="text-2xl font-black text-app-text">{event.event}</h3>
                <p className="opacity-80 leading-relaxed text-app-text">{event.description}</p>
                <div className={`p-4 rounded-xl border-2 bg-app-sidebar border-app-sidebar-border text-white/90`}>
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
        <h2 className="text-4xl font-black mb-2 text-app-text">My Progress</h2>
        <p className="opacity-60 font-bold text-app-text">Track your journey to economic mastery.</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {[
          { label: "Total XP", value: xp, color: "text-yellow-500" },
          { label: "Accuracy", value: totalAnswered > 0 ? `${Math.round((correctAnswered / totalAnswered) * 100)}%` : "N/A", color: "text-green-500" },
          { label: "Lessons Done", value: completedNodes.length, color: "text-blue-500" },
          { label: "Streak", value: `${streak} days`, color: "text-orange-500" },
        ].map((stat, i) => (
          <div key={i} className={`p-6 rounded-3xl border-4 text-center bg-app-card border-app-card-border`}>
            <p className="text-xs font-black uppercase tracking-widest opacity-50 mb-1 text-app-text">{stat.label}</p>
            <p className={`text-3xl font-black ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="space-y-6">
        <h3 className="text-2xl font-black text-app-text">Badges Earned</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { id: "starter", label: "First Lesson", icon: "🥉", unlocked: completedNodes.length > 0 },
            { id: "club", label: "5 Lessons", icon: "🥇", unlocked: completedNodes.length >= 5 },
            { id: "quiz", label: "Quiz Starter", icon: "📝", unlocked: correctAnswered >= 5 },
            { id: "master", label: "Quiz Master", icon: "🎓", unlocked: correctAnswered >= 20 },
          ].map((badge) => (
            <div key={badge.id} className={`p-6 rounded-3xl border-4 text-center transition-all ${
              badge.unlocked 
                ? "bg-app-sidebar border-app-btn text-white shadow-lg scale-105" 
                : "bg-app-sidebar border-app-sidebar-border opacity-40 grayscale text-white/50"
            }`}>
              <div className="text-4xl mb-2">{badge.icon}</div>
              <p className="font-black text-sm">{badge.label}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="pt-8 border-t border-app-text/10">
        <button 
          onClick={() => {
            if (confirm("Are you sure you want to reset all progress?")) {
              localStorage.clear();
              window.location.reload();
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
          <h2 className="text-4xl font-black mb-2 text-app-text">Fill in the Blanks</h2>
          <p className="opacity-60 font-bold text-app-text">Test your terminology knowledge.</p>
        </div>

        {levelQs.map((q, i) => {
          const answerKey = `${level}_${i}`;
          const submitted = fibSubmitted[answerKey];
          const currentInput = fibAnswers[answerKey] || "";

          return (
            <div key={i} className={`p-8 rounded-[2rem] border-4 bg-app-card border-app-card-border shadow-xl space-y-6`}>
              <h3 className="text-xl font-bold leading-relaxed text-app-text">{i + 1}. {q.sentence}</h3>
              
              {!submitted ? (
                <div className="space-y-4">
                  <input 
                    type="text"
                    value={currentInput}
                    onChange={(e) => setFibAnswers(prev => ({ ...prev, [answerKey]: e.target.value }))}
                    placeholder="Type your answer here..."
                    className={`w-full p-4 rounded-xl border-2 font-bold transition-all focus:ring-2 focus:ring-app-btn outline-none bg-app-sidebar border-app-sidebar-border text-white`}
                  />
                  <div className="flex items-center justify-between">
                    <p className="text-xs font-bold opacity-50 italic text-app-text">💡 Hint: {q.hint}</p>
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
                      className="px-8 py-2 bg-app-btn text-white rounded-xl font-black shadow-[0_4px_0_var(--app-btn-shadow)] hover:translate-y-1 hover:shadow-none transition-all"
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
            className="w-full py-4 bg-app-sidebar text-white rounded-2xl font-black transition-all hover:opacity-90"
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
          <h2 className="text-4xl font-black mb-2 text-app-text">Concept Chains</h2>
          <p className="opacity-60 font-bold text-app-text">See how economic forces cascade through the system.</p>
        </div>

        <div className="space-y-12">
          {CONCEPT_CONNECTIONS.map((chain, i) => (
            <div key={i} className={`p-8 rounded-[2rem] border-4 bg-app-card border-app-card-border shadow-xl space-y-6`}>
              <div className="flex items-center justify-between">
                <h3 className="text-2xl font-black text-app-text">{chain.title}</h3>
                <span className={`px-3 py-1 rounded-lg text-[10px] font-black uppercase ${level === "Beginner" ? "bg-green-100 text-green-700" : level === "Intermediate" ? "bg-orange-100 text-orange-700" : "bg-red-100 text-red-700"}`}>
                  {chain.level}
                </span>
              </div>
              <p className="opacity-70 italic font-bold text-app-text">"{chain.description}"</p>
              
              <div className="flex flex-wrap items-center gap-3">
                {chain.concepts.map((concept, j) => (
                  <React.Fragment key={j}>
                    <div className={`px-4 py-2 rounded-xl border-2 font-bold text-sm bg-app-sidebar border-app-sidebar-border text-white`}>
                      {concept}
                    </div>
                    {j < chain.concepts.length - 1 && (
                      <ChevronRight className="text-app-text/40" size={20} />
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


  return (
    <div className={`min-h-screen transition-colors duration-300 bg-app-bg text-app-text font-sans pb-24`}>
      {renderTopBar()}
      
      <main className="pt-16">
        <div className="max-w-4xl mx-auto p-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={page + topic + level}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
            >
              {page === "Home" && renderHome()}
              {page === "Daily Lesson" && renderDailyLesson()}
              {page === "Quiz" && renderQuiz()}
              {page === "Scenarios" && renderScenarios()}
              {page === "Fill in the Blanks" && renderFillInBlanks()}
              {page === "Concept Chains" && renderConceptChains()}
              {page === "Economic History" && renderHistory()}
              {page === "My Progress" && renderProgress()}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>

      {renderBottomNav()}
    </div>
  );
}
