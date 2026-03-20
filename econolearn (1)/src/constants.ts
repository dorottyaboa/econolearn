import { Level, Lesson, QuizQuestion, Scenario, HistoryEvent, FillInBlank, ConceptChain } from "./types";

export const LEVELS: Level[] = ["Beginner", "Intermediate", "Advanced"];

export const TOPICS: Record<string, string> = {
  "Supply & Demand": "🛒",
  "Inflation & Deflation": "💸",
  "GDP & Growth": "📊",
  "Monetary Policy": "🏦",
  "Fiscal Policy": "🏛️",
  "Labor Markets": "👷",
  "Trade & Globalization": "🌍",
  "Financial Markets": "📉",
  "Business Cycles": "🔄",
  "Behavioral Economics": "🧠",
};

export const LESSONS: Record<string, Record<Level, Lesson>> = {
  "Supply & Demand": {
    Beginner: {
      title: "The Basics of Supply & Demand",
      content: `**Supply and demand** is the foundation of economics. It explains how prices are set and how resources are allocated.

### Demand
- **Demand** is the amount of a good or service consumers are *willing and able* to buy at different prices.
- **Law of Demand**: When price rises, quantity demanded falls (inverse relationship).
- Think of it like this: if pizza costs $50, you'd buy less of it than if it costs $5.

### Supply
- **Supply** is the amount of a good or service producers are *willing and able* to sell at different prices.
- **Law of Supply**: When price rises, quantity supplied increases (positive relationship).
- Higher prices = more profit motive = more production.

### Equilibrium
- **Equilibrium** is where supply meets demand — the price at which the market clears.
- If price is *above* equilibrium → **surplus** (excess supply).
- If price is *below* equilibrium → **shortage** (excess demand).

### Real-World Example
After a hurricane destroys orange groves in Florida, **supply of oranges drops**. With the same demand but less supply, prices rise — this is why OJ gets expensive after storms.`,
      key_terms: {
        Demand: "Willingness and ability to buy at a given price",
        Supply: "Willingness and ability to sell at a given price",
        Equilibrium: "Price where quantity supplied equals quantity demanded",
        Surplus: "When supply exceeds demand at a given price",
        Shortage: "When demand exceeds supply at a given price",
      },
    },
    Intermediate: {
      title: "Elasticity & Market Shifts",
      content: `### Price Elasticity of Demand (PED)
Elasticity measures *how responsive* quantity is to a price change.

**Formula**: PED = % Change in Quantity Demanded / % Change in Price

- **Elastic** (PED > 1): Consumers are sensitive to price (luxury goods, things with substitutes).
- **Inelastic** (PED < 1): Consumers are NOT sensitive to price (insulin, gasoline in short term).

### Shifts vs. Movements
- **Movement along the curve**: caused by a price change.
- **Shift of the curve**: caused by everything else (income, tastes, related goods prices, expectations, number of buyers).

### Determinants of Supply Shifts
- Input costs (if steel prices rise, car supply falls)
- Technology (better tech increases supply)
- Number of producers
- Government subsidies/taxes

### Consumer & Producer Surplus
- **Consumer Surplus**: The difference between what you're *willing* to pay and what you *actually* pay.
- **Producer Surplus**: The difference between what a producer *receives* and their minimum acceptable price.
- Total welfare = Consumer Surplus + Producer Surplus`,
      key_terms: {
        Elasticity: "Responsiveness of quantity to price changes",
        Elastic: "PED > 1; consumers highly responsive to price",
        Inelastic: "PED < 1; consumers not sensitive to price",
        "Consumer Surplus": "Benefit consumers gain above what they pay",
        "Producer Surplus": "Benefit producers gain above their minimum price",
      },
    },
    Advanced: {
      title: "Market Failures & Externalities",
      content: `### When Markets Fail
Free markets are efficient *only* under perfect conditions. Market failures occur when:
1. **Externalities** exist (costs/benefits fall on third parties)
2. **Public goods** are underprovided (non-rival, non-excludable)
3. **Information asymmetry** (one party knows more than the other)
4. **Market power** (monopolies distort prices)

### Externalities
- **Negative externality**: Pollution — the social cost exceeds the private cost. Market overproduces.
- **Positive externality**: Education — social benefit exceeds private benefit. Market underproduces.
- **Pigouvian tax**: Tax = external cost, internalizing the externality (e.g., carbon taxes).
- **Coase Theorem**: If property rights are well-defined and transaction costs are zero, parties will negotiate an efficient outcome regardless of who holds the rights.

### Information Asymmetry
- **Adverse Selection**: Low-quality goods drive out high-quality (Akerlof's "Market for Lemons").
- **Moral Hazard**: People take more risk when insured (e.g., reckless driving if fully covered).
- **Principal-Agent Problem**: Agent's interests misalign with principal's (CEO vs. shareholders).

### Game Theory in Markets
- **Nash Equilibrium**: No player benefits from unilaterally changing strategy.
- **Prisoner's Dilemma**: Individually rational choices lead to collectively suboptimal outcomes — explains why OPEC cartels are unstable.`,
      key_terms: {
        Externality: "Cost/benefit falling on uninvolved third parties",
        "Pigouvian Tax": "Tax equal to external cost to correct market failure",
        "Adverse Selection": "Bad products/risks dominate due to information gaps",
        "Moral Hazard": "Risk-taking increases when insured against consequences",
        "Nash Equilibrium": "Stable outcome where no player benefits from changing strategy",
      },
    },
  },
  "Inflation & Deflation": {
    Beginner: {
      title: "What is Inflation?",
      content: `**Inflation** is the general rise in the price level over time. It means your money buys *less* than it used to.

### Measuring Inflation
- **CPI (Consumer Price Index)**: Tracks prices of a "basket" of goods a typical household buys.
- **Core Inflation**: CPI excluding volatile food and energy prices — used for policy decisions.

### Why Does Inflation Happen?
1. **Demand-Pull**: Too much money chasing too few goods. ("Too many dollars, too few pizzas")
2. **Cost-Push**: Production costs rise (wages, oil prices), so businesses charge more.
3. **Built-in Inflation**: Workers expect inflation → demand higher wages → businesses raise prices → cycle repeats.

### Effects of Inflation
- **Savers lose**: $1,000 in 1980 buys much less today.
- **Debtors gain**: You repay loans with "cheaper" future dollars.
- **Fixed-income earners hurt**: Retirees on fixed pensions lose purchasing power.
- **Hyperinflation** (extreme inflation) destroys economies — see Germany 1923, Zimbabwe 2008.

### The Target
Most central banks (like the US Fed) target **~2% annual inflation** — low enough to be stable, high enough to avoid deflation's trap.`,
      key_terms: {
        Inflation: "General rise in price levels over time",
        CPI: "Consumer Price Index — measures household basket of goods",
        Deflation: "General fall in price levels",
        Hyperinflation: "Extremely rapid, out-of-control inflation",
        "Purchasing Power": "The real value of money in terms of goods it can buy",
      },
    },
    Intermediate: {
      title: "Inflation, Interest Rates & the Fisher Effect",
      content: `### Real vs. Nominal Interest Rates
- **Nominal rate**: The stated interest rate on a loan or bond.
- **Real rate**: Adjusted for inflation. Real rate ≈ Nominal rate − Inflation rate.
- **Fisher Equation**: (1 + nominal) = (1 + real)(1 + inflation)

Example: A bank pays 5% nominal. Inflation is 3%. Your real return is ≈ 2%.

### The Phillips Curve
Historically, there was a **trade-off between inflation and unemployment**:
- Low unemployment → workers demand higher wages → firms raise prices → inflation up.
- But the **1970s stagflation** (high inflation + high unemployment) broke this simple trade-off.
- **Expectations-augmented Phillips Curve**: The trade-off only holds in the *short run*. In the long run, there's a **Natural Rate of Unemployment (NAIRU)**.

### Monetary Transmission
1. Fed raises interest rates
2. Borrowing becomes expensive
3. Business investment and consumer spending fall
4. Demand drops → inflation cools

### Inflation Expectations
**Expectations drive inflation** as much as actual money supply. If everyone *expects* 5% inflation, wages and prices adjust to that — it becomes self-fulfilling. Central banks spend enormous effort managing expectations (forward guidance).`,
      key_terms: {
        "Fisher Equation": "Links nominal rates, real rates, and inflation",
        "Phillips Curve": "Short-run trade-off between inflation and unemployment",
        NAIRU: "Natural rate of unemployment consistent with stable inflation",
        Stagflation: "Simultaneous high inflation and high unemployment",
        "Forward Guidance": "Central bank communication about future policy to shape expectations",
      },
    },
    Advanced: {
      title: "Monetary Theory: QE, ZIRP & Modern Debates",
      content: `### Quantitative Easing (QE)
When rates hit zero (**Zero Interest Rate Policy / ZIRP**), central banks lose their main tool. QE is the alternative:
- Central bank *buys* long-term government bonds and mortgage-backed securities
- Injects reserves into banking system
- Pushes down long-term interest rates
- Boosts asset prices → wealth effect → spending

**Criticism**: QE inflates asset prices disproportionately, widening wealth inequality.

### Modern Monetary Theory (MMT)
Controversial heterodox view:
- A government that issues its own currency can *never* run out of money.
- The real constraint is **inflation**, not debt levels.
- Tax policy is used to control inflation (drain money from economy), not to fund spending.

**Mainstream critique**: MMT underestimates inflation risk and political constraints on tax increases.

### Quantity Theory of Money
**MV = PQ** (Fisher's Equation of Exchange)
- M = money supply, V = velocity of money, P = price level, Q = real output
- If V and Q are stable, more M → higher P (inflation).
- Post-2008: Fed expanded M massively but inflation stayed low — V collapsed (hoarding). This challenged simple quantity theory.

### The Debt-Deflation Trap (Fisher, 1933)
- Falling prices increase real value of debts.
- Debtors sell assets to repay.
- Asset prices fall further → more deflation → more defaults.
- This is why central banks *fear* deflation more than moderate inflation.`,
      key_terms: {
        QE: "Quantitative Easing — central bank asset purchases to inject liquidity",
        ZIRP: "Zero Interest Rate Policy — rates at or near 0%",
        MMT: "Modern Monetary Theory — sovereign currency issuers aren't revenue-constrained",
        "MV=PQ": "Quantity theory linking money supply to price level",
        "Debt-Deflation": "Falling prices raise real debt burden, triggering defaults and more deflation",
      },
    },
  },
};

