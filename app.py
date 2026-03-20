import streamlit as st
import random
import hashlib
import sqlite3
import uuid
import json
import os
from datetime import date
from urllib.parse import urlencode

st.set_page_config(page_title="EconoLearn", page_icon="📈", layout="wide")

# ─────────────────────────────────────────────
# CONTENT DATABASE
# ─────────────────────────────────────────────

LEVELS = ["Beginner", "Intermediate", "Advanced"]

TOPICS = {
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
}

LESSONS = {
    "Supply & Demand": {
        "Beginner": {
            "title": "The Basics of Supply & Demand",
            "content": """
**Supply and demand** is the foundation of economics. It explains how prices are set and how resources are allocated.

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
After a hurricane destroys orange groves in Florida, **supply of oranges drops**. With the same demand but less supply, prices rise — this is why OJ gets expensive after storms.
            """,
            "key_terms": {"Demand": "Willingness and ability to buy at a given price", "Supply": "Willingness and ability to sell at a given price", "Equilibrium": "Price where quantity supplied equals quantity demanded", "Surplus": "When supply exceeds demand at a given price", "Shortage": "When demand exceeds supply at a given price"},
        },
        "Intermediate": {
            "title": "Elasticity & Market Shifts",
            "content": """
### Price Elasticity of Demand (PED)
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
- Total welfare = Consumer Surplus + Producer Surplus
            """,
            "key_terms": {"Elasticity": "Responsiveness of quantity to price changes", "Elastic": "PED > 1; consumers highly responsive to price", "Inelastic": "PED < 1; consumers not sensitive to price", "Consumer Surplus": "Benefit consumers gain above what they pay", "Producer Surplus": "Benefit producers gain above their minimum price"},
        },
        "Advanced": {
            "title": "Market Failures & Externalities",
            "content": """
### When Markets Fail
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
- **Prisoner's Dilemma**: Individually rational choices lead to collectively suboptimal outcomes — explains why OPEC cartels are unstable.
            """,
            "key_terms": {"Externality": "Cost/benefit falling on uninvolved third parties", "Pigouvian Tax": "Tax equal to external cost to correct market failure", "Adverse Selection": "Bad products/risks dominate due to information gaps", "Moral Hazard": "Risk-taking increases when insured against consequences", "Nash Equilibrium": "Stable outcome where no player benefits from changing strategy"},
        },
    },
    "Inflation & Deflation": {
        "Beginner": {
            "title": "What is Inflation?",
            "content": """
**Inflation** is the general rise in the price level over time. It means your money buys *less* than it used to.

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
Most central banks (like the US Fed) target **~2% annual inflation** — low enough to be stable, high enough to avoid deflation's trap.
            """,
            "key_terms": {"Inflation": "General rise in price levels over time", "CPI": "Consumer Price Index — measures household basket of goods", "Deflation": "General fall in price levels", "Hyperinflation": "Extremely rapid, out-of-control inflation", "Purchasing Power": "The real value of money in terms of goods it can buy"},
        },
        "Intermediate": {
            "title": "Inflation, Interest Rates & the Fisher Effect",
            "content": """
### Real vs. Nominal Interest Rates
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
**Expectations drive inflation** as much as actual money supply. If everyone *expects* 5% inflation, wages and prices adjust to that — it becomes self-fulfilling. Central banks spend enormous effort managing expectations (forward guidance).
            """,
            "key_terms": {"Fisher Equation": "Links nominal rates, real rates, and inflation", "Phillips Curve": "Short-run trade-off between inflation and unemployment", "NAIRU": "Natural rate of unemployment consistent with stable inflation", "Stagflation": "Simultaneous high inflation and high unemployment", "Forward Guidance": "Central bank communication about future policy to shape expectations"},
        },
        "Advanced": {
            "title": "Monetary Theory: QE, ZIRP & Modern Debates",
            "content": """
### Quantitative Easing (QE)
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
- This is why central banks *fear* deflation more than moderate inflation.
            """,
            "key_terms": {"QE": "Quantitative Easing — central bank asset purchases to inject liquidity", "ZIRP": "Zero Interest Rate Policy — rates at or near 0%", "MMT": "Modern Monetary Theory — sovereign currency issuers aren't revenue-constrained", "MV=PQ": "Quantity theory linking money supply to price level", "Debt-Deflation": "Falling prices raise real debt burden, triggering defaults and more deflation"},
        },
    },
    "GDP & Growth": {
        "Beginner": {
            "title": "What is GDP?",
            "content": """
**GDP (Gross Domestic Product)** is the total value of all goods and services produced in a country in a year. It's the primary measure of economic size and health.

### How GDP is Calculated
**Expenditure Approach** (most common):
> **GDP = C + I + G + (X − M)**
- **C** = Consumer spending (biggest piece, ~70% in the US)
- **I** = Business Investment (machines, buildings, inventory)
- **G** = Government spending (NOT transfers like welfare)
- **X − M** = Net Exports (exports minus imports)

### Real vs. Nominal GDP
- **Nominal GDP**: Measured in today's prices — inflated by price rises.
- **Real GDP**: Adjusted for inflation — shows *actual* output growth.
- If nominal GDP grew 6% but inflation was 4%, real GDP grew only 2%.

### GDP Per Capita
Total GDP divided by population. Better for comparing living standards across countries.
- China's total GDP is huge but per-capita GDP is much lower than Norway's.

### What GDP Misses
- Household work, volunteering
- Environmental degradation
- Income inequality (Gini coefficient is a separate measure)
- Happiness / well-being
            """,
            "key_terms": {"GDP": "Total value of goods/services produced in a country annually", "Real GDP": "GDP adjusted for inflation", "Nominal GDP": "GDP measured in current prices", "GDP Per Capita": "GDP divided by population", "C + I + G + (X-M)": "The expenditure formula for GDP"},
        },
        "Intermediate": {
            "title": "Economic Growth Theory",
            "content": """
### Sources of Long-Run Growth
1. **More inputs**: More workers, more capital.
2. **Better inputs**: Educated workers, advanced machines.
3. **Total Factor Productivity (TFP)**: Technology, institutions, ideas — the "residual."

### Solow Growth Model
- Countries accumulate capital until they reach a **steady state** — where investment = depreciation.
- Rich countries: capital is abundant, diminishing returns kick in → lower growth.
- Poor countries: capital is scarce, high returns → faster growth (catch-up effect / convergence).
- Long-run growth comes *only* from technological progress (exogenous in Solow).

### Endogenous Growth Theory (Romer)
Paul Romer (Nobel 2018): Ideas are non-rival and can be built upon. **Knowledge spillovers** mean returns to technology don't diminish. Innovation drives perpetual growth.
- Policy implication: invest in R&D, education, patents (but not too many!).

### Institutions Matter
**Acemoglu & Robinson** ("Why Nations Fail"):
- **Inclusive institutions** (property rights, rule of law, competitive markets) → growth.
- **Extractive institutions** (rent-seeking elites, arbitrary property seizure) → stagnation.
- Geography (Diamond) and culture (Weber) are secondary; *institutions* are the key variable.
            """,
            "key_terms": {"TFP": "Total Factor Productivity — efficiency gains beyond input increases", "Solow Model": "Growth framework with diminishing returns and a steady state", "Convergence": "Poor countries grow faster than rich ones, closing the gap", "Endogenous Growth": "Growth explained by internal factors like innovation and knowledge", "Inclusive Institutions": "Systems with property rights, rule of law that enable broad participation"},
        },
        "Advanced": {
            "title": "Business Cycles & Macro Stabilization",
            "content": """
### The Business Cycle
Output fluctuates around its long-run potential. Phases:
- **Expansion**: Output growing, unemployment falling.
- **Peak**: Maximum output, often with inflation pressures.
- **Contraction/Recession**: Output falling (2 consecutive quarters of negative GDP growth).
- **Trough**: Minimum output, maximum unemployment.

### Output Gap
**Output Gap = (Actual GDP − Potential GDP) / Potential GDP × 100**
- Positive gap (overheating) → inflationary pressure → Fed tightens.
- Negative gap (slack) → unemployment above natural rate → stimulus warranted.

### Okun's Law
**1% rise in unemployment ≈ 2% fall in GDP** (relative to potential). Captures the employment-output relationship.

### IS-LM-PC Model (Modern Version)
- **IS curve**: Goods market — lower interest rates → higher output.
- **LM → MP curve**: Monetary policy — central bank sets interest rate.
- **PC (Phillips Curve)**: Inflation-output trade-off.
- Together: a complete short-run macro model.

### Automatic Stabilizers vs. Discretionary Policy
- **Automatic**: Unemployment insurance, progressive taxes — automatically expand deficit in recessions.
- **Discretionary**: One-off stimulus packages (2009 ARRA, 2020 CARES Act).
- Lags make discretionary policy tricky: recognition lag + implementation lag + effect lag.
            """,
            "key_terms": {"Business Cycle": "Fluctuations in economic output around its long-run trend", "Output Gap": "Difference between actual and potential GDP", "Okun's Law": "1% unemployment rise ≈ 2% GDP loss vs. potential", "IS Curve": "Inverse relationship between interest rate and output in goods market", "Automatic Stabilizers": "Budget mechanisms that automatically smooth economic fluctuations"},
        },
    },
    "Monetary Policy": {
        "Beginner": {
            "title": "Central Banks & Interest Rates",
            "content": """
**Monetary policy** is how a central bank (like the US Federal Reserve) controls the money supply and interest rates to achieve economic goals.

### The Fed's Dual Mandate
1. **Maximum employment** (unemployment as low as possible without causing inflation)
2. **Stable prices** (~2% inflation target)

### The Key Tool: The Federal Funds Rate
The rate at which banks lend reserves to each other overnight.
- When the Fed **raises rates** → borrowing gets expensive → businesses invest less, consumers spend less → demand falls → inflation cools → but growth slows.
- When the Fed **cuts rates** → borrowing is cheap → spending and investment rise → economy heats up → but inflation can rise.

### How It Flows to You
Fed rate → bank rates → mortgage rates, car loan rates, credit card rates, savings account rates.

### Open Market Operations
The Fed's main tool is **buying or selling Treasury bonds**:
- Buying bonds: injects money into banks → rates fall.
- Selling bonds: removes money from banks → rates rise.

### The Fed's Independence
The Fed is politically independent — it doesn't answer to Congress or the President on day-to-day decisions. This is crucial to keep it from printing money for political gain.
            """,
            "key_terms": {"Federal Reserve": "US central bank responsible for monetary policy", "Federal Funds Rate": "Overnight lending rate between banks, set by the Fed", "Open Market Operations": "Fed buying/selling bonds to adjust money supply", "Dual Mandate": "The Fed's two goals: maximum employment and stable prices", "Monetary Policy": "Central bank management of money supply and interest rates"},
        },
        "Intermediate": {
            "title": "Transmission Mechanisms & Policy Rules",
            "content": """
### How Monetary Policy Transmits
1. **Interest rate channel**: Lower rates → cheaper credit → more investment/consumption.
2. **Asset price channel**: Lower rates → stocks/housing rise → wealth effect → more spending.
3. **Exchange rate channel**: Lower rates → currency depreciates → exports more competitive.
4. **Credit channel**: Easier lending standards → more borrowing available.
5. **Expectations channel**: Credible inflation targets anchor expectations.

### The Taylor Rule
A formula for the "right" interest rate:
> **Fed Rate = 2% + Inflation + 0.5(Inflation − 2%) + 0.5(Output Gap)**

- If inflation is above 2%, raise rates more aggressively.
- If unemployment is high (negative output gap), lower rates.
- Used as a benchmark to evaluate Fed decisions.

### Rules vs. Discretion
- **Rules** (like Taylor Rule): Predictable, builds credibility, reduces political influence.
- **Discretion**: Flexibility to respond to unusual events (2008 crisis, COVID).
- **Inflation targeting**: A middle ground — commit to a target, discretion on methods.

### Zero Lower Bound Problem
You can't cut rates below ~0% (people would just hold cash). This forces unconventional tools: QE, forward guidance, negative interest rate policy (NIRP).
            """,
            "key_terms": {"Taylor Rule": "Formula prescribing interest rates based on inflation and output gap", "Transmission Mechanism": "Channels through which monetary policy affects the economy", "ZLB": "Zero Lower Bound — rates can't go significantly below 0%", "Forward Guidance": "Central bank signals about future policy to shape expectations", "NIRP": "Negative Interest Rate Policy — charging banks to hold reserves"},
        },
        "Advanced": {
            "title": "Monetary Frameworks & Central Bank Theory",
            "content": """
### Inflation Targeting (IT)
Post-1990 consensus: Central banks should publicly commit to an inflation target.
- **New Zealand** was first (1989). Now ~40+ countries.
- Why it works: coordinates expectations → wage/price setters plan around the target → self-reinforcing stability.

### Average Inflation Targeting (AIT)
Fed's 2020 framework shift:
- Instead of hitting 2% always, target *average* 2% over time.
- After undershooting, *allow* inflation to overshoot temporarily.
- Rationale: flatten the Phillips Curve → need to run economy "hot" to push inflation up.

### The Trilemma (Impossible Trinity)
A country cannot simultaneously have all three:
1. **Fixed exchange rate**
2. **Free capital movement**
3. **Independent monetary policy**

Choose two. China: fixed rate + capital controls = monetary independence. Eurozone: fixed rates (single currency) + free capital = no national monetary policy.

### Seigniorage & Inflation Tax
- Government earns **seigniorage** — revenue from creating money.
- Inflation acts as a tax on money holders (erodes real value of cash holdings).
- Hyperinflation historically often results from governments over-using this tool (Weimar Germany, Venezuela).

### The Credibility Problem & Kydland-Prescott
- If the public believes the central bank will *always* accommodate inflation, they demand higher wages.
- Solution: **Time-consistent policy** — commit credibly in advance, even if it's costly to follow through.
- **Inflation hawk reputation** (like Volcker's 1979-82 rate hikes) establishes credibility by demonstrating willingness to accept recession to kill inflation.
            """,
            "key_terms": {"Inflation Targeting": "Explicit public commitment to a numerical inflation target", "AIT": "Average Inflation Targeting — allows temporary overshoots after undershooting", "Impossible Trinity": "Can't have fixed exchange rate, free capital, and monetary independence simultaneously", "Seigniorage": "Revenue a government earns from issuing currency", "Credibility": "Central bank's demonstrated commitment to its stated goals"},
        },
    },
    "Fiscal Policy": {
        "Beginner": {
            "title": "Government Spending & Taxes",
            "content": """
**Fiscal policy** is how governments use spending and taxation to influence the economy.

### Two Levers
1. **Government Spending (G)**: Roads, schools, military, healthcare, transfers (Social Security, welfare).
2. **Taxation**: Income tax, corporate tax, sales tax, property tax — removes money from the economy.

### Budget Positions
- **Surplus**: Tax revenue > Spending (government saves / pays down debt).
- **Deficit**: Spending > Tax revenue (government borrows).
- **Balanced budget**: Revenue = Spending.

### Expansionary vs. Contractionary
- **Expansionary fiscal policy**: Increase G or cut taxes → stimulates demand → fights recession.
- **Contractionary fiscal policy**: Cut G or raise taxes → reduces demand → fights inflation.

### The Multiplier Effect
Government spending has a multiplied effect on GDP. If the government spends $100B:
- Workers receive income → spend more of it
- Those businesses receive income → spend more
- So total GDP increases by *more* than $100B
- **Multiplier = 1 / (1 − MPC)**, where MPC = Marginal Propensity to Consume

### The National Debt
Total accumulated borrowing. The US national debt is ~$34 trillion (2024). **Debt-to-GDP ratio** is what matters, not the absolute number.
            """,
            "key_terms": {"Fiscal Policy": "Government use of spending and taxes to influence the economy", "Budget Deficit": "Government spending exceeds tax revenue in a given year", "Multiplier Effect": "Spending ripples through economy, amplifying total GDP impact", "MPC": "Marginal Propensity to Consume — fraction of extra income spent", "National Debt": "Total accumulated government borrowing over all years"},
        },
        "Intermediate": {
            "title": "Ricardian Equivalence, Debt & Crowding Out",
            "content": """
### Ricardian Equivalence (Barro)
Claim: Deficit spending doesn't stimulate the economy because rational consumers:
- Know the deficit means *future* tax increases.
- Save today to pay those future taxes.
- So fiscal stimulus is completely offset by private saving reduction.

**Reality**: Mostly rejected empirically. People are not fully rational, some are liquidity-constrained (can't borrow against future income), and Ricardian logic requires very strong assumptions.

### Crowding Out
Government borrowing competes with private borrowing:
- More deficit → more bond issuance → bond prices fall → interest rates rise.
- Higher interest rates → businesses borrow less → private investment falls.
- Government "crowds out" private investment.

**Counter-argument**: In a recession with slack resources and near-zero rates, crowding out is minimal.

### Debt Sustainability
**Primary deficit** = Deficit excluding interest payments.
Debt is sustainable if: **r < g** (interest rate on debt < economic growth rate)
- If growth > interest rate, the debt/GDP ratio naturally shrinks over time.
- Post-2008 low interest rates made debt more sustainable even at higher levels.
- **Blanchard (2019)**: Low r-g means debt costs less than historically assumed.

### Automatic vs. Discretionary Fiscal Policy
- **Automatic stabilizers**: Progressive taxes + unemployment insurance automatically cushion recessions.
- **Discretionary**: Congress must act (slow, politically contentious).
            """,
            "key_terms": {"Ricardian Equivalence": "Deficits don't stimulate because consumers save for future taxes", "Crowding Out": "Government borrowing raising interest rates, reducing private investment", "r < g": "Debt is sustainable if interest rate is below GDP growth rate", "Primary Deficit": "Budget deficit excluding interest payments on existing debt", "Automatic Stabilizers": "Tax/spending mechanisms that automatically smooth cycles"},
        },
        "Advanced": {
            "title": "Fiscal Multipliers, Austerity & Political Economy",
            "content": """
### The Size of the Multiplier
The multiplier is not constant — it depends on:
- **State of the economy**: Higher during recessions (idle resources) than booms.
- **Monetary policy**: If rates are at ZLB, monetary policy can't offset fiscal tightening → multiplier is larger.
- **Openness**: More open economies (more imports) have smaller multipliers (leakage abroad).
- **IMF 2012 bombshell**: Olivier Blanchard found multipliers were 3× larger than assumed → 2010-12 European austerity was far more damaging than projected.

### Expansionary Austerity Controversy
**Alesina & Ardagna (2010)**: Claimed fiscal consolidation (austerity) could be expansionary by boosting confidence and cutting rates.
- Used as justification for post-2010 European austerity.
- **Rebuttals**: IMF and others found most "expansionary" consolidations occurred during booms when conditions were already good.

### Helicopter Money
Milton Friedman's thought experiment: central bank credits money directly to citizens' accounts. Pure demand injection without debt creation.
- Different from QE (which just swaps assets with banks).

### Public Goods, Externalities & the Size of Government
**Market failures** justify government intervention:
- Pure public goods (defense, basic research): Non-rival, non-excludable → private market underprovides.
- Externalities → Pigouvian taxes/subsidies or regulation.
- Social insurance → redistribution and risk-pooling against catastrophic events.
            """,
            "key_terms": {"Fiscal Multiplier": "Ratio of change in GDP to change in government spending", "Expansionary Austerity": "Theory that deficit cuts can stimulate growth via confidence", "ZLB": "Zero Lower Bound — when rates can't fall further, fiscal multipliers rise", "Helicopter Money": "Direct cash injection from central bank to citizens", "Public Good": "Non-rival and non-excludable good — private market underprovides"},
        },
    },
    "Trade & Globalization": {
        "Beginner": {
            "title": "Why Countries Trade",
            "content": """
**International trade** allows countries to specialize in what they do best and trade for everything else — raising living standards for all.

### Comparative Advantage (Ricardo)
You don't need to be *absolutely* better at something to benefit from trade. You just need a **comparative advantage** — lower *opportunity cost*.

**Example**:
- Country A can produce 100 cars or 200 phones per hour.
- Country B can produce 20 cars or 80 phones per hour.
- Country A is better at both, but B has a comparative advantage in phones (opportunity cost is lower).
- If B specializes in phones and A in cars, *total* production rises — both can be better off through trade.

### Trade Barriers
- **Tariffs**: Tax on imports → raises price, protects domestic producers, harms consumers.
- **Quotas**: Limits on quantity of imports.
- **Subsidies**: Government support for domestic industries.

### Who Wins, Who Loses
Trade raises *total* welfare but creates winners and losers:
- Consumers win (cheaper goods).
- Import-competing workers lose jobs.
- Exporting industries win.
            """,
            "key_terms": {"Comparative Advantage": "Lower opportunity cost in producing a good relative to others", "Tariff": "Tax on imported goods", "Quota": "Limit on the quantity of imports allowed", "Trade Deficit": "Importing more than exporting in value terms", "Heckscher-Ohlin": "Theory that countries export goods using their abundant factors"},
        },
        "Intermediate": {
            "title": "Globalization, Exchange Rates & Trade Policy",
            "content": """
### Exchange Rates
The price of one currency in terms of another.
- **Appreciation**: Currency buys more foreign currency → exports more expensive, imports cheaper.
- **Depreciation**: Currency buys less → exports cheaper, imports more expensive.

**Purchasing Power Parity (PPP)**: In the long run, exchange rates adjust so the same basket of goods costs the same everywhere.

### The Trade Balance & Capital Flows
**Trade deficit = Capital account surplus** (an accounting identity).
- A country running a deficit must be receiving more foreign investment than it sends abroad.
- US trade deficits reflect the dollar's reserve currency status: the world wants dollar assets → must supply US with goods.

### The WTO & Trade Agreements
- **WTO**: Sets global trade rules, arbitrates disputes, promotes tariff reduction.
- **Most Favored Nation (MFN)**: WTO principle — treat all members equally.
- **Free Trade Agreements (FTAs)**: Preferential tariffs between specific countries (NAFTA/USMCA, EU).

### Infant Industry Argument
Developing countries may need temporary protection for new industries to build scale before competing with established foreign firms. Used by Japan, South Korea — controversial because protection often becomes permanent.
            """,
            "key_terms": {"Exchange Rate": "Price of one currency in terms of another", "PPP": "Purchasing Power Parity — equalizes purchasing power across currencies", "WTO": "World Trade Organization — sets global trade rules", "Infant Industry": "Young industries needing protection before competing globally", "China Shock": "Concentrated job losses from Chinese import competition"},
        },
        "Advanced": {
            "title": "Global Value Chains, Currency Wars & Deglobalization",
            "content": """
### Global Value Chains (GVCs)
Modern production is fragmented across countries:
- iPhone: designed in US, chips from Taiwan, assembled in China, sold globally.
- **Smiling curve**: Most value captured at design/brand ends; assembly has thin margins.

### Currency Manipulation
Countries sometimes deliberately **weaken** their currency to boost exports:
- Buy foreign currency → increase its demand → own currency depreciates.
- **Beggar-thy-neighbor**: If everyone depreciates, the benefit is canceled but disruption increases.

### The Triffin Dilemma
The global reserve currency (dollar) creates a contradiction:
- The world needs dollars → the US must run trade deficits to supply them.
- But large deficits undermine confidence in the dollar as a store of value.

### Deglobalization Trends
Post-2016: political backlash + COVID supply chain disruptions + geopolitics pushing toward **reshoring** and **friend-shoring**:
- US CHIPS Act, Inflation Reduction Act: massive industrial policy to bring back semiconductor and clean-energy manufacturing.

### Trade & Inequality
**Stolper-Samuelson theorem**: Free trade lowers returns to the scarce factor in each country.
- In rich countries (capital-abundant), trade hurts unskilled workers.
            """,
            "key_terms": {"GVCs": "Global Value Chains — production fragmented across multiple countries", "Triffin Dilemma": "Reserve currency must run deficits to supply world liquidity, undermining its value", "Reshoring": "Moving production back to the home country", "Stolper-Samuelson": "Trade reduces returns to the scarce factor of production", "Beggar-thy-Neighbor": "Policies that gain at others' expense (e.g., competitive devaluation)"},
        },
    },
    "Financial Markets": {
        "Beginner": {
            "title": "Stocks, Bonds & How Markets Work",
            "content": """
**Financial markets** allow buyers and sellers to trade financial assets — stocks, bonds, currencies, and more.

### Stocks (Equities)
- A **stock** is a fractional ownership stake in a company.
- If a company does well → stock price rises → shareholders gain.
- **Dividend**: Share of profits paid to shareholders.
- **P/E ratio**: Price-to-Earnings — how much you pay per dollar of earnings. High P/E = high growth expectations.

### Bonds (Fixed Income)
- A **bond** is a loan to a company or government. You receive regular interest (coupon) and principal back at maturity.
- **Bond price and yield move inversely**: If rates rise, existing bonds become less valuable → price falls, yield rises.
- **US Treasury bonds**: Considered risk-free.

### Risk & Return
- Higher risk = higher expected return (risk premium).
- **Diversification**: Spreading investments reduces risk without reducing expected return.
- **Beta**: Measures how much a stock moves with the market.

### The Stock Market ≠ The Economy
- Stock markets anticipate future earnings — they're forward-looking.
- The economy can shrink while stocks rise (if rates fall or future outlook improves).
            """,
            "key_terms": {"Stock": "Ownership share in a company", "Bond": "Loan to a government or company that pays interest", "Dividend": "Regular cash payment to shareholders from company profits", "P/E Ratio": "Price divided by earnings per share — valuation metric", "Yield": "Return on a bond, moves inversely with its price"},
        },
        "Intermediate": {
            "title": "Asset Pricing, Bubbles & Market Efficiency",
            "content": """
### Efficient Market Hypothesis (EMH)
Eugene Fama: All available information is already reflected in asset prices.
- **Weak form**: Past prices can't predict future prices.
- **Semi-strong**: All public information is priced in.
- **Strong form**: Even private information is priced in.

**Implication**: You can't consistently beat the market → index funds are optimal.

**Behavioral critique** (Shiller): Markets show excess volatility, predictable anomalies, and bubbles that EMH can't fully explain.

### The CAPM
Expected return = Risk-free rate + Beta × (Market return − Risk-free rate)
- Only **systematic risk** (non-diversifiable) is rewarded.
- **Idiosyncratic risk** can be diversified away for free.

### Financial Bubbles — Minsky's Framework
1. Displacement (new technology, asset, opportunity)
2. Credit expansion fuels speculation
3. Euphoria — overvaluation, "this time is different"
4. Insider selling
5. Panic and crash

Examples: Tulip mania (1637), Dot-com (2000), Housing (2008).

### Yield Curve
Plots bond yields across maturities. Normally upward sloping.
- **Inverted yield curve**: Short-term yields > long-term yields → signals recession (has predicted every US recession since 1950s).
            """,
            "key_terms": {"EMH": "Efficient Market Hypothesis — prices reflect all available information", "CAPM": "Capital Asset Pricing Model — links expected return to systematic risk (beta)", "Beta": "Sensitivity of a stock's returns to market-wide returns", "Minsky Moment": "Sudden market collapse after speculative excess", "Yield Curve": "Plot of bond yields across different maturities"},
        },
        "Advanced": {
            "title": "Financial Crises, Systemic Risk & Regulation",
            "content": """
### The 2008 Financial Crisis — Anatomy
1. **Housing bubble**: Low rates + lax lending → subprime mortgages to unqualified buyers.
2. **Securitization**: Banks bundled mortgages into MBS and CDOs.
3. **Credit ratings**: Rating agencies gave AAA to toxic instruments.
4. **Leverage**: Banks held thin capital against massive liabilities.
5. **Shadow banking**: Repo markets, money market funds — unregulated bank-like entities.
6. **Trigger**: House prices fall → MBS collapse → interbank lending freezes → Lehman fails.

### Systemic Risk & "Too Big to Fail"
- **Systemic risk**: Risk that failure of one institution cascades through the whole system.
- **Moral hazard of bailouts**: If you're big enough, the government will rescue you → take more risk.
- **Dodd-Frank (2010)**: Stronger capital requirements, stress tests, resolution mechanisms.

### The Leverage Cycle (Geanakoplos)
- In booms: collateral valued highly → more credit → leverage rises.
- In busts: collateral falls → margin calls → forced selling → prices fall further.

### Shadow Banking
The 2008 crisis was largely a **run on the shadow banking system** (repo markets, money market funds).
- Shadow banks perform maturity transformation without deposit insurance.
- 2020: Fed's rapid intervention prevented a repeat.
            """,
            "key_terms": {"MBS": "Mortgage-Backed Security — bonds backed by mortgage payments", "Systemic Risk": "Risk of cascading failures across the financial system", "Too Big to Fail": "Implicit government guarantee for large financial institutions", "Leverage Cycle": "Amplification of booms/busts through rising/falling collateral values", "Shadow Banking": "Bank-like financial intermediaries without bank regulation or deposit insurance"},
        },
    },
}

