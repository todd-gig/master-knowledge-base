import React, { useEffect, useMemo, useState } from 'react'
import { getRegistry, getNamespaces, generateNamespaceDraft, promoteNamespace, submitTransition } from './api'

export default function App() {
  const [registry, setRegistry] = useState({ memory_objects: [] })
  const [namespaces, setNamespaces] = useState({ namespaces: [] })
  const [draft, setDraft] = useState(null)
  const [form, setForm] = useState({
    client_name: 'ACME Template',
    industry: 'template',
    preferred_terminology: '{}',
    workflow_preferences: 'research_first'
  })
  const [transition, setTransition] = useState({
    memory_id: 'MEM-001',
    from_state: 'validated',
    to_state: 'active',
    reason: 'manual promotion'
  })

  async function refresh() {
    setRegistry(await getRegistry())
    setNamespaces(await getNamespaces())
  }

  useEffect(() => { refresh() }, [])

  const tier1 = useMemo(() => registry.memory_objects.filter(m => m.tier === 1).length, [registry])

  async function onGenerateDraft() {
    const payload = {
      client_name: form.client_name,
      industry: form.industry,
      preferred_terminology: JSON.parse(form.preferred_terminology || '{}'),
      workflow_preferences: form.workflow_preferences.split(',').map(s => s.trim()).filter(Boolean)
    }
    const data = await generateNamespaceDraft(payload)
    setDraft(data.draft)
  }

  async function onPromoteDraft() {
    if (!draft) return
    await promoteNamespace(draft)
    await refresh()
  }

  async function onSubmitTransition() {
    await submitTransition(transition)
    alert('transition submitted')
  }

  return (
    <div className="app">
      <aside className="side">
        <div className="brand">Gigaton Ops v6</div>
        <div className="nav">
          <a href="#overview">Overview</a>
          <a href="#namespaces">Namespaces</a>
          <a href="#transitions">Transitions</a>
        </div>
      </aside>

      <main className="main">
        <section className="hero" id="overview">
          <h1 style={{marginTop:0}}>Production control plane</h1>
          <div className="toolbar">
            <span className="status">Memories: {registry.memory_objects.length}</span>
            <span className="status">Tier 1: {tier1}</span>
            <span className="status">Namespaces: {namespaces.namespaces.length}</span>
          </div>
        </section>

        <section className="grid2" id="namespaces">
          <div className="card">
            <h3>Generate namespace draft</h3>
            <div className="field"><label>Client name</label><input value={form.client_name} onChange={e => setForm({...form, client_name: e.target.value})} /></div>
            <div className="field"><label>Industry</label><input value={form.industry} onChange={e => setForm({...form, industry: e.target.value})} /></div>
            <div className="field"><label>Preferred terminology JSON</label><textarea value={form.preferred_terminology} onChange={e => setForm({...form, preferred_terminology: e.target.value})} /></div>
            <div className="field"><label>Workflow preferences CSV</label><input value={form.workflow_preferences} onChange={e => setForm({...form, workflow_preferences: e.target.value})} /></div>
            <div className="toolbar">
              <button className="btn" onClick={onGenerateDraft}>Generate draft</button>
              <button className="btn secondary" onClick={onPromoteDraft}>Promote draft</button>
            </div>
            {draft && <pre>{JSON.stringify(draft, null, 2)}</pre>}
          </div>

          <div className="card">
            <h3>Active namespaces</h3>
            <table className="table">
              <thead><tr><th>Namespace</th><th>Client</th><th>Industry</th><th>Status</th></tr></thead>
              <tbody>
                {namespaces.namespaces.map(ns => (
                  <tr key={ns.namespace_id}>
                    <td>{ns.namespace_id}</td>
                    <td>{ns.client_name}</td>
                    <td>{ns.industry}</td>
                    <td>{ns.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="card" id="transitions">
          <h3>Submit memory lifecycle transition</h3>
          <div className="grid3">
            <div className="field"><label>Memory ID</label><input value={transition.memory_id} onChange={e => setTransition({...transition, memory_id:e.target.value})} /></div>
            <div className="field"><label>From</label><input value={transition.from_state} onChange={e => setTransition({...transition, from_state:e.target.value})} /></div>
            <div className="field"><label>To</label><input value={transition.to_state} onChange={e => setTransition({...transition, to_state:e.target.value})} /></div>
          </div>
          <div className="field"><label>Reason</label><input value={transition.reason} onChange={e => setTransition({...transition, reason:e.target.value})} /></div>
          <button className="btn" onClick={onSubmitTransition}>Submit transition</button>
        </section>
      </main>
    </div>
  )
}
