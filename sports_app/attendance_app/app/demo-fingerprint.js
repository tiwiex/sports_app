"use client";

// A fixed decorative drawing, identical for every player; never biometric data.
const ridges=[
 "M22 112C16 66 35 24 76 20c42-4 67 34 62 77",
 "M30 126C21 88 30 43 63 32c35-13 68 13 67 51",
 "M39 141C24 109 32 61 54 46c28-21 62-3 67 28 4 24-8 41-2 63",
 "M49 153C34 128 35 94 41 76c8-30 38-39 58-20 20 18 13 40 11 57-2 19 2 32 9 44",
 "M58 162C45 145 42 121 46 96c3-24 11-40 28-40 20-1 31 18 28 40-3 24-6 44 4 66",
 "M68 169C53 149 51 121 55 97c3-19 6-31 19-32 13-1 23 10 20 31-3 24-9 53 2 75",
 "M79 174C62 151 61 128 64 106c2-18 0-31 10-32 13-2 13 14 11 27-4 27-8 48 2 69",
 "M76 90c-2 27-10 45 0 65",
 "M23 132c3 16 10 28 19 36",
 "M130 119c-3 18 1 34 6 42",
];

export default function DemoFingerprint({phase="ready"}){
 return <section className={`demo-fingerprint is-${phase}`} aria-label="Simulated fingerprint preview">
  <span className="demo-fingerprint-label">SIMULATED — NO SCANNER</span>
  <div className="demo-fingerprint-screen">
   <svg viewBox="0 0 160 190" role="img" aria-label="Decorative fingerprint illustration — simulated">
    <g fill="none" stroke="currentColor" strokeWidth="3.2" strokeLinecap="round">{ridges.map((d,index)=><path key={index} d={d}/>)}</g>
   </svg>
   {phase==="scanning" && <span className="demo-scan-line" aria-hidden="true"/>}
   {phase==="complete" && <span className="demo-scan-check" aria-hidden="true">✓</span>}
  </div>
  <p role="status">{phase==="scanning"?"Simulating scan…":phase==="complete"?"Demo capture complete":"Demo fingerprint preview"}</p>
  <small>Illustration only. No fingerprint data is collected.</small>
 </section>;
}
