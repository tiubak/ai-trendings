/**
 * Lightweight chart helpers for AI Trendings projects.
 * No dependencies — pure Canvas API.
 * Include via <script src="/lib/charts.js"></script>
 * 
 * Usage:
 *   drawBarChart(canvasId, {labels: [...], values: [...], title: "...", color: "#00f260"})
 *   drawPieChart(canvasId, {labels: [...], values: [...], title: "..."})
 *   drawLineChart(canvasId, {labels: [...], datasets: [{values, label, color}], title: "..."})
 *   drawRadar(canvasId, {labels: [...], datasets: [{values, label, color}], title: "..."})
 */

const COLORS = ['#00f260','#0575e6','#f97316','#ef4444','#a855f7','#eab308','#06b6d4','#ec4899','#84cc16','#6366f1'];

function drawBarChart(canvasId, opts) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const {labels, values, title, color} = opts;
    const W = canvas.width, H = canvas.height;
    const pad = {top: 40, right: 20, bottom: 60, left: 60};
    const maxVal = Math.max(...values) * 1.1;
    const barW = (W - pad.left - pad.right) / labels.length * 0.7;
    const gap = (W - pad.left - pad.right) / labels.length;

    ctx.fillStyle = '#1a1a2e'; ctx.fillRect(0, 0, W, H);
    if (title) { ctx.fillStyle = '#e0e0e0'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center'; ctx.fillText(title, W/2, 25); }

    // Y axis
    ctx.strokeStyle = 'rgba(255,255,255,0.1)'; ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = pad.top + (H - pad.top - pad.bottom) * (1 - i/5);
        ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(W - pad.right, y); ctx.stroke();
        ctx.fillStyle = '#888'; ctx.font = '11px sans-serif'; ctx.textAlign = 'right';
        ctx.fillText((maxVal * i / 5).toFixed(1), pad.left - 8, y + 4);
    }

    // Bars
    values.forEach((v, i) => {
        const x = pad.left + i * gap + (gap - barW) / 2;
        const h = (v / maxVal) * (H - pad.top - pad.bottom);
        const y = H - pad.bottom - h;
        const c = color || COLORS[i % COLORS.length];
        ctx.fillStyle = c; ctx.fillRect(x, y, barW, h);
        ctx.fillStyle = '#e0e0e0'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(v.toFixed(1), x + barW/2, y - 5);
        ctx.save(); ctx.translate(x + barW/2, H - pad.bottom + 10);
        ctx.rotate(labels[i].length > 8 ? -0.5 : 0);
        ctx.fillText(labels[i], 0, 0); ctx.restore();
    });
}

function drawPieChart(canvasId, opts) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const {labels, values, title} = opts;
    const W = canvas.width, H = canvas.height;
    const cx = W * 0.4, cy = H / 2, r = Math.min(W, H) * 0.32;
    const total = values.reduce((a, b) => a + b, 0);

    ctx.fillStyle = '#1a1a2e'; ctx.fillRect(0, 0, W, H);
    if (title) { ctx.fillStyle = '#e0e0e0'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center'; ctx.fillText(title, W/2, 25); }

    let angle = -Math.PI / 2;
    values.forEach((v, i) => {
        const slice = (v / total) * Math.PI * 2;
        ctx.beginPath(); ctx.moveTo(cx, cy);
        ctx.arc(cx, cy, r, angle, angle + slice);
        ctx.fillStyle = COLORS[i % COLORS.length]; ctx.fill();
        angle += slice;
    });

    // Legend
    let ly = 50;
    labels.forEach((l, i) => {
        ctx.fillStyle = COLORS[i % COLORS.length]; ctx.fillRect(W * 0.72, ly, 12, 12);
        ctx.fillStyle = '#e0e0e0'; ctx.font = '12px sans-serif'; ctx.textAlign = 'left';
        ctx.fillText(`${l} (${((values[i]/total)*100).toFixed(1)}%)`, W * 0.72 + 18, ly + 11);
        ly += 22;
    });
}

function drawLineChart(canvasId, opts) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const {labels, datasets, title} = opts;
    const W = canvas.width, H = canvas.height;
    const pad = {top: 40, right: 20, bottom: 60, left: 60};
    const allVals = datasets.flatMap(d => d.values);
    const maxVal = Math.max(...allVals) * 1.1;
    const minVal = Math.min(0, Math.min(...allVals));
    const range = maxVal - minVal;

    ctx.fillStyle = '#1a1a2e'; ctx.fillRect(0, 0, W, H);
    if (title) { ctx.fillStyle = '#e0e0e0'; ctx.font = 'bold 16px sans-serif'; ctx.textAlign = 'center'; ctx.fillText(title, W/2, 25); }

    // Grid
    ctx.strokeStyle = 'rgba(255,255,255,0.1)'; ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = pad.top + (H - pad.top - pad.bottom) * (1 - i/5);
        ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(W - pad.right, y); ctx.stroke();
        ctx.fillStyle = '#888'; ctx.font = '11px sans-serif'; ctx.textAlign = 'right';
        ctx.fillText((minVal + range * i / 5).toFixed(1), pad.left - 8, y + 4);
    }

    // Labels
    const step = (W - pad.left - pad.right) / (labels.length - 1);
    labels.forEach((l, i) => {
        ctx.fillStyle = '#888'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(l, pad.left + i * step, H - pad.bottom + 20);
    });

    // Lines
    datasets.forEach((ds, di) => {
        ctx.strokeStyle = ds.color || COLORS[di]; ctx.lineWidth = 2;
        ctx.beginPath();
        ds.values.forEach((v, i) => {
            const x = pad.left + i * step;
            const y = pad.top + (H - pad.top - pad.bottom) * (1 - (v - minVal) / range);
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        });
        ctx.stroke();
        // Dots
        ds.values.forEach((v, i) => {
            const x = pad.left + i * step;
            const y = pad.top + (H - pad.top - pad.bottom) * (1 - (v - minVal) / range);
            ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fillStyle = ds.color || COLORS[di]; ctx.fill();
        });
    });
}