export const QUIZ_QUESTIONS: Record<Level, QuizQuestion[]> = {
  Beginner: [
    {
      q: "What happens to the price of a good when supply decreases and demand stays the same?",
      options: ["A) Price falls", "B) Price rises", "C) Price stays the same", "D) Quantity demanded falls to zero"],
      answer: "B",
      explanation: "With the same demand but less supply, the equilibrium price rises — there are fewer goods competing for the same buyers.",
    },
    {
      q: "Which formula correctly represents GDP using the expenditure approach?",
      options: ["A) GDP = C + I + G + T", "B) GDP = C + I + G + (X - M)", "C) GDP = C + S + G + X", "D) GDP = C + I - G + (X - M)"],
      answer: "B",
      explanation: "GDP = Consumer spending + Investment + Government spending + Net Exports (Exports minus Imports).",
    },
  ],
  Intermediate: [
    {
      q: "If a good has a price elasticity of demand of -2.5, it is considered:",
      options: ["A) Inelastic", "B) Unit elastic", "C) Elastic", "D) Perfectly inelastic"],
      answer: "C",
      explanation: "When |PED| > 1, demand is elastic — consumers are very responsive to price changes.",
    },
  ],
  Advanced: [
    {
      q: "In the IS-LM model at the Zero Lower Bound, a fiscal expansion will:",
      options: ["A) Be completely crowded out by rising interest rates", "B) Have a smaller multiplier than during normal times", "C) Have a larger multiplier because monetary policy cannot offset it", "D) Have no effect due to Ricardian Equivalence"],
      answer: "C",
      explanation: "At the ZLB, monetary policy cannot tighten to offset fiscal expansion, so the full multiplier applies without crowding out via interest rates.",
    },
  ],
};

