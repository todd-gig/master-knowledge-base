import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  BarChart,
  Bar,
  Legend,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Slider } from "@/components/ui/slider";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Separator } from "@/components/ui/separator";
import { TrendingUp, AlertTriangle, Gauge, Target, Layers3 } from "lucide-react";

type ScenarioName = "conservative" | "base" | "aggressive";

type BenchmarkConfig = {
  profitability: number;
  bias: number;
  customerScale: number;
  revenueCostRatio: number;
};

type ScenarioPreset = {
  name: ScenarioName;
  label: string;
  description: string;
  leadGrowthRate: number;
  aovGrowthRate: number;
  costGrowthRate: number;
  brandLift: number;
  interactionLift: number;
  productLift: number;
  competitorPressureDrift: number;
  riskDrift: number;
  disappointmentDecay: number;
  periods: number;
  monteCarloRuns: number;
};

type BusinessState = {
  brandVoiceScore: number;
  positioningClarityScore: number;
  trustSignalScore: number;
  brandConsistencyScore: number;
  interactionClarityScore: number;
  interactionFrictionScore: number;
  personalizationScore: number;
  responseTimeScore: number;
  interactionConsistencyScore: number;
  productUtilityScore: number;
  productQualityScore: number;
  differentiationScore: number;
  timeToValueScore: number;
  memoryTrustScore: number;
  disappointmentScore: number;
  perceivedRiskScore: number;
  competitorPressureScore: number;
  leadVolume: number;
  activeCustomers: number;
  averageOrderValue: number;
  monetizationEfficiency: number;
  usageIntensity: number;
  fixedCost: number;
  acquisitionCostPerLead: number;
  serviceCostPerCustomer: number;
  experienceManagementCost: number;
  productDeliveryCost: number;
  historicalProfitSeries: number[];
};

type StepResult = {
  period: number;
  brandStrength: number;
  interactionQuality: number;
  productValue: number;
  trustMemory: number;
  friction: number;
  experienceEngineering: number;
  customerBias: number;
  conversionProbability: number;
  retentionProbability: number;
  newCustomers: number;
  churnedCustomers: number;
  customerCount: number;
  effectiveOrderValue: number;
  revenue: number;
  totalCost: number;
  profit: number;
  predictabilityCoefficient: number;
  predictableProfitability: number;
  revenueCostRatio: number;
  profitabilityScore: number;
  biasScore: number;
  scaleScore: number;
  efficiencyScore: number;
  successScore: number;
  successClass: string;
};

type MonteCarloSummary = {
  avgFinalSuccessScore: number;
  p10FinalSuccessScore: number;
  p50FinalSuccessScore: number;
  p90FinalSuccessScore: number;
  avgFinalProfit: number;
  avgFinalCustomerCount: number;
  avgFinalRevenue: number;
};

const clamp = (value: number, min = 0, max = 1) => Math.max(min, Math.min(value, max));
const safeDivide = (n: number, d: number, fallback = 0) => (d === 0 ? fallback : n / d);
const sigmoid = (x: number) => 1 / (1 + Math.exp(-x));
const mean = (arr: number[]) => (arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0);
const variance = (arr: number[]) => {
  if (arr.length <= 1) return 0;
  const m = mean(arr);
  return arr.reduce((acc, v) => acc + (v - m) ** 2, 0) / arr.length;
};
const percentile = (arr: number[], p: number) => {
  if (!arr.length) return 0;
  const sorted = [...arr].sort((a, b) => a - b);
  const idx = (p / 100) * (sorted.length - 1);
  const low = Math.floor(idx);
  const high = Math.ceil(idx);
  if (low === high) return sorted[low];
  const frac = idx - low;
  return sorted[low] + (sorted[high] - sorted[low]) * frac;
};
const formatCurrency = (n: number) =>
  new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(n);
const formatPercent = (n: number) => `${(n * 100).toFixed(1)}%`;
const classifySuccess = (score: number) => {
  if (score < 0.25) return "failing";
  if (score < 0.5) return "unstable";
  if (score < 0.7) return "performing";
  if (score < 0.85) return "advantaged";
  return "dominant";
};

const BENCHMARKS: BenchmarkConfig = {
  profitability: 100000,
  bias: 0.8,
  customerScale: 1000,
  revenueCostRatio: 3.0,
};

