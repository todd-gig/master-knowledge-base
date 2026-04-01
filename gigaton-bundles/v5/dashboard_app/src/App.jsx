import React, { useMemo, useState } from 'react'
import registry from './data/memory_registry.v5.json'
import namespaces from './data/namespaces.json'
import calibration from './data/calibration_report.json'
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar } from 'recharts'

export default function App() {
  const [categoryFilter, setCategoryFilter] = useState('all')

  const filteredMemories = useMemo(() => {
    const all = registry.memory_objects || []
    return categoryFilter === 'all' ? all : all.filter(m => m.category === categoryFilter)
  }, [categoryFilter])

  const tierData = useMemo(() => {
    const counts = {}
    for (const m of registry.memory_objects || []) counts[m.tier] = (counts[m.tier] || 0) + 1
    return Object.keys(counts).sort().map(k => ({ tier: `Tier ${k}`, count: counts[k] }))
  }, [])

  const qualityData = [
    { name: 'Baseline', score: calibration.baseline_score || 0.85 },
    { name: 'Current', score: calibration.average_feedback_score || 0.9 }
  ]

  const categories = ['all', ...Array.from(new Set((registry.memory_objects || []).map(m => m.category)))]

  return (
    <div className="app">
      <aside className="side">
        <div className="brand">Gigaton Ops v5</div>
        <div className="nav">
          <a href="#overview">Overview</a>
          <a href="#memories">Memories</a>
          <a href="#namespaces">Namespaces</a>
          <a href="#calibration">Calibration</a>
        </div>
      </aside>

      <main className="main">
        <section className="hero" id="overview">
          <h1 style={{marginTop:0}}>Execution control plane</h1>
          <p className="muted">Namespace generation, retrieval calibration, and memory operations in one local operator layer.</p>
          <div className="toolbar" style={{marginTop:12}}>
            <span className="pill">Memories: {registry.memory_objects.length}</span>
            <span className="pill">Namespaces: {namespaces.namespaces.length}</span>
            <span className="pill">Avg feedback: {calibration.average_feedback_score}</span>
          </div>
        </section>

        <section className="grid3">
          <div className="card"><div className="metric">{registry.memory_objects.filter(m => m.tier === 1).length}</div><div className="muted">Tier 1 memories</div></div>
          <div className="card"><div className="metric">{namespaces.namespaces.length}</div><div className="muted">Namespaces</div></div>
          <div className="card"><div className="metric">{calibration.rows_processed}</div><div className="muted">Feedback rows processed</div></div>
        </section>

        <section className="grid2">
          <div className="card" id="calibration">
            <h3 className="sectionTitle">Calibration quality</h3>
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={qualityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0.75, 1.0]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="card">
            <h3 className="sectionTitle">Tier distribution</h3>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={tierData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="tier" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="card" id="memories">
          <h3 className="sectionTitle">Memory registry</h3>
          <div className="toolbar" style={{marginBottom:12}}>
            <label>Filter category:</label>
            <select value={categoryFilter} onChange={e => setCategoryFilter(e.target.value)}>
              {categories.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <table className="table">
            <thead>
              <tr>
                <th>ID</th><th>Title</th><th>Category</th><th>Tier</th><th>Confidence</th><th>Lifecycle</th>
              </tr>
            </thead>
            <tbody>
              {filteredMemories.map(m => (
                <tr key={m.memory_id}>
                  <td>{m.memory_id}</td>
                  <td>{m.title}</td>
                  <td>{m.category}</td>
                  <td>{m.tier}</td>
                  <td>{m.confidence_score}</td>
                  <td>{m.lifecycle_state}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="card" id="namespaces">
          <h3 className="sectionTitle">Namespaces</h3>
          <table className="table">
            <thead>
              <tr>
                <th>Namespace</th><th>Client</th><th>Industry</th><th>Top memories</th>
              </tr>
            </thead>
            <tbody>
              {namespaces.namespaces.map(ns => (
                <tr key={ns.namespace_id}>
                  <td>{ns.namespace_id}</td>
                  <td>{ns.client_name}</td>
                  <td>{ns.industry}</td>
                  <td>{(ns.selected_memory_ids || []).slice(0,4).join(', ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  )
}