export const SCENARIO_EXERCISES: Record<Level, Scenario[]> = {
  Beginner: [
    {
      scenario: "🌽 The Corn Crisis",
      situation: "A drought destroys 40% of the US corn crop. Corn is used in food, animal feed, and ethanol fuel.",
      question: "What do you predict will happen to: (1) the price of corn, (2) the price of beef, and (3) the price of gasoline?",
      answer: "1. Corn price RISES (supply decreased, demand unchanged → shortage → higher price). 2. Beef price RISES (corn = cow feed → input cost rises → supply of beef shifts left → price rises). 3. Gasoline price RISES (ethanol is a substitute/blend for gasoline; if corn is scarce, ethanol is scarce, and gasoline demand rises). This is called a 'supply chain ripple effect.'",
      key_concept: "Supply shocks ripple through interconnected markets via input costs and substitutes.",
    },
  ],
  Intermediate: [
    {
      scenario: "🏦 The Fed's Dilemma",
      situation: "It's 2022. Inflation is running at 8% (well above the 2% target). Unemployment is at 3.5% (below the natural rate). But housing prices are already falling and the stock market is down 25%.",
      question: "Should the Fed raise interest rates aggressively, raise them slowly, or hold rates steady? Walk through the trade-offs using the Taylor Rule framework.",
      answer: "Taylor Rule says: with inflation 6 points above target and a positive output gap, rates should be raised substantially — perhaps to 4-5% or higher. Aggressive raises: faster reduction in inflation, at the cost of higher unemployment and risk of recession. Slower raises: less economic disruption, but risk of inflation becoming entrenched in expectations. The Fed chose aggressive (from 0.25% to 5.5% in 16 months). Outcome: inflation fell substantially, no severe recession (a 'soft landing') — but housing market froze.",
      key_concept: "The Taylor Rule provides a systematic framework for rate decisions, but the severity of off-target conditions and lag effects require judgment.",
    },
  ],
  Advanced: [],
};

