import { 
  Level, 
  Lesson, 
  QuizQuestion, 
  Scenario, 
  HistoryEvent, 
  FillInBlank, 
  ConceptChain, 
  Unit 
} from "./types";

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

export const UNITS: Unit[] = [
  {
    id: "unit-1",
    title: "Unit 1: The Core Foundation",
    description: "Master the fundamental principles of supply, demand, and market equilibrium.",
    level: "Beginner",
    nodes: [
      { id: "node-1", title: "Supply & Demand 101", topic: "Supply & Demand", level: "Beginner", icon: "🛒" },
      { id: "node-2", title: "Inflation Basics", topic: "Inflation & Deflation", level: "Beginner", icon: "💸" },
      { id: "node-3", title: "Understanding GDP", topic: "GDP & Growth", level: "Beginner", icon: "📊" },
    ]
  },
  {
    id: "unit-2",
    title: "Unit 2: Policy & Power",
    description: "Explore how governments and central banks influence the economy.",
    level: "Beginner",
    nodes: [
      { id: "node-4", title: "Monetary Policy Intro", topic: "Monetary Policy", level: "Beginner", icon: "🏦" },
      { id: "node-5", title: "Fiscal Policy Intro", topic: "Fiscal Policy", level: "Beginner", icon: "🏛️" },
      { id: "node-6", title: "Labor Markets 101", topic: "Labor Markets", level: "Beginner", icon: "👷" },
    ]
  },
  {
    id: "unit-3",
    title: "Unit 3: Global Connections",
    description: "Learn how countries trade and how markets fluctuate over time.",
    level: "Beginner",
    nodes: [
      { id: "node-7", title: "Trade & Globalization", topic: "Trade & Globalization", level: "Beginner", icon: "🌍" },
      { id: "node-8", title: "Financial Markets Intro", topic: "Financial Markets", level: "Beginner", icon: "📉" },
      { id: "node-9", title: "Business Cycles Intro", topic: "Business Cycles", level: "Beginner", icon: "🔄" },
      { id: "node-10", title: "Behavioral Economics Intro", topic: "Behavioral Economics", level: "Beginner", icon: "🧠" },
    ]
  },
  {
    id: "unit-4",
    title: "Unit 4: Intermediate Dynamics",
    description: "Deep dive into elasticity, market shifts, and the Fisher effect.",
    level: "Intermediate",
    nodes: [
      { id: "node-11", title: "Elasticity & Shifts", topic: "Supply & Demand", level: "Intermediate", icon: "🛒" },
      { id: "node-12", title: "The Fisher Effect", topic: "Inflation & Deflation", level: "Intermediate", icon: "💸" },
      { id: "node-13", title: "Growth Models", topic: "GDP & Growth", level: "Intermediate", icon: "📊" },
    ]
  },
  {
    id: "unit-5",
    title: "Unit 5: Advanced Theory",
    description: "Master complex market failures, game theory, and modern monetary policy.",
    level: "Advanced",
    nodes: [
      { id: "node-14", title: "Market Failures", topic: "Supply & Demand", level: "Advanced", icon: "🛒" },
      { id: "node-15", title: "QE & ZIRP", topic: "Inflation & Deflation", level: "Advanced", icon: "💸" },
      { id: "node-16", title: "Endogenous Growth", topic: "GDP & Growth", level: "Advanced", icon: "📊" },
    ]
  }
];

