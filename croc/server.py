import asyncio
import json
import logging
from typing import Any, Callable, Dict, Optional, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from croc.router import Router
from croc.components.base import Component

logger = logging.getLogger("croc")


class CrocServer:
    """
    Core WebSocket server that powers croc apps.
    Manages connected clients, event dispatch, and UI re-renders.
    """

    def __init__(self, router: Router, title: str = "croc app", theme: str = "light"):
        self.router = router
        self.title = title
        self.theme = theme
        self.fastapi_app = FastAPI(title=title)
        self._connections: Set[WebSocket] = set()
        self._setup_routes()

    def _setup_routes(self):
        app = self.fastapi_app

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.get("/")
        async def index():
            return HTMLResponse(self._render_shell())

        @app.get("/croc-client.js")
        async def client_js():
            from fastapi.responses import Response
            js = self._get_client_js()
            return Response(content=js, media_type="application/javascript")

        @app.websocket("/ws")
        async def websocket_endpoint(ws: WebSocket):
            await ws.accept()
            self._connections.add(ws)
            logger.info(f"Client connected. Total: {len(self._connections)}")

            try:
                # Send initial render for "/"
                await self._send_render(ws, "/")

                async for raw in ws.iter_text():
                    await self._handle_message(ws, raw)
            except WebSocketDisconnect:
                pass
            finally:
                self._connections.discard(ws)
                logger.info(f"Client disconnected. Total: {len(self._connections)}")

    async def _handle_message(self, ws: WebSocket, raw: str):
        """Handle incoming messages from the browser client."""
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON from client: {raw}")
            return

        msg_type = msg.get("type")

        if msg_type == "navigate":
            path = msg.get("path", "/")
            await self._send_render(ws, path)

        elif msg_type == "event":
            component_id = msg.get("componentId")
            event = msg.get("event")
            payload = msg.get("payload", {})
            path = msg.get("path", "/")
            await self._dispatch_event(ws, path, component_id, event, payload)

    async def _send_render(self, ws: WebSocket, path: str):
        """Render the page at `path` and send it to the client."""
        component = self.router.resolve(path)
        if component is None:
            await ws.send_text(json.dumps({
                "type": "error",
                "message": f"No page found for path: {path}"
            }))
            return

        await ws.send_text(json.dumps({
            "type": "render",
            "path": path,
            "tree": component.to_dict(),
        }))

    async def _dispatch_event(self, ws: WebSocket, path: str,
                               component_id: str, event: str, payload: dict):
        """Find and call the event handler, then re-render."""
        component = self.router.resolve(path)
        if component is None:
            return

        handlers = component.collect_handlers()
        key = f"{component_id}:{event}"
        handler = handlers.get(key)

        if handler:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(**payload)
                else:
                    handler(**payload)
            except TypeError:
                # Handler may not accept payload kwargs
                if asyncio.iscoroutinefunction(handler):
                    await handler()
                else:
                    handler()
        else:
            logger.debug(f"No handler found for {key}")

        # Re-render after event
        await self._send_render(ws, path)

    async def broadcast(self, path: str = "/"):
        """Push a re-render to all connected clients."""
        dead = set()
        for ws in self._connections:
            try:
                await self._send_render(ws, path)
            except Exception:
                dead.add(ws)
        self._connections -= dead

    def _render_shell(self) -> str:
        """Return the HTML shell that bootstraps the croc client."""
        return f"""<!DOCTYPE html>
<html lang="en" data-theme="{self.theme}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{self.title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    [data-theme="dark"] {{ background: #0f172a; color: #f1f5f9; }}
    .croc-spinner {{ animation: spin 1s linear infinite; }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  </style>
</head>
<body class="min-h-screen bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-sans">
  <div id="croc-root" class="p-4">
    <div class="flex items-center justify-center h-screen">
      <svg class="croc-spinner w-8 h-8 text-indigo-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
      </svg>
    </div>
  </div>
  <script src="/croc-client.js"></script>
</body>
</html>"""

    def _get_client_js(self) -> str:
        """Return the croc browser-side JavaScript client."""
        return r"""
(function() {
  const root = document.getElementById('croc-root');
  const wsUrl = `ws://${location.host}/ws`;
  let ws;
  let currentPath = window.location.pathname || '/';

  function connect() {
    ws = new WebSocket(wsUrl);
    ws.onopen = () => {
      ws.send(JSON.stringify({ type: 'navigate', path: currentPath }));
    };
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.type === 'render') render(msg.tree);
      if (msg.type === 'error') showError(msg.message);
    };
    ws.onclose = () => setTimeout(connect, 1000); // auto-reconnect
  }

  function sendEvent(componentId, event, payload = {}) {
    ws.send(JSON.stringify({ type: 'event', componentId, event, payload, path: currentPath }));
  }

  function navigate(path) {
    currentPath = path;
    history.pushState({}, '', path);
    ws.send(JSON.stringify({ type: 'navigate', path }));
  }

  window.crocNavigate = navigate;

  // ── Renderer ────────────────────────────────────────────────────────────────

  function render(tree) {
    const el = buildEl(tree);
    root.innerHTML = '';
    root.appendChild(el);
  }

  function buildEl(node) {
    if (!node) return document.createTextNode('');
    if (node.type === 'text') return document.createTextNode(node.value || '');

    const builders = {
      // Layout
      VStack:   buildVStack,
      HStack:   buildHStack,
      Grid:     buildGrid,
      Box:      buildBox,
      Center:   buildCenter,
      Page:     buildPage,
      Divider:  () => el('hr', { class: 'border-slate-200 my-2' }),
      Spacer:   (n) => el('div', { style: `height: ${n.props.size * 4}px` }),
      // Text
      Text:     buildText,
      Heading:  buildHeading,
      Label:    buildLabel,
      Badge:    buildBadge,
      Code:     buildCode,
      Link:     buildLink,
      // Input
      Button:   buildButton,
      Input:    buildInput,
      Textarea: buildTextarea,
      Select:   buildSelect,
      Checkbox: buildCheckbox,
      Switch:   buildSwitch,
      Slider:   buildSlider,
      // Display
      Card:     buildCard,
      Image:    buildImage,
      Table:    buildTable,
      Alert:    buildAlert,
      Spinner:  buildSpinner,
      Progress: buildProgress,
      Avatar:   buildAvatar,
      Stat:     buildStat,
    };

    const builder = builders[node.type];
    if (!builder) {
      const div = el('div', {});
      div.textContent = `[Unknown component: ${node.type}]`;
      return div;
    }
    return builder(node);
  }

  function children(node) {
    return (node.children || []).map(buildEl);
  }

  function el(tag, attrs = {}, kids = []) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === 'class') e.className = v;
      else if (k === 'style') e.style.cssText = v;
      else e.setAttribute(k, v);
    }
    kids.forEach(k => k && e.appendChild(k));
    return e;
  }

  // ── Layout builders ──────────────────────────────────────────────────────────

  function buildVStack(n) {
    const gap = `gap-${n.props.gap || 4}`;
    const d = el('div', { class: `flex flex-col ${gap} w-full` });
    children(n).forEach(c => d.appendChild(c));
    return d;
  }

  function buildHStack(n) {
    const gap = `gap-${n.props.gap || 4}`;
    const d = el('div', { class: `flex flex-row items-center ${gap}` });
    children(n).forEach(c => d.appendChild(c));
    return d;
  }

  function buildGrid(n) {
    const cols = `grid-cols-${n.props.cols || 2}`;
    const gap = `gap-${n.props.gap || 4}`;
    const d = el('div', { class: `grid ${cols} ${gap}` });
    children(n).forEach(c => d.appendChild(c));
    return d;
  }

  function buildBox(n) {
    const p = `p-${n.props.padding || 4}`;
    const d = el('div', { class: p });
    children(n).forEach(c => d.appendChild(c));
    return d;
  }

  function buildCenter(n) {
    const d = el('div', { class: 'flex items-center justify-center' });
    children(n).forEach(c => d.appendChild(c));
    return d;
  }

  function buildPage(n) {
    if (n.props.title) document.title = n.props.title;
    const d = el('div', { class: 'max-w-4xl mx-auto px-4 py-8' });
    children(n).forEach(c => d.appendChild(c));
    return d;
  }

  // ── Text builders ────────────────────────────────────────────────────────────

  const sizeMap = { xs:'text-xs', sm:'text-sm', base:'text-base', lg:'text-lg', xl:'text-xl', '2xl':'text-2xl' };
  const weightMap = { light:'font-light', normal:'font-normal', medium:'font-medium', semibold:'font-semibold', bold:'font-bold' };

  function buildText(n) {
    const sz = sizeMap[n.props.size] || 'text-base';
    const wt = weightMap[n.props.weight] || 'font-normal';
    const p = el('p', { class: `${sz} ${wt}` });
    children(n).forEach(c => p.appendChild(c));
    return p;
  }

  function buildHeading(n) {
    const lvl = n.props.level || 1;
    const sizes = ['', 'text-4xl', 'text-3xl', 'text-2xl', 'text-xl', 'text-lg', 'text-base'];
    const h = el(`h${lvl}`, { class: `${sizes[lvl] || 'text-2xl'} font-bold` });
    children(n).forEach(c => h.appendChild(c));
    return h;
  }

  function buildLabel(n) {
    const attrs = { class: 'text-sm font-medium text-slate-700 dark:text-slate-300' };
    if (n.props.for_id) attrs.for = n.props.for_id;
    const lb = el('label', attrs);
    children(n).forEach(c => lb.appendChild(c));
    return lb;
  }

  function buildBadge(n) {
    const variants = { default:'bg-slate-100 text-slate-800', success:'bg-green-100 text-green-800', warning:'bg-yellow-100 text-yellow-800', error:'bg-red-100 text-red-800', info:'bg-blue-100 text-blue-800' };
    const cls = variants[n.props.variant] || variants.default;
    const b = el('span', { class: `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${cls}` });
    children(n).forEach(c => b.appendChild(c));
    return b;
  }

  function buildCode(n) {
    if (n.props.block) {
      const pre = el('pre', { class: 'bg-slate-900 text-green-400 p-4 rounded-lg overflow-auto text-sm font-mono' });
      children(n).forEach(c => pre.appendChild(c));
      return pre;
    }
    const code = el('code', { class: 'bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded text-sm font-mono' });
    children(n).forEach(c => code.appendChild(c));
    return code;
  }

  function buildLink(n) {
    const a = el('a', { href: n.props.href || '#', class: 'text-indigo-600 hover:underline' });
    if (n.props.external) a.target = '_blank';
    children(n).forEach(c => a.appendChild(c));
    a.addEventListener('click', (e) => {
      if (!n.props.external && !n.props.href?.startsWith('http')) {
        e.preventDefault();
        navigate(n.props.href);
      }
    });
    return a;
  }

  // ── Input builders ───────────────────────────────────────────────────────────

  function buildButton(n) {
    const variants = {
      primary: 'bg-indigo-600 hover:bg-indigo-700 text-white',
      secondary: 'bg-slate-200 hover:bg-slate-300 text-slate-900',
      danger: 'bg-red-600 hover:bg-red-700 text-white',
      ghost: 'hover:bg-slate-100 text-slate-700',
      outline: 'border border-slate-300 hover:bg-slate-50 text-slate-700',
    };
    const cls = variants[n.props.variant] || variants.primary;
    const btn = el('button', {
      class: `inline-flex items-center justify-center px-4 py-2 rounded-lg text-sm font-medium transition-colors ${cls} ${n.props.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`,
    });
    if (n.props.disabled) btn.disabled = true;
    children(n).forEach(c => btn.appendChild(c));
    if (n.events?.includes('click')) {
      btn.addEventListener('click', () => sendEvent(n.id, 'click'));
    }
    return btn;
  }

  function wrapWithLabel(input, label, id) {
    if (!label) return input;
    input.id = id;
    const wrapper = el('div', { class: 'flex flex-col gap-1' });
    const lb = el('label', { for: id, class: 'text-sm font-medium text-slate-700 dark:text-slate-300' });
    lb.textContent = label;
    wrapper.appendChild(lb);
    wrapper.appendChild(input);
    return wrapper;
  }

  function buildInput(n) {
    const input = el('input', {
      type: n.props.input_type || 'text',
      placeholder: n.props.placeholder || '',
      value: n.props.value || '',
      class: 'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-slate-800 dark:border-slate-600',
    });
    if (n.events?.includes('change')) {
      input.addEventListener('input', () => sendEvent(n.id, 'change', { value: input.value }));
    }
    return wrapWithLabel(input, n.props.label, n.id);
  }

  function buildTextarea(n) {
    const ta = el('textarea', {
      placeholder: n.props.placeholder || '',
      rows: n.props.rows || 4,
      class: 'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-slate-800 dark:border-slate-600',
    });
    ta.value = n.props.value || '';
    if (n.events?.includes('change')) {
      ta.addEventListener('input', () => sendEvent(n.id, 'change', { value: ta.value }));
    }
    return wrapWithLabel(ta, n.props.label, n.id);
  }

  function buildSelect(n) {
    const sel = el('select', {
      class: 'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-slate-800 dark:border-slate-600',
    });
    (n.props.options || []).forEach(([val, label]) => {
      const opt = el('option', { value: val });
      opt.textContent = label;
      if (val === n.props.value) opt.selected = true;
      sel.appendChild(opt);
    });
    if (n.events?.includes('change')) {
      sel.addEventListener('change', () => sendEvent(n.id, 'change', { value: sel.value }));
    }
    return wrapWithLabel(sel, n.props.label, n.id);
  }

  function buildCheckbox(n) {
    const wrapper = el('div', { class: 'flex items-center gap-2' });
    const cb = el('input', { type: 'checkbox', class: 'w-4 h-4 text-indigo-600 rounded border-slate-300' });
    cb.checked = !!n.props.checked;
    const lb = el('label', { class: 'text-sm text-slate-700 dark:text-slate-300' });
    lb.textContent = n.props.label || '';
    if (n.events?.includes('change')) {
      cb.addEventListener('change', () => sendEvent(n.id, 'change', { checked: cb.checked }));
    }
    wrapper.appendChild(cb);
    wrapper.appendChild(lb);
    return wrapper;
  }

  function buildSwitch(n) {
    const wrapper = el('div', { class: 'flex items-center gap-3' });
    const track = el('button', {
      role: 'switch',
      class: `relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${n.props.checked ? 'bg-indigo-600' : 'bg-slate-200'}`,
    });
    const thumb = el('span', {
      class: `inline-block h-4 w-4 rounded-full bg-white shadow transition-transform ${n.props.checked ? 'translate-x-6' : 'translate-x-1'}`,
    });
    track.appendChild(thumb);
    if (n.events?.includes('change')) {
      track.addEventListener('click', () => {
        const next = !n.props.checked;
        sendEvent(n.id, 'change', { checked: next });
      });
    }
    const lb = el('span', { class: 'text-sm text-slate-700 dark:text-slate-300' });
    lb.textContent = n.props.label || '';
    wrapper.appendChild(track);
    wrapper.appendChild(lb);
    return wrapper;
  }

  function buildSlider(n) {
    const slider = el('input', {
      type: 'range',
      min: n.props.min ?? 0,
      max: n.props.max ?? 100,
      value: n.props.value ?? 50,
      class: 'w-full accent-indigo-600',
    });
    if (n.events?.includes('change')) {
      slider.addEventListener('input', () => sendEvent(n.id, 'change', { value: parseInt(slider.value) }));
    }
    return wrapWithLabel(slider, n.props.label, n.id);
  }

  // ── Display builders ─────────────────────────────────────────────────────────

  function buildCard(n) {
    const card = el('div', { class: 'bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm' });
    if (n.props.title) {
      const t = el('h3', { class: 'text-lg font-semibold mb-1' });
      t.textContent = n.props.title;
      card.appendChild(t);
    }
    if (n.props.subtitle) {
      const s = el('p', { class: 'text-sm text-slate-500 mb-3' });
      s.textContent = n.props.subtitle;
      card.appendChild(s);
    }
    children(n).forEach(c => card.appendChild(c));
    return card;
  }

  function buildImage(n) {
    const attrs = { src: n.props.src, alt: n.props.alt || '', class: 'rounded-lg object-cover' };
    if (n.props.width) attrs.width = n.props.width;
    if (n.props.height) attrs.height = n.props.height;
    return el('img', attrs);
  }

  function buildTable(n) {
    const wrapper = el('div', { class: 'overflow-auto rounded-lg border border-slate-200 dark:border-slate-700' });
    const table = el('table', { class: 'w-full text-sm text-left' });
    const thead = el('thead', { class: 'bg-slate-50 dark:bg-slate-800' });
    const hrow = el('tr');
    (n.props.columns || []).forEach(col => {
      const th = el('th', { class: 'px-4 py-3 font-medium text-slate-600 dark:text-slate-300' });
      th.textContent = col;
      hrow.appendChild(th);
    });
    thead.appendChild(hrow);
    const tbody = el('tbody');
    (n.props.rows || []).forEach((row, i) => {
      const tr = el('tr', { class: i % 2 === 0 ? '' : 'bg-slate-50 dark:bg-slate-800/50' });
      row.forEach(cell => {
        const td = el('td', { class: 'px-4 py-3 border-t border-slate-100 dark:border-slate-700' });
        td.textContent = cell;
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
    table.appendChild(thead);
    table.appendChild(tbody);
    wrapper.appendChild(table);
    return wrapper;
  }

  function buildAlert(n) {
    const variants = {
      info:    'bg-blue-50 border-blue-200 text-blue-800',
      success: 'bg-green-50 border-green-200 text-green-800',
      warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      error:   'bg-red-50 border-red-200 text-red-800',
    };
    const cls = variants[n.props.variant] || variants.info;
    const div = el('div', { class: `border rounded-lg p-4 ${cls}` });
    if (n.props.title) {
      const t = el('p', { class: 'font-semibold mb-1' });
      t.textContent = n.props.title;
      div.appendChild(t);
    }
    children(n).forEach(c => div.appendChild(c));
    return div;
  }

  function buildSpinner(n) {
    const sizes = { sm: 'w-4 h-4', md: 'w-8 h-8', lg: 'w-12 h-12' };
    const sz = sizes[n.props.size] || sizes.md;
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', `croc-spinner ${sz} text-indigo-500`);
    svg.setAttribute('fill', 'none');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.innerHTML = '<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>';
    return svg;
  }

  function buildProgress(n) {
    const pct = Math.round(((n.props.value || 0) / (n.props.max || 100)) * 100);
    const wrapper = el('div', { class: 'w-full' });
    if (n.props.label) {
      const hdr = el('div', { class: 'flex justify-between text-sm mb-1' });
      const lb = el('span'); lb.textContent = n.props.label;
      const pctEl = el('span'); pctEl.textContent = `${pct}%`;
      hdr.appendChild(lb); hdr.appendChild(pctEl);
      wrapper.appendChild(hdr);
    }
    const bg = el('div', { class: 'w-full bg-slate-200 rounded-full h-2' });
    const bar = el('div', { class: 'bg-indigo-600 h-2 rounded-full transition-all', style: `width: ${pct}%` });
    bg.appendChild(bar);
    wrapper.appendChild(bg);
    return wrapper;
  }

  function buildAvatar(n) {
    if (n.props.src) {
      const sizes = { sm: 'w-8 h-8', md: 'w-10 h-10', lg: 'w-16 h-16' };
      return el('img', { src: n.props.src, alt: n.props.name || '', class: `${sizes[n.props.size] || sizes.md} rounded-full object-cover` });
    }
    const initials = (n.props.name || '?').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
    const sizes = { sm: 'w-8 h-8 text-xs', md: 'w-10 h-10 text-sm', lg: 'w-16 h-16 text-xl' };
    const div = el('div', { class: `${sizes[n.props.size] || sizes.md} rounded-full bg-indigo-500 text-white flex items-center justify-center font-semibold` });
    div.textContent = initials;
    return div;
  }

  function buildStat(n) {
    const div = el('div', { class: 'bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5' });
    const label = el('p', { class: 'text-sm text-slate-500 mb-1' });
    label.textContent = n.props.label || '';
    const value = el('p', { class: 'text-3xl font-bold' });
    value.textContent = n.props.value || '';
    div.appendChild(label);
    div.appendChild(value);
    if (n.props.delta) {
      const isPos = n.props.delta.startsWith('+');
      const delta = el('p', { class: `text-sm mt-1 ${isPos ? 'text-green-600' : 'text-red-600'}` });
      delta.textContent = n.props.delta;
      div.appendChild(delta);
    }
    return div;
  }

  function showError(msg) {
    root.innerHTML = `<div class="p-8 text-red-600 font-mono text-sm">[croc error] ${msg}</div>`;
  }

  // Boot
  connect();
})();
"""