ECONOMIC_HISTORY = [
    {"year": "1776", "event": "The Wealth of Nations", "description": "Adam Smith publishes *The Wealth of Nations*, founding modern economics. Key ideas: division of labor, the 'invisible hand' of markets, free trade over mercantilism.", "lesson": "Markets can coordinate complex activity without central direction through price signals.", "era": "Classical Economics"},
    {"year": "1848", "event": "The Communist Manifesto", "description": "Marx & Engels argue capitalism creates class conflict. Capital accumulation leads to immiseration of the proletariat.", "lesson": "Capitalism generates distributional conflicts — labor conditions and inequality became central economic questions.", "era": "Political Economy"},
    {"year": "1890", "event": "Marshall's Principles of Economics", "description": "Alfred Marshall develops supply and demand curves, consumer surplus, and elasticity — establishing the neoclassical framework.", "lesson": "Marginal analysis (thinking at the margin) is the key to understanding economic decisions.", "era": "Neoclassical Economics"},
    {"year": "1914–1918", "event": "World War I & War Economies", "description": "Governments mobilize economies for total war. Gold standard suspended. Post-war reparations (Versailles Treaty) set stage for instability.", "lesson": "Keynes warned in *The Economic Consequences of the Peace* (1919) that punitive reparations would destabilize Germany — a prediction that proved tragically correct.", "era": "War & Interwar"},
    {"year": "1929", "event": "The Great Crash & Great Depression", "description": "Stock market crashes in October 1929. By 1933, US unemployment hits 25%. GDP falls ~30%. The Smoot-Hawley Tariff Act worsens global depression through trade wars.", "lesson": "Bank panics and monetary contraction can turn recessions into depressions. Milton Friedman blamed the Fed for letting the money supply collapse by 1/3.", "era": "Great Depression"},
    {"year": "1936", "event": "Keynes: The General Theory", "description": "John Maynard Keynes publishes *The General Theory of Employment, Interest and Money* — arguing markets don't automatically clear and government spending can stimulate demand.", "lesson": "During depressions, aggregate demand fails. Government must step in. 'In the long run we are all dead' — waiting for market self-correction is not always viable.", "era": "Keynesian Revolution"},
    {"year": "1944", "event": "Bretton Woods Conference", "description": "44 Allied nations design the post-war international monetary system: fixed exchange rates tied to the US dollar, tied to gold ($35/oz). IMF and World Bank created.", "lesson": "International cooperation can build stable monetary frameworks. But the Triffin Dilemma eventually doomed Bretton Woods.", "era": "Post-War Order"},
    {"year": "1971", "event": "Nixon Closes the Gold Window", "description": "Nixon unilaterally ends dollar-gold convertibility — ending Bretton Woods. The world moves to floating exchange rates. The 'Nixon Shock' fundamentally changes international finance.", "lesson": "The Triffin Dilemma proved irresolvable. Floating rates give nations more monetary policy autonomy but introduce currency volatility.", "era": "Post-Bretton Woods"},
    {"year": "1973–1974", "event": "Oil Crisis & Stagflation", "description": "OPEC oil embargo quadruples oil prices. Western economies hit by inflation AND recession simultaneously — stagflation — which simple Keynesian models couldn't explain.", "lesson": "Supply shocks can cause both inflation and unemployment at once, breaking the simple Phillips Curve trade-off.", "era": "Stagflation Era"},
    {"year": "1979–1982", "event": "Volcker's War on Inflation", "description": "Fed Chair Paul Volcker raises the federal funds rate to ~20% to crush 13% inflation. The 'Volcker Shock' causes a severe recession but breaks the inflationary spiral.", "lesson": "Inflation can be beaten with credible, sustained tight monetary policy — but at enormous short-run cost. Established the importance of central bank credibility.", "era": "Monetarist Revolution"},
    {"year": "1980s", "event": "Reagan & Thatcher: Supply-Side Revolution", "description": "Reagan (US) and Thatcher (UK) implement tax cuts, deregulation, and union-busting. Deficits rise sharply in the US.", "lesson": "Tax cuts can stimulate growth, but 'trickle-down' effects on inequality are weak. The debate between supply-side and demand-side economics continues.", "era": "Neoliberal Era"},
    {"year": "1989–1991", "event": "Fall of the Berlin Wall & Soviet Collapse", "description": "Communist bloc collapses. 'Shock therapy' transitions in Eastern Europe. Washington Consensus spreads globally: free markets, fiscal discipline, openness.", "lesson": "Rapid vs. gradual transition matters enormously. Russia's shock therapy led to oligarchic capture. China's gradual approach preserved institutional capacity.", "era": "Post-Cold War"},
    {"year": "1997–1998", "event": "Asian Financial Crisis", "description": "Fixed exchange rates, large capital inflows, and current account deficits leave Asian economies vulnerable. Speculative attacks crash currencies. IMF bailouts with harsh austerity conditions.", "lesson": "Capital account liberalization without strong financial regulation creates crisis vulnerability. Fixed exchange rates can collapse under speculative attack.", "era": "Emerging Market Crises"},
    {"year": "2001", "event": "Dot-com Bust", "description": "Internet stock bubble collapses. NASDAQ falls 78% from peak. Trillions in paper wealth evaporate. The Fed responds by cutting rates aggressively.", "lesson": "'This time is different' is the most expensive phrase in finance. Technological innovation doesn't override the need for profits eventually.", "era": "Dot-Com Era"},
    {"year": "2008", "event": "Global Financial Crisis", "description": "US housing bubble collapses. Lehman Brothers fails (Sept 15, 2008). Global financial system freezes. The Fed, Treasury, and Congress conduct massive bailouts (TARP). Great Recession: deepest since 1930s.", "lesson": "Financial innovation (securitization, CDOs) can obscure risk and create systemic fragility. Regulation lags innovation dangerously.", "era": "Global Financial Crisis"},
    {"year": "2010–2012", "event": "Eurozone Debt Crisis", "description": "Greece, Ireland, Portugal, Spain, and Italy face sovereign debt crises. ECB (Mario Draghi): 'whatever it takes' to preserve the euro. Austerity programs cause deep recessions.", "lesson": "Monetary union without fiscal union creates asymmetric shocks with no adjustment mechanism. The euro's design had fundamental flaws that nearly destroyed it.", "era": "Eurozone Crisis"},
    {"year": "2020", "event": "COVID-19 Pandemic Shock", "description": "Largest peacetime economic shock in a century. GDP falls sharply but recovers rapidly due to unprecedented fiscal and monetary response. Supply chain disruptions cause inflation spike in 2021-22.", "lesson": "Fast, large-scale government intervention can prevent depression. But the inflation consequence of massive stimulus + supply shocks was underestimated.", "era": "COVID Era"},
    {"year": "2022–2023", "event": "Post-COVID Inflation Surge", "description": "CPI hits 9.1% in June 2022 (US) — highest in 40 years. Fed hikes rates from 0.25% to 5.5% in 16 months, the fastest tightening in modern history. Economy achieves 'soft landing' by late 2023.", "lesson": "Persistently easy monetary policy + fiscal stimulus + supply constraints can produce inflation even in developed economies. Inflation once unanchored is costly to control.", "era": "Post-COVID Era"},
]

