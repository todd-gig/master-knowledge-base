import React, { useEffect, useState } from 'react'
import { createSession, createIntent, getPayment } from './api'

export default function App() {
  const [sessionForm, setSessionForm] = useState({
    provider: 'auto',
    amount_cents: 50000,
    currency: 'usd',
    order_id: 'ORD-001',
    success_url: 'https://example.com/success',
    cancel_url: 'https://example.com/cancel'
  })
  const [intentForm, setIntentForm] = useState({
    provider: 'auto',
    amount_cents: 50000,
    currency: 'usd',
    order_id: 'ORD-002',
    capture_mode: 'automatic'
  })
  const [paymentId, setPaymentId] = useState('')
  const [liveRefresh, setLiveRefresh] = useState(false)
  const [result, setResult] = useState(null)
  const refreshMs = Number(import.meta.env.VITE_REFRESH_MS || 5000)

  useEffect(() => {
    if (!liveRefresh || !paymentId) return
    const timer = setInterval(async () => {
      setResult(await getPayment(paymentId))
    }, refreshMs)
    return () => clearInterval(timer)
  }, [liveRefresh, paymentId, refreshMs])

  return (
    <div className="app">
      <div className="card">
        <h2>Create checkout/session</h2>
        <div className="field"><label>Provider</label><select value={sessionForm.provider} onChange={e => setSessionForm({...sessionForm, provider: e.target.value})}><option value="auto">auto</option><option value="stripe">stripe</option><option value="godaddy_poynt">godaddy_poynt</option></select></div>
        <div className="field"><label>Amount cents</label><input value={sessionForm.amount_cents} onChange={e => setSessionForm({...sessionForm, amount_cents: Number(e.target.value)})} /></div>
        <div className="field"><label>Currency</label><input value={sessionForm.currency} onChange={e => setSessionForm({...sessionForm, currency: e.target.value})} /></div>
        <div className="field"><label>Order ID</label><input value={sessionForm.order_id} onChange={e => setSessionForm({...sessionForm, order_id: e.target.value})} /></div>
        <button className="btn" onClick={async () => setResult(await createSession(sessionForm))}>Create session</button>
      </div>

      <div className="card">
        <h2>Create intent</h2>
        <div className="field"><label>Provider</label><select value={intentForm.provider} onChange={e => setIntentForm({...intentForm, provider: e.target.value})}><option value="auto">auto</option><option value="stripe">stripe</option><option value="godaddy_poynt">godaddy_poynt</option></select></div>
        <div className="field"><label>Amount cents</label><input value={intentForm.amount_cents} onChange={e => setIntentForm({...intentForm, amount_cents: Number(e.target.value)})} /></div>
        <div className="field"><label>Currency</label><input value={intentForm.currency} onChange={e => setIntentForm({...intentForm, currency: e.target.value})} /></div>
        <div className="field"><label>Order ID</label><input value={intentForm.order_id} onChange={e => setIntentForm({...intentForm, order_id: e.target.value})} /></div>
        <button className="btn" onClick={async () => setResult(await createIntent(intentForm))}>Create intent</button>
      </div>

      <div className="card">
        <h2>Lookup payment</h2>
        <div className="field"><label>Payment ID</label><input value={paymentId} onChange={e => setPaymentId(e.target.value)} /></div>
        <div className="field"><label><input type="checkbox" checked={liveRefresh} onChange={e => setLiveRefresh(e.target.checked)} /> Live refresh</label></div>
        <button className="btn" onClick={async () => setResult(await getPayment(paymentId))}>Get payment</button>
      </div>

      <div className="card">
        <h2>Result</h2>
        <pre>{result ? JSON.stringify(result, null, 2) : 'No result yet'}</pre>
      </div>
    </div>
  )
}
