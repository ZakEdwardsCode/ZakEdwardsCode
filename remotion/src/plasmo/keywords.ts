// Spoken word stem -> lucide icon shown above the caption when that word is said.
const MAP: [RegExp, string][] = [
  [/^(ai|claude|chatgpt|gpt|llm)$/, "Sparkles"],
  [/^(feedback)$/, "MessageSquareText"],
  [/^(mark|marks|marked|marking|marker|scheme)$/, "ClipboardCheck"],
  [/^(paper|papers|pdf|pdfs)$/, "FileText"],
  [/^(exam|exams|gcse|gcses|a-level|levels|igcse)$/, "GraduationCap"],
  [/^(revision|revise|revising|studying|study|learn|learning|learnt)$/, "BookOpen"],
  [/^(time|minutes|hours|hour|weeks|days|instantly|instant|seconds)$/, "Clock"],
  [/^(fast|faster|fastest|quick|quickly|speed)$/, "Zap"],
  [/^(build|built|building|code|coded|coding|developer)$/, "Code"],
  [/^(students|student|people|everyone|users|friends)$/, "Users"],
  [/^(teacher|teachers|tutor|tutors|school|college)$/, "School"],
  [/^(leaderboard|top|best|win|winning|rank|ranking)$/, "Trophy"],
  [/^(score|scores|grade|grades|results|progress|improve|improving|compound)$/, "TrendingUp"],
  [/^(wrong|mistake|mistakes|outdated|problem|problems|bad)$/, "TriangleAlert"],
  [/^(idea|ideas|smarter|smart|why)$/, "Lightbulb"],
  [/^(free|money|pay|paid|price|cost|cheap|subscription)$/, "PoundSterling"],
  [/^(maths|math|calculator|equation)$/, "Calculator"],
  [/^(question|questions|answer|answers|answered)$/, "CircleHelp"],
  [/^(stuck|hint|hints)$/, "LifeBuoy"],
  [/^(target|goal|goals|focus|weak|weakest)$/, "Target"],
  [/^(data|database|stats|statistics|analytics|dashboard)$/, "ChartColumn"],
  [/^(write|writing|written|essay)$/, "PenLine"],
  [/^(voice|speak|talk|microphone)$/, "Mic"],
  [/^(online|website|web|site|app|platform|plasmo)$/, "Globe"],
  [/^(launch|launched|ship|shipped|start|started)$/, "Rocket"],
  [/^(love|enjoy|happy)$/, "Heart"],
];

export const iconForWord = (word: string): string | null => {
  const w = word.toLowerCase();
  for (const [re, icon] of MAP) if (re.test(w)) return icon;
  return null;
};

export const ALL_ICONS = MAP.map(([, i]) => i);