export const HISTORY_EVENTS: HistoryEvent[] = [
  {
    year: "1776",
    event: "The Wealth of Nations",
    description: "Adam Smith publishes *The Wealth of Nations*, founding modern economics. Key ideas: division of labor, the 'invisible hand' of markets, free trade over mercantilism.",
    lesson: "Markets can coordinate complex activity without central direction through price signals.",
    era: "Classical Economics",
  },
  {
    year: "1929",
    event: "The Great Crash & Great Depression",
    description: "Stock market crashes in October 1929. By 1933, US unemployment hits 25%. GDP falls ~30%. The Smoot-Hawley Tariff Act worsens global depression through trade wars.",
    lesson: "Bank panics and monetary contraction can turn recessions into depressions. Milton Friedman blamed the Fed for letting the money supply collapse by 1/3.",
    era: "Great Depression",
  },
];

export const FILL_IN_BLANKS: FillInBlank[] = [
  {
    sentence: "GDP = ___ + Investment + Government Spending + Net Exports",
    answer: "Consumer Spending",
    hint: "The biggest component, ~70% of US GDP",
    level: "Beginner",
  },
  {
    sentence: "When price rises, quantity demanded falls — this is the Law of ___.",
    answer: "Demand",
    hint: "The fundamental inverse relationship between price and quantity bought",
    level: "Beginner",
  },
  {
    sentence: "The ___ is the central bank of the United States.",
    answer: "Federal Reserve",
    hint: "Created in 1913, it sets US monetary policy",
    level: "Beginner",
  },
  {
    sentence: "The ___ Curve shows the short-run trade-off between inflation and unemployment.",
    answer: "Phillips",
    hint: "Named after New Zealand economist A.W. Phillips",
    level: "Intermediate",
  },
  {
    sentence: "MV = PQ is the ___ of Money, where V is the velocity of money.",
    answer: "Quantity Theory",
    hint: "Links money supply to price level",
    level: "Intermediate",
  },
  {
    sentence: "According to the Efficient Market Hypothesis, ___ form states even inside information is priced in.",
    answer: "Strong",
    hint: "The most extreme version of the EMH",
    level: "Advanced",
  },
];

export const CONCEPT_CONNECTIONS: ConceptChain[] = [
  {
    title: "Connect: Inflation → Interest Rates → GDP",
    concepts: ["Inflation rises", "Fed raises rates", "Borrowing costs up", "Investment falls", "GDP growth slows", "Unemployment rises", "Wage growth slows", "Inflation falls"],
    description: "Trace how an inflation spike triggers a chain of cause and effect through the economy.",
    level: "Beginner",
  },
  {
    title: "Connect: Asset Bubble Formation",
    concepts: ["Low interest rates", "Cheap credit", "Asset price rises", "Collateral value rises", "More borrowing", "More asset buying", "Prices rise further", "MINSKY MOMENT: debt can't be serviced", "Forced selling", "Prices crash", "Credit tightens"],
    description: "Hyman Minsky's financial instability hypothesis — trace how booms sow the seeds of busts.",
    level: "Intermediate",
  },
];
