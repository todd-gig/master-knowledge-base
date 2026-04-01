import React, { useEffect, useState } from 'react'
import { getRegistry, getNamespaces, getHealth, getReady, getApprovalQueue, generateNamespaceDraft, promoteNamespace, submitTransition, emitBillingEvent } from './api'

export default function App() {
  const [registry, setRegistry] = useState({ memory_objects: [] })
  const [namespaces, setNamespaces] = useState({ namespaces: [] })
  const [queue, setQueue] = useState({ items: [] })
  const [health, setHealth] = useState(null)
  const [ready, setReady] = useState(null)
  const [draft, setDraft] = useState(null)
  const [form, setForm] = useState({
    client_name: 'ACME Template',
    industry: 'template',
    preferred_terminology: '{"customer":"stakeholder"}',
    workflow_preferences: 'research_first'
  })
  const [transition, setTransition] = useState({
    memory_id: 'MEM-001',
    from_state: 'validated',
    to_state: 'active',
    reason: 'production promotion'
  })
  const [billing, setBilling] = useState({
    event_type: 'tenant_created',
    amount_cents: 50000,
    currency: 'USD',
    metadata: '{"source":"ui"}'
  })

  async function refresh() {
    setRegistry(await getRegistry())
    setNamespaces(await getNamespaces())
    setQueue(await getApprovalQueue())
    setHealth(await getHealth())
    setReady(await getReady())
  }

  useEffect(() => { refresh() }, [])

  async function makeDraft() {
    const payload = {
      client_name: form.client_name,
      industry: form.industry,
      preferred_terminology: JSON.parse(form.preferred_terminology || '{}'),
      workflow_preferences: form.workflow_preferences.split(',').map(s => s.trim()).filter(Boolean)
    }
    const data = await generateNamespaceDraft(payload)
    setDraft(data.draft)
  }

  async function promote() {
    if (!draft) return
    await promoteNamespace(draft)
    await refresh()
  }

  async function transitionMemory() {
    await submitTransition(transition)
    alert('transition submitted')
  }

  async function sendBilling() {
    await emitBillingEvent({
      event_type: billing.event_type,
      amount_cents: Number(billing.amount_cents),
      currency: billing.currency,
      metadata: JSON.parse(billing.metadata || '{}')
    })
    alert('billing event emitted')
  }

  return (
    <div className="app">
      <aside className="side"><div className="brand">Gigaton Ops v10</div></aside>
      <main className="main">
        <section className="hero">
          <h1 style={{marginTop:0}}>Commercialization control plane</h1>
          <p>Memories: {registry.memory_objects.length} | Namespaces: {namespaces.namespaces.length}</p>
          <p>Health: {health?.ok ? 'ok' : 'unknown'} | Ready: {ready?.ok ? 'ok' : 'unknown'} | Approvals: {queue.items.length}</p>
        </section>
        <section className="grid2">
          <div className="card">
            <h3>Namespace draft + promote</h3>
            <div className="field"><label>Client name</label><input value={form.client_name} onChange={e => setForm({...form, client_name:e.target.value})} /></div>
            <div className="field"><label>Industry</label><input value={form.industry} onChange={e => setForm({...form, industry:e.target.value})} /></div>
            <div className="field"><label>Preferred terminology JSON</label><textarea value={form.preferred_terminology} onChange={e => setForm({...form, preferred_terminology:e.target.value})} /></div>
            <div className="field"><label>Workflow preferences CSV</label><input value={form.workflow_preferences} onChange={e => setForm({...form, workflow_preferences:e.target.value})} /></div>
            <button className="btn" onClick={makeDraft}>Generate draft</button>
            <button className="btn" style={{marginLeft:10}} onClick={promote}>Promote draft</button>
            {draft && <pre>{JSON.stringify(draft, null, 2)}</pre>}
          </div>
          <div className="card">
            <h3>Approval queue</h3>
            <table className="table">
              <thead><tr><th>ID</th><th>Type</th><th>Status</th></tr></thead>
              <tbody>{queue.items.map(item => <tr key={item.id}><td>{item.id}</td><td>{item.type}</td><td>{item.status}</td></tr>)}</tbody>
            </table>
          </div>
        </section>
        <section className="grid2">
          <div className="card">
            <h3>Billing event</h3>
            <div className="field"><label>Event type</label><input value={billing.event_type} onChange={e => setBilling({...billing, event_type:e.target.value})} /></div>
            <div className="field"><label>Amount cents</label><input value={billing.amount_cents} onChange={e => setBilling({...billing, amount_cents:e.target.value})} /></div>
            <div className="field"><label>Currency</label><input value={billing.currency} onChange={e => setBilling({...billing, currency:e.target.value})} /></div>
            <div className="field"><label>Metadata JSON</label><textarea value={billing.metadata} onChange={e => setBilling({...billing, metadata:e.target.value})} /></div>
            <button className="btn" onClick={sendBilling}>Emit billing event</button>
          </div>
          <div className="card">
            <h3>Memory transition</h3>
            <div className="field"><label>Memory ID</label><input value={transition.memory_id} onChange={e => setTransition({...transition, memory_id:e.target.value})} /></div>
            <div className="field"><label>From</label><input value={transition.from_state} onChange={e => setTransition({...transition, from_state:e.target.value})} /></div>
            <div className="field"><label>To</label><input value={transition.to_state} onChange={e => setTransition({...transition, to_state:e.target.value})} /></div>
            <div className="field"><label>Reason</label><input value={transition.reason} onChange={e => setTransition({...transition, reason:e.target.value})} /></div>
            <button className="btn" onClick={transitionMemory}>Submit transition</button>
          </div>
        </section>
      </main>
    </div>
  )
}
