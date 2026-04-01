import React, { useEffect, useState } from 'react'
import { getRegistry, getNamespaces, getHealth, getReady, generateNamespaceDraft, promoteNamespace, submitTransition } from './api'

export default function App() {
  const [registry, setRegistry] = useState({ memory_objects: [] })
  const [namespaces, setNamespaces] = useState({ namespaces: [] })
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

  async function refresh() {
    setRegistry(await getRegistry())
    setNamespaces(await getNamespaces())
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

  return (
    <div className="app">
      <aside className="side"><div className="brand">Gigaton Ops v9</div></aside>
      <main className="main">
        <section className="hero">
          <h1 style={{marginTop:0}}>Launch readiness control plane</h1>
          <p>Memories: {registry.memory_objects.length} | Namespaces: {namespaces.namespaces.length}</p>
          <p>Health: {health?.ok ? 'ok' : 'unknown'} | Ready: {ready?.ok ? 'ok' : 'unknown'}</p>
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
            <h3>Namespaces</h3>
            <table className="table">
              <thead><tr><th>Namespace</th><th>Client</th><th>Status</th></tr></thead>
              <tbody>{namespaces.namespaces.map(ns => <tr key={ns.namespace_id}><td>{ns.namespace_id}</td><td>{ns.client_name}</td><td>{ns.status}</td></tr>)}</tbody>
            </table>
          </div>
        </section>
        <section className="card">
          <h3>Memory transition</h3>
          <div className="field"><label>Memory ID</label><input value={transition.memory_id} onChange={e => setTransition({...transition, memory_id:e.target.value})} /></div>
          <div className="field"><label>From</label><input value={transition.from_state} onChange={e => setTransition({...transition, from_state:e.target.value})} /></div>
          <div className="field"><label>To</label><input value={transition.to_state} onChange={e => setTransition({...transition, to_state:e.target.value})} /></div>
          <div className="field"><label>Reason</label><input value={transition.reason} onChange={e => setTransition({...transition, reason:e.target.value})} /></div>
          <button className="btn" onClick={transitionMemory}>Submit transition</button>
        </section>
      </main>
    </div>
  )
}
