# Decision 0002 — numerical acceptance before runtime execution

Frozen 2026-09-07, before a numerical kernel was implemented or its results observed.
Model/evaluator policy ID: BOX-EULER-1. Root and independent Astra numerical-contract reviewer checked these rules. Agent calculation is numerical evidence, not a human hand-calculation observation.

## Bounded study

The default in scenarios/box-001.json is exactly EXPERIMENTS.md's source fixture. Custom inputs remain synthetic. V: [1,1e6] m3; each equal positive inflow/outflow Q: [1e-6,1e3] m3/s; L: [0,1000] kg/s; M0: [0,1e6] kg; each duration: [0,86400] s. Source factor and capture fraction lie in [0,1]. These are computational bounds, not environmental plausibility. Exactly dry then storm; total duration must be positive. Reject unsupported fields and units rather than convert implicitly. Maximum 100000 numerical steps per arm across the three refinement levels, checked before calculation.

## Interval semantics and numerics

Each segment uses [start,end); its closing stock opens the next segment. Clip the last timestep to the segment endpoint. For each segment, choose integer n=ceil(T/min(60,0.05*V/Q)); zero duration has no steps. Levels use n,2n,4n equally sized steps, so actual grids always refine and endpoints are shared. Never independently reapply a cap that can make grids identical.

Explicit Euler records source=L*h and outlet=(Q/V)*opening_mass*h, then closing_mass=opening_mass+source-outlet. Split that outlet into escaped=(1-c)*outlet and captured=c*outlet. Water in and out are each Q*h and volume remains V. CFL k*h<=0.05 ensures the update is a convex combination of opening stock and nonnegative source contributions; negative or nonfinite state rejects. No clamping.

## Independent analytic path

Let x=k*t, k=Q/V, a=-expm1(-x), phi=a/x (phi(0)=1). Stock=M0*exp(-x)+L*t*phi. Outlet=M0*a+L*t*(1-phi). For x<1e-4 compute 1-phi using x/2-x²/6+x³/24-x⁴/120+x⁵/720 to avoid cancellation; no empirical constants enter. Segment state continuity yields the piecewise trajectory. The analytic oracle never calls the numerical update.

Controls: L=k*M0 has constant stock and outlet=L*t. For V=Q=M0=1, L=0 and t=log(2), stock=1/2 and outlet=1/2. Source-free decay tests sign; zero initial/source tests the zero trajectory. Independent default analytic calculations: dry stock 3.0232367392896893 kg, dry outlet 0.5767632607103108 kg; storm closing stock 4.789738373964693 kg, storm outlet 3.6334983653249973 kg. These values are cross-checks, not hardcoded simulation outputs.

## Acceptance

Conservation uses |residual| <= 1e-10*max(1,opening_stock+source) per step/segment/run, likewise water and custody at their respective scale. This conservative binary64 allowance exceeds accumulated arithmetic error over the bounded step budget; the report also gives raw and scale-normalized residuals. Tests inject defects far larger than this allowance, including conserving but physically wrong fluxes, so closure alone cannot pass a wrong model.

For explicit Euler, local truncation is bounded by h²*k*|L-k*M|/2. Because 0<=1-k*h<=1 and |L-k*M(t)| does not increase within a constant segment, a conservative accumulated stock bound advances as B_end <= B_start + T*h*k*|L-k*M_analytic_start|/2. At each recorded point, compare Euler stock and integrated outlet with independent analytic trajectories against this a-priori bound plus roundoff allowance. Do not choose thresholds from observed output. Refinement must not increase the maximum stock/outlet trajectory discrepancy (except roundoff); the default nonstationary fixture must show fine/coarse error ratio <=0.35 (expected first-order ratio about 0.25). Stationary/zero trajectories can be at the arithmetic floor and do not establish observed order.

Use the finest valid trajectory in the main comparison, retain all three levels and analytic data. Report ordering signatures for each supported metric and level. A ranking reversal suspends comparison, remains visible in invalid attempt evidence and is never averaged away. Physical/model/parameter/ecological uncertainty remains unquantified and NOT_EVALUATED, separate from measured numerical discrepancy.

## Custody

Each step records outlet->stored then stored->destination_unknown. Captured is cumulative transfer, stored_throughput is the same transfer's intermediate throughput, terminal stored stock is zero, terminal destination_unknown equals captured. Boundary balance counts captured once; downstream balance counts the terminal custody stocks instead of adding them to captured. Missing records or a disposed/removed destination fail, as does any claim value other than NOT_EVALUATED for disposal, lifecycle, ecology or health.

## Report contract

Question: where does the fictional mass go, and how closely do the independent methods agree? Use directly labeled mass comparison rows plus stock-versus-time lines, exact mass/water/custody tables, explicit SI axes, zero-based absolute mass scales, and a finest-grid CSV with segment and flow context. Capture and baseline stock overlap physically; use separate small multiples or say so explicitly. White background, dark ink, blue/ochre marks and distinct solid/dashed lines. All evidence can be read without color, scripts or network. Narrow layouts stack; tables retain semantic headers and keyboard scrolling. Source data stays in result.json and CSV, not pixels. External chart builders are omitted to honor the owner's standard-library distributable runtime contract.

## Implementation review clarification

The fresh critic found that a positive subnormal duration could underflow during step-count division and allocate zero steps. The parser now assigns at least one coarse step for any positive duration and rejects grids whose finest step or absolute-time increment cannot advance in binary64. This enforces the predeclared nonadvancing-grid rejection; no result tolerance was changed. Deeply nested JSON also rejects with a normal validation diagnostic.

Custody events are two integrated run-level transfers, each with a deterministic arm/refinement-scoped ID. The terminal event links the capture-total event; the evaluator reconstructs that integrated mass from every raw per-step captured flux. A missing terminal event identifies its unmatched capture transfer. CLI source/capture changes record their parent study hash in run provenance; independently authored external study files have no inferred parent. These identity additions do not change physics or acceptance thresholds.
