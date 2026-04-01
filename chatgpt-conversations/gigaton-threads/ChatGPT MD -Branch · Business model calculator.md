# Branch · Business model calculator

**User:** Todd Nelson (todd.cx@turtleisland.solutions)  
**Created:** 12/16/2025 0:55:33  
**Updated:** 12/16/2025 15:50:27  
**Exported:** 3/19/2026 16:46:45  
**Link:** [https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/6940f451-a540-8328-abec-d1b38b91c7df](https://chatgpt.com/g/g-p-6882aa12c04c8191b859fd11dc4e66da-gigaton/c/6940f451-a540-8328-abec-d1b38b91c7df)  

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

## Prompt:
how can I inject this into a browser? Can I export the code to html

## Response:
*   **Inject into a browser (fastest path)**
    *   Copy the full code block into a plain text editor.
    *   Save the file as: `cbp-roi-calculator.html`
    *   Double-click it to open in Chrome/Safari/Edge (it runs locally; no server needed).
*   **Option A: One-click “Open as a local file”**
    *   **Mac**: TextEdit → Format → _Make Plain Text_ → paste → Save as `.html` → open.
    *   **Windows**: Notepad → paste → Save as **All Files** → `cbp-roi-calculator.html` → open.
*   **Option B: “Inject” via DevTools (temporary)**
    *   Open any webpage → right-click → **Inspect** → **Console**
    *   Paste this and press Enter:
        ```
        document.open();
        document.write(`PASTE_THE_HTML_CODE_HERE`);
        document.close();
        ```
    *   This is disposable (refresh wipes it). Use only for quick demos.
*   **Option C: Host it (shareable link)**
    *   **GitHub Pages**: create a repo → add `index.html` (paste code) → enable Pages → share URL.
    *   **Netlify/Vercel**: drag-and-drop the `.html` file (or deploy a repo) → share URL.
*   **Yes — you can export to HTML**
    *   The code already _is_ a complete HTML file. Export = save it with a `.html` extension.

If you want, I can also restructure it into:

*   `index.html` + `app.js` + `styles.css` (cleaner for iteration), or
*   a lightweight React version for embedding into an existing site.

## Prompt:
What is the math formula for finding the optimum path on a neuro net with hexagonal node structure up to 7 decisions where the path must travel in an order able to create a tesseract with each node having a value + trust accuracy above 0

## Response:
*   **Model it as a constrained optimization on a graph**
    *   Hex node structure ⇒ graph  $G=(V,E)$  where  $E$  connects the 6 neighbors (hex grid adjacency).
    *   Each node  $i\in V$  has:
        *   value  $v_i \in \mathbb{R}$ 
        *   trust/accuracy  $t_i \in \mathbb{R}$ 
    *   Hard constraint: **eligible nodes**  $V^+ = \{ i \in V \;|\; t_i>0 \}$ 

* * *

*   **Decision horizon: “up to 7 decisions”**
    *   7 decisions = 7 edges = **8 visited nodes**.
    *   Path  $P = (x_0,x_1,\dots,x_L)$  with  $L \le 7$ 
    *   Feasibility:  $(x_k,x_{k+1}) \in E$  and  $x_k\in V^+$ 

* * *

*   **Core objective function (optimum path)**
    *   If you want “optimum” to mean **max expected value under trust**, a clean objective is:
        
$$
\max_{x_0,\dots,x_L} \;\; \sum_{k=0}^{L} \Big(v_{x_k}\cdot t_{x_k}\Big)\;-\;\lambda\sum_{k=0}^{L-1} c(x_k,x_{k+1})
$$
*   where:
    *    $c(\cdot,\cdot)$  is step cost (often 1 per move, or energy/time)
    *    $\lambda\ge 0$  trades off reward vs path cost

* * *

*   **“Must travel in an order able to create a tesseract” = add a tesseract-consistency constraint**
    *   A tesseract is the 4D hypercube with vertex labels in  $\{0,1\}^4$ .
    *   Enforce that the visited nodes can be assigned to **distinct** tesseract vertices and the move order matches hypercube edges (Hamming distance 1).
    *   Introduce an assignment  $y_k \in \{0,1\}^4$  (the tesseract vertex label for step  $k$ ) and require:
        
$$
\forall k:\; y_k \neq y_j \text{ for } j\neq k \quad\text{(injective mapping)}
$$
 
$$
\forall k < L:\; \|y_{k+1}-y_k\|_1 = 1 \quad\text{(hypercube edge traversal)}
$$
*   If you want the _path_ to be a valid “tesseract-walk”, you’re effectively constraining the order to be a walk on the tesseract graph.

* * *

*   **Full problem statement (one-line “math formula”)**
    
$$
\begin{aligned} \max_{L\le 7,\;x_0,\dots,x_L,\;y_0,\dots,y_L}\;\;& \sum_{k=0}^{L} \big(v_{x_k}t_{x_k}\big)-\lambda\sum_{k=0}^{L-1} c(x_k,x_{k+1})\\ \text{s.t. }\;\;& (x_k,x_{k+1})\in E \;\;\forall k<L\\ & t_{x_k}>0 \;\;\forall k\le L\\ & y_k\in\{0,1\}^4 \;\;\forall k\le L\\ & y_k\neq y_j \;\;\forall k\neq j\\ & \|y_{k+1}-y_k\|_1 = 1 \;\;\forall k<L \end{aligned}
$$

* * *

*   **Operational reality check**
    *   This is a **constrained path optimization** (combinatorial). With the tesseract-order constraint, you’re in ILP / DP / A\* territory, not a single closed-form “one-shot” equation.
    *   Fast execution pattern:
        *   Pre-filter  $V^+$  (trust gate) → reduces search space.
        *   Search paths length  $\le 7$  on hex graph → branch factor  $\approx 6$ .
        *   Only keep paths whose order can satisfy the hypercube-walk constraint (Hamming-1 on  $y_k$ ).

If you tell me what “create a tesseract” means operationally in your system (8 nodes forming a partial tesseract walk vs 16-node full tesseract embedding), I can lock the constraint set to your exact definition and give the cleanest solver form (ILP formulation or A\* heuristic).

## Prompt:
6-node full tesseract embedding

## Response:
Thought for 20s

*   **Define the hex net as a directed, 6-neighbor graph**
    *   Hex grid graph:  $G=(V,E)$ 
    *   Six movement directions:  $D=\{1,2,3,4,5,6\}$ 
    *   Neighbor operator:  $N_d(i)$  = the node you reach from  $i$  by taking direction  $d$  (if it exists)
    *   Node attributes: value  $v_i\in\mathbb{R}$ , trust  $t_i\in\mathbb{R}$ 
    *   Trust gate:  $V^+=\{i\in V\mid t_i>0\}$ 

* * *

*   **Full tesseract = embed the 4D hypercube graph into the hex net**
    *   Tesseract vertex set:  $U=\{0,1\}^4$  (16 vertices)
    *   Tesseract edges:  $(u,u\oplus e_m)$  for  $m\in\{1,2,3,4\}$ , where  $e_m$  flips bit  $m$ 

### 1) “Strict” (single-hop) embedding using 6 directions

You want a mapping  $f:U\to V^+$  and a dimension→direction map  $\phi:\{1,2,3,4\}\to D$  such that every tesseract edge is realized as **one hex move**:

$$
\forall u\in U,\;\forall m\in\{1,2,3,4\}:\quad f(u\oplus e_m)=N_{\phi(m)}(f(u))
$$
 
$$
\text{and}\quad f \text{ is injective: } f(u)\neq f(w)\;\; \forall u\neq w
$$

**Feasibility warning (tell-it-like-it-is):** a planar hex grid has 3 axes (6 directions), while a tesseract has 4 independent dimensions. A strict 1-hop, axis-faithful embedding is generally **overconstrained** unless you allow “folding” (two hypercube dimensions reuse the same axis/direction family) or you’re embedding into a non-planar/neural-net “hex” that isn’t a true planar lattice.

* * *

### 2) Practical “network” embedding (multi-hop edges) — usually what you actually want

Let each tesseract edge be routed as a short path in the hex net (so you can still use only 6 directions, but allow 2–k hops per hypercube edge).

*   Decision variables:
    *    $f:U\to V^+$  injective
    *   For each hypercube edge  $(u,m)$ , a route  $R_{u,m}=(r^0_{u,m},\dots,r^{\ell_{u,m}}_{u,m})$  with:
        *    $r^0_{u,m}=f(u)$ 
        *    $r^{\ell_{u,m}}_{u,m}=f(u\oplus e_m)$ 
        *    $(r^j_{u,m},r^{j+1}_{u,m})\in E$ 
        *    $\ell_{u,m}\le L_{\max}$  (small, e.g., 2–4)

Constraint form:

$$
\forall (u,m):\quad r^0_{u,m}=f(u),\;\; r^{\ell_{u,m}}_{u,m}=f(u\oplus e_m),\;\; (r^j_{u,m},r^{j+1}_{u,m})\in E
$$
 
$$
\forall (u,m):\;\;\ell_{u,m}\le L_{\max}
$$
 
$$
f(u)\in V^+,\;\; f \text{ injective}
$$

This is the “deployable” version: it respects your **6-direction hex structure** while still achieving a **full 16-vertex tesseract** as a routed subgraph.

* * *

Optimum path with up to 7 decisions inside the embedded tesseract
-----------------------------------------------------------------

You’re optimizing a length- $L\le 7$  walk on the tesseract vertices, then projecting into the hex net via  $f$ .

*   Path on tesseract vertices:  $u_0,u_1,\dots,u_L$  with
    
$$
\|u_{k+1}-u_k\|_1 = 1 \quad (\text{Hamming-1 step})
$$
*   Projected nodes:  $x_k=f(u_k)$ , and trust gate implies  $t_{x_k}>0$ 

A clean objective (value × trust, minus movement cost):

$$
\max_{L\le 7,\;u_0..u_L,\;f,\;R}\;\;\sum_{k=0}^{L} \big(v_{f(u_k)}\cdot t_{f(u_k)}\big)\;-\;\lambda\sum_{k=0}^{L-1} \text{Cost}(u_k\to u_{k+1})
$$

Where movement cost can be:

*   **Strict embedding:**  $\text{Cost}(u_k\to u_{k+1}) = c\big(f(u_k),f(u_{k+1})\big)$  with  $(f(u_k),f(u_{k+1}))\in E$ 
*   **Routed embedding:**  $\text{Cost}(u_k\to u_{k+1}) = \ell_{u_k,m}$  (route length for that hypercube edge)

Add the trust constraint explicitly:

$$
t_{f(u_k)} > 0\quad \forall k
$$

* * *

“6-node” interpretation (how it fits mathematically)
----------------------------------------------------

If by “6-node” you mean “6-direction” (hex adjacency), the above is the correct formalization. If you literally mean “only 6 physical nodes” are allowed, you **cannot** embed a full tesseract (needs 16 distinct vertices) unless you permit node reuse (which breaks injectivity and collapses the hypercube).

* * *

If you want this to be solver-ready (ILP / CP-SAT), the next step is to convert  $f$  and routing into binaries:

*    $z_{u,i}\in\{0,1\}$ : tesseract vertex  $u$  assigned to hex node  $i$ 
*   enforce  $\sum_i z_{u,i}=1$ ,  $\sum_u z_{u,i}\le 1$ , and routing/adjacency constraints per edge.

## Prompt:
solver-ready (ILP / CP-SAT), the next step is to convert fff and routing into binaries

explain this

## Response:
Here’s the **straight explanation**, no abstraction fluff.

* * *

What “convert  $f$  and routing into binaries” actually means
-------------------------------------------------------------

You currently have a **conceptual model**:

*    $f$ : maps **tesseract vertices → hex-network nodes**
*    $R$ : routes **tesseract edges → hex paths**

That’s mathematically clean, but **solvers don’t understand functions**.  
ILP / CP-SAT solvers only understand **binary decision variables + linear constraints**.

So we **flatten the intelligence into switches**.

* * *

Step 1: Replace the mapping function  $f$  with binary variables
----------------------------------------------------------------

Instead of:

$$
f(u) = i
$$

We define:

$$
z_{u,i} = \begin{cases} 1 & \text{if tesseract vertex } u \text{ is assigned to hex node } i \\ 0 & \text{otherwise} \end{cases}
$$

This turns “assignment” into a **yes/no decision** the solver can optimize.

### Required constraints

*   **Each tesseract vertex maps to exactly one hex node**
    
$$
\sum_{i \in V} z_{u,i} = 1 \quad \forall u
$$
*   **No hex node can host more than one tesseract vertex**
    
$$
\sum_{u \in U} z_{u,i} \le 1 \quad \forall i
$$
*   **Trust gate**
    
$$
z_{u,i} = 0 \quad \text{if } t_i \le 0
$$

➡️ Result: a **one-to-one, trust-positive embedding** enforced by math.

* * *

Step 2: Replace routing paths with binary edge-usage variables
--------------------------------------------------------------

Instead of:

$$
R_{u,m} = (r^0, r^1, \dots, r^\ell)
$$

Define:

$$
y_{u,m,e} = \begin{cases} 1 & \text{if hex edge } e \text{ is used to realize tesseract edge } (u,m) \\ 0 & \text{otherwise} \end{cases}
$$

Where:

*    $u$  = tesseract vertex
*    $m$  = hypercube dimension (1–4)
*    $e \in E$  = hex-network edge

* * *

Step 3: Enforce valid routing (flow constraints)
------------------------------------------------

For each tesseract edge  $(u,m)$ :

### Start at the mapped source

$$
\sum_{e \in \delta^+(i)} y_{u,m,e} - \sum_{e \in \delta^-(i)} y_{u,m,e} = z_{u,i}
$$

### End at the mapped destination

$$
\sum_{e \in \delta^+(i)} y_{u,m,e} - \sum_{e \in \delta^-(i)} y_{u,m,e} = - z_{u\oplus e_m,i}
$$

### Intermediate nodes must conserve flow

$$
\sum_{e \in \delta^+(i)} y_{u,m,e} - \sum_{e \in \delta^-(i)} y_{u,m,e} = 0
$$

This guarantees:

*   Routes **start and end correctly**
*   No teleportation
*   No broken paths

* * *

Step 4: Limit complexity (why this stays computable)
----------------------------------------------------

You cap routing length:

$$
\sum_{e} y_{u,m,e} \le L_{\max}
$$

This prevents the solver from “cheating” with giant loops.

* * *

Step 5: Objective function (what the solver is optimizing)
----------------------------------------------------------

Now everything is binary, so optimization becomes trivial for the solver:

$$
\max \sum_{u,i} z_{u,i}(v_i \cdot t_i) \;-\; \lambda \sum_{u,m,e} y_{u,m,e}
$$

Interpretation:

*   **Reward** high-value, high-trust nodes
*   **Penalize** longer or more complex routes
*   Automatically selects the **optimal embedding + traversal**

* * *

Why this matters (business logic translation)
---------------------------------------------

*   You’ve converted **neural reasoning** into a **deterministic optimization engine**
*   Trust becomes a **hard gate**, not a probability
*   The “optimum path” is **provably optimal**, not heuristic
*   This scales → more nodes, higher dimensions, same structure

In short:  
**You turned abstract intelligence into executable economics.**

If you want, next step is:

*   CP-SAT (faster, more scalable), or
*   A\* + constraint pruning (real-time, approximate, cheaper).

## Prompt:
convert this to code

## Response:
```
"""
Tesseract (4D hypercube) -> Hex-grid network embedding + routed edges (multi-hop),
modeled as a binary optimization (ILP/CP-SAT) using OR-Tools CP-SAT.

What it does
- Chooses an injective mapping f: {0,1}^4 (16 vertices) -> hex nodes with trust > 0
- For every tesseract edge (u -> u^flip_dim), chooses a short route in the hex graph
- Optimizes: maximize sum(value*trust of selected nodes) - lambda*(total route length)

You provide
- nodes: list of node IDs
- edges: list of directed edges (u,v) (or undirected; we’ll convert to directed)
- value[node], trust[node]
- L_max: max hops per tesseract edge (routing cap)
"""

from ortools.sat.python import cp_model
from collections import defaultdict
import itertools

# -----------------------------
# Helpers: tesseract definition
# -----------------------------
def tesseract_vertices():
    # Represent vertex as int 0..15 where bits are the 4D coordinates
    return list(range(16))

def flip_bit(u: int, dim: int) -> int:
    # dim in {0,1,2,3} flips that bit
    return u ^ (1 << dim)

def tesseract_edges_directed():
    # Directed edges (u, dim) meaning u -> u^e_dim
    U = tesseract_vertices()
    for u in U:
        for dim in range(4):
            yield (u, dim, flip_bit(u, dim))

# -----------------------------------
# Core solver: binary embedding model
# -----------------------------------
def solve_tesseract_embedding(
    nodes,
    undirected_edges,
    value,
    trust,
    L_max=3,
    lam=1,
    time_limit_s=30,
    log=False,
):
    """
    nodes: list of node IDs (hashable)
    undirected_edges: list of (a,b) edges
    value: dict node->float (can be int)
    trust: dict node->float (can be int); trust>0 is required for selection
    L_max: int, max hops allowed per tesseract edge route
    lam: int, penalty weight per used hex-edge hop
    """

    # Convert to directed edge set E_dir
    E_dir = set()
    for a, b in undirected_edges:
        E_dir.add((a, b))
        E_dir.add((b, a))
    E_dir = list(E_dir)

    # Precompute outgoing/incoming adjacency for flow constraints
    out_edges = defaultdict(list)
    in_edges = defaultdict(list)
    for (a, b) in E_dir:
        out_edges[a].append((a, b))
        in_edges[b].append((a, b))

    # Trust-gated candidate nodes
    eligible_nodes = [i for i in nodes if trust.get(i, 0) > 0]

    # Safety check: need at least 16 eligible nodes for a full tesseract embedding (injective)
    if len(eligible_nodes) < 16:
        raise ValueError(f"Need >= 16 trust-positive nodes; got {len(eligible_nodes)}")

    model = cp_model.CpModel()

    U = tesseract_vertices()
    T_edges = list(tesseract_edges_directed())  # (u, dim, v)

    # ----------------------------
    # Variables
    # ----------------------------
    # z[u,i] = 1 if tesseract vertex u is assigned to hex node i
    z = {}
    for u in U:
        for i in eligible_nodes:
            z[(u, i)] = model.NewBoolVar(f"z_u{u}_i{i}")

    # For routing: y[u,dim,e] = 1 if hex directed edge e is used in route for tesseract edge (u,dim)
    # e is a tuple (a,b)
    y = {}
    for (u, dim, v) in T_edges:
        for e in E_dir:
            y[(u, dim, e)] = model.NewBoolVar(f"y_u{u}_d{dim}_e{e[0]}_{e[1]}")

    # ----------------------------
    # Mapping constraints (injective)
    # ----------------------------
    # Each tesseract vertex maps to exactly one eligible node
    for u in U:
        model.Add(sum(z[(u, i)] for i in eligible_nodes) == 1)

    # No hex node can host more than one tesseract vertex
    for i in eligible_nodes:
        model.Add(sum(z[(u, i)] for u in U) <= 1)

    # ----------------------------
    # Flow constraints for routing
    # For each tesseract directed edge (u -> v via dim), enforce a single-unit flow
    # from node assigned to u to node assigned to v using y variables on hex directed edges.
    # ----------------------------
    for (u, dim, v) in T_edges:
        # Length cap per routed edge
        model.Add(sum(y[(u, dim, e)] for e in E_dir) <= L_max)

        # Flow conservation on every node i in the graph:
        # out(i) - in(i) = z[u,i] - z[v,i]
        # (i is source if assigned to u; sink if assigned to v; else 0)
        for i in nodes:
            # If i is not eligible, it can still be used as intermediate routing node.
            out_sum = sum(y[(u, dim, e)] for e in out_edges[i]) if out_edges[i] else 0
            in_sum = sum(y[(u, dim, e)] for e in in_edges[i]) if in_edges[i] else 0

            # Need z[u,i] and z[v,i] terms. If i not eligible, those are 0 (not assignable).
            z_ui = z[(u, i)] if i in eligible_nodes else 0
            z_vi = z[(v, i)] if i in eligible_nodes else 0

            # out - in == z_ui - z_vi
            # CP-SAT requires linear expressions; 0 is fine.
            model.Add(out_sum - in_sum == z_ui - z_vi)

    # ----------------------------
    # Objective
    # Maximize sum(value*trust over assigned nodes) - lam*(total hops used)
    # Note: CP-SAT expects integer objective. Scale floats if needed.
    # ----------------------------
    # Convert value*trust to integer score (scale if you use decimals)
    # If your data are floats, pick a SCALE (e.g., 100) and round.
    SCALE = 100
    score = {}
    for i in eligible_nodes:
        score[i] = int(round(value.get(i, 0) * trust.get(i, 0) * SCALE))

    reward_term = sum(score[i] * z[(u, i)] for u in U for i in eligible_nodes)
    hop_term = sum(y[(u, dim, e)] for (u, dim, _) in T_edges for e in E_dir)

    model.Maximize(reward_term - int(lam) * hop_term)

    # ----------------------------
    # Solve
    # ----------------------------
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = float(time_limit_s)
    solver.parameters.log_search_progress = bool(log)

    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {"status": "INFEASIBLE_OR_TIMEOUT"}

    # ----------------------------
    # Extract solution
    # ----------------------------
    # Mapping f(u) = i where z[u,i]=1
    f = {}
    for u in U:
        for i in eligible_nodes:
            if solver.Value(z[(u, i)]) == 1:
                f[u] = i
                break

    # Routes for each tesseract edge (u,dim): list of used directed hex edges
    routes = {}
    for (u, dim, v) in T_edges:
        used = []
        for e in E_dir:
            if solver.Value(y[(u, dim, e)]) == 1:
                used.append(e)
        routes[(u, dim, v)] = used

    return {
        "status": "OPTIMAL" if status == cp_model.OPTIMAL else "FEASIBLE",
        "objective": solver.ObjectiveValue() / SCALE,  # unscale reward component for readability
        "mapping_f": f,
        "routes": routes,
    }

# -----------------------------------
# Minimal example usage (replace with your data)
# -----------------------------------
if __name__ == "__main__":
    # Example tiny hex-ish graph generator using axial coords (radius=3)
    # Produces enough nodes for demonstration.
    def axial_neighbors(q, r):
        dirs = [(1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1)]
        for dq, dr in dirs:
            yield (q+dq, r+dr)

    radius = 3
    coords = []
    for q in range(-radius, radius+1):
        for r in range(-radius, radius+1):
            s = -q - r
            if -radius <= s <= radius:
                coords.append((q, r))

    nodes = coords
    edges = []
    coord_set = set(coords)
    for (q, r) in coords:
        for nb in axial_neighbors(q, r):
            if nb in coord_set:
                edges.append(((q, r), nb))  # undirected edges added twice later is okay

    # Assign demo values/trust
    value = {n: (abs(n[0]) + abs(n[1]) + 1) for n in nodes}
    trust = {n: 1 for n in nodes}  # all eligible (>0)

    result = solve_tesseract_embedding(
        nodes=nodes,
        undirected_edges=edges,
        value=value,
        trust=trust,
        L_max=3,     # cap routing hops
        lam=1,       # hop penalty
        time_limit_s=10,
        log=False,
    )

    print("STATUS:", result["status"])
    if result["status"] in ("OPTIMAL", "FEASIBLE"):
        print("Objective (scaled):", result["objective"])
        print("Mapping f(u)->node (u=0..15):")
        for u in range(16):
            print(u, "->", result["mapping_f"][u])
        # Example: show number of hops used per tesseract edge
        total_hops = sum(len(v) for v in result["routes"].values())
        print("Total routed hops across all tesseract edges:", total_hops)
```

If you want the **“optimum path up to 7 decisions”** layered on top of this (after embedding), you add a second stage that searches the tesseract graph for the best length- $\le7$  walk using the embedded node scores  $v_{f(u)}t_{f(u)}$  and edge costs from the routed hop counts.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)