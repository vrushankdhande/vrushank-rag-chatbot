"""Animated AI background: drifting gradient orbs + a particle network on a canvas.

The canvas lives in the main page (behind all content, pointer-events: none). A tiny
same-origin st.iframe injects one <script> into the parent document; the script guards
against double-starting, so Streamlit reruns never stack animations. It pauses when
the tab is hidden and draws a single static frame under prefers-reduced-motion.
If the injection is unavailable, the CSS gradient background in styles.py remains.
"""
import json

import streamlit as st

_BG_SCRIPT = r"""
(function () {
  if (window.__aiBgStarted) return;
  window.__aiBgStarted = true;
  const doc = document;
  const canvas = doc.createElement('canvas');
  canvas.id = 'ai-bg';
  // z-index -1: painted above the body background but below every app element,
  // so it can never cover content or intercept clicks.
  Object.assign(canvas.style, {
    position: 'fixed', inset: '0', width: '100vw', height: '100vh',
    zIndex: '-1', pointerEvents: 'none', opacity: '0.9'
  });
  doc.body.prepend(canvas);

  const ctx = canvas.getContext('2d');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W, H, DPR, particles = [], t = 0;
  const orbs = [
    { x: .15, y: .2, r: .45, c: [79, 140, 255], s: .00012, p: 0 },
    { x: .85, y: .25, r: .40, c: [139, 92, 246], s: .00015, p: 2 },
    { x: .55, y: .95, r: .50, c: [34, 211, 238], s: .0001, p: 4 },
  ];

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = W * DPR; canvas.height = H * DPR;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    const n = Math.min(70, Math.floor((W * H) / 22000));
    particles = Array.from({ length: n }, () => ({
      x: Math.random() * W, y: Math.random() * H,
      vx: (Math.random() - .5) * .25, vy: (Math.random() - .5) * .25,
      r: Math.random() * 1.6 + .6,
    }));
  }

  function frame() {
    ctx.clearRect(0, 0, W, H);
    // drifting gradient orbs
    for (const o of orbs) {
      const x = (o.x + Math.sin(t * o.s * 6 + o.p) * .06) * W;
      const y = (o.y + Math.cos(t * o.s * 5 + o.p) * .05) * H;
      const r = o.r * Math.max(W, H);
      const g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, `rgba(${o.c.join(',')},0.10)`);
      g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    }
    // particle network
    const maxD = 140;
    for (let i = 0; i < particles.length; i++) {
      const a = particles[i];
      a.x += a.vx; a.y += a.vy;
      if (a.x < 0 || a.x > W) a.vx *= -1;
      if (a.y < 0 || a.y > H) a.vy *= -1;
      for (let j = i + 1; j < particles.length; j++) {
        const b = particles[j];
        const dx = a.x - b.x, dy = a.y - b.y, d = Math.hypot(dx, dy);
        if (d < maxD) {
          ctx.strokeStyle = `rgba(110,160,255,${(1 - d / maxD) * 0.16})`;
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
      ctx.fillStyle = 'rgba(160,200,255,0.55)';
      ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2); ctx.fill();
    }
    t += 16;
  }

  function loop() {
    if (!doc.hidden) frame();
    requestAnimationFrame(loop);
  }

  resize();
  window.addEventListener('resize', resize);
  if (reduce) frame(); else loop();
})();
"""

_INJECTOR = f"""
<script>
(function () {{
  try {{
    const p = window.parent;
    if (p.__aiBgStarted) return;
    const s = p.document.createElement('script');
    s.textContent = {json.dumps(_BG_SCRIPT)};
    p.document.head.appendChild(s);
  }} catch (e) {{ /* cross-origin: CSS gradient fallback stays */ }}
}})();
</script>
"""


def render_background() -> None:
    """Start the animated background (idempotent across reruns)."""
    with st.container(key="bg_anim"):
        # Trusted, static HTML authored here (never user/LLM content).
        st.iframe(_INJECTOR, height=1)
    # Collapse the injector's (empty) iframe so it takes no layout space.
    st.markdown(
        "<style>.st-key-bg_anim{position:absolute;height:0;overflow:hidden;margin:0;padding:0}</style>",
        unsafe_allow_html=True,
    )
