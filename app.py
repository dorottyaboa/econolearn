import streamlit as st
import random
import json
import hashlib
from datetime import datetime, date

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

**Counter-argument**: In a recession with slack resources and near-zero rates, crowding out is minimal. Expansionary spending fills idle capacity rather than competing with it.

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
- **Rebuttals**: IMF and others found most "expansionary" consolidations occurred during booms when conditions were already good, or benefited from exchange rate depreciation not available to Eurozone members.

### Helicopter Money
Milton Friedman's thought experiment: central bank credits money directly to citizens' accounts (bypassing the banking system). Pure demand injection without debt creation.
- Different from QE (which just swaps assets with banks).
- MMT advocates see this as equivalent to fiscal policy financed by money creation.

### Public Goods, Externalities & the Size of Government
**Market failures** justify government intervention:
- Pure public goods (defense, basic research): Non-rival, non-excludable → private market underprovides.
- Externalities → Pigouvian taxes/subsidies or regulation.
- Social insurance → redistribution and risk-pooling against catastrophic events.
The debate is over *how much* market failure exists and *how efficient* government intervention is.
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

### What Countries Export
- **Factor endowments** (Heckscher-Ohlin): Countries export goods that use their abundant factors intensively.
  - Capital-rich countries (US): export capital-intensive goods.
  - Labor-rich countries (Bangladesh): export labor-intensive goods.

### Trade Barriers
- **Tariffs**: Tax on imports → raises price, protects domestic producers, harms consumers.
- **Quotas**: Limits on quantity of imports.
- **Subsidies**: Government support for domestic industries.

### Who Wins, Who Loses
Trade raises *total* welfare but creates winners and losers:
- Consumers win (cheaper goods).
- Import-competing workers lose jobs.
- Exporting industries win.
This explains political tensions around trade (Rust Belt, manufacturing decline).
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

**Purchasing Power Parity (PPP)**: In the long run, exchange rates adjust so the same basket of goods costs the same everywhere. Used to compare real living standards.

### The Trade Balance & Capital Flows
**Trade deficit = Capital account surplus** (an accounting identity).
- A country running a deficit must be receiving more foreign investment than it sends abroad.
- US trade deficits reflect the dollar's reserve currency status: the world wants dollar assets → must supply US with goods.

### The WTO & Trade Agreements
- **WTO (World Trade Organization)**: Sets global trade rules, arbitrates disputes, promotes tariff reduction.
- **Most Favored Nation (MFN)**: WTO principle — treat all members equally.
- **Free Trade Agreements (FTAs)**: Preferential tariffs between specific countries (NAFTA/USMCA, EU).

### Infant Industry Argument
Developing countries may need temporary protection for new industries to build scale and experience before competing with established foreign firms. Used by Japan, South Korea — controversial because protection often becomes permanent.

### China's Rise & the China Shock
David Autor (2016): Chinese import competition eliminated ~2.4M US manufacturing jobs 1990–2011. Affected regions showed long-lasting economic distress not offset by retraining/relocation.
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
- GVCs mean trade statistics overstate bilateral imbalances (China "exports" phones but much of the value is from Japan, Korea, and the US).

### Currency Manipulation
Countries sometimes deliberately **weaken** their currency to boost exports:
- Buy foreign currency → increase its demand → own currency depreciates.
- China accused of this in the 2000s-2010s.
- **Beggar-thy-neighbor**: If everyone depreciates, the benefit is canceled but disruption increases.

### The Triffin Dilemma
The global reserve currency (dollar) creates a contradiction:
- The world needs dollars → the US must run trade deficits to supply them.
- But large deficits undermine confidence in the dollar as a store of value.
- Triffin predicted this in 1960 — still unresolved; alternatives (SDRs, digital currencies) lack depth.

### Deglobalization Trends
Post-2016: political backlash + COVID supply chain disruptions + geopolitics pushing toward **reshoring** and **friend-shoring**:
- US CHIPS Act, Inflation Reduction Act: massive industrial policy to bring back semiconductor and clean-energy manufacturing.
- **Geopolitical decoupling**: China-US tech rivalry fragmenting the global tech supply chain.

### Trade & Inequality
**Stolper-Samuelson theorem**: Free trade lowers returns to the scarce factor in each country.
- In rich countries (capital-abundant), trade hurts unskilled workers.
- Explains why globalization + trade expanded GDP but worsened within-country inequality in the West.
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
- **Capital gain**: Profit from selling a stock at a higher price than you paid.
- **P/E ratio**: Price-to-Earnings — how much you pay per dollar of earnings. A high P/E = high growth expectations.

