# Business model calculator

**User:** Todd Nelson (todd.cx@turtleisland.solutions)  
**Created:** 12/16/2025 0:48:16  
**Updated:** 12/16/2025 0:53:12  
**Exported:** 3/19/2026 16:47:39  
**Link:** [https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/6940f29e-3868-8326-9008-b03f295ff502](https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/6940f29e-3868-8326-9008-b03f295ff502)  

## Prompt:
@context:
  objective: create a business modeling calcualator
  domain: real estate
  audience: property owner
  model_role: Operator
  time_horizon: Immediate (0-2 weeks)
  output_format: Bullets
  constraints: [
    !must be engineered to incentivize the receiver to maximize carmen beach property services to ensure maximum value of service offerings, relative the value added to each other partner or connected business node on the gigaton network
  ]

::entities
  (none)

::properties
  (none)

::causal_links
  (none)

::truth_state
  ✓ (none)
  ✗ (none)
  ? (none)

::frequency
  (none)

::instructions
  1) Use @context as fixed state.
  2) Respect all constraints starting with !.
  3) Prefer causal reasoning (→, ++/--, ↑/↓) over narrative.
  4) Separate ✓ facts from ? hypotheses; do not assert ? as fact.
  5) If key inputs are missing, list them as a short ‘Missing Inputs’ section.

::deliverable
  Produce output in: Bullets.
  Optimize for decision-readiness and ROI.
  Success criteria: (none specified)

::required_sections
  ::Pricing structure
  ::package breakdowns
  ::expected ROI of property broken down into cost centers and revenue drivers that combine to create predictably profitable performance

## Response:
::Pricing structure

*   **Base Platform Fee (Monthly)**
    *   Fixed ops + tech layer → ensures minimum service viability
    *   Typical range: **$XXX–$XXXX / property / month** (scales with unit count)
*   **Performance Fee (Variable)**
    *   % of **incremental net revenue** generated
    *   Aligns incentives → Carmen Beach Property (CBP) only wins if owner wins
    *   ++ utilization ↑ ADR → ++ CBP upside
*   **Network Leverage Multiplier (Gigaton Node Access)**
    *   Optional but strongly value-accretive
    *   Access to demand routing, partner services, data intelligence
    *   More nodes activated → compounding ROI (↑ network effects)

* * *

::package breakdowns

*   **Core Optimization Package (Entry Point)**
    *   Revenue management (pricing, availability)
    *   Distribution optimization (channels, listing quality)
    *   Ops baseline (cleaning, turnover, maintenance SLAs)
    *   Outcome → stabilize cash flow, reduce leakage
*   **Growth Acceleration Package (Recommended)**
    *   Everything in Core ++
    *   Demand amplification (direct bookings, partner referrals)
    *   Cost compression via preferred vendors
    *   Data feedback loops → faster pricing + ops decisions
    *   Outcome → ↑ RevPAR, ↓ cost per booking
*   **Network-Maximized Package (Best ROI)**
    *   Everything above ++
    *   Full Gigaton network integration
    *   Cross-property demand routing
    *   Ancillary revenue activation (experiences, services, upsells)
    *   Outcome → non-linear revenue growth via ecosystem leverage
    *   **Designed to outperform standalone property management**

* * *

::expected ROI of property

*   **Revenue Drivers**
    *   ADR ↑ via dynamic pricing + demand intelligence
    *   Occupancy ↑ via channel + network routing
    *   Ancillary revenue ↑ (experiences, services, partner offers)
    *   Direct bookings ↑ → -- platform fees
*   **Cost Centers**
    *   Ops (cleaning, maintenance, staffing)
    *   Distribution fees (OTAs, payment processing)
    *   Management + tech fees
    *   Vacancy + pricing inefficiency losses
*   **Causal Performance Model**
    *   Better pricing → ADR ↑
    *   Better distribution → occupancy ↑
    *   Network routing → demand volatility ↓
    *   Vendor consolidation → ops costs ↓
    *   Data feedback loops → decision latency ↓
*   **Net Effect**
    *   Revenue ↑↑ faster than costs ↑
    *   Margin expansion → predictable profitability
    *   ROI improves with **more CBP services activated**, not fewer

* * *

::Missing Inputs