QUIZ_QUESTIONS = {
    "Beginner": [
        {"q": "What happens to the price of a good when supply decreases and demand stays the same?", "options": ["A) Price falls", "B) Price rises", "C) Price stays the same", "D) Quantity demanded falls to zero"], "answer": "B", "explanation": "With the same demand but less supply, the equilibrium price rises — there are fewer goods competing for the same buyers."},
        {"q": "Which formula correctly represents GDP using the expenditure approach?", "options": ["A) GDP = C + I + G + T", "B) GDP = C + I + G + (X - M)", "C) GDP = C + S + G + X", "D) GDP = C + I - G + (X - M)"], "answer": "B", "explanation": "GDP = Consumer spending + Investment + Government spending + Net Exports (Exports minus Imports)."},
        {"q": "Inflation of 4% and a nominal interest rate of 6% gives you a real interest rate of approximately:", "options": ["A) 10%", "B) 4%", "C) 2%", "D) -2%"], "answer": "C", "explanation": "Real rate ≈ Nominal rate − Inflation rate = 6% − 4% = 2%."},
        {"q": "The Federal Reserve's 'dual mandate' refers to its goals of:", "options": ["A) Low inflation and a strong dollar", "B) Maximum employment and stable prices", "C) Low deficits and high growth", "D) Trade balance and currency stability"], "answer": "B", "explanation": "The Fed is legally mandated to pursue both maximum employment and price stability (around 2% inflation)."},
        {"q": "When a government spends more than it collects in taxes, this is called a:", "options": ["A) Trade deficit", "B) Current account surplus", "C) Budget deficit", "D) Primary surplus"], "answer": "C", "explanation": "A budget deficit occurs when government spending exceeds tax revenue in a given period."},
        {"q": "What is 'comparative advantage'?", "options": ["A) Producing more of everything than other countries", "B) Lower opportunity cost in producing a good relative to others", "C) Having more natural resources than trade partners", "D) A country's technological superiority"], "answer": "B", "explanation": "Comparative advantage is about opportunity costs, not absolute productivity. Even if one country is better at everything, trade can still benefit both sides."},
        {"q": "The law of demand states that:", "options": ["A) As income rises, demand rises", "B) As price rises, quantity demanded falls", "C) As supply rises, demand falls", "D) As price falls, supply falls"], "answer": "B", "explanation": "The law of demand describes an inverse relationship between price and quantity demanded, all else equal."},
        {"q": "Which of these best describes 'GDP per capita'?", "options": ["A) Total value of exports per year", "B) Average income of government workers", "C) Total GDP divided by the population", "D) GDP adjusted for inflation"], "answer": "C", "explanation": "GDP per capita = Total GDP / Population. It's a better measure of average living standards than total GDP."},
    ],
    "Intermediate": [
        {"q": "If a good has a price elasticity of demand of -2.5, it is considered:", "options": ["A) Inelastic", "B) Unit elastic", "C) Elastic", "D) Perfectly inelastic"], "answer": "C", "explanation": "When |PED| > 1, demand is elastic — consumers are very responsive to price changes."},
        {"q": "The Solow Growth Model predicts that poor countries will grow faster than rich ones due to:", "options": ["A) Higher population growth", "B) More democracy", "C) Diminishing returns to capital (convergence)", "D) Better monetary policy"], "answer": "C", "explanation": "Poor countries have less capital, so the marginal return to each unit of capital is higher — they grow faster until reaching steady state."},
        {"q": "The Taylor Rule primarily determines:", "options": ["A) The optimal fiscal deficit", "B) The target interest rate for central banks", "C) The exchange rate policy", "D) The optimal tariff rate"], "answer": "B", "explanation": "The Taylor Rule is a formula prescribing the appropriate interest rate based on inflation and the output gap."},
        {"q": "Ricardian Equivalence predicts that tax cuts will:", "options": ["A) Always stimulate GDP significantly", "B) Be offset by increased private saving for future taxes", "C) Reduce interest rates immediately", "D) Increase the money supply"], "answer": "B", "explanation": "Robert Barro's Ricardian Equivalence: rational consumers save the tax cut to pay future taxes, offsetting the stimulus."},
        {"q": "What does an inverted yield curve typically signal?", "options": ["A) High current inflation", "B) Strong economic growth ahead", "C) An upcoming recession", "D) Currency depreciation"], "answer": "C", "explanation": "An inverted yield curve (short-term rates > long-term rates) has preceded every US recession since the 1950s."},
        {"q": "The 'impossible trinity' states a country cannot simultaneously have:", "options": ["A) Low inflation, full employment, and trade balance", "B) Fixed exchange rate, free capital movement, and independent monetary policy", "C) High growth, low debt, and trade surplus", "D) Free trade, welfare state, and low taxes"], "answer": "B", "explanation": "A country must choose two of the three: fixed exchange rate, free capital flows, and monetary policy autonomy."},
        {"q": "A negative externality causes the market to:", "options": ["A) Underproduce the good", "B) Overproduce the good relative to the social optimum", "C) Produce exactly the right amount", "D) Always require government subsidies"], "answer": "B", "explanation": "With a negative externality, the social cost exceeds the private cost, so the market ignores external costs and overproduces."},
        {"q": "According to the Efficient Market Hypothesis (semi-strong form), which CAN earn above-market returns?", "options": ["A) Fundamental analysis (studying company financials)", "B) Technical analysis (studying past price patterns)", "C) Insider trading using private information", "D) None — the market is always efficient"], "answer": "C", "explanation": "Semi-strong EMH says all *public* information is priced in. Only truly private information (insider trading) could theoretically beat the market."},
    ],
    "Advanced": [
        {"q": "In the IS-LM model at the Zero Lower Bound, a fiscal expansion will:", "options": ["A) Be completely crowded out by rising interest rates", "B) Have a smaller multiplier than during normal times", "C) Have a larger multiplier because monetary policy cannot offset it", "D) Have no effect due to Ricardian Equivalence"], "answer": "C", "explanation": "At the ZLB, monetary policy cannot tighten to offset fiscal expansion, so the full multiplier applies without crowding out via interest rates."},
        {"q": "The Kydland-Prescott time inconsistency problem arises because:", "options": ["A) Tax policy takes time to implement", "B) Governments promise low inflation but have incentives to inflate once expectations are set", "C) Central banks respond too slowly to economic shocks", "D) Bond markets cannot predict future policy"], "answer": "B", "explanation": "Once the private sector sets wages based on expected low inflation, the government has an incentive to inflate and boost employment — but rational agents anticipate this."},
        {"q": "In Minsky's financial instability hypothesis, a 'Minsky moment' occurs when:", "options": ["A) Interest rates hit the zero lower bound", "B) Speculative and Ponzi borrowers are forced to sell assets to service debts, causing a crash", "C) The central bank unexpectedly raises rates", "D) Government debt reaches 100% of GDP"], "answer": "B", "explanation": "Minsky describes how speculative borrowing grows in booms until cash flows can't cover debt — then forced selling triggers a collapse."},
        {"q": "The Triffin Dilemma describes the contradiction that:", "options": ["A) Trade deficits require capital surpluses", "B) The reserve currency country must run deficits to supply liquidity, undermining confidence in the currency", "C) Fixed exchange rates cannot coexist with free capital flows", "D) Fiscal and monetary policy cannot simultaneously be expansionary"], "answer": "B", "explanation": "Robert Triffin noted the US had to run deficits to supply global dollar liquidity, but deficits would eventually erode confidence in the dollar's gold backing."},
        {"q": "According to Acemoglu & Robinson, the PRIMARY determinant of long-run economic development is:", "options": ["A) Geographic location and climate", "B) Cultural and religious values", "C) Political and economic institutions (inclusive vs. extractive)", "D) Natural resource endowments"], "answer": "C", "explanation": "In *Why Nations Fail*, Acemoglu & Robinson argue inclusive institutions (property rights, rule of law, competitive politics) drive growth; geography and culture are secondary."},
        {"q": "The Stolper-Samuelson theorem implies that free trade in developed (capital-abundant) countries will:", "options": ["A) Increase wages of all workers", "B) Reduce returns to unskilled labor (the scarce factor)", "C) Increase returns to both capital and labor", "D) Have no distributional effects"], "answer": "B", "explanation": "Stolper-Samuelson: trade raises returns to the abundant factor (capital in rich countries) and lowers returns to the scarce factor (unskilled labor)."},
        {"q": "Quantitative Easing (QE) differs from traditional monetary policy primarily because it:", "options": ["A) Changes the federal funds rate", "B) Directly purchases long-term assets to reduce long-term yields when short-term rates are at zero", "C) Is conducted by the Treasury, not the central bank", "D) Directly transfers money to households"], "answer": "B", "explanation": "QE bypasses the short-term rate (already at ZLB) and targets long-term rates directly through large-scale asset purchases."},
        {"q": "MV = PQ (Quantity Theory of Money) suggests that if money velocity (V) collapses after a financial crisis:", "options": ["A) Money supply expansion will reliably cause inflation", "B) Fiscal policy becomes more effective than monetary policy", "C) Money supply expansion may not cause proportional inflation", "D) Interest rates must rise to restore velocity"], "answer": "C", "explanation": "Post-2008: the Fed tripled the monetary base but inflation stayed low because V collapsed (banks hoarded reserves). M×V = P×Q, so falling V offset rising M."},
    ],
}