const PRESETS: Record<ScenarioName, ScenarioPreset> = {
  conservative: {
    name: "conservative",
    label: "Conservative",
    description: "Capital preservation, lower demand expansion, tighter upside assumptions.",
    leadGrowthRate: 0.015,
    aovGrowthRate: 0.008,
    costGrowthRate: 0.01,
    brandLift: 0.005,
    interactionLift: 0.005,
    productLift: 0.004,
    competitorPressureDrift: 0.008,
    riskDrift: 0.004,
    disappointmentDecay: 0.015,
    periods: 12,
    monteCarloRuns: 250,
  },
  base: {
    name: "base",
    label: "Base",
    description: "Balanced operating case with moderate compounding improvements.",
    leadGrowthRate: 0.035,
    aovGrowthRate: 0.015,
    costGrowthRate: 0.018,
    brandLift: 0.01,
    interactionLift: 0.012,
    productLift: 0.01,
    competitorPressureDrift: 0.002,
    riskDrift: -0.003,
    disappointmentDecay: 0.025,
    periods: 12,
    monteCarloRuns: 300,
  },
  aggressive: {
    name: "aggressive",
    label: "Aggressive",
    description: "Growth-maximizing case with higher upside and more operating strain.",
    leadGrowthRate: 0.07,
    aovGrowthRate: 0.025,
    costGrowthRate: 0.032,
    brandLift: 0.016,
    interactionLift: 0.018,
    productLift: 0.015,
    competitorPressureDrift: -0.002,
    riskDrift: -0.006,
    disappointmentDecay: 0.03,
    periods: 12,
    monteCarloRuns: 400,
  },
};

const DEFAULT_STATE: BusinessState = {
  brandVoiceScore: 0.72,
  positioningClarityScore: 0.68,
  trustSignalScore: 0.66,
  brandConsistencyScore: 0.7,
  interactionClarityScore: 0.69,
  interactionFrictionScore: 0.28,
  personalizationScore: 0.55,
  responseTimeScore: 0.74,
  interactionConsistencyScore: 0.67,
  productUtilityScore: 0.76,
  productQualityScore: 0.71,
  differentiationScore: 0.62,
  timeToValueScore: 0.64,
  memoryTrustScore: 0.58,
  disappointmentScore: 0.18,
  perceivedRiskScore: 0.24,
  competitorPressureScore: 0.31,
  leadVolume: 500,
  activeCustomers: 220,
  averageOrderValue: 1200,
  monetizationEfficiency: 0.62,
  usageIntensity: 0.58,
  fixedCost: 85000,
  acquisitionCostPerLead: 35,
  serviceCostPerCustomer: 45,
  experienceManagementCost: 18000,
  productDeliveryCost: 24000,
  historicalProfitSeries: [15000, 18000, 13000, 21000, 19000, 17000],
};

function normalizeBrand(state: BusinessState) {
  return clamp(
    state.brandVoiceScore * 0.25 +
      state.positioningClarityScore * 0.25 +
      state.trustSignalScore * 0.25 +
      state.brandConsistencyScore * 0.25,
  );
}

function normalizeInteraction(state: BusinessState) {
  return clamp(
    state.interactionClarityScore * 0.25 +
      (1 - state.interactionFrictionScore) * 0.2 +
      state.personalizationScore * 0.2 +
      state.responseTimeScore * 0.15 +
      state.interactionConsistencyScore * 0.2,
  );
}

function normalizeProduct(state: BusinessState) {
  return clamp(
    state.productUtilityScore * 0.3 +
      state.productQualityScore * 0.3 +
      state.differentiationScore * 0.2 +
      state.timeToValueScore * 0.2,
  );
}

function normalizeMemory(state: BusinessState) {
  return clamp(state.memoryTrustScore - state.disappointmentScore);
}

function normalizeFriction(state: BusinessState) {
  return clamp(
    state.perceivedRiskScore * 0.3 +
      state.interactionFrictionScore * 0.25 +
      state.disappointmentScore * 0.2 +
      state.competitorPressureScore * 0.25,
  );
}

