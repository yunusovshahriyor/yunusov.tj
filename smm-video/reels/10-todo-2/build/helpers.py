
K = lambda s: f'<span class="k">{s}</span>'; P = lambda s: f'<span class="p">{s}</span>'
S_ = lambda s: f'<span class="s">{s}</span>'; N = lambda s: f'<span class="n">{s}</span>'; F = lambda s: f'<span class="f">{s}</span>'
CT = lambda s: f'<span class="c">{s}</span>'; CM = lambda s: f'<span class="cm">{s}</span>'
ERR = "color:var(--err)"

def task(top, text, a, left=40, right=40, done=False, idx=None, extra="", cls="pop"):
    mark = "☑" if done else "☐"
    ix = f'<span style="font:800 13px var(--mono);color:var(--muted);margin-right:12px">[{idx}]</span>' if idx is not None else ""
    st = "text-decoration:line-through;color:var(--muted)" if done else "color:var(--white)"
    return (f'<div class="card {cls}" style="--a:{a:.2f}s;left:{left}px;right:{right}px;top:{top}px;padding:12px 18px;display:flex;align-items:center;{extra}">'
            f'{ix}<span style="font:700 22px \'Segoe UI\';margin-right:12px;color:var(--purple)">{mark}</span><span style="font:700 20px \'Segoe UI\';{st}">{text}</span></div>')

