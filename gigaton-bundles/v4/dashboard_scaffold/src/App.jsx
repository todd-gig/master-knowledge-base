import React from 'react'
import { BarChart3, Database, Layers3, Settings2, Users } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, CartesianGrid } from 'recharts'

const taskData = [
  { name: 'W1', score: 0.71 },
  { name: 'W2', score: 0.76 },
  { name: 'W3', score: 0.82 },
  { name: 'W4', score: 0.88 },
]

const memoryData = [
  { name: 'Tier 1', count: 12 },
  { name: 'Tier 2', count: 7 },
  { name: 'Tier 3', count: 1 },
]

function Card({ title, children, icon }) {
  return (
    <div className="card">
      <div className="card-head">
        <div className="icon-wrap">{icon}</div>
        <h3>{title}</h3>
      </div>
      <div>{children}</div>
    </div>
  )
}

export default function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Gigaton Ops v4</div>
        <nav className="nav">
          <a href="#overview">Overview</a>
          <a href="#namespaces">Namespaces</a>
          <a href="#retrieval">Retrieval</a>
          <a href="#lifecycle">Lifecycle</a>
          <a href="#clients">Clients</a>
          <a href="#settings">Settings</a>
        </nav>
      </aside>

      <main className="content">
        <section className="hero" id="overview">
          <div>
            <p className="eyebrow">Deployment package</p>
            <h1>Client ops dashboard scaffold</h1>
            <p className="subcopy">
              Starter control plane for namespace generation, retrieval calibration, and memory lifecycle operations.
            </p>
          </div>
        </section>

        <section className="grid three">
          <Card title="Namespaces" icon={<Layers3 size={18} />}>
            <p className="metric">14</p>
            <p className="muted">Global + client overlays managed</p>
          </Card>
          <Card title="Calibration" icon={<BarChart3 size={18} />}>
            <p className="metric">0.88</p>
            <p className="muted">Current retrieval quality benchmark</p>
          </Card>
          <Card title="Intake forms" icon={<Users size={18} />}>
            <p className="metric">26</p>
            <p className="muted">Processed client onboarding submissions</p>
          </Card>
        </section>

        <section className="grid two">
          <Card title="Retrieval score trend" icon={<BarChart3 size={18} />}>
            <div className="chart-wrap">
              <ResponsiveContainer width="100%" height={260}>
                <LineChart data={taskData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0.6, 1.0]} />
                  <Tooltip />
                  <Line type="monotone" dataKey="score" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card title="Memory distribution" icon={<Database size={18} />}>
            <div className="chart-wrap">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={memoryData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </section>

        <section className="grid two">
          <Card title="Client namespace generator" icon={<Layers3 size={18} />}>
            <div className="list-block">
              <div className="row"><span>Input schema</span><strong>v1 intake form</strong></div>
              <div className="row"><span>Inheritance</span><strong>global → client</strong></div>
              <div className="row"><span>Constraint</span><strong>doctrine locked</strong></div>
              <button className="btn">Generate namespace</button>
            </div>
          </Card>

          <Card title="Lifecycle state machine" icon={<Settings2 size={18} />}>
            <div className="list-block">
              <div className="row"><span>Active</span><strong>20</strong></div>
              <div className="row"><span>Watchlist</span><strong>0</strong></div>
              <div className="row"><span>Deprecated</span><strong>0</strong></div>
              <button className="btn">Review transitions</button>
            </div>
          </Card>
        </section>

        <section className="table-card" id="clients">
          <div className="card-head">
            <div className="icon-wrap"><Users size={18} /></div>
            <h3>Starter client queue</h3>
          </div>
          <table>
            <thead>
              <tr>
                <th>Client</th>
                <th>Industry</th>
                <th>Namespace</th>
                <th>Status</th>
                <th>Priority</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>ACME Template</td>
                <td>Template</td>
                <td>client_acme_template</td>
                <td>Draft</td>
                <td>Medium</td>
              </tr>
              <tr>
                <td>Liquefex Example</td>
                <td>Insurance</td>
                <td>client_liquefex</td>
                <td>Illustrative</td>
                <td>High</td>
              </tr>
            </tbody>
          </table>
        </section>
      </main>
    </div>
  )
}