*   Property type (single unit vs portfolio)
*   Average nightly rate (current)
*   Historical occupancy (%)
*   Current management + OTA fee stack
*   Owner risk tolerance (aggressive vs defensive growth)

## Prompt:
build it with conditional logic so it is a functional calculator able to be injected with inputs for each individual property so that scenarios are able to be ran

## Response:
Thought for 12s

```
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Carmen Beach Property — ROI Scenario Calculator</title>
  <style>
    :root { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
    body { margin: 0; background:#0b0f17; color:#e8eefc; }
    .wrap { max-width: 1150px; margin: 0 auto; padding: 24px; }
    h1 { margin: 0 0 6px; font-size: 20px; }
    .sub { margin: 0 0 18px; color:#a8b4d6; font-size: 13px; }
    .grid { display:grid; grid-template-columns: 420px 1fr; gap: 16px; }
    .card { background:#10192a; border:1px solid #1b2a49; border-radius: 14px; padding: 14px; }
    .card h2 { margin: 0 0 10px; font-size: 14px; color:#cfe0ff; }
    label { display:block; font-size: 12px; color:#b7c5e8; margin: 10px 0 6px; }
    input, select { width: 100%; padding: 10px; border-radius: 10px; border:1px solid #22365f; background:#0c1424; color:#e8eefc; }
    input[type="checkbox"]{ width:auto; transform: scale(1.1); margin-right: 8px; }
    .row { display:grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .row3 { display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
    .btns { display:flex; gap:10px; margin-top: 12px; flex-wrap: wrap; }
    button { cursor:pointer; padding: 10px 12px; border-radius: 10px; border:1px solid #2b4580; background:#132244; color:#e8eefc; }
    button.secondary { background:#0c1424; }
    button.danger { border-color:#7a2b2b; background:#2a1010; }
    .muted { color:#a8b4d6; font-size: 12px; }
    table { width:100%; border-collapse: collapse; }
    th, td { padding: 10px; border-bottom: 1px solid #1b2a49; font-size: 13px; text-align: right; }
    th:first-child, td:first-child { text-align:left; }
    .kpi { display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin-bottom: 12px; }
    .k { background:#0c1424; border:1px solid #1b2a49; border-radius: 12px; padding: 10px; }
    .k .t { font-size: 11px; color:#a8b4d6; }
    .k .v { font-size: 16px; margin-top: 6px; }
    .note { margin-top: 10px; padding: 10px; border-radius: 12px; background:#0c1424; border:1px dashed #2b4580; color:#cfe0ff; font-size: 12px; }
    .pill { display:inline-block; padding: 3px 8px; border-radius: 999px; border:1px solid #2b4580; background:#0c1424; font-size: 12px; color:#cfe0ff; }
    .warn { border-color:#7a6b2b; }
    .ok { border-color:#2b7a4a; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>CBP ROI Scenario Calculator (Per-Property)</h1>
    <p class="sub">Conditional logic + scenario storage. Model role: Operator. Goal: decision-ready ROI that incentivizes maximum CBP service utilization.</p>

    <div class="grid">
      <div class="card">
        <h2>1) Property Inputs (Baseline)</h2>

        <label>Property ID / Name</label>
        <input id="propName" placeholder="e.g., Casa Sol #12" />

        <div class="row">
          <div>
            <label>Nights available / month</label>
            <input id="nightsAvail" type="number" min="0" step="1" value="30" />
          </div>
          <div>
            <label>Average length of stay (nights)</label>
            <input id="alos" type="number" min="1" step="0.1" value="4" />
          </div>
        </div>

        <div class="row">
          <div>
            <label>Current ADR ($)</label>
            <input id="adr" type="number" min="0" step="1" value="220" />
          </div>
          <div>
            <label>Current occupancy (%)</label>
            <input id="occ" type="number" min="0" max="100" step="0.1" value="65" />
          </div>
        </div>

        <h2 style="margin-top:14px;">2) Cost Stack (Baseline)</h2>
        <div class="row">
          <div>
            <label>Cleaning cost / turnover ($)</label>
            <input id="cleanCost" type="number" min="0" step="1" value="75" />
          </div>
          <div>
            <label>Variable ops cost (% of revenue)</label>
            <input id="varOpsPct" type="number" min="0" max="100" step="0.1" value="8" />
          </div>
        </div>

        <div class="row">
          <div>
            <label>Fixed monthly costs ($)</label>
            <input id="fixedCost" type="number" min="0" step="1" value="450" />
          </div>
          <div>
            <label>OTA fee rate (%)</label>
            <input id="otaFeePct" type="number" min="0" max="100" step="0.1" value="14" />
          </div>
        </div>

        <label>Direct booking share (%)</label>
        <input id="directShare" type="number" min="0" max="100" step="0.1" value="12" />

        <h2 style="margin-top:14px;">3) CBP Package + Commercials</h2>

        <label>Package</label>
        <select id="package">
          <option value="core">Core Optimization</option>
          <option value="growth" selected>Growth Acceleration (Recommended)</option>
          <option value="network">Network-Maximized (Best ROI)</option>
        </select>

        <div class="row3">
          <div>
            <label>Base platform fee ($/mo)</label>
            <input id="baseFee" type="number" min="0" step="1" value="650" />
          </div>
          <div>
            <label>Network access fee ($/mo)</label>
            <input id="networkFee" type="number" min="0" step="1" value="350" />
          </div>
          <div>
            <label>Performance fee (% of incremental net)</label>
            <input id="perfFeePct" type="number" min="0" max="100" step="0.1" value="15" />
          </div>
        </div>

        <label><input id="enableNetworkFee" type="checkbox" checked />Enable Network Fee (only applies to Network-Maximized)</label>

        <h2 style="margin-top:14px;">4) Scenario Levers (Conditional Defaults by Package)</h2>
        <p class="muted" style="margin:0 0 8px;">
          Defaults auto-update when package changes. You can override to run what-if scenarios.
        </p>

        <div class="row3">
          <div>
            <label>ADR lift (%)</label>
            <input id="liftAdrPct" type="number" step="0.1" />
          </div>
          <div>
            <label>Occupancy lift (percentage points)</label>
            <input id="liftOccPp" type="number" step="0.1" />
          </div>
          <div>
            <label>Direct share lift (percentage points)</label>
            <input id="liftDirectPp" type="number" step="0.1" />
          </div>
        </div>

        <div class="row3">
          <div>
            <label>Ops cost reduction (% of variable ops)</label>
            <input id="liftOpsDownPct" type="number" step="0.1" />
          </div>
          <div>
            <label>Ancillary revenue ($ per booking)</label>
            <input id="ancPerBooking" type="number" step="1" />
          </div>
          <div>
            <label>Vacancy risk buffer (pp to subtract from projected occ)</label>
            <input id="riskBufferPp" type="number" step="0.1" value="0" />
          </div>
        </div>

        <div class="btns">
          <button id="calcBtn">Recalculate</button>
          <button class="secondary" id="saveBtn">Save Scenario</button>
          <button class="secondary" id="loadBtn">Load Scenario</button>
          <button class="danger" id="resetBtn">Reset</button>
        </div>

        <div class="note" id="logicNote"></div>
      </div>

      <div class="card">
        <h2>Results (Baseline vs. Projected)</h2>

        <div class="kpi">
          <div class="k">
            <div class="t">Incremental Net Profit / month</div>
            <div class="v" id="kpiDeltaNet">$0</div>
          </div>
          <div class="k">
            <div class="t">Owner ROI (Incremental Net ÷ CBP Fees)</div>
            <div class="v" id="kpiRoi">0.0×</div>
          </div>
          <div class="k">
            <div class="t">Payback (CBP Fees ÷ Incremental Net)</div>
            <div class="v" id="kpiPayback">—</div>
          </div>
        </div>

        <table>
          <thead>
            <tr>
              <th>Line Item</th>
              <th>Baseline</th>
              <th>Projected</th>
              <th>Δ</th>
            </tr>
          </thead>
          <tbody id="tbody"></tbody>
        </table>

        <div class="note" id="packageFit"></div>
        <div class="note" id="missingInputs" style="display:none;"></div>
      </div>
    </div>
  </div>

<script>
(function () {
  const $ = (id) => document.getElementById(id);

  const defaultsByPackage = {
    core:   { liftAdrPct: 3.0,  liftOccPp: 2.0,  liftDirectPp: 1.0,  liftOpsDownPct: 2.0,  ancPerBooking: 0 },
    growth: { liftAdrPct: 6.0,  liftOccPp: 4.0,  liftDirectPp: 4.0,  liftOpsDownPct: 5.0,  ancPerBooking: 6 },
    network:{ liftAdrPct: 10.0, liftOccPp: 6.0,  liftDirectPp: 8.0,  liftOpsDownPct: 8.0,  ancPerBooking: 14 }
  };

  const fmt$ = (n) => (isFinite(n) ? n.toLocaleString(undefined,{style:"currency",currency:"USD",maximumFractionDigits:0}) : "—");
  const fmt = (n, d=1) => (isFinite(n) ? n.toLocaleString(undefined,{maximumFractionDigits:d,minimumFractionDigits:d}) : "—");
  const clamp = (x, a, b) => Math.min(Math.max(x, a), b);

  function getInputs() {
    const x = {
      propName: $("propName").value.trim() || "Unnamed Property",
      nightsAvail: +$("nightsAvail").value,
      alos: +$("alos").value,
      adr: +$("adr").value,
      occ: +$("occ").value,
      cleanCost: +$("cleanCost").value,
      varOpsPct: +$("varOpsPct").value,
      fixedCost: +$("fixedCost").value,
      otaFeePct: +$("otaFeePct").value,
      directShare: +$("directShare").value,
      package: $("package").value,
      baseFee: +$("baseFee").value,
      networkFee: +$("networkFee").value,
      enableNetworkFee: $("enableNetworkFee").checked,
      liftAdrPct: +$("liftAdrPct").value,
      liftOccPp: +$("liftOccPp").value,
      liftDirectPp: +$("liftDirectPp").value,
      liftOpsDownPct: +$("liftOpsDownPct").value,
      ancPerBooking: +$("ancPerBooking").value,
      riskBufferPp: +$("riskBufferPp").value,
      ts: new Date().toISOString()
    };
    return x;
  }

  function validate(x) {
    const missing = [];
    const must = [
      ["nightsAvail", "Nights available / month"],
      ["alos", "Average length of stay"],
      ["adr", "Current ADR"],
      ["occ", "Current occupancy"],
      ["otaFeePct", "OTA fee rate"],
      ["directShare", "Direct booking share"],
    ];
    must.forEach(([k,label]) => {
      if (!isFinite(x[k]) || x[k] <= 0 && (k==="adr" || k==="alos" || k==="nightsAvail")) missing.push(label);
      if (!isFinite(x[k]) && (k!=="adr" && k!=="alos" && k!=="nightsAvail")) missing.push(label);
    });
    if (x.directShare < 0 || x.directShare > 100) missing.push("Direct booking share must be 0–100%");
    if (x.occ < 0 || x.occ > 100) missing.push("Occupancy must be 0–100%");
    return missing;
  }

  function applyDefaults(pkg) {
    const d = defaultsByPackage[pkg];
    $("liftAdrPct").value = d.liftAdrPct;
    $("liftOccPp").value = d.liftOccPp;
    $("liftDirectPp").value = d.liftDirectPp;
    $("liftOpsDownPct").value = d.liftOpsDownPct;
    $("ancPerBooking").value = d.ancPerBooking;

    // Conditional UI/logic: network fee only meaningful in network package
    const isNetwork = pkg === "network";
    $("enableNetworkFee").disabled = !isNetwork;
    $("networkFee").disabled = !isNetwork;
  }

  function calcScenario(x) {
    // Baseline
    const occBase = clamp(x.occ / 100, 0, 1);
    const occNightsBase = x.nightsAvail * occBase;
    const bookingsBase = occNightsBase / Math.max(x.alos, 1);
    const revenueBase = bookingsBase * x.alos * x.adr; // occupied nights * ADR
    const directBase = clamp(x.directShare / 100, 0, 1);
    const otaShareBase = 1 - directBase;
    const otaFeesBase = revenueBase * otaShareBase * (x.otaFeePct / 100);
    const cleanBase = bookingsBase * x.cleanCost;
    const varOpsBase = revenueBase * (x.varOpsPct / 100);
    const netBase = revenueBase - otaFeesBase - cleanBase - varOpsBase - x.fixedCost;

    // Projected levers (conditional logic)
    const adrProj = x.adr * (1 + (x.liftAdrPct / 100));
    const occProjPct = clamp(x.occ + x.liftOccPp - x.riskBufferPp, 0, 100);
    const occProj = occProjPct / 100;
    const directProjPct = clamp(x.directShare + x.liftDirectPp, 0, 100);
    const directProj = directProjPct / 100;
    const otaShareProj = 1 - directProj;

    const occNightsProj = x.nightsAvail * occProj;
    const bookingsProj = occNightsProj / Math.max(x.alos, 1);
    const revenueProj = bookingsProj * x.alos * adrProj;

    const otaFeesProj = revenueProj * otaShareProj * (x.otaFeePct / 100);
    const cleanProj = bookingsProj * x.cleanCost;

    // Variable ops reduction applies to var ops pct (e.g., 8% reduced by 5% => 7.6%)
    const varOpsPctProj = (x.varOpsPct) * (1 - (x.liftOpsDownPct / 100));
    const varOpsProj = revenueProj * (varOpsPctProj / 100);

    const ancillaryProj = bookingsProj * Math.max(x.ancPerBooking, 0);

    // CBP fee stack (conditional)
    const baseFee = Math.max(x.baseFee, 0);
    const networkFee = (x.package === "network" && x.enableNetworkFee) ? Math.max(x.networkFee, 0) : 0;

    // Incremental net BEFORE performance fee (owner-side)
    const netProjPrePerf = (revenueProj + ancillaryProj) - otaFeesProj - cleanProj - varOpsProj - x.fixedCost - baseFee - networkFee;

    const netBaseForDelta = netBase; // baseline excludes CBP fees
    const deltaNetPrePerf = netProjPrePerf - netBaseForDelta;

    // Performance fee only applies if owner is winning (incremental net positive)
    const perfFee = (deltaNetPrePerf > 0) ? (deltaNetPrePerf * (x.perfFeePct / 100)) : 0;

    const netProj = netProjPrePerf - perfFee;

    const cbpFees = baseFee + networkFee + perfFee;

    const deltaNet = netProj - netBaseForDelta;

    const ownerRoi = (cbpFees > 0) ? (deltaNet / cbpFees) : NaN;
    const payback = (deltaNet > 0) ? (cbpFees / deltaNet) : Infinity;

    return {
      baseline: { revenue: revenueBase, otaFees: otaFeesBase, cleaning: cleanBase, varOps: varOpsBase, fixed: x.fixedCost, net: netBase,
                  adr: x.adr, occPct: x.occ, directPct: x.directShare, bookings: bookingsBase, ancillary: 0, cbpFees: 0, perfFee: 0, baseFee: 0, networkFee: 0 },
      projected:{ revenue: revenueProj, otaFees: otaFeesProj, cleaning: cleanProj, varOps: varOpsProj, fixed: x.fixedCost, net: netProj,
                  adr: adrProj, occPct: occProjPct, directPct: directProjPct, bookings: bookingsProj, ancillary: ancillaryProj, cbpFees, perfFee, baseFee, networkFee },
      delta: { revenue: revenueProj - revenueBase, otaFees: otaFeesProj - otaFeesBase, cleaning: cleanProj - cleanBase, varOps: varOpsProj - varOpsBase,
               ancillary: ancillaryProj, net: deltaNet, cbpFees },
      kpi: { deltaNet, ownerRoi, paybackMonths: payback }
    };
  }

  function render(x, r) {
    // KPI
    $("kpiDeltaNet").textContent = fmt$(r.kpi.deltaNet);

    const roi = r.kpi.ownerRoi;
    $("kpiRoi").textContent = isFinite(roi) ? `${fmt(roi,1)}×` : "—";

    const pb = r.kpi.paybackMonths;
    $("kpiPayback").textContent = (isFinite(pb) && pb >= 0 && pb < 999) ? `${fmt(pb,1)} mo` : "—";

    // Table
    const lines = [
      ["Bookings (stays)", r.baseline.bookings, r.projected.bookings, r.projected.bookings - r.baseline.bookings, "num"],
      ["ADR", r.baseline.adr, r.projected.adr, r.projected.adr - r.baseline.adr, "cur"],
      ["Occupancy", r.baseline.occPct, r.projected.occPct, r.projected.occPct - r.baseline.occPct, "pct"],
      ["Direct booking share", r.baseline.directPct, r.projected.directPct, r.projected.directPct - r.baseline.directPct, "pct"],
      ["Gross revenue", r.baseline.revenue, r.projected.revenue, r.delta.revenue, "cur"],
      ["Ancillary revenue", r.baseline.ancillary, r.projected.ancillary, r.projected.ancillary - r.baseline.ancillary, "cur"],
      ["OTA fees", r.baseline.otaFees, r.projected.otaFees, r.delta.otaFees, "cur"],
      ["Cleaning", r.baseline.cleaning, r.projected.cleaning, r.delta.cleaning, "cur"],
      ["Variable ops", r.baseline.varOps, r.projected.varOps, r.delta.varOps, "cur"],
      ["Fixed costs", r.baseline.fixed, r.projected.fixed, 0, "cur"],
      ["CBP base fee", 0, r.projected.baseFee, r.projected.baseFee, "cur"],
      ["Network access fee", 0, r.projected.networkFee, r.projected.networkFee, "cur"],
      ["Performance fee", 0, r.projected.perfFee, r.projected.perfFee, "cur"],
      ["Total CBP fees", 0, r.projected.cbpFees, r.projected.cbpFees, "cur"],
      ["Net profit", r.baseline.net, r.projected.net, r.kpi.deltaNet, "cur"]
    ];

    const tb = $("tbody");
    tb.innerHTML = "";
    lines.forEach(([label, b, p, d, type]) => {
      const tr = document.createElement("tr");
      const td0 = document.createElement("td"); td0.textContent = label;

      const td1 = document.createElement("td");
      const td2 = document.createElement("td");
      const td3 = document.createElement("td");

      function f(v) {
        if (type === "cur") return fmt$(v);
        if (type === "pct") return `${fmt(v,1)}%`;
        if (type === "num") return fmt(v,1);
        return String(v);
      }

      td1.textContent = f(b);
      td2.textContent = f(p);

      // Δ formatting
      const sign = (type === "cur" || type === "num" || type === "pct") ? (d > 0 ? "+" : "");
      td3.textContent = (type === "pct") ? `${sign}${fmt(d,1)}pp`
                      : (type === "cur") ? `${sign}${fmt$(d)}`
                      : `${sign}${fmt(d,1)}`;

      tr.appendChild(td0); tr.appendChild(td1); tr.appendChild(td2); tr.appendChild(td3);
      tb.appendChild(tr);
    });

    // Logic note (causal, incentive-aligned)
    const pkg = x.package;
    const pkgName = pkg === "core" ? "Core" : pkg === "growth" ? "Growth" : "Network";
    const networkOn = (pkg === "network" && x.enableNetworkFee);

    const perfApplies = (r.delta.net > 0);
    const perfPill = perfApplies ? `<span class="pill ok">Performance fee ACTIVE</span>` : `<span class="pill warn">Performance fee OFF (no incremental win)</span>`;
    const netPill = (r.kpi.deltaNet > 0) ? `<span class="pill ok">Owner net ↑</span>` : `<span class="pill warn">Owner net not ↑</span>`;

    $("logicNote").innerHTML =
      `<div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:8px;">
         <span class="pill">${pkgName} Package</span>
         ${networkOn ? `<span class="pill">Network Fee ON</span>` : `<span class="pill">Network Fee OFF</span>`}
         ${perfPill}
         ${netPill}
       </div>
       <div>
         Causal model: pricing lift → ADR ↑, distribution + network routing → occupancy ↑ and volatility ↓, direct share ↑ → OTA leakage ↓, ops downlift → margin ↑, ancillaries → revenue diversification ↑.
         Performance fee is conditionally applied only when incremental net is positive.
       </div>`;

    // Package fit note (explicit incentive alignment)
    const leverMsg = (pkg === "network")
      ? "Network-Maximized is engineered for compounding ROI via ecosystem leverage: demand routing + partner upsells + higher direct mix."
      : (pkg === "growth")
        ? "Growth is the highest expected ROI-per-effort for 0–2 weeks: quick wins in ADR/occ/direct mix and ops compression."
        : "Core stabilizes fundamentals; it’s the minimum viable layer before scaling into network effects.";

    $("packageFit").innerHTML =
      `<b>Operator readout:</b> ${leverMsg} Best ROI occurs when you activate more CBP surface area (pricing + distribution + ops + network), because gains stack multiplicatively rather than additively.`;
  }

  function recalc() {
    const x = getInputs();
    const missing = validate(x);
    const missBox = $("missingInputs");

    if (missing.length) {
      missBox.style.display = "block";
      missBox.innerHTML = `<b>Missing Inputs:</b> ${missing.map(s => `<span class="pill warn">${s}</span>`).join(" ")}`;
      // Still run calculation where possible (keeps UI responsive), but results may be junk.
    } else {
      missBox.style.display = "none";
    }

    const r = calcScenario(x);
    render(x, r);
  }

  function saveScenario() {
    const x = getInputs();
    const key = "cbp_scenarios_v1";
    const store = JSON.parse(localStorage.getItem(key) || "[]");
    store.unshift({ name: x.propName, data: x });
    localStorage.setItem(key, JSON.stringify(store.slice(0, 30))); // cap to 30
    alert("Saved.");
  }

  function loadScenario() {
    const key = "cbp_scenarios_v1";
    const store = JSON.parse(localStorage.getItem(key) || "[]");
    if (!store.length) { alert("No saved scenarios."); return; }

    const pick = prompt(
      "Paste the number to load:\n" +
      store.slice(0, 10).map((s, i) => `${i+1}) ${s.name} — ${s.data.ts}`).join("\n")
    );
    const idx = (+pick - 1);
    if (!isFinite(idx) || idx < 0 || idx >= store.length) return;

    const x = store[idx].data;

    // Populate fields
    $("propName").value = x.propName || "";
    $("nightsAvail").value = x.nightsAvail;
    $("alos").value = x.alos;
    $("adr").value = x.adr;
    $("occ").value = x.occ;
    $("cleanCost").value = x.cleanCost;
    $("varOpsPct").value = x.varOpsPct;
    $("fixedCost").value = x.fixedCost;
    $("otaFeePct").value = x.otaFeePct;
    $("directShare").value = x.directShare;
    $("package").value = x.package;
    $("baseFee").value = x.baseFee;
    $("networkFee").value = x.networkFee;
    $("enableNetworkFee").checked = !!x.enableNetworkFee;
    $("liftAdrPct").value = x.liftAdrPct;
    $("liftOccPp").value = x.liftOccPp;
    $("liftDirectPp").value = x.liftDirectPp;
    $("liftOpsDownPct").value = x.liftOpsDownPct;
    $("ancPerBooking").value = x.ancPerBooking;
    $("riskBufferPp").value = x.riskBufferPp ?? 0;
    $("perfFeePct").value = x.perfFeePct;

    // apply conditional disables
    $("enableNetworkFee").disabled = x.package !== "network";
    $("networkFee").disabled = x.package !== "network";

    recalc();
  }

  function resetAll() {
    $("propName").value = "";
    $("nightsAvail").value = 30;
    $("alos").value = 4;
    $("adr").value = 220;
    $("occ").value = 65;
    $("cleanCost").value = 75;
    $("varOpsPct").value = 8;
    $("fixedCost").value = 450;
    $("otaFeePct").value = 14;
    $("directShare").value = 12;

    $("package").value = "growth";
    $("baseFee").value = 650;
    $("networkFee").value = 350;
    $("perfFeePct").value = 15;
    $("enableNetworkFee").checked = true;
    $("riskBufferPp").value = 0;

    applyDefaults("growth");
    recalc();
  }

  // Events
  $("package").addEventListener("change", (e) => {
    applyDefaults(e.target.value);
    recalc();
  });

  // Recalc on key inputs (fast iteration)
  [
    "nightsAvail","alos","adr","occ","cleanCost","varOpsPct","fixedCost","otaFeePct","directShare",
    "baseFee","networkFee","perfFeePct","enableNetworkFee",
    "liftAdrPct","liftOccPp","liftDirectPp","liftOpsDownPct","ancPerBooking","riskBufferPp"
  ].forEach(id => {
    $(id).addEventListener("input", () => recalc());
    $(id).addEventListener("change", () => recalc());
  });

  $("calcBtn").addEventListener("click", recalc);
  $("saveBtn").addEventListener("click", saveScenario);
  $("loadBtn").addEventListener("click", loadScenario);
  $("resetBtn").addEventListener("click", resetAll);

  // Init defaults
  applyDefaults($("package").value);
  recalc();
})();
</script>
</body>
</html>
```



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)