SCENARIO_EXERCISES = {
    "Beginner": [
        {"scenario": "🌽 The Corn Crisis", "situation": "A drought destroys 40% of the US corn crop. Corn is used in food, animal feed, and ethanol fuel.", "question": "What do you predict will happen to: (1) the price of corn, (2) the price of beef, and (3) the price of gasoline?", "answer": "1. Corn price RISES (supply decreased, demand unchanged → shortage → higher price). 2. Beef price RISES (corn = cow feed → input cost rises → supply of beef shifts left → price rises). 3. Gasoline price RISES (ethanol is a substitute/blend for gasoline; if corn is scarce, ethanol is scarce, and gasoline demand rises). This is called a 'supply chain ripple effect.'", "key_concept": "Supply shocks ripple through interconnected markets via input costs and substitutes."},
        {"scenario": "🏠 The Housing Boom", "situation": "The government launches a program giving first-time homebuyers a $20,000 subsidy. At the same time, construction costs rise due to a lumber shortage.", "question": "What happens to house prices? Who wins and who loses from this policy?", "answer": "Demand RISES (subsidy makes buying more attractive → demand curve shifts right). Supply contracts (higher lumber costs shift supply left). Result: prices RISE significantly. Winners: Existing homeowners, real estate agents, sellers. Losers: Non-first-time buyers (prices rose and they get no subsidy), renters (housing becomes less affordable), taxpayers. The policy may help first-time buyers less than intended because prices adjust up.", "key_concept": "Subsidies that boost demand often get partially captured as higher prices, especially if supply is constrained."},
    ],
    "Intermediate": [
        {"scenario": "🏦 The Fed's Dilemma", "situation": "It's 2022. Inflation is running at 8% (well above the 2% target). Unemployment is at 3.5% (below the natural rate). But housing prices are already falling and the stock market is down 25%.", "question": "Should the Fed raise interest rates aggressively, raise them slowly, or hold rates steady? Walk through the trade-offs using the Taylor Rule framework.", "answer": "Taylor Rule says: with inflation 6 points above target and a positive output gap, rates should be raised substantially — perhaps to 4-5% or higher. Aggressive raises: faster reduction in inflation, at the cost of higher unemployment and risk of recession. Slower raises: less economic disruption, but risk of inflation becoming entrenched in expectations. The Fed chose aggressive (from 0.25% to 5.5% in 16 months). Outcome: inflation fell substantially, no severe recession (a 'soft landing') — but housing market froze.", "key_concept": "The Taylor Rule provides a systematic framework for rate decisions, but the severity of off-target conditions and lag effects require judgment."},
        {"scenario": "📉 The Asian Tiger's Trap", "situation": "Thailand (1997) had: fixed exchange rate pegged to the dollar, large current account deficit, and booming capital inflows. Speculators began to doubt the peg could be maintained.", "question": "Explain why the fixed peg made Thailand vulnerable and what happened when speculators attacked it. Use the Impossible Trinity to frame your answer.", "answer": "The Impossible Trinity: Thailand had chosen a fixed exchange rate + free capital flows. To maintain the peg, they had to sacrifice monetary independence — using reserves to buy baht when attacked. When speculators shorted the baht, the Bank of Thailand burned through its dollar reserves. Eventually reserves ran out → they had to float → baht collapsed 40%+ → all corporations with dollar-denominated debt became instantly insolvent → banking crisis → IMF bailout with harsh conditions.", "key_concept": "The Impossible Trinity is not just theoretical — capital mobility makes fixed exchange rates extremely fragile under speculative attacks."},
    ],
    "Advanced": [
        {"scenario": "🌍 The Sovereign Debt Spiral", "situation": "A country has 120% debt-to-GDP. The real interest rate on its debt is 4%. Real GDP growth is 1%. The government must choose: (A) Austerity, (B) Default / restructuring, or (C) Monetization.", "question": "Evaluate each option using the debt sustainability condition (r vs. g) and the political-economic constraints of each choice.", "answer": "r(4%) > g(1%): debt is on an unsustainable path. Option A (Austerity): primary surplus can stop the spiral IF large enough. But Blanchard 2012 showed multipliers are high in crisis → austerity cuts GDP → debt ratio may WORSEN. Option B (Default): Stops the debt service math immediately but devastating to credibility — cut off from capital markets for years. Works best if debt is largely external. Option C (Monetization): Only works if country issues debt in its OWN currency. Risk: hyperinflation if overused. Summary: The optimal path is often a combination: moderate fiscal adjustment + debt restructuring + growth-enhancing structural reforms.", "key_concept": "Debt sustainability requires r < g; the policy response involves severe trade-offs between creditor losses, output losses, and inflation risk."},
        {"scenario": "🏭 Industrial Policy Bet", "situation": "The US CHIPS Act (2022) commits $52B to semiconductor manufacturing subsidies. Critics say this is inefficient industrial policy; supporters say it's necessary for national security and supply chain resilience.", "question": "Evaluate the economic case for and against this policy using market failure theory, comparative advantage, and infant industry arguments.", "answer": "FOR: 1. National security externality: semiconductors are critical for defense — a market failure justifies subsidy. 2. Supply chain externality: the 2020-21 chip shortage disrupted the entire US economy — a systemic risk the market underpriced. 3. Infant industry: US fabs need to rebuild scale. 4. Geopolitical insurance: overconcentration in Taiwan creates tail risk. AGAINST: 1. Comparative advantage: TSMC in Taiwan produces chips far more efficiently — subsidizing US fabs destroys value. 2. Government failure risk: picking winners historically fails (Solyndra). 3. Escalation risk: invites WTO challenges and foreign retaliation.", "key_concept": "Market failure arguments can justify industrial policy, but the quality of government intervention matters as much as whether intervention is warranted in principle."},
    ],
}

FILL_IN_BLANKS = [
    {"sentence": "GDP = ___ + Investment + Government Spending + Net Exports", "answer": "Consumer Spending (C)", "hint": "The biggest component, ~70% of US GDP", "level": "Beginner"},
    {"sentence": "When price rises, quantity demanded falls — this is the Law of ___.", "answer": "Demand", "hint": "The fundamental inverse relationship between price and quantity bought", "level": "Beginner"},
    {"sentence": "The ___ is the central bank of the United States.", "answer": "Federal Reserve (the Fed)", "hint": "Created in 1913, it sets US monetary policy", "level": "Beginner"},
    {"sentence": "Inflation rate minus the nominal interest rate gives the ___ interest rate.", "answer": "Real", "hint": "Adjusted for purchasing power loss", "level": "Beginner"},
    {"sentence": "The ___ Curve shows the short-run trade-off between inflation and unemployment.", "answer": "Phillips", "hint": "Named after New Zealand economist A.W. Phillips", "level": "Intermediate"},
    {"sentence": "MV = PQ is the ___ of Money, where V is the velocity of money.", "answer": "Quantity Theory", "hint": "Links money supply to price level", "level": "Intermediate"},
    {"sentence": "A country cannot simultaneously maintain a fixed exchange rate, free capital flows, and independent monetary policy — this is the ___.", "answer": "Impossible Trinity (Mundell-Fleming Trilemma)", "hint": "Choose any two of three", "level": "Intermediate"},
    {"sentence": "The ___ theorem states that if property rights are well-defined, private negotiation can solve externality problems.", "answer": "Coase", "hint": "Ronald ___ won the Nobel Prize in 1991", "level": "Intermediate"},
    {"sentence": "According to the Efficient Market Hypothesis, ___ form states even inside information is priced in.", "answer": "Strong", "hint": "The most extreme version of the EMH", "level": "Advanced"},
    {"sentence": "The debt sustainability condition requires that the real interest rate (r) be ___ than the real GDP growth rate (g).", "answer": "Less (r < g)", "hint": "If this isn't satisfied, the debt/GDP ratio grows without bound", "level": "Advanced"},
    {"sentence": "Kydland and Prescott argued central banks face a ___ problem — the optimal policy announced in advance may not be optimal to carry out later.", "answer": "Time inconsistency", "hint": "This is why central bank credibility and commitment matter so much", "level": "Advanced"},
    {"sentence": "___ is the revenue a government earns from creating new money — effectively a tax on money holders.", "answer": "Seigniorage", "hint": "Excessive use of this leads to hyperinflation", "level": "Advanced"},
]