function computeOneStep(state: BusinessState) {
  const brandStrength = normalizeBrand(state);
  const interactionQuality = normalizeInteraction(state);
  const productValue = normalizeProduct(state);
  const trustMemory = normalizeMemory(state);
  const friction = normalizeFriction(state);

  const experienceEngineering = clamp(0.45 * brandStrength + 0.45 * interactionQuality + 0.1 * brandStrength * interactionQuality);
  const customerBias = clamp(sigmoid(-1 + 2.2 * experienceEngineering + 1.6 * productValue + 1.8 * trustMemory - 2.0 * friction));
  const conversionProbability = clamp(sigmoid(-1.2 + 2.0 * customerBias + 1.5 * productValue - 1.7 * friction));
  const retentionProbability = clamp(
    sigmoid(-0.8 + 2.0 * customerBias + 1.4 * productValue + 1.5 * experienceEngineering - 1.3 * state.competitorPressureScore),
  );

  const newCustomers = state.leadVolume * conversionProbability;
  const churnedCustomers = state.activeCustomers * (1 - retentionProbability);
  const customerCount = Math.max(0, state.activeCustomers + newCustomers - churnedCustomers);

  const effectiveOrderValue = state.averageOrderValue * (1 + 0.25 * customerBias + 0.2 * productValue + 0.2 * state.usageIntensity + 0.35 * state.monetizationEfficiency);
  const revenue = customerCount * effectiveOrderValue;
  const totalCost =
    state.fixedCost +
    state.leadVolume * state.acquisitionCostPerLead +
    customerCount * state.serviceCostPerCustomer +
    state.experienceManagementCost +
    state.productDeliveryCost;
  const profit = revenue - totalCost;

  const profitSeries = [...state.historicalProfitSeries, profit].slice(-12);
  const predictabilityCoefficient = clamp(Math.exp(-0.000001 * variance(profitSeries)));
  const predictableProfitability = profit * predictabilityCoefficient;
  const revenueCostRatio = safeDivide(revenue, totalCost, 0);

  const profitabilityScore = clamp(safeDivide(predictableProfitability, BENCHMARKS.profitability, 0));
  const biasScore = clamp(safeDivide(customerBias, BENCHMARKS.bias, 0));
  const scaleScore = clamp(safeDivide(customerCount, BENCHMARKS.customerScale, 0));
  const efficiencyScore = clamp(safeDivide(revenueCostRatio, BENCHMARKS.revenueCostRatio, 0));
  const successScore = clamp(0.4 * profitabilityScore + 0.2 * biasScore + 0.2 * scaleScore + 0.2 * efficiencyScore);

  return {
    brandStrength,
    interactionQuality,
    productValue,
    trustMemory,
    friction,
    experienceEngineering,
    customerBias,
    conversionProbability,
    retentionProbability,
    newCustomers,
    churnedCustomers,
    customerCount,
    effectiveOrderValue,
    revenue,
    totalCost,
    profit,
    predictabilityCoefficient,
    predictableProfitability,
    revenueCostRatio,
    profitabilityScore,
    biasScore,
    scaleScore,
    efficiencyScore,
    successScore,
    successClass: classifySuccess(successScore),
    updatedProfitSeries: profitSeries,
  };
}

