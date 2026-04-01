import React, { useEffect, useState } from 'react'
import { createSession, listPayments, listPaymentEvents, runReconciliation, replayWebhook, getProviderHealth } from './api'

export default function App() {
  const [sessionForm, setSessionForm] = useState({ provider:'auto', amount_cents:50000, currency:'usd', order_id:'ORD-001', success_url:'https://example.com/success', cancel_url:'https://example.com/cancel' })
  const [filters, setFilters] = useState({ provider:'', normalized_status:'', order_id:'', q:'' })
  const [payments, setPayments] = useState([])
  const [events, setEvents] = useState([])
  const [health, setHealth] = useState([])
  const [replay, setReplay] = useState({ event_id:'', operator_note:'replay for ops recovery' })
  const [result, setResult] = useState(null)
  const refreshMs = Number(import.meta.env.VITE_REFRESH_MS || 5000)

  async function refreshAll() {
    setPayments(await listPayments(filters))
    setEvents(await listPaymentEvents())
    setHealth(await getProviderHealth())
  }

  useEffect(() => { refreshAll() }, [])
  useEffect(() => {
    const timer = setInterval(refreshAll, refreshMs)
    return () => clearInterval(timer)
  }, [refreshMs])

  return (
    <div className="app">
      <div className="grid2">
        <div className="card">
          <h2>Create checkout/session</h2>
          <div className="field"><label>Provider</label><select value={sessionForm.provider} onChange={e => setSessionForm({...sessionForm, provider: e.target.value})}><option value="auto">auto</option><option value="stripe">stripe</option><option value="godaddy_poynt">godaddy_poynt</option></select></div>
          <div className="field"><label>Amount cents</label><input value={sessionForm.amount_cents} onChange={e => setSessionForm({...sessionForm, amount_cents: Number(e.target.value)})} /></div>
          <div className="field"><label>Currency</label><input value={sessionForm.currency} onChange={e => setSessionForm({...sessionForm, currency: e.target.value})} /></div>
          <div className="field"><label>Order ID</label><input value={sessionForm.order_id} onChange={e => setSessionForm({...sessionForm, order_id: e.target.value})} /></div>
          <button className="btn" onClick={async () => { setResult(await createSession(sessionForm)); await refreshAll() }}>Create session</button>
        </div>

        <div className="card">
          <h2>Search and filter</h2>
          <div className="field"><label>Provider</label><input value={filters.provider} onChange={e => setFilters({...filters, provider:e.target.value})} /></div>
          <div className="field"><label>Status</label><input value={filters.normalized_status} onChange={e => setFilters({...filters, normalized_status:e.target.value})} /></div>
          <div className="field"><label>Order ID</label><input value={filters.order_id} onChange={e => setFilters({...filters, order_id:e.target.value})} /></div>
          <div className="field"><label>Free text</label><input value={filters.q} onChange={e => setFilters({...filters, q:e.target.value})} /></div>
          <button className="btn" onClick={refreshAll}>Apply filters</button>
        </div>
      </div>

      <div className="grid2">
        <div className="card">
          <h2>Reconciliation</h2>
          <button className="btn" onClick={async () => setResult(await runReconciliation())}>Run reconciliation</button>
        </div>
        <div className="card">
          <h2>Webhook replay</h2>
          <div className="field"><label>Event ID</label><input value={replay.event_id} onChange={e => setReplay({...replay, event_id:e.target.value})} /></div>
          <div className="field"><label>Operator note</label><input value={replay.operator_note} onChange={e => setReplay({...replay, operator_note:e.target.value})} /></div>
          <button className="btn" onClick={async () => setResult(await replayWebhook(replay.event_id, replay.operator_note))}>Replay event</button>
        </div>
      </div>

      <div className="card">
        <h2>Provider health</h2>
        <table className="table">
          <thead><tr><th>Provider</th><th>Success</th><th>Failure</th><th>Failure rate</th><th>Window start</th><th>Window end</th></tr></thead>
          <tbody>
            {health.map(h => <tr key={h.id}><td>{h.provider}</td><td>{h.success_count}</td><td>{h.failure_count}</td><td>{h.failure_rate}</td><td>{h.window_start}</td><td>{h.window_end}</td></tr>)}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Recent payments</h2>
        <table className="table">
          <thead><tr><th>ID</th><th>Provider</th><th>Status</th><th>Amount</th><th>Order</th><th>Created</th></tr></thead>
          <tbody>
            {payments.map(p => <tr key={p.payment_id}><td>{p.payment_id}</td><td>{p.provider}</td><td>{p.normalized_status}</td><td>{p.amount_cents} {p.currency}</td><td>{p.order_id}</td><td>{p.created_at}</td></tr>)}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Payment events</h2>
        <table className="table">
          <thead><tr><th>ID</th><th>Provider</th><th>Event</th><th>Status</th><th>Replayable</th><th>Created</th></tr></thead>
          <tbody>
            {events.map(e => <tr key={e.id}><td>{e.id}</td><td>{e.provider}</td><td>{e.event_type}</td><td>{e.normalized_status}</td><td>{String(e.replayable)}</td><td>{e.created_at}</td></tr>)}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h2>Result</h2>
        <pre>{result ? JSON.stringify(result, null, 2) : 'No result yet'}</pre>
      </div>
    </div>
  )
}