CONCEPT_CONNECTIONS = [
    {"title": "Connect: Inflation → Interest Rates → GDP", "concepts": ["Inflation rises", "Fed raises rates", "Borrowing costs up", "Investment falls", "GDP growth slows", "Unemployment rises", "Wage growth slows", "Inflation falls"], "description": "Trace how an inflation spike triggers a chain of cause and effect through the economy.", "level": "Beginner"},
    {"title": "Connect: Asset Bubble Formation", "concepts": ["Low interest rates", "Cheap credit", "Asset price rises", "Collateral value rises", "More borrowing", "More asset buying", "Prices rise further", "MINSKY MOMENT: debt can't be serviced", "Forced selling", "Prices crash", "Credit tightens"], "description": "Hyman Minsky's financial instability hypothesis — trace how booms sow the seeds of busts.", "level": "Intermediate"},
    {"title": "Connect: Trade Deficit Mechanics", "concepts": ["US consumers prefer imports", "Imports > Exports", "Trade deficit", "Dollars flow abroad", "Foreigners invest dollars in US assets", "Capital account surplus", "Foreign demand for US bonds", "Interest rates stay low", "More consumption, less saving"], "description": "The balance of payments accounting identity: trade deficit = capital account surplus.", "level": "Advanced"},
]

# ─────────────────────────────────────────────
# DATABASE & AUTH
# ─────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "econolearn.db")

def db_init():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        name TEXT,
        password_hash TEXT,
        google_id TEXT,
        apple_id TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS progress (
        user_id TEXT PRIMARY KEY,
        xp INTEGER DEFAULT 0,
        level TEXT DEFAULT 'Beginner',
        topic TEXT DEFAULT 'Supply & Demand',
        total_answered INTEGER DEFAULT 0,
        correct_answered INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        last_active TEXT,
        daily_done TEXT DEFAULT '[]',
        quiz_answered TEXT DEFAULT '{}',
        badges TEXT DEFAULT '[]',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")
    conn.commit()
    conn.close()

db_init()

def _db_row_to_user(row):
    if not row: return None
    return {"id": row[0], "email": row[1], "name": row[2],
            "password_hash": row[3], "google_id": row[4], "apple_id": row[5]}

def db_get_user_by_email(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email.lower().strip(),))
    row = c.fetchone(); conn.close()
    return _db_row_to_user(row)

def db_get_user_by_google_id(google_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
    row = c.fetchone(); conn.close()
    return _db_row_to_user(row)

def db_create_user(email, name, password_hash=None, google_id=None, apple_id=None):
    user_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (id, email, name, password_hash, google_id, apple_id) VALUES (?,?,?,?,?,?)",
              (user_id, email.lower().strip(), name, password_hash, google_id, apple_id))
    c.execute("INSERT INTO progress (user_id) VALUES (?)", (user_id,))
    conn.commit(); conn.close()
    return user_id

def db_save_progress(user_id):
    ss = st.session_state
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""INSERT OR REPLACE INTO progress
        (user_id, xp, level, topic, total_answered, correct_answered,
         streak, last_active, daily_done, quiz_answered, badges)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (user_id, ss.xp, ss.level, ss.topic, ss.total_answered, ss.correct_answered,
         ss.streak, str(date.today()),
         json.dumps(list(ss.daily_done)),
         json.dumps(ss.quiz_answered),
         json.dumps(ss.badges)))
    conn.commit(); conn.close()

def db_load_progress(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM progress WHERE user_id = ?", (user_id,))
    row = c.fetchone(); conn.close()
    if row:
        return {"xp": row[1], "level": row[2], "topic": row[3],
                "total_answered": row[4], "correct_answered": row[5],
                "streak": row[6], "last_active": row[7],
                "daily_done": set(json.loads(row[8] or "[]")),
                "quiz_answered": json.loads(row[9] or "{}"),
                "badges": json.loads(row[10] or "[]")}
    return None

def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return (salt + key).hex()

def verify_password(password, stored_hex):
    try:
        stored = bytes.fromhex(stored_hex)
        salt, stored_key = stored[:32], stored[32:]
        return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000) == stored_key
    except Exception:
        return False

def get_user_initials(name):
    parts = (name or "?").strip().split()
    if len(parts) >= 2: return (parts[0][0] + parts[-1][0]).upper()
    return parts[0][:2].upper() if parts else "?"

def _set_logged_in(user):
    st.session_state.logged_in  = True
    st.session_state.user_id    = user["id"]
    st.session_state.user_name  = user.get("name") or user.get("email", "").split("@")[0]
    st.session_state.user_email = user.get("email", "")
    st.session_state.user_avatar = get_user_initials(st.session_state.user_name)
    prog = db_load_progress(user["id"])
    if prog:
        for k, v in prog.items():
            st.session_state[k] = v

# ── Google OAuth ─────────────────────────────
def _google_creds():
    try:
        g = st.secrets["google"]
        return (g.get("client_id",""), g.get("client_secret",""),
                g.get("redirect_uri","http://localhost:8501"))
    except Exception:
        return (os.environ.get("GOOGLE_CLIENT_ID",""),
                os.environ.get("GOOGLE_CLIENT_SECRET",""),
                os.environ.get("GOOGLE_REDIRECT_URI","http://localhost:8501"))

def get_google_auth_url():
    cid, _, ruri = _google_creds()
    if not cid: return None
    return "https://accounts.google.com/o/oauth2/auth?" + urlencode({
        "client_id": cid, "redirect_uri": ruri,
        "response_type": "code", "scope": "openid email profile",
        "access_type": "offline", "state": "google_oauth",
        "prompt": "select_account",
    })

