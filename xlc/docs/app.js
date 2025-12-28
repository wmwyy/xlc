// 消力池计算（附录 B.1）
(function () {
  const $ = (id) => document.getElementById(id);
  const fmt = (v) => (Number.isFinite(v) ? v.toFixed(4) : "--");

  const defaults = {
    sigma0: 1.05,
    alpha: 1.0,
    q: 5.0,
    b1: 10.0,
    b2: 12.0,
    T0: 8.0,
    p: 1.0,
    hs: 3.0,
    Ls: 5.0,
    beta: 0.75,
    g: 9.81,
  };

  function cbrt(x) {
    return Math.sign(x) * Math.pow(Math.abs(x), 1 / 3);
  }

  // Solve x^3 + a x^2 + b x + d = 0; return real roots
  function solveCubic(a, b, d) {
    const p = b - (a * a) / 3;
    const q = (2 * Math.pow(a, 3)) / 27 - (a * b) / 3 + d;
    const disc = Math.pow(q / 2, 2) + Math.pow(p / 3, 3);
    if (disc >= 0) {
      const sqrt = Math.sqrt(disc);
      const u = cbrt(-q / 2 + sqrt);
      const v = cbrt(-q / 2 - sqrt);
      return [u + v - a / 3];
    }
    const r = Math.sqrt(-p / 3);
    const phi = Math.acos(-q / (2 * Math.pow(r, 3)));
    const roots = [];
    for (let k = 0; k < 3; k++) {
      const t = 2 * r * Math.cos((phi + (2 * Math.PI * k) / 3) / 1);
      roots.push(t - a / 3);
    }
    return roots;
  }

  function compute() {
    const val = (id) => parseFloat($(id).value);
    const sigma0 = val("sigma0");
    const alpha = val("alpha");
    const q = val("q");
    const b1 = val("b1");
    const b2 = val("b2");
    const T0 = val("T0");
    const p = val("p");
    const hs = val("hs");
    const Ls = val("Ls");
    const beta = val("beta");
    const g = val("g");

    if (![sigma0, alpha, q, b1, b2, T0, p, hs, Ls, beta, g].every(Number.isFinite)) {
      return "输入不完整";
    }
    if ([sigma0, alpha, q, b1, b2, T0, p, hs, g].some((x) => x <= 0)) {
      return "σ0/α/q/b1/b2/T0/p/hs/g 需大于 0";
    }

    // h_c from h_c^3 - T0*h_c^2 + α*q^2/(2*g*p^2) = 0
    const coeffC = (alpha * q * q) / (2 * g * p * p);
    const roots = solveCubic(-T0, 0, coeffC);
    const positives = roots.filter((r) => r > 0);
    const hc = positives.length ? Math.max(...positives) : Math.max(...roots);

    // h_c'' from B.1.1-2
    const shrink = Math.pow(b1 / b2, 0.25);
    const sqrtTerm = Math.sqrt(1 + (8 * alpha * q * q) / (g * Math.pow(hc, 3)));
    const hc2 = (hc / 2) * (sqrtTerm - 1) * shrink;

    // ΔZ from B.1.1-4
    const deltaZ = (alpha * q * q) / (2 * g * p * p * hs * hs) - (alpha * q * q) / (2 * g * hc2 * hc2);

    // d from B.1.1-1
    const d = sigma0 * hc2 - hs - deltaZ;

    // Lj and Lsj from B.1.2
    const Lj = 6.9 * (hc2 - hc);
    const Lsj = Ls + beta * Lj;

    return [
      `h_c = ${fmt(hc)} m`,
      `h_c'' = ${fmt(hc2)} m`,
      `ΔZ = ${fmt(deltaZ)} m`,
      `d (消力池深度) = ${fmt(d)} m`,
      `L_j (水跃长度) = ${fmt(Lj)} m`,
      `L_sj (消力池长度) = ${fmt(Lsj)} m`,
    ].join("\n");
  }

  function fillSample() {
    Object.entries(defaults).forEach(([k, v]) => {
      $(k).value = v;
    });
    $("result").textContent = "";
  }

  function bind() {
    $("fill-sample").addEventListener("click", fillSample);
    $("reset").addEventListener("click", fillSample);
    $("run").addEventListener("click", () => {
      const res = compute();
      $("result").textContent = res;
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    fillSample();
    bind();
  });
})();