function evolveState(state: BusinessState, preset: ScenarioPreset, step: ReturnType<typeof computeOneStep>) {
  return {
    ...state,
    brandVoiceScore: clamp(state.brandVoiceScore + preset.brandLift),
    positioningClarityScore: clamp(state.positioningClarityScore + preset.brandLift),
    trustSignalScore: clamp(state.trustSignalScore + preset.brandLift * 0.8),
    brandConsistencyScore: clamp(state.brandConsistencyScore + preset.brandLift * 0.9),
    interactionClarityScore: clamp(state.interactionClarityScore + preset.interactionLift),
    interactionFrictionScore: clamp(state.interactionFrictionScore - preset.interactionLift * 0.6),
    personalizationScore: clamp(state.personalizationScore + preset.interactionLift),
    responseTimeScore: clamp(state.responseTimeScore + preset.interactionLift * 0.7),
    interactionConsistencyScore: clamp(state.interactionConsistencyScore + preset.interactionLift * 0.8),
    productUtilityScore: clamp(state.productUtilityScore + preset.productLift),
    productQualityScore: clamp(state.productQualityScore + preset.productLift),
    differentiationScore: clamp(state.differentiationScore + preset.productLift * 0.8),
    timeToValueScore: clamp(state.timeToValueScore + preset.productLift * 0.6),
    memoryTrustScore: clamp(0.65 * state.memoryTrustScore + 0.2 * step.experienceEngineering + 0.15 * step.productValue),
    disappointmentScore: clamp(Math.max(0, 0.7 * state.disappointmentScore + 0.3 * (1 - step.retentionProbability) - preset.disappointmentDecay)),
    perceivedRiskScore: clamp(0.6 * state.perceivedRiskScore + 0.2 * (1 - step.customerBias) + 0.2 * (1 - step.experienceEngineering) + preset.riskDrift),
    competitorPressureScore: clamp(state.competitorPressureScore + preset.competitorPressureDrift),
    leadVolume: Math.max(0, state.leadVolume * (1 + preset.leadGrowthRate)),
    activeCustomers: step.customerCount,
    averageOrderValue: Math.max(0, state.averageOrderValue * (1 + preset.aovGrowthRate)),
    fixedCost: Math.max(0, state.fixedCost * (1 + preset.costGrowthRate)),
    acquisitionCostPerLead: Math.max(0, state.acquisitionCostPerLead * (1 + preset.costGrowthRate * 0.5)),
    serviceCostPerCustomer: Math.max(0, state.serviceCostPerCustomer * (1 + preset.costGrowthRate * 0.4)),
    experienceManagementCost: Math.max(0, state.experienceManagementCost * (1 + preset.costGrowthRate * 0.8)),
    productDeliveryCost: Math.max(0, state.productDeliveryCost * (1 + preset.costGrowthRate * 0.6)),
    historicalProfitSeries: step.updatedProfitSeries,
  };
}

function runScenario(baseState: BusinessState, preset: ScenarioPreset): StepResult[] {
  let state = { ...baseState, historicalProfitSeries: [...baseState.historicalProfitSeries] };
  const steps: StepResult[] = [];

  for (let period = 1; period <= preset.periods; period += 1) {
    const step = computeOneStep(state);
    steps.push({ period, ...step });
    state = evolveState(state, preset, step);
  }

  return steps;
}

function runMonteCarlo(baseState: BusinessState, preset: ScenarioPreset): MonteCarloSummary {
  const success: number[] = [];
  const profit: number[] = [];
  const customers: number[] = [];
  const revenue: number[] = [];

  for (let i = 0; i < preset.monteCarloRuns; i += 1) {
    let state = { ...baseState, historicalProfitSeries: [...baseState.historicalProfitSeries] };
    const randomizedPreset = {
      ...preset,
      leadGrowthRate: preset.leadGrowthRate + (Math.random() - 0.5) * 0.02,
      aovGrowthRate: preset.aovGrowthRate + (Math.random() - 0.5) * 0.01,
      costGrowthRate: Math.max(0, preset.costGrowthRate + (Math.random() - 0.5) * 0.015),
      competitorPressureDrift: preset.competitorPressureDrift + (Math.random() - 0.5) * 0.01,
      riskDrift: preset.riskDrift + (Math.random() - 0.5) * 0.01,
    };

    let lastStep: StepResult | null = null;
    for (let period = 1; period <= preset.periods; period += 1) {
      const step = computeOneStep(state);
      lastStep = { period, ...step };
      state = evolveState(state, randomizedPreset, step);
    }

    if (lastStep) {
      success.push(lastStep.successScore);
      profit.push(lastStep.profit);
      customers.push(lastStep.customerCount);
      revenue.push(lastStep.revenue);
    }
  }

  return {
    avgFinalSuccessScore: mean(success),
    p10FinalSuccessScore: percentile(success, 10),
    p50FinalSuccessScore: percentile(success, 50),
    p90FinalSuccessScore: percentile(success, 90),
    avgFinalProfit: mean(profit),
    avgFinalCustomerCount: mean(customers),
    avgFinalRevenue: mean(revenue),
  };
}

function MetricCard({ title, value, subtext, icon }: { title: string; value: string; subtext: string; icon: React.ReactNode }) {
  return (
    <Card className="rounded-2xl border-slate-200 shadow-sm">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm text-slate-500">{title}</p>
            <p className="mt-2 text-3xl font-semibold tracking-tight text-slate-900">{value}</p>
            <p className="mt-2 text-xs text-slate-500">{subtext}</p>
          </div>
          <div className="rounded-2xl bg-slate-100 p-3 text-slate-700">{icon}</div>
        </div>
      </CardContent>
    </Card>
  );
}