def handle_google_callback(code):
    cid, csec, ruri = _google_creds()
    if not cid: return None
    try:
        import requests
        tokens = requests.post("https://oauth2.googleapis.com/token", data={
            "code": code, "client_id": cid, "client_secret": csec,
            "redirect_uri": ruri, "grant_type": "authorization_code"
        }, timeout=10).json()
        if "access_token" not in tokens: return None
        return requests.get("https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}, timeout=10).json()
    except Exception:
        return None

def login_with_google_user(guser):
    gid   = guser.get("sub", "")
    email = guser.get("email", "")
    name  = guser.get("name", email.split("@")[0])
    user  = db_get_user_by_google_id(gid)
    if not user:
        user = db_get_user_by_email(email)
        if user:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("UPDATE users SET google_id=? WHERE id=?", (gid, user["id"]))
            conn.commit(); conn.close()
        else:
            uid  = db_create_user(email, name, google_id=gid)
            user = {"id": uid, "email": email, "name": name}
    _set_logged_in(user)

# ── Apple Sign In ─────────────────────────────
def _apple_creds():
    try:
        a = st.secrets["apple"]
        return (a.get("client_id",""), a.get("team_id",""),
                a.get("key_id",""), a.get("private_key",""),
                a.get("redirect_uri","http://localhost:8501"))
    except Exception:
        return ("","","","","")

def get_apple_auth_url():
    cid, _, _, _, ruri = _apple_creds()
    if not cid: return None
    return "https://appleid.apple.com/auth/authorize?" + urlencode({
        "client_id": cid, "redirect_uri": ruri,
        "response_type": "code", "scope": "name email",
        "response_mode": "query", "state": "apple_oauth",
    })

def handle_apple_callback(code):
    cid, team_id, key_id, private_key, ruri = _apple_creds()
    if not cid or not private_key: return None
    try:
        import jwt as pyjwt, time, requests
        now = int(time.time())
        client_secret = pyjwt.encode({
            "iss": team_id, "iat": now, "exp": now + 86400,
            "aud": "https://appleid.apple.com", "sub": cid,
        }, private_key, algorithm="ES256", headers={"kid": key_id})
        tokens = requests.post("https://appleid.apple.com/auth/token", data={
            "client_id": cid, "client_secret": client_secret,
            "code": code, "grant_type": "authorization_code", "redirect_uri": ruri,
        }, timeout=10).json()
        if "id_token" not in tokens: return None
        claims = pyjwt.decode(tokens["id_token"], options={"verify_signature": False})
        return {"sub": claims.get("sub",""), "email": claims.get("email","")}
    except Exception:
        return None

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

def init_state():
    defaults = {
        "level": "Beginner", "topic": "Supply & Demand", "page": "Home",
        "total_answered": 0, "correct_answered": 0, "streak": 0,
        "daily_done": set(), "quiz_answered": {}, "xp": 0, "badges": [],
        "dark_mode": False,
        # auth
        "logged_in": False, "user_id": None, "user_name": None,
        "user_email": None, "user_avatar": None, "auth_mode": "login",
        "auth_error": "", "auth_success": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def get_daily_topic():
    day_num = (date.today() - date(2024, 1, 1)).days
    return list(TOPICS.keys())[day_num % len(TOPICS)]

def award_xp(amount):
    st.session_state.xp += amount
    xp = st.session_state.xp
    badges = st.session_state.badges
    if xp >= 100 and "First 100 XP" not in badges: badges.append("First 100 XP")
    if xp >= 500 and "500 XP Club" not in badges: badges.append("500 XP Club")
    if st.session_state.correct_answered >= 5 and "Quiz Starter" not in badges: badges.append("Quiz Starter")
    if st.session_state.correct_answered >= 20 and "Quiz Master" not in badges: badges.append("Quiz Master")
    if st.session_state.streak >= 3 and "3-Day Streak" not in badges: badges.append("3-Day Streak")
    if st.session_state.logged_in and st.session_state.user_id:
        db_save_progress(st.session_state.user_id)

BADGE_ICONS = {"First 100 XP": "🥉", "500 XP Club": "🥇", "Quiz Starter": "📝", "Quiz Master": "🎓", "3-Day Streak": "🔥"}

# ─────────────────────────────────────────────
# THEME PALETTES
# ─────────────────────────────────────────────
def get_theme(dark: bool) -> dict:
    if dark:
        # ── Dark: deep purple-night (Palette 12 + 11) ──
        return dict(
            BG        = "#1e1c2e",
            TEXT      = "#e3e1c8",
            CARD      = "#514d86",
            CARD_B    = "#816cb1",
            CARD_SH   = "#16142a",
            SIDEBAR   = "#16142a",
            SB_B      = "#514d86",
            TILE      = "#514d86",
            TILE_B    = "#816cb1",
            TILE_SH   = "#16142a",
            HIST      = "#2a2840",
            INP_BG    = "#514d86",
            EXP_BG    = "#514d86",
            METRIC    = "#514d86",
            SUB_COL   = "#c5c5ff",
            SEL_BG    = "#514d86",
            SEL_TEXT  = "#e3e1c8",
            SEL_MENU  = "#2a2840",
            SEL_OPT   = "#e3e1c8",
            SEL_OPT_H = "#514d86",
            SB_SEL    = "#2a2840",
            SB_SEL_B  = "#816cb1",
            SB_MENU   = "#1e1c2e",
            SB_MENU_H = "#2a2840",
            BTN_BG    = "#d289ae",
            BTN_SH    = "#8a4a6e",
            BTN_TXT   = "#16142a",
            SB_BTN    = "#816cb1",
            SB_BTN_SH = "#514d86",
            TITLE_COL = "#e2d6fa",
            TITLE_SH  = "#816cb1",
            ACCENT_H3 = "#c5c5ff",
            ACCENT_HAS= "#c5c5ff",
            ACCENT_NO = "#816cb1",
            XP_BG     = "#16142a",
            XP_FILL   = "#d289ae",
            XP_BORDER = "#816cb1",
            BADGE_BEG = "#816cb1",
            BADGE_INT = "#d289ae",
            BADGE_ADV = "#a2aef7",
            CHAIN_ARR = "#d289ae",
            ERA_BG    = "#514d86",
            CBOX_BG   = "#2a2840",
            CBOX_B    = "#816cb1",
            CG_BG     = "#1e2e3a",
            CG_B      = "#6aa08f",
            CG_SH     = "#0e1820",
            CR_BG     = "#3a1e2a",
            CR_B      = "#d289ae",
            CR_SH     = "#1e0e18",
            CGOLD_BG  = "#2e2810",
            CGOLD_B   = "#e8ae7d",
            CGOLD_SH  = "#1e1808",
            TOGGLE_SH = "#514d86",
            BG_GRAD   = "#2a2840",
            CARD_GRAD = "#5e5a9a",
            LOGIN_CARD= "#2a2840",
            LOGIN_B   = "#816cb1",
        )
    else:
        # ── Light: warm sage-peach (Palette 6 + 4 + 5) ──
        return dict(
            BG        = "#f9f6e3",
            TEXT      = "#2d2020",
            CARD      = "#dbe8cd",
            CARD_B    = "#b8c4a4",
            CARD_SH   = "#8b82a8",
            SIDEBAR   = "#6aa08f",
            SB_B      = "#b8c4a4",
            TILE      = "#dbe8cd",
            TILE_B    = "#b8c4a4",
            TILE_SH   = "#8b82a8",
            HIST      = "#f9f6e3",
            INP_BG    = "#f9f6e3",
            EXP_BG    = "#dbe8cd",
            METRIC    = "#dbe8cd",
            SUB_COL   = "#6aa08f",
            SEL_BG    = "#f9f6e3",
            SEL_TEXT  = "#2d2020",
            SEL_MENU  = "#f9f6e3",
            SEL_OPT   = "#2d2020",
            SEL_OPT_H = "#dbe8cd",
            SB_SEL    = "#4a7a6e",
            SB_SEL_B  = "#b8c4a4",
            SB_MENU   = "#4a7a6e",
            SB_MENU_H = "#6aa08f",
            BTN_BG    = "#e8ae7d",
            BTN_SH    = "#a56066",
            BTN_TXT   = "#2d2020",
            SB_BTN    = "#4a7a6e",
            SB_BTN_SH = "#2d5548",
            TITLE_COL = "#7f4a4f",
            TITLE_SH  = "#b8c4a4",
            ACCENT_H3 = "#6aa08f",
            ACCENT_HAS= "#6aa08f",
            ACCENT_NO = "#8b82a8",
            XP_BG     = "#4a7a6e",
            XP_FILL   = "#e8ae7d",
            XP_BORDER = "#b8c4a4",
            BADGE_BEG = "#6aa08f",
            BADGE_INT = "#e8ae7d",
            BADGE_ADV = "#7f4a4f",
            CHAIN_ARR = "#7f4a4f",
            ERA_BG    = "#6aa08f",
            CBOX_BG   = "#fff6ae",
            CBOX_B    = "#e8ae7d",
            CG_BG     = "#b8c4a4",
            CG_B      = "#6aa08f",
            CG_SH     = "#4a7a6e",
            CR_BG     = "#ffd9bc",
            CR_B      = "#a56066",
            CR_SH     = "#7f4a4f",
            CGOLD_BG  = "#fff6ae",
            CGOLD_B   = "#e8ae7d",
            CGOLD_SH  = "#a56066",
            TOGGLE_SH = "#4a7a6e",
            BG_GRAD   = "#ede9d0",
            CARD_GRAD = "#cfe0c2",
            LOGIN_CARD= "#f0ede0",
            LOGIN_B   = "#b8c4a4",
        )

def render_css(T: dict):
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Nunito:wght@400;600;700;800&display=swap');

    html, body, .stApp, [class*="appview-container"] {{
        font-family: 'Nunito', sans-serif !important;
        background: linear-gradient(160deg, {T['BG']} 0%, {T['BG_GRAD']} 100%) !important;
        background-attachment: fixed !important;
        color: {T['TEXT']} !important;
    }}
    .main .block-container {{
        background-color: transparent !important;
        padding-top: 2rem !important;
    }}
    p, span, label, li, h1, h2, h3, h4, strong, em {{
        color: {T['TEXT']} !important;
    }}

    /* ── SIDEBAR ── */
    section[data-testid="stSidebar"] {{
        background-color: {T['SIDEBAR']} !important;
        border-right: 4px solid {T['SB_B']} !important;
    }}
    section[data-testid="stSidebar"] * {{ color: #f9f6e3 !important; }}
    section[data-testid="stSidebar"] hr {{ border-color: {T['SB_B']} !important; opacity: 0.5; }}

    /* ── BUTTONS (main) ── */
    .stButton > button {{
        font-family: 'Nunito', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        color: {T['BTN_TXT']} !important;
        background: linear-gradient(135deg, {T['BTN_BG']} 0%, {T['BTN_SH']}44 200%) !important;
        background-color: {T['BTN_BG']} !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.65rem 1.1rem !important;
        box-shadow: 0 3px 0 {T['BTN_SH']}, 0 8px 20px rgba(0,0,0,0.07) !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease !important;
        width: 100% !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }}
    .stButton > button > div,
    .stButton > button > div > div {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
    }}
    .stButton > button p,
    .stButton > button span {{
        color: {T['BTN_TXT']} !important;
        font-weight: 800 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }}
    .stButton > button [data-testid="stShortcutHint"],
    .stButton > button kbd,
    .stButton > button svg,
    .stButton > button [class*="shortcut"] {{ display: none !important; }}
    .stButton > button:hover {{
        transform: translateY(2px) !important;
        box-shadow: 0 1px 0 {T['BTN_SH']}, 0 4px 10px rgba(0,0,0,0.05) !important;
    }}
    .stButton > button:active {{
        transform: translateY(3px) !important;
        box-shadow: none !important;
    }}

    /* ── SIDEBAR BUTTONS ── */
    section[data-testid="stSidebar"] .stButton > button {{
        background-color: {T['SB_BTN']} !important;
        box-shadow: 0px 5px 0px {T['SB_BTN_SH']} !important;
        color: #f9f6e3 !important;
        margin-bottom: 5px !important;
    }}
    section[data-testid="stSidebar"] .stButton > button p,
    section[data-testid="stSidebar"] .stButton > button span {{ color: #f9f6e3 !important; }}
    section[data-testid="stSidebar"] .stButton > button:hover {{
        box-shadow: 0px 2px 0px {T['SB_BTN_SH']} !important;
    }}

    /* ── DARK MODE TOGGLE (circle) ── */
    div[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button {{
        min-height: unset !important;
        height: 36px !important;
        width: 36px !important;
        padding: 0 !important;
        border-radius: 50% !important;
        font-size: 1.2rem !important;
        box-shadow: 0px 3px 0px {T['TOGGLE_SH']} !important;
        margin-top: 2px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1 !important;
    }}
    div[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button > div,
    div[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button > div > div {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        height: 100% !important;
    }}
    div[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button p,
    div[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button span {{
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    div[data-testid="stSidebar"] div[data-testid="column"]:last-child .stButton > button:hover {{
        box-shadow: 0px 1px 0px {T['TOGGLE_SH']} !important;
    }}

    /* ── SELECTBOX ── */
    [data-testid="stSelectbox"] > div > div,
    [data-baseweb="select"] > div,
    [data-baseweb="select"] {{
        background-color: {T['SEL_BG']} !important;
        color: {T['SEL_TEXT']} !important;
        border: 3px solid {T['CARD_B']} !important;
        border-radius: 14px !important;
    }}
    [data-baseweb="select"] * {{ color: {T['SEL_TEXT']} !important; }}
    [data-baseweb="select"] svg {{ fill: {T['SEL_TEXT']} !important; }}
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="menu"] {{
        background-color: {T['SEL_MENU']} !important;
        border: 2px solid {T['CARD_B']} !important;
        border-radius: 12px !important;
    }}
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"] {{
        background-color: {T['SEL_MENU']} !important;
        color: {T['SEL_OPT']} !important;
        font-weight: 700 !important;
    }}
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover,
    [data-baseweb="menu"] [aria-selected="true"] {{
        background-color: {T['SEL_OPT_H']} !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"] > div,
    section[data-testid="stSidebar"] [data-baseweb="select"] {{
        background-color: {T['SB_SEL']} !important;
        border-color: {T['SB_SEL_B']} !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="select"] * {{ color: #f9f6e3 !important; }}
    section[data-testid="stSidebar"] [data-baseweb="select"] svg {{ fill: #f9f6e3 !important; }}
    section[data-testid="stSidebar"] [data-baseweb="menu"] {{ background-color: {T['SB_MENU']} !important; }}
    section[data-testid="stSidebar"] [data-baseweb="menu"] li {{ color: #f9f6e3 !important; }}
    section[data-testid="stSidebar"] [data-baseweb="menu"] li:hover {{ background-color: {T['SB_MENU_H']} !important; }}

    /* ── CARDS ── */
    .card {{
        background: linear-gradient(135deg, {T['CARD']} 0%, {T['CARD_GRAD']} 100%) !important;
        border-radius: 22px !important;
        padding: 1.3rem 1.6rem !important;
        margin-bottom: 1rem !important;
        border: 3px solid {T['CARD_B']} !important;
        box-shadow: 4px 4px 0 {T['CARD_SH']}, 0 10px 30px rgba(0,0,0,0.05) !important;
        color: {T['TEXT']} !important;
    }}
    .card * {{ color: {T['TEXT']} !important; }}
    .card-green {{ background: {T['CG_BG']} !important; border-color: {T['CG_B']} !important; box-shadow: 6px 6px 0px {T['CG_SH']} !important; }}
    .card-red   {{ background: {T['CR_BG']} !important; border-color: {T['CR_B']} !important; box-shadow: 6px 6px 0px {T['CR_SH']} !important; }}
    .card-gold  {{ background: {T['CGOLD_BG']} !important; border-color: {T['CGOLD_B']} !important; box-shadow: 6px 6px 0px {T['CGOLD_SH']} !important; }}

    /* ── TITLES ── */
    .main-title {{
        font-family: 'Playfair Display', serif !important;
        font-size: 3rem; font-weight: 800;
        color: {T['TITLE_COL']} !important;
        text-shadow: 3px 3px 0px {T['TITLE_SH']};
        text-align: center; margin-bottom: 0.2rem;
        letter-spacing: -0.01em;
    }}
    .subtitle {{
        color: {T['SUB_COL']} !important;
        font-size: 1.2rem; font-weight: 800;
        text-align: center; margin-bottom: 2rem;
    }}
    .accent-h3 {{ color: {T['ACCENT_H3']} !important; }}

    /* ── XP BAR ── */
    .xp-bar {{
        background: {T['XP_BG']}; border-radius: 50px; height: 18px;
        border: 3px solid {T['XP_BORDER']}; overflow: hidden; margin: 6px 0 12px 0;
    }}
    .xp-fill {{ background: {T['XP_FILL']}; height: 100%; border-radius: 50px; }}

    /* ── LEVEL BADGES ── */
    .level-badge {{
        display: inline-block; padding: 4px 14px;
        border-radius: 20px; font-size: 0.85rem; font-weight: 800; color: #fff !important;
    }}
    .beginner     {{ background: {T['BADGE_BEG']} !important; }}
    .intermediate {{ background: {T['BADGE_INT']} !important; }}
    .advanced     {{ background: {T['BADGE_ADV']} !important; }}

    /* ── METRICS ── */
    [data-testid="metric-container"] {{
        background: {T['METRIC']} !important;
        border-radius: 16px !important; padding: 0.8rem !important;
        border: 3px solid {T['CARD_B']} !important;
        box-shadow: 5px 5px 0px {T['CARD_SH']} !important;
    }}
    [data-testid="metric-container"] label,
    [data-testid="metric-container"] div {{ color: {T['TEXT']} !important; font-weight: 800 !important; }}

    /* ── TOPIC TILES ── */
    .topic-tile {{
        background: {T['TILE']}; border: 3px solid {T['TILE_B']}; border-radius: 14px;
        padding: 10px 4px 6px 4px; text-align: center;
        color: {T['TEXT']} !important; font-weight: 800; font-size: 0.8rem;
        box-shadow: 4px 4px 0px {T['TILE_SH']}; margin-bottom: 4px; line-height: 1.4;
    }}

    /* ── CONCEPT CHAIN ── */
    .concept-box {{
        background: {T['CBOX_BG']} !important;
        border: 2px solid {T['CBOX_B']};
        border-radius: 10px; padding: 6px 12px; margin: 3px;
        display: inline-block; font-weight: 700;
        color: {T['TEXT']} !important; font-size: 0.88rem;
    }}
    .chain-arrow {{ font-size: 1.3rem; color: {T['CHAIN_ARR']} !important; margin: 2px; }}

    /* ── HISTORY CARDS ── */
    .history-card {{
        background: {T['HIST']} !important;
        border: 3px solid {T['CARD_B']} !important; border-radius: 16px !important;
        padding: 1rem 1.4rem !important; margin-bottom: 1rem !important;
        box-shadow: 4px 4px 0px {T['CARD_SH']} !important; color: {T['TEXT']} !important;
    }}
    .history-card * {{ color: {T['TEXT']} !important; }}
    .era-tag {{
        background: {T['ERA_BG']} !important;
        color: #f9f6e3 !important; padding: 3px 12px;
        border-radius: 12px; font-size: 0.75rem; font-weight: 700;
    }}

    /* ── EXPANDER ── */
    [data-testid="stExpander"] {{
        background: {T['EXP_BG']} !important;
        border: 3px solid {T['CARD_B']} !important;
        border-radius: 14px !important; margin-bottom: 6px !important;
    }}
    [data-testid="stExpander"] summary {{ color: {T['TEXT']} !important; font-weight: 800 !important; }}
    [data-testid="stExpander"] * {{ color: {T['TEXT']} !important; }}

    /* ── TEXT INPUT ── */
    .stTextInput input {{
        background: {T['INP_BG']} !important;
        border: 3px solid {T['CARD_B']} !important; border-radius: 12px !important;
        color: {T['TEXT']} !important; font-family: 'Nunito', sans-serif !important; font-weight: 700 !important;
    }}

    /* ── LOGIN PAGE ── */
    .login-wrap {{
        max-width: 460px; margin: 1.5rem auto 0 auto;
    }}
    .login-card {{
        background: linear-gradient(140deg, {T['LOGIN_CARD']} 0%, {T['CARD']} 100%) !important;
        border: 3px solid {T['LOGIN_B']} !important;
        border-radius: 28px !important;
        padding: 2.5rem 2.2rem 2rem 2.2rem !important;
        box-shadow: 5px 5px 0 {T['CARD_SH']}, 0 24px 60px rgba(0,0,0,0.10) !important;
    }}
    .login-logo {{
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem; font-weight: 800;
        color: {T['TITLE_COL']} !important;
        text-align: center; text-shadow: 2px 2px 0 {T['TITLE_SH']};
        margin-bottom: 0.2rem; letter-spacing: -0.01em;
    }}
    .login-tagline {{
        color: {T['SUB_COL']} !important;
        text-align: center; font-size: 0.95rem; font-weight: 600;
        margin-bottom: 1.8rem;
    }}
    .social-btn {{
        display: flex !important; align-items: center !important;
        justify-content: center !important; gap: 10px !important;
        width: 100% !important; padding: 0.72rem 1.2rem !important;
        border-radius: 14px !important; font-weight: 700 !important;
        font-size: 0.95rem !important; font-family: 'Nunito', sans-serif !important;
        cursor: pointer !important; text-decoration: none !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease !important;
        box-sizing: border-box !important;
    }}
    .google-btn {{
        background: #ffffff !important; color: #3c3c3c !important;
        border: 2px solid #e0e0e0 !important;
        box-shadow: 0 3px 0 #c8c8c8, 0 6px 16px rgba(0,0,0,0.07) !important;
    }}
    .google-btn:hover {{ transform: translateY(2px) !important; box-shadow: 0 1px 0 #c8c8c8 !important; }}
    .apple-btn {{
        background: #1a1a1a !important; color: #ffffff !important;
        border: 2px solid #1a1a1a !important;
        box-shadow: 0 3px 0 #000, 0 6px 16px rgba(0,0,0,0.18) !important;
    }}
    .apple-btn:hover {{ transform: translateY(2px) !important; box-shadow: 0 1px 0 #000 !important; }}
    .login-divider {{
        display: flex; align-items: center; gap: 14px;
        margin: 1.2rem 0; color: {T['TEXT']}88 !important; font-size: 0.85rem; font-weight: 700;
    }}
    .login-divider::before, .login-divider::after {{
        content: ''; flex: 1; height: 1px; background: {T['CARD_B']};
    }}
    .login-toggle {{
        text-align: center; margin-top: 0.6rem;
        color: {T['TEXT']}99 !important; font-size: 0.88rem;
    }}
    .login-error {{
        background: {T['CR_BG']} !important; border: 2px solid {T['CR_B']} !important;
        border-radius: 12px !important; padding: 0.7rem 1rem !important;
        color: {T['TEXT']} !important; font-weight: 700 !important; margin-bottom: 0.8rem;
    }}
    .login-success {{
        background: {T['CG_BG']} !important; border: 2px solid {T['CG_B']} !important;
        border-radius: 12px !important; padding: 0.7rem 1rem !important;
        color: {T['TEXT']} !important; font-weight: 700 !important; margin-bottom: 0.8rem;
    }}
    .user-avatar {{
        display: inline-flex; align-items: center; justify-content: center;
        width: 34px; height: 34px; border-radius: 50%;
        background: {T['BTN_BG']} !important; color: {T['BTN_TXT']} !important;
        font-weight: 800; font-size: 0.85rem; border: 2px solid {T['BTN_SH']};
        flex-shrink: 0;
    }}
</style>
""", unsafe_allow_html=True)

T = get_theme(st.session_state.dark_mode)
render_css(T)

# ─────────────────────────────────────────────
# OAUTH CALLBACKS (must run before any render)
# ─────────────────────────────────────────────
_qp = st.query_params
if "code" in _qp and not st.session_state.logged_in:
    _state = _qp.get("state", "")
    _code  = _qp["code"]
    if _state == "google_oauth":
        _guser = handle_google_callback(_code)
        if _guser:
            login_with_google_user(_guser)
            st.query_params.clear()
            st.rerun()
        else:
            st.session_state.auth_error = "Google sign-in failed. Please try again."
            st.query_params.clear()
    elif _state == "apple_oauth":
        _auser = handle_apple_callback(_code)
        if _auser:
            _email = _auser.get("email", "")
            _user  = db_get_user_by_email(_email) if _email else None
            if not _user and _email:
                _uid  = db_create_user(_email, _email.split("@")[0])
                _user = {"id": _uid, "email": _email, "name": _email.split("@")[0]}
            if _user:
                _set_logged_in(_user)
                st.query_params.clear()
                st.rerun()
        else:
            st.session_state.auth_error = "Apple sign-in failed. Please try again."
            st.query_params.clear()

# ─────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────
def render_login_page():
    mode = st.session_state.auth_mode

    _, col, _ = st.columns([1, 6, 1])
    with col:
        st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)

        st.markdown("<div class='login-logo'>📈 EconoLearn</div>", unsafe_allow_html=True)
        st.markdown("<div class='login-tagline'>Master economics — one lesson at a time.</div>", unsafe_allow_html=True)

        if st.session_state.auth_error:
            st.markdown(f"<div class='login-error'>⚠️ {st.session_state.auth_error}</div>", unsafe_allow_html=True)
        if st.session_state.auth_success:
            st.markdown(f"<div class='login-success'>✅ {st.session_state.auth_success}</div>", unsafe_allow_html=True)

        # ── Social sign-in buttons ──
        google_url = get_google_auth_url()
        apple_url  = get_apple_auth_url()

        if google_url:
            st.markdown(f"""<a href="{google_url}" class="social-btn google-btn" target="_self">
                <svg width="18" height="18" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google</a>""", unsafe_allow_html=True)
        else:
            st.markdown("<div class='social-btn google-btn' style='opacity:0.45;cursor:not-allowed;'>🔑 Google (add credentials in secrets.toml)</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if apple_url:
            st.markdown(f"""<a href="{apple_url}" class="social-btn apple-btn" target="_self">
                 Continue with Apple</a>""", unsafe_allow_html=True)
        else:
            st.markdown("<div class='social-btn apple-btn' style='opacity:0.45;cursor:not-allowed;'> Apple (add credentials in secrets.toml)</div>", unsafe_allow_html=True)

        st.markdown("<div class='login-divider'>or</div>", unsafe_allow_html=True)

        # ── Email / password form ──
        if mode == "register":
            reg_name = st.text_input("Your name", placeholder="Ada Lovelace", key="reg_name")
        auth_email = st.text_input("Email", placeholder="you@example.com", key="auth_email")
        auth_pass  = st.text_input("Password", type="password",
                                   placeholder="Min 8 characters", key="auth_password")

        if mode == "login":
            if st.button("Sign In →", key="btn_login"):
                st.session_state.auth_error = ""
                _u = db_get_user_by_email(auth_email)
                if not _u or not _u.get("password_hash"):
                    st.session_state.auth_error = "No account found with that email."
                    st.rerun()
                elif not verify_password(auth_pass, _u["password_hash"]):
                    st.session_state.auth_error = "Wrong password. Try again."
                    st.rerun()
                else:
                    _set_logged_in(_u)
                    st.session_state.auth_success = ""
                    st.rerun()
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='login-toggle'>Don't have an account?</div>", unsafe_allow_html=True)
            if st.button("Create a free account", key="to_register"):
                st.session_state.auth_mode = "register"
                st.session_state.auth_error = ""
                st.rerun()
        else:
            if st.button("Create Account →", key="btn_register"):
                st.session_state.auth_error = ""
                _name = reg_name.strip() if reg_name.strip() else auth_email.split("@")[0]
                if len(auth_pass) < 8:
                    st.session_state.auth_error = "Password must be at least 8 characters."
                    st.rerun()
                elif "@" not in auth_email or "." not in auth_email:
                    st.session_state.auth_error = "Please enter a valid email address."
                    st.rerun()
                elif db_get_user_by_email(auth_email):
                    st.session_state.auth_error = "An account with this email already exists."
                    st.rerun()
                else:
                    _uid = db_create_user(auth_email, _name, password_hash=hash_password(auth_pass))
                    _set_logged_in({"id": _uid, "email": auth_email, "name": _name})
                    st.session_state.auth_success = f"Welcome, {_name}! Account created."
                    st.session_state.auth_mode = "login"
                    st.rerun()
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            st.markdown("<div class='login-toggle'>Already have an account?</div>", unsafe_allow_html=True)
            if st.button("Sign in instead", key="to_login"):
                st.session_state.auth_mode = "login"
                st.session_state.auth_error = ""
                st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    render_login_page()
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    dark = st.session_state.dark_mode
    col_title, col_toggle = st.columns([5, 1])
    with col_title:
        st.markdown("<h2 style='color:#FDF6E3 !important;margin:0;padding-top:4px;font-family:Playfair Display,serif;'>📈 EconoLearn</h2>", unsafe_allow_html=True)
    with col_toggle:
        if st.button("☀️" if dark else "🌙", key="dark_toggle"):
            st.session_state.dark_mode = not dark
            st.rerun()
    st.markdown("---")

    # ── User info + logout ──
    _av   = st.session_state.user_avatar or "?"
    _name = st.session_state.user_name or "User"
    _email = st.session_state.user_email or ""
    st.markdown(f"""<div style='display:flex;align-items:center;gap:10px;margin-bottom:6px;'>
        <div class='user-avatar'>{_av}</div>
        <div>
          <div style='color:#FDF6E3 !important;font-weight:800;font-size:0.9rem;line-height:1.2;'>{_name}</div>
          <div style='color:#FDF6E3aa !important;font-size:0.75rem;line-height:1.2;'>{_email}</div>
        </div>
    </div>""", unsafe_allow_html=True)
    if st.button("🚪 Log out", key="btn_logout"):
        if st.session_state.user_id:
            db_save_progress(st.session_state.user_id)
        for k in ["logged_in","user_id","user_name","user_email","user_avatar",
                  "xp","level","topic","total_answered","correct_answered","streak",
                  "daily_done","quiz_answered","badges","page"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()
    st.markdown("---")

    xp = st.session_state.xp
    xp_level = xp // 100
    xp_pct = xp % 100
    st.markdown(f"<p style='color:#FDF6E3 !important;font-weight:800;margin-bottom:2px;'>Level {xp_level} Explorer ✨ — {xp} XP</p>", unsafe_allow_html=True)
    st.markdown(f'<div class="xp-bar"><div class="xp-fill" style="width:{xp_pct}%;"></div></div>', unsafe_allow_html=True)

    if st.session_state.badges:
        badge_str = "  ".join(BADGE_ICONS.get(b, "🏅") for b in st.session_state.badges)
        st.markdown(f"<p style='color:#FDF6E3 !important;font-size:1.3rem;'>{badge_str}</p>", unsafe_allow_html=True)

    st.markdown(f"<p style='color:#FDF6E3 !important;font-weight:700;'>{'🔥' * min(st.session_state.streak, 7)} Streak: {st.session_state.streak} days</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color:#FDF6E3 !important;font-weight:800;font-size:1rem;'>🗺️ Navigation</p>", unsafe_allow_html=True)
    pages = [("🏠", "Home"), ("📚", "Daily Lesson"), ("❓", "Quiz"), ("🎯", "Scenarios"),
             ("✍️", "Fill in the Blanks"), ("🔗", "Concept Chains"), ("🏛️", "Economic History"), ("📊", "My Progress")]
    for icon, pg in pages:
        if st.button(f"{icon} {pg}", key=f"nav_{pg}"):
            st.session_state.page = pg
            st.rerun()

    st.markdown("---")
    st.markdown("<p style='color:#FDF6E3 !important;font-weight:800;font-size:1rem;'>🏆 Level</p>", unsafe_allow_html=True)
    level_icons = {"Beginner": "🌱", "Intermediate": "⚡", "Advanced": "🔥"}
    for lvl in LEVELS:
        if st.button(f"{level_icons[lvl]} {lvl}", key=f"lvl_{lvl}"):
            st.session_state.level = lvl
            st.rerun()
    st.markdown(f"<p style='color:#FDF6E3 !important;margin-top:6px;'>Active: <span class='level-badge {st.session_state.level.lower()}'>{st.session_state.level}</span></p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<p style='color:#FDF6E3 !important;font-weight:800;font-size:1rem;'>📌 Topic</p>", unsafe_allow_html=True)
    selected_topic = st.selectbox("topic", list(TOPICS.keys()),
                                  index=list(TOPICS.keys()).index(st.session_state.topic),
                                  label_visibility="collapsed")
    if selected_topic != st.session_state.topic:
        st.session_state.topic = selected_topic
        st.rerun()

# ─────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────
page  = st.session_state.page
level = st.session_state.level
topic = st.session_state.topic

# ── HOME ──────────────────────────────────────
if page == "Home":
    st.markdown('<p class="main-title">📈 EconoLearn</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Master economics — from supply & demand to financial crises.</p>', unsafe_allow_html=True)

    daily_topic = get_daily_topic()
    today_str   = str(date.today())

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Your XP", f"{st.session_state.xp} XP")
    with c2: st.metric("Accuracy", f"{st.session_state.correct_answered}/{st.session_state.total_answered}" if st.session_state.total_answered else "—")
    with c3: st.metric("Streak", f"{st.session_state.streak} days 🔥")

    st.markdown("---")
    st.markdown(f"<h3 class='accent-h3'>Today's Topic: {TOPICS[daily_topic]} {daily_topic}</h3>", unsafe_allow_html=True)
    lesson = LESSONS.get(daily_topic, {}).get(level)
    if lesson:
        st.markdown(f"<div class='card'><b>{lesson['title']}</b> &nbsp; <span class='level-badge {level.lower()}'>{level}</span></div>", unsafe_allow_html=True)
        if today_str not in st.session_state.daily_done:
            if st.button("Start Today's Lesson →"):
                st.session_state.page = "Daily Lesson"
                st.session_state.topic = daily_topic
                st.session_state.daily_done.add(today_str)
                award_xp(10)
                st.rerun()
        else:
            st.success("✅ Today's lesson completed! +10 XP earned.")

    st.markdown("---")
    st.markdown("<h3 class='accent-h3'>Quick Start</h3>", unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("❓ Take a Quiz"): st.session_state.page = "Quiz"; st.rerun()
    with q2:
        if st.button("🎯 Scenario Exercise"): st.session_state.page = "Scenarios"; st.rerun()
    with q3:
        if st.button("🏛️ Economic History"): st.session_state.page = "Economic History"; st.rerun()

    st.markdown("---")
    st.markdown("<h3 class='accent-h3'>Topics Available</h3>", unsafe_allow_html=True)
    topic_cols = st.columns(5)
    for i, (t, icon) in enumerate(TOPICS.items()):
        with topic_cols[i % 5]:
            has = t in LESSONS
            color = T['ACCENT_HAS'] if has else T['ACCENT_NO']
            st.markdown(f"<div class='topic-tile'><span style='font-size:1.4rem;'>{icon}</span><br><span style='color:{color};'>{t}</span></div>", unsafe_allow_html=True)

# ── DAILY LESSON ──────────────────────────────
elif page == "Daily Lesson":
    lesson = LESSONS.get(topic, {}).get(level)
    st.markdown(f"<p class='main-title'>{TOPICS.get(topic, '📚')} {topic}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'><span class='level-badge {level.lower()}'>{level}</span></p>", unsafe_allow_html=True)

    if not lesson:
        st.info(f"No lesson yet for '{topic}' at {level} level. Try another topic or level!")
    else:
        st.markdown(f"## {lesson['title']}")
        st.markdown(lesson['content'])

        if lesson.get('key_terms'):
            st.markdown("---")
            st.markdown("<h3 class='accent-h3'>🔑 Key Terms</h3>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, (term, definition) in enumerate(lesson['key_terms'].items()):
                with cols[i % 2]:
                    st.markdown(f"<div class='card'><b>{term}</b><br><small>{definition}</small></div>", unsafe_allow_html=True)

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("❓ Take Quiz on This Topic"):
                st.session_state.page = "Quiz"; st.rerun()
        with c2:
            if st.button("🎯 Try a Scenario"):
                st.session_state.page = "Scenarios"; st.rerun()

# ── QUIZ ──────────────────────────────────────
elif page == "Quiz":
    st.markdown(f"<p class='main-title'>❓ Quiz</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>Level: <span class='level-badge {level.lower()}'>{level}</span></p>", unsafe_allow_html=True)

    questions = QUIZ_QUESTIONS.get(level, [])
    if not questions:
        st.info("No quiz questions available for this level.")
    else:
        random.seed(hashlib.md5(f"{level}{date.today()}".encode()).hexdigest())
        selected_qs = random.sample(questions, min(5, len(questions)))

        for idx, q_data in enumerate(selected_qs):
            q_key = f"{level}_{idx}_{date.today()}"
            st.markdown(f"<div class='card'><b>Q{idx+1}: {q_data['q']}</b></div>", unsafe_allow_html=True)
            answered = st.session_state.quiz_answered.get(q_key)

            if answered is None:
                for opt in q_data['options']:
                    if st.button(opt, key=f"q_{q_key}_{opt[0]}"):
                        correct = opt[0] == q_data['answer']
                        st.session_state.quiz_answered[q_key] = {"chosen": opt[0], "correct": correct}
                        st.session_state.total_answered += 1
                        if correct:
                            st.session_state.correct_answered += 1
                            award_xp(15)
                        else:
                            award_xp(2)
                        st.rerun()
            else:
                chosen  = answered['chosen']
                correct = answered['correct']
                for opt in q_data['options']:
                    if opt[0] == q_data['answer']:
                        st.markdown(f"✅ **{opt}**")
                    elif opt[0] == chosen and not correct:
                        st.markdown(f"❌ ~~{opt}~~")
                    else:
                        st.markdown(f"&nbsp;&nbsp; {opt}")
                box_cls = "card-green" if correct else "card-red"
                mark    = "✅ Correct! +15 XP" if correct else f"❌ Answer: **{q_data['answer']}**"
                st.markdown(f"<div class='card {box_cls}'>{mark}<br><small>{q_data['explanation']}</small></div>", unsafe_allow_html=True)
            st.markdown("---")

        answered_today = sum(1 for k in st.session_state.quiz_answered if str(date.today()) in k and level in k)
        st.markdown(f"**Progress**: {answered_today}/{len(selected_qs)} answered")

        if answered_today >= len(selected_qs):
            correct_today = sum(1 for k, v in st.session_state.quiz_answered.items() if str(date.today()) in k and level in k and v['correct'])
            pct = int(correct_today / len(selected_qs) * 100)
            if pct == 100: st.balloons(); st.success(f"🎉 Perfect score! {correct_today}/{len(selected_qs)}")
            elif pct >= 60: st.success(f"Good work! {correct_today}/{len(selected_qs)} correct ({pct}%)")
            else: st.warning(f"{correct_today}/{len(selected_qs)} correct ({pct}%). Review the lessons!")
            if st.button("Reset Quiz"):
                st.session_state.quiz_answered = {}; st.rerun()

# ── SCENARIOS ─────────────────────────────────
elif page == "Scenarios":
    st.markdown("<p class='main-title'>🎯 Scenarios</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>Apply your knowledge to real-world situations.</p>", unsafe_allow_html=True)

    scenarios = SCENARIO_EXERCISES.get(level, [])
    if not scenarios:
        st.info("No scenario exercises for this level yet. Try Beginner or Intermediate!")
    else:
        for i, s in enumerate(scenarios):
            st.markdown(f"### {s['scenario']}")
            st.markdown(f"<div class='card'>{s['situation']}</div>", unsafe_allow_html=True)
            st.markdown(f"**❓ {s['question']}**")

            reveal_key = f"scenario_reveal_{level}_{i}"
            if reveal_key not in st.session_state:
                st.session_state[reveal_key] = False

            if not st.session_state[reveal_key]:
                if st.button("Reveal Answer", key=f"reveal_{i}"):
                    st.session_state[reveal_key] = True
                    award_xp(5)
                    st.rerun()
            else:
                st.markdown(f"<div class='card card-green'><b>Answer & Analysis:</b><br><br>{s['answer']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card card-gold'>💡 <b>Key Concept:</b> {s['key_concept']}</div>", unsafe_allow_html=True)
            st.markdown("---")

# ── FILL IN THE BLANKS ────────────────────────
elif page == "Fill in the Blanks":
    st.markdown("<p class='main-title'>✍️ Fill in the Blanks</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'><span class='level-badge {level.lower()}'>{level}</span></p>", unsafe_allow_html=True)

    level_qs = [q for q in FILL_IN_BLANKS if q['level'] == level]
    if not level_qs:
        st.info(f"No fill-in-the-blank exercises for {level} yet.")
    else:
        for i, q in enumerate(level_qs):
            st.markdown(f"<div class='card'><b>{i+1}. {q['sentence']}</b></div>", unsafe_allow_html=True)
            submitted_key = f"fib_sub_{level}_{i}"
            if submitted_key not in st.session_state:
                st.session_state[submitted_key] = None

            if st.session_state[submitted_key] is None:
                user_ans = st.text_input("", key=f"fib_{level}_{i}", placeholder="Type your answer here...")
                c1, c2 = st.columns([1, 4])
                with c1:
                    if st.button("Check", key=f"fib_check_{level}_{i}"):
                        st.session_state[submitted_key] = user_ans
                        st.session_state.total_answered += 1
                        cwords = q['answer'].lower().split()
                        uwords = user_ans.lower().split()
                        overlap = sum(1 for w in uwords if any(w in cw or cw in w for cw in cwords))
                        if overlap >= min(2, len(cwords)):
                            st.session_state.correct_answered += 1
                            award_xp(10)
                        else:
                            award_xp(2)
                        st.rerun()
                with c2:
                    st.caption(f"💡 Hint: {q['hint']}")
            else:
                uwords  = st.session_state[submitted_key].lower().split() if st.session_state[submitted_key] else []
                cwords  = q['answer'].lower().split()
                overlap = sum(1 for w in uwords if any(w in cw or cw in w for cw in cwords))
                correct = overlap >= min(2, len(cwords))
                if correct:
                    st.markdown(f"<div class='card card-green'>✅ Correct! Answer: <b>{q['answer']}</b></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card card-red'>❌ Your answer: '{st.session_state[submitted_key]}' | Correct: <b>{q['answer']}</b></div>", unsafe_allow_html=True)
            st.markdown("---")

        if st.button("Reset and try again"):
            for i in range(len(level_qs)):
                k = f"fib_sub_{level}_{i}"
                if k in st.session_state: del st.session_state[k]
            st.rerun()

# ── CONCEPT CHAINS ────────────────────────────
elif page == "Concept Chains":
    st.markdown("<p class='main-title'>🔗 Concept Chains</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>See how economic forces cascade through the system.</p>", unsafe_allow_html=True)

    for chain in CONCEPT_CONNECTIONS:
        st.markdown(f"### {chain['title']}")
        st.markdown(f"<span class='level-badge {chain['level'].lower()}'>{chain['level']}</span>", unsafe_allow_html=True)
        st.markdown(f"*{chain['description']}*")
        st.markdown("<br>", unsafe_allow_html=True)
        html = ""
        for j, concept in enumerate(chain['concepts']):
            html += f"<span class='concept-box'>{concept}</span>"
            if j < len(chain['concepts']) - 1:
                html += "<span class='chain-arrow'> → </span>"
        st.markdown(html, unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

# ── ECONOMIC HISTORY ──────────────────────────
elif page == "Economic History":
    st.markdown("<p class='main-title'>🏛️ Economic History</p>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>The events that shaped the global economy — and what they teach us.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📜 Timeline", "🔍 Deep Dive"])

    with tab1:
        search = st.text_input("🔍 Search (keyword, year, era):", placeholder="e.g., Great Depression, 2008, Keynesian")
        filtered = ECONOMIC_HISTORY
        if search:
            q = search.lower()
            filtered = [e for e in ECONOMIC_HISTORY if q in e['year'].lower() or q in e['event'].lower() or q in e['description'].lower() or q in e['era'].lower() or q in e['lesson'].lower()]

        for event in filtered:
            with st.expander(f"**{event['year']}** — {event['event']}  |  *{event['era']}*"):
                st.markdown(event['description'])
                st.markdown(f"<div class='card card-gold'>💡 <b>Lesson:</b> {event['lesson']}</div>", unsafe_allow_html=True)
                st.markdown(f"<span class='era-tag'>{event['era']}</span>", unsafe_allow_html=True)

    with tab2:
        era_list = sorted(set(e['era'] for e in ECONOMIC_HISTORY))
        selected_era = st.selectbox("Filter by era:", ["All"] + era_list)
        era_events = ECONOMIC_HISTORY if selected_era == "All" else [e for e in ECONOMIC_HISTORY if e['era'] == selected_era]
        st.markdown(f"**{len(era_events)} event(s)** in this era")

        for event in era_events:
            st.markdown(f"""
<div class='history-card'>
    <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;'>
        <b style='font-size:1.05rem;color:#2D1B1E !important;'>{event['event']}</b>
        <span class='era-tag'>{event['era']}</span>
    </div>
    <p style='color:#555 !important;margin:4px 0 8px 0;font-weight:700;'>📅 {event['year']}</p>
    <p style='color:#2D1B1E !important;'>{event['description']}</p>
    <div class='card card-gold' style='margin-top:8px;'>💡 <b>Lesson:</b> {event['lesson']}</div>
</div>
""", unsafe_allow_html=True)

# ── MY PROGRESS ───────────────────────────────
elif page == "My Progress":
    st.markdown("<p class='main-title'>📊 My Progress</p>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total XP", st.session_state.xp)
    with c2:
        total   = st.session_state.total_answered
        correct = st.session_state.correct_answered
        st.metric("Quiz Accuracy", f"{int(correct/total*100)}%" if total else "N/A")
    with c3: st.metric("Questions Answered", total)
    with c4: st.metric("Streak", f"{st.session_state.streak} days")

    st.markdown("---")
    st.markdown("<h3 class='accent-h3'>Badges Earned</h3>", unsafe_allow_html=True)
    if st.session_state.badges:
        badge_cols = st.columns(len(st.session_state.badges))
        for col, badge in zip(badge_cols, st.session_state.badges):
            with col:
                icon = BADGE_ICONS.get(badge, "🏅")
                st.markdown(f"<div class='card' style='text-align:center;'><div style='font-size:2rem;'>{icon}</div><b>{badge}</b></div>", unsafe_allow_html=True)
    else:
        st.info("No badges yet. Complete lessons and quizzes to earn them!")

    st.markdown("---")
    st.markdown("<h3 class='accent-h3'>How to Earn XP</h3>", unsafe_allow_html=True)
    for action, reward in [("Start a daily lesson", "+10 XP"), ("Correct quiz answer", "+15 XP"), ("Quiz attempt (wrong)", "+2 XP"), ("Complete scenario", "+5 XP"), ("Fill-in correct", "+10 XP"), ("Fill-in attempt", "+2 XP")]:
        st.markdown(f"- **{action}**: {reward}")

    st.markdown("---")
    st.markdown("<h3 class='accent-h3'>Lesson Coverage</h3>", unsafe_allow_html=True)
    for t, levels_dict in LESSONS.items():
        icon = TOPICS.get(t, "📚")
        badges_html = " ".join(f"<span class='level-badge {l.lower()}'>{l}</span>" for l in levels_dict.keys())
        st.markdown(f"{icon} **{t}**: {badges_html}", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Reset All Progress"):
        for k in ["total_answered", "correct_answered", "streak", "xp"]:
            st.session_state[k] = 0
        for k in ["daily_done", "quiz_answered", "badges"]:
            st.session_state[k] = set() if k == "daily_done" else ([] if k == "badges" else {})
        if st.session_state.logged_in and st.session_state.user_id:
            db_save_progress(st.session_state.user_id)
        st.success("Progress reset.")
        st.rerun()
