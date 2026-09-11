import React, {useEffect, useMemo, useState} from 'react';
import { createRoot } from 'react-dom/client';
import { Search, Newspaper, Sparkles, ExternalLink, Activity, RotateCcw, ShieldCheck } from 'lucide-react';
import './styles.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App(){
  const [query,setQuery]=useState('What are the latest developments in AI agents?');
  const [loading,setLoading]=useState(false);
  const [result,setResult]=useState(null);
  const [health,setHealth]=useState({mode:'demo'});
  useEffect(()=>{fetch(`${API}/health`).then(r=>r.json()).then(setHealth).catch(()=>{})},[]);
  const topics = ['AI agents','Cloud AI infrastructure','Agent evaluation','MCP interoperability'];
  async function runResearch(q=query){
    setQuery(q); setLoading(true);
    try{
      const r=await fetch(`${API}/research`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({query:q})});
      setResult(await r.json());
    } finally {setLoading(false)}
  }
  return <div className="app">
    <aside className="sidebar">
      <div className="brand"><div className="brandIcon"><Newspaper size={20}/></div><div><strong>NewsBot</strong><span>Autonomous research</span></div></div>
      <div className="sectionTitle">Suggested research</div>
      <div className="topics">{topics.map(t=><button key={t} onClick={()=>runResearch(`Latest ${t}: key developments and impact`)}>{t}</button>)}</div>
      <div className="agentCard">
        <div className="agentTitle"><Activity size={16}/> Agent workflow</div>
        <div className="flowStep active"><span>1</span> Plan query</div>
        <div className="flowStep active"><span>2</span> Search web</div>
        <div className="flowStep active"><span>3</span> Evaluate sources</div>
        <div className="flowStep"><span>4</span> Refine if needed</div>
        <div className="flowStep active"><span>5</span> Generate briefing</div>
      </div>
      <div className="mode"><span className="dot"></span>{health.mode === 'live' ? 'Live research' : 'Demo mode'}<small>{health.mode === 'live' ? 'Tavily + GPT-4o mini' : 'No API keys required'}</small></div>
    </aside>

    <main>
      <header><div><div className="eyebrow"><Sparkles size={14}/> AGENTIC NEWS INTELLIGENCE</div><h1>Research what matters.<br/><span>Know why it matters.</span></h1><p>NewsBot searches, evaluates, retries, and synthesizes source-backed briefings automatically.</p></div></header>
      <div className="searchBox"><Search size={20}/><input value={query} onChange={e=>setQuery(e.target.value)} onKeyDown={e=>e.key==='Enter'&&runResearch()} placeholder="Ask about a company, technology, market, or event..."/><button onClick={()=>runResearch()} disabled={loading}>{loading?'Researching…':'Research'}</button></div>
      {!result && <div className="empty"><div className="orbit"><Search size={28}/></div><h2>Start an autonomous research run</h2><p>NewsBot will optimize your query, retrieve current sources, judge whether the evidence is sufficient, retry when necessary, and produce a cited briefing.</p><button onClick={()=>runResearch()}><Sparkles size={16}/> Run sample research</button></div>}
      {result && <div className="results">
        <section className="brief"><div className="cardHeader"><div><span className="pill"><ShieldCheck size={14}/> Source-backed</span><h2>Research briefing</h2></div><span className="modeBadge">{result.mode}</span></div><article>{result.answer.split('\n').map((x,i)=>x.startsWith('##')?<h3 key={i}>{x.replaceAll('#','').trim()}</h3>:x.startsWith('###')?<h4 key={i}>{x.replaceAll('#','').trim()}</h4>:<p key={i}>{x}</p>)}</article></section>
        <aside className="rightRail">
          <section className="sources"><h3>Sources <span>{result.sources.length}</span></h3>{result.sources.map((s,i)=><a className="source" href={s.url} target="_blank" key={i}><div className="sourceNum">{i+1}</div><div><strong>{s.title}</strong><p>{s.published_date || 'Current source'}</p></div><ExternalLink size={14}/></a>)}</section>
          <section className="trace"><h3>Agent trace</h3>{result.trace.map((t,i)=><div className="traceRow" key={i}><div className="check">✓</div><div><strong>{t.node.replaceAll('_',' ')}</strong><p>{t.detail}</p></div></div>)}</section>
        </aside>
      </div>}
    </main>
  </div>
}
createRoot(document.getElementById('root')).render(<App/>);