export const LESSONS: Record<string, Record<Level, Lesson>> = {
  "Supply & Demand": {
    Beginner: {
      id: "sd-beg", topic: "Supply & Demand", level: "Beginner",
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
      id: "sd-int", topic: "Supply & Demand", level: "Intermediate",
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
      id: "sd-adv", topic: "Supply & Demand", level: "Advanced",
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
      id: "id-beg", topic: "Inflation & Deflation", level: "Beginner",
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
      id: "id-int", topic: "Inflation & Deflation", level: "Intermediate",
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
      id: "id-adv", topic: "Inflation & Deflation", level: "Advanced",
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
  "GDP & Growth": {
    Beginner: {
      id: "gdp-beg", topic: "GDP & Growth", level: "Beginner",
      title: "Understanding GDP",
      content: `**Gross Domestic Product (GDP)** is the total value of all final goods and services produced in a country in a year.

### Components of GDP
- **Consumption (C)**: What households buy (food, cars, haircuts).
- **Investment (I)**: What businesses spend (new factories, software, new houses).
- **Government Spending (G)**: Infrastructure, defense, public schools.
- **Net Exports (X - M)**: Exports minus Imports.

### Real vs. Nominal GDP
- **Nominal GDP**: Measured in current prices. It can rise just because prices rose (inflation).
- **Real GDP**: Adjusted for inflation. It measures the *actual volume* of production.

### Why Growth Matters
Economic growth (rising Real GDP) leads to higher living standards, better healthcare, and more opportunities.`,
      key_terms: {
        GDP: "Gross Domestic Product — total output of an economy",
        Consumption: "Household spending on goods and services",
        Investment: "Business spending on capital and inventories",
        "Real GDP": "GDP adjusted for inflation",
        "Nominal GDP": "GDP measured in current prices",
      },
    },
    Intermediate: {
      id: "gdp-int", topic: "GDP & Growth", level: "Intermediate",
      title: "Growth Models & Productivity",
      content: `### The Solow Growth Model
Growth comes from three sources:
1. **Capital Accumulation**: More machines and tools.
2. **Labor Force Growth**: More workers.
3. **Technological Progress**: Better ways of using capital and labor.

### Diminishing Returns
Adding more capital to the same number of workers leads to smaller and smaller increases in output. This is why rich countries grow slower than developing ones (Convergence).

### Total Factor Productivity (TFP)
TFP measures how efficiently an economy combines its inputs. It's often seen as the "secret sauce" of growth — innovation and efficiency.`,
      key_terms: {
        "Solow Model": "Framework for understanding long-run economic growth",
        "Diminishing Returns": "Decreasing incremental output from increasing one input",
        Convergence: "The theory that poorer economies grow faster than richer ones",
        TFP: "Total Factor Productivity — efficiency of production",
      },
    },
    Advanced: {
      id: "gdp-adv", topic: "GDP & Growth", level: "Advanced",
      title: "Endogenous Growth & Institutions",
      content: `### Endogenous Growth Theory
Unlike the Solow model, this theory suggests that growth is driven by internal factors like:
- **Human Capital**: Education and skills.
- **Innovation**: R&D and intellectual property.
- **Knowledge Spillovers**: One firm's innovation helps others.

### The Role of Institutions
Why are some countries rich and others poor? Daron Acemoglu argues it's about **Institutions**:
- **Inclusive Institutions**: Protect property rights, encourage investment, and allow creative destruction.
- **Extractive Institutions**: Designed to extract wealth from one subset of society to benefit a different subset.

### Creative Destruction (Schumpeter)
Growth requires the destruction of old, inefficient industries to make way for new, innovative ones.`,
      key_terms: {
        "Endogenous Growth": "Growth driven by internal innovation and human capital",
        "Human Capital": "The skills and knowledge of the workforce",
        Institutions: "The rules and norms that shape economic behavior",
        "Creative Destruction": "The process of industrial mutation that revolutionizes the economic structure",
      },
    },
  },
  "Monetary Policy": {
    Beginner: {
      id: "mp-beg", topic: "Monetary Policy", level: "Beginner",
      title: "The Role of Central Banks",
      content: `**Monetary Policy** is how a central bank (like the Fed) manages the money supply and interest rates to influence the economy.

### The Dual Mandate
The US Federal Reserve has two main goals:
1. **Price Stability**: Keeping inflation low and stable (target ~2%).
2. **Maximum Employment**: Keeping unemployment at its natural rate.

### Tools of the Fed
- **Interest Rates**: Raising rates slows the economy (fights inflation); lowering rates speeds it up (fights recession).
- **Open Market Operations**: Buying and selling government bonds to change the money supply.`,
      key_terms: {
        "Monetary Policy": "Management of money supply and interest rates",
        "Central Bank": "Institution that manages a country's currency and monetary policy",
        "Dual Mandate": "The Fed's goals of price stability and maximum employment",
        "Interest Rate": "The cost of borrowing money",
      },
    },
    Intermediate: { id: "mp-int", topic: "Monetary Policy", level: "Intermediate", title: "Coming Soon", content: "Intermediate content coming soon.", key_terms: {} },
    Advanced: { id: "mp-adv", topic: "Monetary Policy", level: "Advanced", title: "Coming Soon", content: "Advanced content coming soon.", key_terms: {} },
  },
  "Fiscal Policy": {
    Beginner: {
      id: "fp-beg", topic: "Fiscal Policy", level: "Beginner",
      title: "Government Spending & Taxes",
      content: `**Fiscal Policy** is how the government uses spending and taxes to influence the economy.

### Expansionary vs. Contractionary
- **Expansionary**: Increasing spending or cutting taxes to boost demand (used in recessions).
- **Contractionary**: Decreasing spending or raising taxes to slow demand (used to fight inflation).

### Deficits & Debt
- **Budget Deficit**: When the government spends more than it collects in taxes in a year.
- **National Debt**: The total amount of money the government owes.`,
      key_terms: {
        "Fiscal Policy": "Government use of spending and taxes",
        "Budget Deficit": "Annual shortfall in government revenue",
        "National Debt": "Accumulated government borrowing",
        "Expansionary Policy": "Policy designed to boost economic activity",
      },
    },
    Intermediate: { id: "fp-int", topic: "Fiscal Policy", level: "Intermediate", title: "Coming Soon", content: "Intermediate content coming soon.", key_terms: {} },
    Advanced: { id: "fp-adv", topic: "Fiscal Policy", level: "Advanced", title: "Coming Soon", content: "Advanced content coming soon.", key_terms: {} },
  },
  "Labor Markets": {
    Beginner: {
      id: "lm-beg", topic: "Labor Markets", level: "Beginner",
      title: "Jobs, Wages & Unemployment",
      content: `The **Labor Market** is where workers sell their time and skills, and employers buy them.

### Unemployment Types
- **Frictional**: People between jobs (searching for the right fit).
- **Structural**: Mismatch between worker skills and job requirements (e.g., automation).
- **Cyclical**: Caused by economic downturns (recessions).

### The Minimum Wage
A price floor on labor. It helps low-wage workers but can lead to fewer jobs if set too high.`,
      key_terms: {
        "Labor Market": "Market where labor is traded",
        Unemployment: "People willing and able to work but without a job",
        "Minimum Wage": "Lowest legal price for labor",
        "Human Capital": "Skills and education of workers",
      },
    },
    Intermediate: { id: "lm-int", topic: "Labor Markets", level: "Intermediate", title: "Coming Soon", content: "Intermediate content coming soon.", key_terms: {} },
    Advanced: { id: "lm-adv", topic: "Labor Markets", level: "Advanced", title: "Coming Soon", content: "Advanced content coming soon.", key_terms: {} },
  },
  "Trade & Globalization": {
    Beginner: {
      id: "tg-beg", topic: "Trade & Globalization", level: "Beginner",
      title: "Why Countries Trade",
      content: `**Globalization** is the increasing interconnectedness of countries through trade, investment, and technology.

### Comparative Advantage
Countries should produce what they are *relatively* best at and trade for the rest. This makes both countries better off.

### Barriers to Trade
- **Tariffs**: Taxes on imported goods.
- **Quotas**: Limits on the quantity of imports.
- **Protectionism**: Policies designed to protect domestic industries from foreign competition.`,
      key_terms: {
        Globalization: "Increasing global interconnectedness",
        "Comparative Advantage": "Ability to produce at a lower opportunity cost",
        Tariff: "Tax on imports",
        Protectionism: "Shielding domestic industries from foreign competition",
      },
    },
    Intermediate: { id: "tg-int", topic: "Trade & Globalization", level: "Intermediate", title: "Coming Soon", content: "Intermediate content coming soon.", key_terms: {} },
    Advanced: { id: "tg-adv", topic: "Trade & Globalization", level: "Advanced", title: "Coming Soon", content: "Advanced content coming soon.", key_terms: {} },
  },
  "Financial Markets": {
    Beginner: {
      id: "fm-beg", topic: "Financial Markets", level: "Beginner",
      title: "Stocks, Bonds & Banks",
      content: `**Financial Markets** channel funds from savers to borrowers.

### Key Instruments
- **Stocks**: Ownership in a company.
- **Bonds**: Loans to a company or government.
- **Banks**: Intermediaries that take deposits and give loans.

### Risk & Return
Generally, higher risk = higher potential return. Diversification (owning many different assets) helps manage risk.`,
      key_terms: {
        "Financial Market": "Market where financial assets are traded",
        Stock: "Share of ownership in a corporation",
        Bond: "Debt instrument issued by an entity",
        Risk: "Uncertainty about future returns",
      },
    },
    Intermediate: { id: "fm-int", topic: "Financial Markets", level: "Intermediate", title: "Coming Soon", content: "Intermediate content coming soon.", key_terms: {} },
    Advanced: { id: "fm-adv", topic: "Financial Markets", level: "Advanced", title: "Coming Soon", content: "Advanced content coming soon.", key_terms: {} },
  },
  "Business Cycles": {
    Beginner: {
      id: "bc-beg", topic: "Business Cycles", level: "Beginner",
      title: "Booms & Busts",
      content: `The **Business Cycle** is the natural rise and fall of economic activity over time.

### Phases
1. **Expansion**: GDP rising, unemployment falling.
2. **Peak**: The top of the cycle.
3. **Contraction (Recession)**: GDP falling, unemployment rising.
4. **Trough**: The bottom of the cycle.

### Indicators
- **Leading**: Predict future activity (stock market, building permits).
- **Lagging**: Confirm past activity (unemployment rate).`,
      key_terms: {
        "Business Cycle": "Fluctuations in economic activity",
        Recession: "Significant decline in economic activity",
        Expansion: "Period of economic growth",
        Peak: "Highest point of an expansion",
      },
    },
    Intermediate: { id: "bc-int", topic: "Business Cycles", level: "Intermediate", title: "Coming Soon", content: "Intermediate content coming soon.", key_terms: {} },
    Advanced: { id: "bc-adv", topic: "Business Cycles", level: "Advanced", title: "Coming Soon", content: "Advanced content coming soon.", key_terms: {} },
  },
  "Behavioral Economics": {
    Beginner: {
      id: "be-beg", topic: "Behavioral Economics", level: "Beginner",
      title: "How People Actually Decide",
      content: `**Behavioral Economics** combines psychology and economics to understand why people often make "irrational" choices.

### Key Biases
- **Loss Aversion**: We hate losing $10 more than we like winning $10.
- **Anchoring**: Relying too heavily on the first piece of information offered.
- **Nudge Theory**: Small changes in how choices are presented can influence behavior (e.g., making organ donation the default).`,
      key_terms: {
        "Behavioral Economics": "Study of psychological factors in economic decisions",
        "Loss Aversion": "Preference for avoiding losses over acquiring gains",
        Anchoring: "Cognitive bias toward initial information",
        Nudge: "Subtle policy shift to encourage better choices",
      },
    },
    Intermediate: { id: "be-int", topic: "Behavioral Economics", level: "Intermediate", title: "Coming Soon", content: "Intermediate content coming soon.", key_terms: {} },
    Advanced: { id: "be-adv", topic: "Behavioral Economics", level: "Advanced", title: "Coming Soon", content: "Advanced content coming soon.", key_terms: {} },
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
