import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

type Result = {score:number; matched:string[]; missing:string[]; recommendations:string[]; disclaimer:string};
const demoCV = "Backend developer with 3 years of Python, Django, PostgreSQL, Docker and Git. Built REST APIs.";
const demoJob = "Looking for Python, Django, PostgreSQL, Docker, Redis, AWS, Git and CI/CD experience.";
const endpoint = import.meta.env.VITE_API_URL || "/api/analyze/";

function App(){
  const [cv,setCv] = useState("");
  const [job,setJob] = useState("");
  const [file,setFile] = useState<File|null>(null);
  const [result,setResult] = useState<Result|null>(null);
  const [previous,setPrevious] = useState<number|null>(null);
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState("");
  async function submit(){
    setLoading(true);setError("");
    const data = new FormData();
    data.append("job_description",job);
    if(file)data.append("resume_file",file);else data.append("resume_text",cv);
    try{
      const response = await fetch(endpoint,{method:"POST",body:data});
      const body = await response.json();
      if(!response.ok)throw new Error(JSON.stringify(body));
      setPrevious(result?.score ?? null);setResult(body);
    }catch(e){setError(e instanceof Error?e.message:"Unexpected error");}
    finally{setLoading(false);}
  }
  return <main>
    <header><div className="brand">◎ ATS <span>Beater</span></div><a href="https://github.com/ale13211/ats-beater" target="_blank" rel="noreferrer">GitHub ↗</a></header>
    <section className="hero"><div className="eyebrow">OPEN SOURCE · RESUME INTELLIGENCE</div><h1>Make your experience<br/><em>stand out.</em></h1><p>Compare your resume against a job description. Find relevant skills, identify gaps, and improve your CV with evidence-based suggestions.</p></section>
    <section className="grid">
      <article><h2>01 / Your resume</h2><p>Paste your resume or upload a PDF (max 3 MB, 10 pages).</p><textarea value={cv} onChange={e=>{setCv(e.target.value);setFile(null);}} placeholder="Paste your resume text here..." aria-label="Resume text"/><label className="upload">Upload PDF <input type="file" accept=".pdf,application/pdf" onChange={e=>{setFile(e.target.files?.[0]||null);setCv("");}}/></label>{file&&<small>{file.name}</small>}</article>
      <article><h2>02 / Job description</h2><p>Paste the requirements from the role you're applying for.</p><textarea value={job} onChange={e=>setJob(e.target.value)} placeholder="Paste the job description here..." aria-label="Job description"/></article>
    </section>
    <div className="actions"><button className="secondary" onClick={()=>{setCv(demoCV);setJob(demoJob);setFile(null);setResult(null);setPrevious(null);}}>Load example</button><button disabled={loading||!job.trim()||(!cv.trim()&&!file)} onClick={submit}>{loading?"Analyzing...":"Analyze match →"}</button></div>
    {error&&<p role="alert" className="error">{error}</p>}
    {result&&<section className="results"><div className="resulttop"><div><div className="eyebrow">MATCH REPORT</div><h2>Your skill coverage</h2></div><div className="score">{result.score}%</div></div>
      <div className="bar"><div style={{width:`${result.score}%`}}/></div>
      {previous!==null&&<p>Previous analysis: {previous}% → Current: {result.score}% ({(result.score-previous).toFixed(1)} points)</p>}
      <div className="grid"><article><h3>✓ Matched skills</h3><div className="tags">{result.matched.map(s=><span className="tag good" key={s}>{s}</span>)}</div></article><article><h3>↗ Potential gaps</h3><div className="tags">{result.missing.map(s=><span className="tag missing" key={s}>{s}</span>)}</div></article></div>
      <h3>Suggested improvements</h3>{result.recommendations.length?result.recommendations.map(r=><p key={r}>→ {r}</p>):<p>No missing recognized skills.</p>}
      <small>{result.disclaimer}</small></section>}
    <footer>Built for transparent resume analysis · No resumes are stored by this demo.</footer>
  </main>
}
createRoot(document.getElementById("root")!).render(<React.StrictMode><App/></React.StrictMode>);