### Bonds (Fixed Income)
- A **bond** is a loan to a company or government. You receive regular interest (coupon) and your principal back at maturity.
- **Bond price and yield move inversely**: If rates rise, existing bonds (paying lower rates) become less valuable → their price falls, their yield rises.
- **US Treasury bonds**: Considered risk-free (the US government won't default on dollar debt).

### Risk & Return
- Higher risk = higher expected return (risk premium).
- **Diversification**: Spreading investments reduces risk without reducing expected return.
- **Beta**: Measures how much a stock moves with the market. Beta > 1 = amplifies market swings.

### The Stock Market ≠ The Economy
- Stock markets anticipate future earnings — they're forward-looking.
- The economy can shrink while stocks rise (if rates fall or future outlook improves).
- Stocks represent large corporations, not the whole economy (small businesses, workers, etc.).
            """,
            "key_terms": {"Stock": "Ownership share in a company", "Bond": "Loan to a government or company that pays interest", "Dividend": "Regular cash payment to shareholders from company profits", "P/E Ratio": "Price divided by earnings per share — valuation metric", "Yield": "Return on a bond, moves inversely with its price"},
        },
        "Intermediate": {
            "title": "Asset Pricing, Bubbles & Market Efficiency",
            "content": """
### Efficient Market Hypothesis (EMH)
Eugene Fama: All available information is already reflected in asset prices.
- **Weak form**: Past prices can't predict future prices.
- **Semi-strong**: All public information is priced in. Fundamental analysis can't beat the market.
- **Strong form**: Even private information is priced in (insider trading can't beat it).

**Implication**: You can't consistently beat the market → index funds are optimal.

**Behavioral critique** (Shiller): Markets show excess volatility, predictable anomalies (momentum, value premium), and bubbles that EMH can't fully explain.

### The CAPM (Capital Asset Pricing Model)
Expected return of an asset = Risk-free rate + Beta × (Market return − Risk-free rate)
- Only **systematic risk** (non-diversifiable, market-wide) is rewarded.
- **Idiosyncratic risk** (company-specific) can be diversified away for free.

### Financial Bubbles
Mechanism (Minsky moment):
1. Displacement (new technology, asset, opportunity)
2. Credit expansion fuels speculation
3. Euphoria — overvaluation, "this time is different"
4. Insider selling
5. Panic and crash

Examples: Tulip mania (1637), South Sea Bubble (1720), Dot-com (2000), Housing (2008).

### Yield Curve
Plots bond yields across maturities. Normally upward sloping (long-term > short-term).
- **Inverted yield curve**: Short-term yields > long-term yields → signals recession (has predicted every US recession since 1950s).
            """,
            "key_terms": {"EMH": "Efficient Market Hypothesis — prices reflect all available information", "CAPM": "Capital Asset Pricing Model — links expected return to systematic risk (beta)", "Beta": "Sensitivity of a stock's returns to market-wide returns", "Minsky Moment": "Sudden market collapse after speculative excess", "Yield Curve": "Plot of bond yields across different maturities"},
        },
        "Advanced": {
            "title": "Financial Crises, Systemic Risk & Regulation",
            "content": """
### The 2008 Financial Crisis — Anatomy
1. **Housing bubble**: Low rates + lax lending → subprime mortgages to unqualified buyers.
2. **Securitization**: Banks bundled mortgages into MBS (Mortgage-Backed Securities) and CDOs.
3. **Credit ratings**: Rating agencies (S&P, Moody's) gave AAA to toxic instruments (conflict of interest).
4. **Leverage**: Banks held thin capital against massive liabilities.
5. **Shadow banking**: Repo markets, money market funds — unregulated bank-like entities.
6. **Trigger**: House prices fall → MBS values collapse → interbank lending freezes → Lehman Brothers fails.

### Systemic Risk & "Too Big to Fail"
- **Systemic risk**: Risk that failure of one institution cascades through the whole system.
- **Moral hazard of bailouts**: If you're big enough, the government will rescue you → take more risk.
- **Dodd-Frank (2010)**: Stronger capital requirements (Basel III), stress tests, resolution mechanisms for SIFIs (Systemically Important Financial Institutions).

### The Leverage Cycle (Geanakoplos)
- In booms: collateral is valued highly → lenders extend more credit → leverage rises.
- In busts: collateral falls → margin calls → forced selling → prices fall further → leverage cycle amplifies both up and down.

### Shadow Banking & Modern Risks
The 2008 crisis was largely a **run on the shadow banking system** (repo markets, money market funds).
- Shadow banks perform maturity transformation without deposit insurance.
- Vulnerability: short-term funding can evaporate overnight.
- 2020: Fed's rapid intervention prevented a repeat.

### Crypto & DeFi
- Bitcoin: Decentralized, fixed supply, inflation hedge claim — but high volatility undermines "store of value."
- **DeFi (Decentralized Finance)**: Smart contracts replicate financial services without intermediaries — but also without consumer protection, and vulnerable to code exploits.
            """,
            "key_terms": {"MBS": "Mortgage-Backed Security — bonds backed by mortgage payments", "Systemic Risk": "Risk of cascading failures across the financial system", "Too Big to Fail": "Implicit government guarantee for large financial institutions", "Leverage Cycle": "Amplification of booms/busts through rising/falling collateral values", "Shadow Banking": "Bank-like financial intermediaries without bank regulation or deposit insurance"},
        },
    },
}

ECONOMIC_HISTORY = [
    {
        "year": "1776",
        "event": "The Wealth of Nations",
        "description": "Adam Smith publishes *The Wealth of Nations*, founding modern economics. Key ideas: division of labor, the 'invisible hand' of markets, free trade over mercantilism.",
        "lesson": "Markets can coordinate complex activity without central direction through price signals.",
        "era": "Classical Economics",
    },
    {
        "year": "1848",
        "event": "The Communist Manifesto",
        "description": "Marx & Engels argue capitalism creates class conflict. Predicts worker revolution. Capital accumulation leads to immiseration of the proletariat.",
        "lesson": "Capitalism generates distributional conflicts that pure market theory ignored — labor conditions and inequality became central economic questions.",
        "era": "Political Economy",
    },
    {
        "year": "1890",
        "event": "Marshall's Principles of Economics",
        "description": "Alfred Marshall develops supply and demand curves, consumer surplus, and elasticity — establishing the neoclassical framework that still dominates microeconomics.",
        "lesson": "Marginal analysis (thinking at the margin) is the key to understanding economic decisions.",
        "era": "Neoclassical Economics",
    },
    {
        "year": "1914–1918",
        "event": "World War I & War Economies",
        "description": "Governments mobilize economies for total war. Gold standard suspended. First major experience of government-directed production. Post-war reparations (Versailles Treaty) set stage for instability.",
        "lesson": "Keynes warned in *The Economic Consequences of the Peace* (1919) that punitive reparations would destabilize Germany — a prediction that proved tragically correct.",
        "era": "War & Interwar",
    },
    {
        "year": "1929",
        "event": "The Great Crash & Great Depression",
        "description": "Stock market crashes in October 1929. By 1933, US unemployment hits 25%. GDP falls ~30%. Banks collapse. The Smoot-Hawley Tariff Act worsens global depression through trade wars.",
        "lesson": "Bank panics and monetary contraction can turn recessions into depressions. Milton Friedman blamed the Fed for letting the money supply collapse by 1/3.",
        "era": "Great Depression",
    },
    {
        "year": "1936",
        "event": "Keynes: The General Theory",
        "description": "John Maynard Keynes publishes *The General Theory of Employment, Interest and Money* — arguing markets don't automatically clear, unemployment can persist, and government spending can stimulate demand.",
        "lesson": "During depressions, aggregate demand fails. Government must step in. 'In the long run we are all dead' — waiting for market self-correction is not always viable.",
        "era": "Keynesian Revolution",
    },
    {
        "year": "1944",
        "event": "Bretton Woods Conference",
        "description": "44 Allied nations meet in New Hampshire and design the post-war international monetary system: fixed exchange rates tied to the US dollar, which is tied to gold ($35/oz). IMF and World Bank created.",
        "lesson": "International cooperation can build stable monetary frameworks. But the Triffin Dilemma eventually doomed Bretton Woods.",
        "era": "Post-War Order",
    },
    {
        "year": "1971",
        "event": "Nixon Closes the Gold Window",
        "description": "Nixon unilaterally ends dollar-gold convertibility — ending Bretton Woods. The world moves to floating exchange rates. The 'Nixon Shock' fundamentally changes international finance.",
        "lesson": "The Triffin Dilemma proved irresolvable. Floating rates give nations more monetary policy autonomy but introduce currency volatility.",
        "era": "Post-Bretton Woods",
    },
    {
        "year": "1973–1974",
        "event": "Oil Crisis & Stagflation",
        "description": "OPEC oil embargo quadruples oil prices. Western economies hit by inflation AND recession simultaneously — stagflation — which simple Keynesian models couldn't explain.",
        "lesson": "Supply shocks can cause both inflation and unemployment at once, breaking the simple Phillips Curve trade-off.",
        "era": "Stagflation Era",
    },
    {
        "year": "1979–1982",
        "event": "Volcker's War on Inflation",
        "description": "Fed Chair Paul Volcker raises the federal funds rate to ~20% to crush 13% inflation. The 'Volcker Shock' causes a severe recession (unemployment peaks at 10.8%) but breaks the inflationary spiral.",
        "lesson": "Inflation can be beaten with credible, sustained tight monetary policy — but at enormous short-run cost. Established the importance of central bank credibility.",
        "era": "Monetarist Revolution",
    },
    {
        "year": "1980s",
        "event": "Reagan & Thatcher: Supply-Side Revolution",
        "description": "Reagan (US) and Thatcher (UK) implement tax cuts, deregulation, and union-busting. The idea: supply-side incentives drive growth. Deficits rise sharply in the US ('voodoo economics' per critics).",
        "lesson": "Tax cuts can stimulate growth, but 'trickle-down' effects on inequality are weak. The debate between supply-side and demand-side economics continues.",
        "era": "Neoliberal Era",
    },
    {
        "year": "1989–1991",
        "event": "Fall of the Berlin Wall & Soviet Collapse",
        "description": "Communist bloc collapses. 'Shock therapy' transitions in Eastern Europe — rapid privatization and liberalization. Washington Consensus spreads globally: free markets, fiscal discipline, openness.",
        "lesson": "Rapid vs. gradual transition matters enormously. Russia's shock therapy led to oligarchic capture. China's gradual approach preserved institutional capacity.",
        "era": "Post-Cold War",
    },
    {
        "year": "1997–1998",
        "event": "Asian Financial Crisis",
        "description": "Fixed exchange rates, large capital inflows, and current account deficits leave Asian economies (Thailand, Indonesia, South Korea) vulnerable. Speculative attacks crash currencies. IMF bailouts with harsh austerity conditions.",
        "lesson": "Capital account liberalization without strong financial regulation creates crisis vulnerability. Fixed exchange rates can collapse under speculative attack.",
        "era": "Emerging Market Crises",
    },
    {
        "year": "2001",
        "event": "Dot-com Bust",
        "description": "Internet stock bubble collapses. NASDAQ falls 78% from peak. Trillions in paper wealth evaporate. The Fed responds by cutting rates aggressively — sowing seeds of the housing bubble.",
        "lesson": "'This time is different' is the most expensive phrase in finance. Technological innovation doesn't override the need for profits eventually.",
        "era": "Dot-Com Era",
    },
    {
        "year": "2008",
        "event": "Global Financial Crisis",
        "description": "US housing bubble collapses. Lehman Brothers fails (Sept 15, 2008). Global financial system freezes. The Fed, Treasury, and Congress conduct massive bailouts (TARP). Great Recession: deepest since 1930s.",
        "lesson": "Financial innovation (securitization, CDOs) can obscure risk and create systemic fragility. Regulation lags innovation dangerously.",
        "era": "Global Financial Crisis",
    },
    {
        "year": "2010–2012",
        "event": "Eurozone Debt Crisis",
        "description": "Greece, Ireland, Portugal, Spain, and Italy face sovereign debt crises. ECB (Mario Draghi): 'whatever it takes' to preserve the euro. Austerity programs imposed in exchange for bailouts, causing deep recessions.",
        "lesson": "Monetary union without fiscal union creates asymmetric shocks with no adjustment mechanism. The euro's design had fundamental flaws that nearly destroyed it.",
        "era": "Eurozone Crisis",
    },
    {
        "year": "2020",
        "event": "COVID-19 Pandemic Shock",
        "description": "Largest peacetime economic shock in a century. GDP falls sharply but recovers rapidly due to unprecedented fiscal (stimulus checks, PPP loans) and monetary (QE, near-zero rates) response. Supply chain disruptions cause inflation spike in 2021-22.",
        "lesson": "Fast, large-scale government intervention can prevent depression. But the inflation consequence of massive stimulus + supply shocks was underestimated.",
        "era": "COVID Era",
    },
    {
        "year": "2022–2023",
        "event": "Post-COVID Inflation Surge",
        "description": "CPI hits 9.1% in June 2022 (US) — highest in 40 years. Fed hikes rates from 0.25% to 5.5% in 16 months, the fastest tightening in modern history. Economy achieves 'soft landing' by late 2023.",
        "lesson": "Persistently easy monetary policy + fiscal stimulus + supply constraints can produce inflation even in developed economies. Inflation once unanchored is costly to control.",
        "era": "Post-COVID Era",
    },
]

QUIZ_QUESTIONS = {
    "Beginner": [
        {
            "q": "What happens to the price of a good when supply decreases and demand stays the same?",
            "options": ["A) Price falls", "B) Price rises", "C) Price stays the same", "D) Quantity demanded falls to zero"],
            "answer": "B",
            "explanation": "With the same demand but less supply, the equilibrium price rises — there are fewer goods competing for the same buyers.",
        },
        {
            "q": "Which formula correctly represents GDP using the expenditure approach?",
            "options": ["A) GDP = C + I + G + T", "B) GDP = C + I + G + (X - M)", "C) GDP = C + S + G + X", "D) GDP = C + I - G + (X - M)"],
            "answer": "B",
            "explanation": "GDP = Consumer spending + Investment + Government spending + Net Exports (Exports minus Imports).",
        },
        {
            "q": "Inflation of 4% and a nominal interest rate of 6% gives you a real interest rate of approximately:",
            "options": ["A) 10%", "B) 4%", "C) 2%", "D) -2%"],
            "answer": "C",
            "explanation": "Real rate ≈ Nominal rate − Inflation rate = 6% − 4% = 2%. The Fisher equation gives the exact value.",
        },
        {
            "q": "The Federal Reserve's 'dual mandate' refers to its goals of:",
            "options": ["A) Low inflation and a strong dollar", "B) Maximum employment and stable prices", "C) Low deficits and high growth", "D) Trade balance and currency stability"],
            "answer": "B",
            "explanation": "The Fed is legally mandated to pursue both maximum employment and price stability (around 2% inflation).",
        },
        {
            "q": "When a government spends more than it collects in taxes, this is called a:",
            "options": ["A) Trade deficit", "B) Current account surplus", "C) Budget deficit", "D) Primary surplus"],
            "answer": "C",
            "explanation": "A budget deficit occurs when government spending exceeds tax revenue in a given period.",
        },
        {
            "q": "What is 'comparative advantage'?",
            "options": ["A) Producing more of everything than other countries", "B) Lower opportunity cost in producing a good relative to others", "C) Having more natural resources than trade partners", "D) A country's technological superiority"],
            "answer": "B",
            "explanation": "Comparative advantage is about opportunity costs, not absolute productivity. Even if one country is better at everything, trade can still benefit both sides.",
        },
        {
            "q": "The law of demand states that:",
            "options": ["A) As income rises, demand rises", "B) As price rises, quantity demanded falls", "C) As supply rises, demand falls", "D) As price falls, supply falls"],
            "answer": "B",
            "explanation": "The law of demand describes an inverse relationship between price and quantity demanded, all else equal.",
        },
        {
            "q": "Which of these best describes 'GDP per capita'?",
            "options": ["A) Total value of exports per year", "B) Average income of government workers", "C) Total GDP divided by the population", "D) GDP adjusted for inflation"],
            "answer": "C",
            "explanation": "GDP per capita = Total GDP / Population. It's a better measure of average living standards than total GDP.",
        },
    ],
    "Intermediate": [
        {
            "q": "If a good has a price elasticity of demand of -2.5, it is considered:",
            "options": ["A) Inelastic", "B) Unit elastic", "C) Elastic", "D) Perfectly inelastic"],
            "answer": "C",
            "explanation": "When |PED| > 1, demand is elastic — consumers are very responsive to price changes.",
        },
        {
            "q": "The Solow Growth Model predicts that poor countries will grow faster than rich ones due to:",
            "options": ["A) Higher population growth", "B) More democracy", "C) Diminishing returns to capital (convergence)", "D) Better monetary policy"],
            "answer": "C",
            "explanation": "Poor countries have less capital, so the marginal return to each unit of capital is higher — they grow faster until reaching steady state.",
        },
        {
            "q": "The Taylor Rule primarily determines:",
            "options": ["A) The optimal fiscal deficit", "B) The target interest rate for central banks", "C) The exchange rate policy", "D) The optimal tariff rate"],
            "answer": "B",
            "explanation": "The Taylor Rule is a formula prescribing the appropriate interest rate based on inflation and the output gap.",
        },
        {
            "q": "Ricardian Equivalence predicts that tax cuts will:",
            "options": ["A) Always stimulate GDP significantly", "B) Be offset by increased private saving for future taxes", "C) Reduce interest rates immediately", "D) Increase the money supply"],
            "answer": "B",
            "explanation": "Robert Barro's Ricardian Equivalence: rational consumers save the tax cut to pay future taxes, offsetting the stimulus.",
        },
        {
            "q": "What does an inverted yield curve typically signal?",
            "options": ["A) High current inflation", "B) Strong economic growth ahead", "C) An upcoming recession", "D) Currency depreciation"],
            "answer": "C",
            "explanation": "An inverted yield curve (short-term rates > long-term rates) has preceded every US recession since the 1950s.",
        },
        {
            "q": "The 'impossible trinity' (Mundell-Fleming trilemma) states a country cannot simultaneously have:",
            "options": ["A) Low inflation, full employment, and trade balance", "B) Fixed exchange rate, free capital movement, and independent monetary policy", "C) High growth, low debt, and trade surplus", "D) Free trade, welfare state, and low taxes"],
            "answer": "B",
            "explanation": "A country must choose two of the three: fixed exchange rate, free capital flows, and monetary policy autonomy.",
        },
        {
            "q": "A negative externality causes the market to:",
            "options": ["A) Underproduce the good", "B) Overproduce the good relative to the social optimum", "C) Produce exactly the right amount", "D) Always require government subsidies"],
            "answer": "B",
            "explanation": "With a negative externality, the social cost exceeds the private cost, so the market ignores external costs and overproduces.",
        },
        {
            "q": "According to the Efficient Market Hypothesis (semi-strong form), which of the following CAN earn above-market returns?",
            "options": ["A) Fundamental analysis (studying company financials)", "B) Technical analysis (studying past price patterns)", "C) Insider trading using private information", "D) None — the market is always efficient"],
            "answer": "C",
            "explanation": "Semi-strong EMH says all *public* information is priced in. Only truly private information (insider trading) could theoretically beat the market — and it's also illegal.",
        },
    ],
    "Advanced": [
        {
            "q": "In the IS-LM model at the Zero Lower Bound, a fiscal expansion will:",
            "options": ["A) Be completely crowded out by rising interest rates", "B) Have a smaller multiplier than during normal times", "C) Have a larger multiplier because monetary policy cannot offset it", "D) Have no effect due to Ricardian Equivalence"],
            "answer": "C",
            "explanation": "At the ZLB, monetary policy cannot tighten to offset fiscal expansion, so the full multiplier applies without crowding out via interest rates.",
        },
        {
            "q": "The Kydland-Prescott time inconsistency problem arises because:",
            "options": ["A) Tax policy takes time to implement", "B) Governments promise low inflation but have incentives to inflate once expectations are set", "C) Central banks respond too slowly to economic shocks", "D) Bond markets cannot predict future policy"],
            "answer": "B",
            "explanation": "Once the private sector sets wages based on expected low inflation, the government has an incentive to inflate and boost employment — but rational agents anticipate this and don't believe the promise.",
        },
        {
            "q": "In Minsky's financial instability hypothesis, a 'Minsky moment' occurs when:",
            "options": ["A) Interest rates hit the zero lower bound", "B) Speculative and Ponzi borrowers are forced to sell assets to service debts, causing a crash", "C) The central bank unexpectedly raises rates", "D) Government debt reaches 100% of GDP"],
            "answer": "B",
            "explanation": "Minsky describes how speculative borrowing grows in booms until cash flows can't cover debt — then forced selling triggers a collapse.",
        },
        {
            "q": "The Triffin Dilemma describes the contradiction that:",
            "options": ["A) Trade deficits require capital surpluses", "B) The reserve currency country must run deficits to supply liquidity, undermining confidence in the currency", "C) Fixed exchange rates cannot coexist with free capital flows", "D) Fiscal and monetary policy cannot simultaneously be expansionary"],
            "answer": "B",
            "explanation": "Robert Triffin noted the US had to run deficits to supply global dollar liquidity, but deficits would eventually erode confidence in the dollar's gold backing.",
        },
        {
            "q": "According to Acemoglu & Robinson, the PRIMARY determinant of long-run economic development is:",
            "options": ["A) Geographic location and climate", "B) Cultural and religious values", "C) Political and economic institutions (inclusive vs. extractive)", "D) Natural resource endowments"],
            "answer": "C",
            "explanation": "In *Why Nations Fail*, Acemoglu & Robinson argue inclusive institutions (property rights, rule of law, competitive politics) drive growth; geography and culture are secondary.",
        },
        {
            "q": "The Stolper-Samuelson theorem implies that free trade in developed (capital-abundant) countries will:",
            "options": ["A) Increase wages of all workers", "B) Reduce returns to unskilled labor (the scarce factor)", "C) Increase returns to both capital and labor", "D) Have no distributional effects"],
            "answer": "B",
            "explanation": "Stolper-Samuelson: trade raises returns to the abundant factor (capital in rich countries) and lowers returns to the scarce factor (unskilled labor) — explaining trade's role in wage inequality.",
        },
        {
            "q": "Quantitative Easing (QE) differs from traditional monetary policy primarily because it:",
            "options": ["A) Changes the federal funds rate", "B) Directly purchases long-term assets to reduce long-term yields when short-term rates are at zero", "C) Is conducted by the Treasury, not the central bank", "D) Directly transfers money to households"],
            "answer": "B",
            "explanation": "QE bypasses the short-term rate (already at ZLB) and targets long-term rates directly through large-scale asset purchases.",
        },
        {
            "q": "MV = PQ (Quantity Theory of Money) suggests that if money velocity (V) collapses after a financial crisis:",
            "options": ["A) Money supply expansion will reliably cause inflation", "B) Fiscal policy becomes more effective than monetary policy", "C) Money supply expansion may not cause proportional inflation", "D) Interest rates must rise to restore velocity"],
            "answer": "C",
            "explanation": "Post-2008: the Fed tripled the monetary base but inflation stayed low because V collapsed (banks hoarded reserves). M×V = P×Q, so falling V offset rising M.",
        },
    ],
}

SCENARIO_EXERCISES = {
    "Beginner": [
        {
            "scenario": "🌽 The Corn Crisis",
            "situation": "A drought destroys 40% of the US corn crop. Corn is used in food, animal feed, and ethanol fuel.",
            "question": "What do you predict will happen to: (1) the price of corn, (2) the price of beef, and (3) the price of gasoline?",
            "answer": "1. Corn price RISES (supply decreased, demand unchanged → shortage → higher price). 2. Beef price RISES (corn = cow feed → input cost rises → supply of beef shifts left → price rises). 3. Gasoline price RISES (ethanol is a substitute/blend for gasoline; if corn is scarce, ethanol is scarce, and gasoline demand rises OR ethanol prices rise). This is called a 'supply chain ripple effect' or 'derived demand.'",
            "key_concept": "Supply shocks ripple through interconnected markets via input costs and substitutes.",
        },
        {
            "scenario": "🏠 The Housing Boom",
            "situation": "The government launches a program giving first-time homebuyers a $20,000 subsidy. At the same time, construction costs rise due to a lumber shortage.",
            "question": "What happens to house prices? Who wins and who loses from this policy?",
            "answer": "Demand RISES (subsidy makes buying more attractive → demand curve shifts right). Supply contracts (higher lumber costs shift supply left). Result: prices RISE significantly. Winners: Existing homeowners (wealth increases), real estate agents, sellers. Losers: Non-first-time buyers (prices rose and they get no subsidy), renters (housing becomes less affordable), taxpayers (funding the subsidy). The policy may help first-time buyers less than intended because prices adjust up.",
            "key_concept": "Subsidies that boost demand often get partially captured as higher prices, especially if supply is constrained.",
        },
    ],
    "Intermediate": [
        {
            "scenario": "🏦 The Fed's Dilemma",
            "situation": "It's 2022. Inflation is running at 8% (well above the 2% target). Unemployment is at 3.5% (below the natural rate). But housing prices are already falling and the stock market is down 25%.",
            "question": "Should the Fed raise interest rates aggressively, raise them slowly, or hold rates steady? Walk through the trade-offs using the Taylor Rule framework.",
            "answer": "Taylor Rule says: with inflation 6 points above target and a positive output gap (unemployment below NAIRU), rates should be raised substantially — perhaps to 4-5% or higher. Aggressive raises: faster reduction in inflation, at the cost of higher unemployment and risk of recession. Slower raises: less economic disruption, but risk of inflation becoming entrenched in expectations. This was essentially the 2022 debate. The Fed chose aggressive (from 0.25% to 5.5% in 16 months). Outcome: inflation fell substantially, no severe recession (a 'soft landing') — but housing market froze. The Taylor Rule analysis supports aggressive action when inflation is well above target.",
            "key_concept": "The Taylor Rule provides a systematic framework for rate decisions, but the severity of the off-target conditions and lag effects require judgment.",
        },
        {
            "scenario": "📉 The Asian Tiger's Trap",
            "situation": "Thailand (1997) had: fixed exchange rate pegged to the dollar, large current account deficit, and booming capital inflows. Speculators began to doubt the peg could be maintained.",
            "question": "Explain why the fixed peg made Thailand vulnerable and what happened when speculators attacked it. Use the Impossible Trinity to frame your answer.",
            "answer": "The Impossible Trinity: Thailand had chosen a fixed exchange rate + free capital flows. To maintain the peg with free capital flows, they had to sacrifice monetary independence — using reserves to buy baht when attacked. When speculators shorted the baht, the Bank of Thailand burned through its dollar reserves defending the peg. Eventually reserves ran out → they had to float → baht collapsed 40%+ → all corporations with dollar-denominated debt became instantly insolvent → banking crisis → IMF bailout with harsh conditions. Lesson: You CANNOT maintain a fixed rate under sustained speculative pressure if you also have free capital flows.",
            "key_concept": "The Impossible Trinity is not just theoretical — capital mobility makes fixed exchange rates extremely fragile under speculative attacks.",
        },
    ],
    "Advanced": [
        {
            "scenario": "🌍 The Sovereign Debt Spiral",
            "situation": "A country has 120% debt-to-GDP. The real interest rate on its debt is 4%. Real GDP growth is 1%. Markets are nervous. The government must choose: (A) Austerity (cut spending, raise taxes), (B) Default / restructuring, or (C) Monetization (have the central bank print money).",
            "question": "Evaluate each option using the debt sustainability condition (r vs. g) and the political-economic constraints of each choice.",
            "answer": "r(4%) > g(1%): debt is on an unsustainable path — it will grow as % of GDP. Option A (Austerity): primary surplus can stop the debt spiral IF large enough. But Blanchard 2012 showed multipliers are high in crisis → austerity cuts GDP → debt ratio may WORSEN. Political costs are severe (Greece riots). Works if confidence restored, rates fall, and growth returns. Option B (Default): Stops the debt service math immediately. But devastating to credibility — cut off from capital markets for years, domestic banking sector (holding government bonds) collapses. Works best if debt is largely external (Argentina), catastrophic if domestic. Option C (Monetization): Only works if country issues debt in its OWN currency. Risk: hyperinflation if overused. The ECB prevented Eurozone members from using this option. Summary: The optimal path is often a combination: moderate fiscal adjustment (not extreme austerity) + debt restructuring with creditors + growth-enhancing structural reforms. Greece got forced austerity without restructuring initially — the IMF later admitted this was a mistake.",
            "key_concept": "Debt sustainability requires r < g; but the policy response to an unsustainable path involves severe trade-offs between creditor losses, output losses, and inflation risk.",
        },
        {
            "scenario": "🏭 Industrial Policy Bet",
            "situation": "The US CHIPS Act (2022) commits $52B to semiconductor manufacturing subsidies to build domestic chip fabs. Critics say this is inefficient industrial policy; supporters say it's necessary for national security and supply chain resilience.",
            "question": "Evaluate the economic case for and against this policy using market failure theory, comparative advantage, and infant industry arguments.",
            "answer": "FOR: 1. National security externality: semiconductors are critical for defense/critical infrastructure — a market failure (positive externality not priced by markets) justifies subsidy. 2. Supply chain externality: the 2020-21 chip shortage disrupted the entire US economy — a systemic risk the market underpriced. 3. Infant industry: US fabs need to rebuild scale — time-limited protection is justified. 4. Geopolitical insurance: overconcentration in Taiwan creates tail risk (Taiwan Strait conflict). AGAINST: 1. Comparative advantage: TSMC in Taiwan produces chips far more efficiently — subsidizing US fabs destroys value and misallocates resources. 2. Government failure risk: picking winners historically fails (Solyndra). 3. Escalation risk: invites WTO challenges and foreign retaliation. 4. Cost: $52B may subsidize activity that would happen anyway ('additionality' problem). VERDICT: The national security and systemic risk externality arguments are the strongest. Pure comparative advantage arguments are insufficient when geopolitical risk is high. But implementation efficiency and avoiding subsidy capture matter enormously.",
            "key_concept": "Market failure arguments can justify industrial policy, but the quality of government intervention matters as much as whether intervention is warranted in principle.",
        },
    ],
}

FILL_IN_BLANKS = [
    {
        "sentence": "GDP = ___ + Investment + Government Spending + Net Exports",
        "answer": "Consumer Spending (C)",
        "hint": "The biggest component, ~70% of US GDP",
        "level": "Beginner",
    },
    {
        "sentence": "When price rises, quantity demanded falls — this is the Law of ___.",
        "answer": "Demand",
        "hint": "The fundamental inverse relationship between price and quantity bought",
        "level": "Beginner",
    },
    {
        "sentence": "The ___ is the central bank of the United States.",
        "answer": "Federal Reserve (the Fed)",
        "hint": "Created in 1913, it sets US monetary policy",
        "level": "Beginner",
    },
    {
        "sentence": "Inflation rate minus the nominal interest rate gives the ___ interest rate.",
        "answer": "Real",
        "hint": "Adjusted for purchasing power loss",
        "level": "Beginner",
    },
    {
        "sentence": "The ___ Curve shows the short-run trade-off between inflation and unemployment.",
        "answer": "Phillips",
        "hint": "Named after New Zealand economist A.W. Phillips",
        "level": "Intermediate",
    },
    {
        "sentence": "MV = PQ is the ___ of Money, where V is the velocity of money.",
        "answer": "Quantity Theory",
        "hint": "Links money supply to price level",
        "level": "Intermediate",
    },
    {
        "sentence": "A country cannot simultaneously maintain a fixed exchange rate, free capital flows, and independent monetary policy — this is the ___.",
        "answer": "Impossible Trinity (Mundell-Fleming Trilemma)",
        "hint": "Choose any two of three",
        "level": "Intermediate",
    },
    {
        "sentence": "The ___ theorem states that if property rights are well-defined, private negotiation can solve externality problems.",
        "answer": "Coase",
        "hint": "Ronald ___ won the Nobel Prize in 1991",
        "level": "Intermediate",
    },
    {
        "sentence": "According to the Efficient Market Hypothesis, ___ form states even inside information is priced in.",
        "answer": "Strong",
        "hint": "The most extreme version of the EMH",
        "level": "Advanced",
    },
    {
        "sentence": "The debt sustainability condition requires that the real interest rate (r) be ___ than the real GDP growth rate (g).",
        "answer": "Less (r < g)",
        "hint": "If this isn't satisfied, the debt/GDP ratio grows without bound",
        "level": "Advanced",
    },
    {
        "sentence": "Kydland and Prescott argued central banks face a ___ problem — the optimal policy announced in advance may not be optimal to carry out later.",
        "answer": "Time inconsistency",
        "hint": "This is why central bank credibility and commitment matter so much",
        "level": "Advanced",
    },
    {
        "sentence": "___ is the revenue a government earns from creating new money — effectively a tax on money holders.",
        "answer": "Seigniorage",
        "hint": "Excessive use of this leads to hyperinflation",
        "level": "Advanced",
    },
]

CONCEPT_CONNECTIONS = [
    {
        "title": "Connect: Inflation → Interest Rates → GDP",
        "concepts": ["Inflation rises", "Fed raises rates", "Borrowing costs up", "Investment falls", "GDP growth slows", "Unemployment rises", "Wage growth slows", "Inflation falls"],
        "description": "Trace how an inflation spike triggers a chain of cause and effect through the economy.",
        "level": "Beginner",
    },
    {
        "title": "Connect: Asset Bubble Formation",
        "concepts": ["Low interest rates", "Cheap credit", "Asset price rises", "Collateral value rises", "More borrowing", "More asset buying", "Prices rise further", "MINSKY MOMENT: debt can't be serviced", "Forced selling", "Prices crash", "Credit tightens"],
        "description": "Hyman Minsky's financial instability hypothesis — trace how booms sow the seeds of busts.",
        "level": "Intermediate",
    },
    {
        "title": "Connect: Trade Deficit Mechanics",
        "concepts": ["US consumers prefer imports", "Imports > Exports", "Trade deficit", "Dollars flow abroad", "Foreigners invest dollars in US assets", "Capital account surplus", "Foreign demand for US bonds", "Interest rates stay low", "More consumption, less saving"],
        "description": "The balance of payments accounting identity: trade deficit = capital account surplus.",
        "level": "Advanced",
    },
]

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────

def init_state():
    defaults = {
        "level": "Beginner",
        "topic": "Supply & Demand",
        "page": "Home",
        "score": 0,
        "total_answered": 0,
        "correct_answered": 0,
        "streak": 0,
        "daily_done": set(),
        "quiz_answered": {},
        "fill_answers": {},
        "xp": 0,
        "badges": [],
        "history_idx": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# DAILY LESSON SELECTOR
# ─────────────────────────────────────────────

def get_daily_topic():
    day_num = (date.today() - date(2024, 1, 1)).days
    topic_list = list(TOPICS.keys())
    return topic_list[day_num % len(topic_list)]

# ─────────────────────────────────────────────
# XP & BADGE SYSTEM
# ─────────────────────────────────────────────

def award_xp(amount, reason=""):
    st.session_state.xp += amount
    check_badges()

def check_badges():
    badges = st.session_state.badges
    xp = st.session_state.xp
    correct = st.session_state.correct_answered
    if xp >= 100 and "First 100 XP" not in badges:
        badges.append("First 100 XP")
    if xp >= 500 and "500 XP Club" not in badges:
        badges.append("500 XP Club")
    if correct >= 5 and "Quiz Starter" not in badges:
        badges.append("Quiz Starter")
    if correct >= 20 and "Quiz Master" not in badges:
        badges.append("Quiz Master")
    if st.session_state.streak >= 3 and "3-Day Streak" not in badges:
        badges.append("3-Day Streak")

BADGE_ICONS = {
    "First 100 XP": "🥉",
    "500 XP Club": "🥇",
    "Quiz Starter": "📝",
    "Quiz Master": "🎓",
    "3-Day Streak": "🔥",
}

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 800; color: #1a1a2e !important; margin-bottom: 0; }
    .subtitle { color: #444 !important; margin-top: 0; margin-bottom: 1.5rem; }
    .card { background: #f0f4ff !important; color: #111 !important; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; border-left: 4px solid #0066cc; }
    .card * { color: #111 !important; }
    .card-green { border-left-color: #28a745 !important; background: #e6f9ec !important; }
    .card-red { border-left-color: #dc3545 !important; background: #fdecea !important; }
    .card-gold { border-left-color: #e6a817 !important; background: #fff8e1 !important; }
    .level-badge { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
    .beginner { background: #dbeafe !important; color: #1e40af !important; }
    .intermediate { background: #ffedd5 !important; color: #c2410c !important; }
    .advanced { background: #fce7f3 !important; color: #9d174d !important; }
    .xp-bar { background: #d1d5db; border-radius: 10px; height: 12px; overflow: hidden; }
    .xp-fill { background: linear-gradient(90deg, #0066cc, #00ccaa); border-radius: 10px; height: 12px; }
    .history-card { background: #f9fafb !important; color: #111 !important; border-radius: 10px; padding: 1rem 1.5rem; margin-bottom: 1rem; border: 1px solid #e5e7eb; }
    .history-card * { color: #111 !important; }
    .era-tag { background: #1a1a2e !important; color: #fff !important; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; }
    .concept-box { background: #dbeafe !important; border-radius: 8px; padding: 0.6rem 1rem; margin: 0.3rem; display: inline-block; font-weight: 600; color: #1e3a8a !important; font-size: 0.9rem; }
    .chain-arrow { font-size: 1.5rem; color: #0066cc !important; margin: 0.2rem; }
    .stButton > button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📈 EconoLearn")
    st.markdown("---")

    # XP display
    xp = st.session_state.xp
    xp_level = min(xp // 100, 10)
    xp_progress = (xp % 100) / 100
    st.markdown(f"**XP: {xp}** | Level {xp_level}")
    st.markdown(f"""
    <div class="xp-bar"><div class="xp-fill" style="width:{int(xp_progress*100)}%">&nbsp;</div></div>
    """, unsafe_allow_html=True)

    if st.session_state.badges:
        badge_str = " ".join([BADGE_ICONS.get(b, "🏅") for b in st.session_state.badges])
        st.markdown(f"**Badges**: {badge_str}")

    st.markdown(f"**Streak**: {'🔥' * min(st.session_state.streak, 7)} {st.session_state.streak} days")
    st.markdown(f"**Quiz accuracy**: {st.session_state.correct_answered}/{st.session_state.total_answered}")

    st.markdown("---")
    st.markdown("### Navigation")
    pages = ["Home", "Daily Lesson", "Quiz", "Scenarios", "Fill in the Blanks", "Concept Chains", "Economic History", "My Progress"]
    page_icons = ["🏠", "📚", "❓", "🎯", "✍️", "🔗", "🏛️", "📊"]
    for icon, pg in zip(page_icons, pages):
        if st.button(f"{icon} {pg}", key=f"nav_{pg}", use_container_width=True):
            st.session_state.page = pg

    st.markdown("---")
    st.markdown("### Level")
    for lvl in LEVELS:
        cls = lvl.lower()
        badge = f'<span class="level-badge {cls}">{lvl}</span>'
        if st.button(lvl, key=f"lvl_{lvl}", use_container_width=True):
            st.session_state.level = lvl
            st.rerun()
    st.markdown(f"**Active**: {st.session_state.level}")

    st.markdown("---")
    st.markdown("### Topic")
    selected_topic = st.selectbox("Focus topic", list(TOPICS.keys()), index=list(TOPICS.keys()).index(st.session_state.topic), label_visibility="collapsed")
    if selected_topic != st.session_state.topic:
        st.session_state.topic = selected_topic
        st.rerun()

# ─────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────

page = st.session_state.page
level = st.session_state.level
topic = st.session_state.topic

# ── HOME ──────────────────────────────────────
if page == "Home":
    st.markdown('<p class="main-title">📈 EconoLearn</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Master economics — from supply & demand to financial crises.</p>', unsafe_allow_html=True)

    daily_topic = get_daily_topic()
    today_str = str(date.today())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Your XP", f"{st.session_state.xp} XP")
    with col2:
        st.metric("Accuracy", f"{st.session_state.correct_answered}/{st.session_state.total_answered}" if st.session_state.total_answered else "—")
    with col3:
        st.metric("Streak", f"{st.session_state.streak} days 🔥")

    st.markdown("---")

    st.markdown(f"### Today's Topic: {TOPICS[daily_topic]} {daily_topic}")
    lesson = LESSONS.get(daily_topic, {}).get(level)
    if lesson:
        st.markdown(f"<div class='card'><b>{lesson['title']}</b><br><small>Level: <span class='level-badge {level.lower()}'>{level}</span></small></div>", unsafe_allow_html=True)
        if today_str not in st.session_state.daily_done:
            if st.button("Start Today's Lesson →", type="primary"):
                st.session_state.page = "Daily Lesson"
                st.session_state.topic = daily_topic
                st.session_state.daily_done.add(today_str)
                award_xp(10, "Daily lesson started")
                st.rerun()
        else:
            st.success("✅ Today's lesson completed! +10 XP earned.")

    st.markdown("---")
    st.markdown("### Quick Start")
    cols = st.columns(3)
    quick_actions = [("❓ Take a Quiz", "Quiz"), ("🎯 Scenario Exercise", "Scenarios"), ("🏛️ Economic History", "Economic History")]
    for col, (label, pg) in zip(cols, quick_actions):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.page = pg
                st.rerun()

    st.markdown("---")
    st.markdown("### Topics Available")
    topic_cols = st.columns(5)
    for i, (t, icon) in enumerate(TOPICS.items()):
        with topic_cols[i % 5]:
            has_lesson = t in LESSONS
            color = "#0055bb" if has_lesson else "#555555"
            st.markdown(f"<div style='text-align:center;padding:8px;background:#dbeafe;border-radius:8px;margin:4px;font-size:0.85rem;'><span style='color:{color};font-weight:700;'>{icon} {t}</span></div>", unsafe_allow_html=True)

# ── DAILY LESSON ──────────────────────────────
elif page == "Daily Lesson":
    lesson = LESSONS.get(topic, {}).get(level)

    st.markdown(f"### {TOPICS.get(topic, '📚')} {topic}")
    st.markdown(f"<span class='level-badge {level.lower()}'>{level}</span>", unsafe_allow_html=True)

    if not lesson:
        st.info(f"No lesson yet for '{topic}' at {level} level. Try another topic or level!")
    else:
        st.markdown(f"## {lesson['title']}")
        st.markdown(lesson['content'])

        if lesson.get('key_terms'):
            st.markdown("---")
            st.markdown("### 🔑 Key Terms")
            cols = st.columns(2)
            for i, (term, definition) in enumerate(lesson['key_terms'].items()):
                with cols[i % 2]:
                    st.markdown(f"<div class='card'><b>{term}</b><br><small>{definition}</small></div>", unsafe_allow_html=True)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Take Quiz on This Topic →", type="primary"):
                st.session_state.page = "Quiz"
                st.rerun()
        with col2:
            if st.button("Try a Scenario →"):
                st.session_state.page = "Scenarios"
                st.rerun()

# ── QUIZ ──────────────────────────────────────
elif page == "Quiz":
    st.markdown(f"## ❓ Quiz — {level}")
    st.markdown(f"Topic filter: **{topic}** | Change topic in the sidebar to focus.")

    questions = QUIZ_QUESTIONS.get(level, [])
    if not questions:
        st.info("No quiz questions available for this level.")
    else:
        random.seed(hashlib.md5(f"{level}{date.today()}".encode()).hexdigest())
        selected_qs = random.sample(questions, min(5, len(questions)))

        for idx, q_data in enumerate(selected_qs):
            q_key = f"{level}_{idx}_{str(date.today())}"
            st.markdown(f"---\n**Q{idx+1}: {q_data['q']}**")

            answered = st.session_state.quiz_answered.get(q_key)

            if answered is None:
                for opt in q_data['options']:
                    letter = opt[0]
                    if st.button(opt, key=f"q_{q_key}_{letter}"):
                        correct = letter == q_data['answer']
                        st.session_state.quiz_answered[q_key] = {"chosen": letter, "correct": correct}
                        st.session_state.total_answered += 1
                        if correct:
                            st.session_state.correct_answered += 1
                            award_xp(15, "Correct quiz answer")
                        else:
                            award_xp(2, "Quiz attempt")
                        st.rerun()
            else:
                chosen = answered['chosen']
                correct = answered['correct']
                for opt in q_data['options']:
                    letter = opt[0]
                    if letter == q_data['answer']:
                        st.markdown(f"✅ **{opt}**")
                    elif letter == chosen and not correct:
                        st.markdown(f"❌ ~~{opt}~~")
                    else:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;{opt}")

                if correct:
                    st.markdown(f"<div class='card card-green'>✅ Correct! +15 XP<br><small>{q_data['explanation']}</small></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card card-red'>❌ The answer was **{q_data['answer']}**.<br><small>{q_data['explanation']}</small></div>", unsafe_allow_html=True)

        answered_today = sum(1 for k in st.session_state.quiz_answered if str(date.today()) in k and level in k)
        total_today = len(selected_qs)

        st.markdown("---")
        st.markdown(f"**Progress today**: {answered_today}/{total_today} questions answered")

        if answered_today >= total_today:
            correct_today = sum(1 for k, v in st.session_state.quiz_answered.items() if str(date.today()) in k and level in k and v['correct'])
            pct = int(correct_today / total_today * 100)
            if pct == 100:
                st.balloons()
                st.success(f"🎉 Perfect score! {correct_today}/{total_today} — you're crushing it!")
            elif pct >= 60:
                st.success(f"Good work! {correct_today}/{total_today} correct ({pct}%)")
            else:
                st.warning(f"{correct_today}/{total_today} correct ({pct}%). Review the lessons and try again tomorrow!")

            if st.button("Try Different Level"):
                st.session_state.quiz_answered = {}
                st.rerun()

# ── SCENARIOS ─────────────────────────────────
elif page == "Scenarios":
    st.markdown(f"## 🎯 Scenario Exercises — {level}")
    st.markdown("Apply your knowledge to real-world situations. Think it through before revealing the answer.")

    scenarios = SCENARIO_EXERCISES.get(level, [])
    if not scenarios:
        st.info("No scenario exercises for this level yet. Try Beginner or Intermediate!")
    else:
        for i, s in enumerate(scenarios):
            st.markdown(f"---")
            st.markdown(f"### {s['scenario']}")
            st.markdown(f"<div class='card'>{s['situation']}</div>", unsafe_allow_html=True)
            st.markdown(f"**❓ {s['question']}**")

            reveal_key = f"scenario_reveal_{level}_{i}"
            if reveal_key not in st.session_state:
                st.session_state[reveal_key] = False

            if not st.session_state[reveal_key]:
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Reveal Answer", key=f"reveal_{level}_{i}"):
                        st.session_state[reveal_key] = True
                        award_xp(5, "Scenario completed")
                        st.rerun()
            else:
                st.markdown(f"<div class='card card-green'><b>Answer & Analysis:</b><br><br>{s['answer']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='card card-gold'>💡 <b>Key Concept:</b> {s['key_concept']}</div>", unsafe_allow_html=True)

        st.markdown("---")
        other_levels = [l for l in LEVELS if l != level]
        st.markdown(f"Try scenarios at other levels: " + " | ".join(other_levels))

# ── FILL IN THE BLANKS ────────────────────────
elif page == "Fill in the Blanks":
    st.markdown(f"## ✍️ Fill in the Blanks — {level}")
    st.markdown("Complete the economic statement with the correct term.")

    level_qs = [q for q in FILL_IN_BLANKS if q['level'] == level]
    if not level_qs:
        st.info(f"No fill-in-the-blank exercises for {level} yet.")
    else:
        for i, q in enumerate(level_qs):
            st.markdown(f"---")
            st.markdown(f"**{i+1}. {q['sentence']}**")

            fib_key = f"fib_{level}_{i}"
            submitted_key = f"fib_sub_{level}_{i}"

            if submitted_key not in st.session_state:
                st.session_state[submitted_key] = None

            if st.session_state[submitted_key] is None:
                user_ans = st.text_input("Your answer:", key=fib_key, label_visibility="collapsed", placeholder="Type your answer here...")
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Check", key=f"fib_check_{level}_{i}"):
                        st.session_state[submitted_key] = user_ans
                        st.session_state.total_answered += 1
                        correct_words = q['answer'].lower().split()
                        user_words = user_ans.lower().split()
                        overlap = sum(1 for w in user_words if any(w in cw or cw in w for cw in correct_words))
                        if overlap >= min(2, len(correct_words)):
                            st.session_state.correct_answered += 1
                            award_xp(10, "Fill-in correct")
                        else:
                            award_xp(2, "Fill-in attempt")
                        st.rerun()
                with col2:
                    st.caption(f"💡 Hint: {q['hint']}")
            else:
                user_ans = st.session_state[submitted_key]
                correct_words = q['answer'].lower().split()
                user_words = user_ans.lower().split() if user_ans else []
                overlap = sum(1 for w in user_words if any(w in cw or cw in w for cw in correct_words))
                correct = overlap >= min(2, len(correct_words))

                if correct:
                    st.markdown(f"<div class='card card-green'>✅ Correct! Answer: <b>{q['answer']}</b></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card card-red'>❌ Your answer: '{user_ans}' | Correct: <b>{q['answer']}</b></div>", unsafe_allow_html=True)

        if st.button("Reset and try again"):
            for i in range(len(level_qs)):
                submitted_key = f"fib_sub_{level}_{i}"
                if submitted_key in st.session_state:
                    del st.session_state[submitted_key]
            st.rerun()

# ── CONCEPT CHAINS ────────────────────────────
elif page == "Concept Chains":
    st.markdown("## 🔗 Concept Chains")
    st.markdown("Understand how economic forces cascade through the system.")

    for chain in CONCEPT_CONNECTIONS:
        if chain['level'] == level or True:  # show all chains
            chain_level = chain['level']
            st.markdown(f"---")
            st.markdown(f"### {chain['title']}")
            st.markdown(f"<span class='level-badge {chain_level.lower()}'>{chain_level}</span>", unsafe_allow_html=True)
            st.markdown(f"*{chain['description']}*")

            st.markdown("<br>", unsafe_allow_html=True)
            chain_html = ""
            for j, concept in enumerate(chain['concepts']):
                chain_html += f"<span class='concept-box'>{concept}</span>"
                if j < len(chain['concepts']) - 1:
                    chain_html += "<span class='chain-arrow'> → </span>"
            st.markdown(chain_html, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

# ── ECONOMIC HISTORY ──────────────────────────
elif page == "Economic History":
    st.markdown("## 🏛️ Economic History")
    st.markdown("The biggest events that shaped the global economy — and the lessons they teach.")

    tab1, tab2 = st.tabs(["📜 Timeline", "🔍 Deep Dive"])

    with tab1:
        search = st.text_input("🔍 Search events (keyword, year, era):", placeholder="e.g., Great Depression, 2008, Keynesian")

        filtered = ECONOMIC_HISTORY
        if search:
            q = search.lower()
            filtered = [e for e in ECONOMIC_HISTORY if q in e['year'].lower() or q in e['event'].lower() or q in e['description'].lower() or q in e['era'].lower() or q in e['lesson'].lower()]

        for event in filtered:
            with st.expander(f"**{event['year']}** — {event['event']} | *{event['era']}*"):
                st.markdown(event['description'])
                st.markdown(f"<div class='card card-gold'>💡 <b>Lesson:</b> {event['lesson']}</div>", unsafe_allow_html=True)
                st.markdown(f"<span class='era-tag'>{event['era']}</span>", unsafe_allow_html=True)

    with tab2:
        era_list = sorted(set(e['era'] for e in ECONOMIC_HISTORY))
        selected_era = st.selectbox("Filter by era:", ["All"] + era_list)

        era_events = ECONOMIC_HISTORY if selected_era == "All" else [e for e in ECONOMIC_HISTORY if e['era'] == selected_era]

        st.markdown(f"**{len(era_events)} events** in this era")

        for event in era_events:
            st.markdown(f"""
<div class='history-card'>
    <div style='display:flex;justify-content:space-between;align-items:center;'>
        <b style='font-size:1.1rem;'>{event['event']}</b>
        <span class='era-tag'>{event['era']}</span>
    </div>
    <p style='color:#444 !important;margin:4px 0 8px 0;'>📅 {event['year']}</p>
    <p>{event['description']}</p>
    <div class='card card-gold' style='margin-top:8px;'>💡 {event['lesson']}</div>
</div>
""", unsafe_allow_html=True)

# ── MY PROGRESS ───────────────────────────────
elif page == "My Progress":
    st.markdown("## 📊 My Progress")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total XP", st.session_state.xp)
    with col2:
        total = st.session_state.total_answered
        correct = st.session_state.correct_answered
        acc = f"{int(correct/total*100)}%" if total else "N/A"
        st.metric("Quiz Accuracy", acc)
    with col3:
        st.metric("Questions Answered", total)
    with col4:
        st.metric("Streak", f"{st.session_state.streak} days")

    st.markdown("---")
    st.markdown("### Badges Earned")
    if st.session_state.badges:
        badge_cols = st.columns(len(st.session_state.badges))
        for col, badge in zip(badge_cols, st.session_state.badges):
            with col:
                icon = BADGE_ICONS.get(badge, "🏅")
                st.markdown(f"<div style='text-align:center;padding:1rem;background:#fff8e1;border-radius:10px;color:#111 !important;'><div style='font-size:2rem;'>{icon}</div><b style='color:#111 !important;'>{badge}</b></div>", unsafe_allow_html=True)
    else:
        st.info("No badges yet. Complete lessons and quizzes to earn them!")

    st.markdown("---")
    st.markdown("### How to Earn XP")
    xp_table = [
        ("Start a daily lesson", "+10 XP"),
        ("Correct quiz answer", "+15 XP"),
        ("Quiz attempt (wrong)", "+2 XP"),
        ("Complete scenario", "+5 XP"),
        ("Fill-in correct", "+10 XP"),
        ("Fill-in attempt", "+2 XP"),
    ]
    for action, reward in xp_table:
        st.markdown(f"- **{action}**: {reward}")

    st.markdown("---")
    st.markdown("### Lesson Coverage")
    topics_with_lessons = list(LESSONS.keys())
    for t in topics_with_lessons:
        levels_available = list(LESSONS[t].keys())
        icon = TOPICS.get(t, "📚")
        st.markdown(f"{icon} **{t}**: " + " | ".join([f"<span class='level-badge {l.lower()}'>{l}</span>" for l in levels_available]), unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Reset All Progress", type="secondary"):
        for key in ["score", "total_answered", "correct_answered", "streak", "daily_done", "quiz_answered", "fill_answers", "xp", "badges"]:
            if key in ["daily_done", "quiz_answered", "fill_answers", "badges"]:
                st.session_state[key] = set() if key == "daily_done" else ({} if key != "badges" else [])
            else:
                st.session_state[key] = 0
        st.success("Progress reset.")
        st.rerun()