function ScoreBadge({ score }: { score: number }) {
  const label = classifySuccess(score);
  return <Badge className="rounded-full px-3 py-1 text-xs uppercase tracking-wide">{label}</Badge>;
}

function NumericInput({ label, value, onChange, step = 1 }: { label: string; value: number; onChange: (v: number) => void; step?: number }) {
  return (
    <div className="space-y-2">
      <Label>{label}</Label>
      <Input type="number" step={step} value={Number.isFinite(value) ? value : 0} onChange={(e) => onChange(Number(e.target.value))} />
    </div>
  );
}

function SliderInput({
  label,
  value,
  onChange,
}: {
  label: string;
  value: number;
  onChange: (v: number) => void;
}) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <Label>{label}</Label>
        <span className="text-xs text-slate-500">{value.toFixed(2)}</span>
      </div>
      <Slider value={[value]} min={0} max={1} step={0.01} onValueChange={(vals) => onChange(vals[0])} />
    </div>
  );
}

export default function GigatonScenarioDashboard() {
  const [scenario, setScenario] = useState<ScenarioName>("base");
  const [state, setState] = useState<BusinessState>(DEFAULT_STATE);

  const preset = PRESETS[scenario];

  const steps = useMemo(() => runScenario(state, preset), [state, preset]);
  const monteCarlo = useMemo(() => runMonteCarlo(state, preset), [state, preset]);
  const lastStep = steps[steps.length - 1];

  const comparisonData = useMemo(() => {
    return (Object.keys(PRESETS) as ScenarioName[]).map((key) => {
      const scenarioSteps = runScenario(state, PRESETS[key]);
      const last = scenarioSteps[scenarioSteps.length - 1];
      return {
        name: PRESETS[key].label,
        success: Number((last?.successScore ?? 0).toFixed(3)),
        profit: Number((last?.profit ?? 0).toFixed(0)),
        customers: Number((last?.customerCount ?? 0).toFixed(0)),
      };
    });
  }, [state]);

  const radarData = useMemo(() => {
    if (!lastStep) return [];
    return [
      { metric: "Brand", value: Number(lastStep.brandStrength.toFixed(3)) },
      { metric: "Interaction", value: Number(lastStep.interactionQuality.toFixed(3)) },
      { metric: "Product", value: Number(lastStep.productValue.toFixed(3)) },
      { metric: "Bias", value: Number(lastStep.customerBias.toFixed(3)) },
      { metric: "Efficiency", value: Number(lastStep.efficiencyScore.toFixed(3)) },
      { metric: "Scale", value: Number(lastStep.scaleScore.toFixed(3)) },
    ];
  }, [lastStep]);

  const issues = useMemo(() => {
    if (!lastStep) return [];
    const out: string[] = [];
    if (lastStep.brandStrength < 0.5) out.push("Brand system is constraining downstream preference formation.");
    if (lastStep.interactionQuality < 0.5) out.push("Interaction quality is degrading conversion leverage.");
    if (lastStep.customerBias < 0.5) out.push("Customer preference is too weak to create efficient growth.");
    if (lastStep.retentionProbability < 0.6) out.push("Retention weakness is likely increasing CAC burden.");
    if (lastStep.revenueCostRatio < 1.2) out.push("Revenue-to-cost ratio is below a viable scaling threshold.");
    if (lastStep.predictabilityCoefficient < 0.6) out.push("Profit volatility is undermining predictable profitability.");
    return out;
  }, [lastStep]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-7xl px-4 py-8 md:px-8">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-sm font-medium uppercase tracking-[0.2em] text-slate-500">Gigaton Scenario Dashboard</p>
              <h1 className="mt-2 text-4xl font-semibold tracking-tight">Experience Engineering Scenario Analysis</h1>
              <p className="mt-3 max-w-3xl text-sm text-slate-600">
                Stress-test how brand, interaction, product quality, customer bias, revenue, cost, and predictability compound into benchmark-normalized success.
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {(Object.keys(PRESETS) as ScenarioName[]).map((key) => (
                <Button key={key} variant={scenario === key ? "default" : "outline"} className="rounded-2xl" onClick={() => setScenario(key)}>
                  {PRESETS[key].label}
                </Button>
              ))}
            </div>
          </div>
        </motion.div>

        <Alert className="mb-8 rounded-2xl border-slate-200 bg-white">
          <AlertDescription className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
            <div>
              <span className="font-medium">Selected scenario:</span> {preset.label} — {preset.description}
            </div>
            {lastStep ? <ScoreBadge score={lastStep.successScore} /> : null}
          </AlertDescription>
        </Alert>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
          <MetricCard title="Final Success Score" value={lastStep ? lastStep.successScore.toFixed(3) : "0.000"} subtext="Benchmark-normalized composite score" icon={<Gauge className="h-5 w-5" />} />
          <MetricCard title="Final Profit" value={lastStep ? formatCurrency(lastStep.profit) : "$0"} subtext="Period-end operating surplus" icon={<TrendingUp className="h-5 w-5" />} />
          <MetricCard title="Final Customer Count" value={lastStep ? lastStep.customerCount.toFixed(0) : "0"} subtext="Active customers after conversion and churn" icon={<Layers3 className="h-5 w-5" />} />
          <MetricCard title="Predictability" value={lastStep ? formatPercent(lastStep.predictabilityCoefficient) : "0.0%"} subtext="Variance-adjusted profitability coefficient" icon={<Target className="h-5 w-5" />} />
        </div>

        <Tabs defaultValue="dashboard" className="mt-8">
          <TabsList className="grid w-full grid-cols-3 rounded-2xl bg-white">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="drivers">Driver Inputs</TabsTrigger>
            <TabsTrigger value="economics">Economic Inputs</TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard" className="mt-6 space-y-6">
            <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
              <Card className="rounded-2xl border-slate-200 xl:col-span-2">
                <CardHeader>
                  <CardTitle>Scenario Progression</CardTitle>
                </CardHeader>
                <CardContent className="h-[360px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={steps}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="period" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="successScore" name="Success" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="customerBias" name="Bias" strokeWidth={2} dot={false} />
                      <Line type="monotone" dataKey="revenueCostRatio" name="Rev/Cost" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="rounded-2xl border-slate-200">
                <CardHeader>
                  <CardTitle>Capability Radar</CardTitle>
                </CardHeader>
                <CardContent className="h-[360px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={radarData}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="metric" />
                      <PolarRadiusAxis domain={[0, 1]} />
                      <Radar dataKey="value" fillOpacity={0.4} />
                    </RadarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-1 gap-6 xl:grid-cols-2">
              <Card className="rounded-2xl border-slate-200">
                <CardHeader>
                  <CardTitle>Scenario Comparison</CardTitle>
                </CardHeader>
                <CardContent className="h-[320px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={comparisonData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="success" name="Success" />
                      <Bar dataKey="customers" name="Customers" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="rounded-2xl border-slate-200">
                <CardHeader>
                  <CardTitle>Monte Carlo Envelope</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
                    <div>
                      <p className="text-xs text-slate-500">Avg Final Success</p>
                      <p className="text-xl font-semibold">{monteCarlo.avgFinalSuccessScore.toFixed(3)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">P10</p>
                      <p className="text-xl font-semibold">{monteCarlo.p10FinalSuccessScore.toFixed(3)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">P50</p>
                      <p className="text-xl font-semibold">{monteCarlo.p50FinalSuccessScore.toFixed(3)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">P90</p>
                      <p className="text-xl font-semibold">{monteCarlo.p90FinalSuccessScore.toFixed(3)}</p>
                    </div>
                  </div>
                  <Separator />
                  <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
                    <div>
                      <p className="text-xs text-slate-500">Avg Final Profit</p>
                      <p className="text-lg font-semibold">{formatCurrency(monteCarlo.avgFinalProfit)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Avg Final Revenue</p>
                      <p className="text-lg font-semibold">{formatCurrency(monteCarlo.avgFinalRevenue)}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Avg Final Customers</p>
                      <p className="text-lg font-semibold">{monteCarlo.avgFinalCustomerCount.toFixed(0)}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card className="rounded-2xl border-slate-200">
              <CardHeader>
                <CardTitle>Constraint Diagnostics</CardTitle>
              </CardHeader>
              <CardContent>
                {issues.length ? (
                  <div className="space-y-3">
                    {issues.map((issue) => (
                      <div key={issue} className="flex items-start gap-3 rounded-2xl bg-slate-50 p-3">
                        <AlertTriangle className="mt-0.5 h-4 w-4" />
                        <p className="text-sm text-slate-700">{issue}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="rounded-2xl bg-slate-50 p-4 text-sm text-slate-700">No critical system constraints flagged under the current configuration.</div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="drivers" className="mt-6">
            <Card className="rounded-2xl border-slate-200">
              <CardHeader>
                <CardTitle>Core Driver Inputs</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-1 gap-8 lg:grid-cols-2">
                <div className="space-y-6">
                  <SliderInput label="Brand Voice" value={state.brandVoiceScore} onChange={(v) => setState((s) => ({ ...s, brandVoiceScore: v }))} />
                  <SliderInput label="Positioning Clarity" value={state.positioningClarityScore} onChange={(v) => setState((s) => ({ ...s, positioningClarityScore: v }))} />
                  <SliderInput label="Trust Signals" value={state.trustSignalScore} onChange={(v) => setState((s) => ({ ...s, trustSignalScore: v }))} />
                  <SliderInput label="Brand Consistency" value={state.brandConsistencyScore} onChange={(v) => setState((s) => ({ ...s, brandConsistencyScore: v }))} />
                  <SliderInput label="Interaction Clarity" value={state.interactionClarityScore} onChange={(v) => setState((s) => ({ ...s, interactionClarityScore: v }))} />
                  <SliderInput label="Interaction Friction" value={state.interactionFrictionScore} onChange={(v) => setState((s) => ({ ...s, interactionFrictionScore: v }))} />
                </div>
                <div className="space-y-6">
                  <SliderInput label="Personalization" value={state.personalizationScore} onChange={(v) => setState((s) => ({ ...s, personalizationScore: v }))} />
                  <SliderInput label="Response Time" value={state.responseTimeScore} onChange={(v) => setState((s) => ({ ...s, responseTimeScore: v }))} />
                  <SliderInput label="Interaction Consistency" value={state.interactionConsistencyScore} onChange={(v) => setState((s) => ({ ...s, interactionConsistencyScore: v }))} />
                  <SliderInput label="Product Utility" value={state.productUtilityScore} onChange={(v) => setState((s) => ({ ...s, productUtilityScore: v }))} />
                  <SliderInput label="Product Quality" value={state.productQualityScore} onChange={(v) => setState((s) => ({ ...s, productQualityScore: v }))} />
                  <SliderInput label="Differentiation" value={state.differentiationScore} onChange={(v) => setState((s) => ({ ...s, differentiationScore: v }))} />
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="economics" className="mt-6">
            <Card className="rounded-2xl border-slate-200">
              <CardHeader>
                <CardTitle>Economic Inputs</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-1 gap-6 lg:grid-cols-3">
                <NumericInput label="Lead Volume" value={state.leadVolume} onChange={(v) => setState((s) => ({ ...s, leadVolume: v }))} />
                <NumericInput label="Active Customers" value={state.activeCustomers} onChange={(v) => setState((s) => ({ ...s, activeCustomers: v }))} />
                <NumericInput label="Average Order Value" value={state.averageOrderValue} onChange={(v) => setState((s) => ({ ...s, averageOrderValue: v }))} />
                <NumericInput label="Fixed Cost" value={state.fixedCost} onChange={(v) => setState((s) => ({ ...s, fixedCost: v }))} />
                <NumericInput label="Acquisition Cost / Lead" value={state.acquisitionCostPerLead} onChange={(v) => setState((s) => ({ ...s, acquisitionCostPerLead: v }))} />
                <NumericInput label="Service Cost / Customer" value={state.serviceCostPerCustomer} onChange={(v) => setState((s) => ({ ...s, serviceCostPerCustomer: v }))} />
                <NumericInput label="Experience Mgmt Cost" value={state.experienceManagementCost} onChange={(v) => setState((s) => ({ ...s, experienceManagementCost: v }))} />
                <NumericInput label="Product Delivery Cost" value={state.productDeliveryCost} onChange={(v) => setState((s) => ({ ...s, productDeliveryCost: v }))} />
                <NumericInput label="Monetization Efficiency" value={state.monetizationEfficiency} onChange={(v) => setState((s) => ({ ...s, monetizationEfficiency: v }))} step={0.01} />
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
