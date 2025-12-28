// Online calculator for gate width (A.0.1~A.0.3)
(function () {
  const $ = (id) => document.getElementById(id);
  const fmt = (v) => Number.isFinite(v) ? v.toFixed(4) : "--";

  // Sigma' table for A.0.3
  const tableA03 = [
    [0.000, 0.02], [0.100, 0.05], [0.200, 0.10], [0.300, 0.16], [0.400, 0.21],
    [0.500, 0.27], [0.550, 0.30], [0.600, 0.36], [0.650, 0.42], [0.700, 0.49],
    [0.750, 0.56], [0.800, 0.63], [0.850, 0.70], [0.900, 0.78], [0.920, 0.86],
    [0.930, 0.94], [0.940, 1.02], [0.950, 1.10], [0.960, 1.18], [0.980, 1.26],
    [0.995, 1.30],
  ];

  function interpSigmaPrime(ratio) {
    if (ratio <= tableA03[0][0]) return tableA03[0][1];
    if (ratio >= tableA03[tableA03.length - 1][0]) return tableA03[tableA03.length - 1][1];
    for (let i = 0; i < tableA03.length - 1; i++) {
      const [ra, va] = tableA03[i];
      const [rb, vb] = tableA03[i + 1];
      if (ratio >= ra && ratio <= rb) {
        const t = (ratio - ra) / (rb - ra);
        return va + t * (vb - va);
      }
    }
    return tableA03[tableA03.length - 1][1];
  }

  function computeA01() {
    const Q = parseFloat($("a01-q").value);
    const H0 = parseFloat($("a01-h0").value);
    const H = parseFloat($("a01-h").value);
    const h1 = parseFloat($("a01-h1").value);
    const b0 = parseFloat($("a01-b0").value);
    const b1 = parseFloat($("a01-b1").value);
    const N = parseInt($("a01-n").value, 10);
    const dc = parseFloat($("a01-dc").value);
    const db = parseFloat($("a01-db").value);
    const m = parseFloat($("a01-m").value);
    const g = parseFloat($("a01-g").value);
    const single = $("a01-single").checked || N === 1;

    if (![Q,H0,H,h1,b0,b1,m,g].every(Number.isFinite) || !Number.isFinite(N)) return "输入不完整";
    if (H0 <= 0 || H <= 0 || b0 <= 0 || b1 <= 0 || N <= 0) return "H0/H/b0/b1/N 需大于 0";

    const ratio = h1 / H0;
    const sigma = 2.31 * Math.pow(ratio * (1 - ratio), 0.4);
    let epsilon = NaN, epsilonC = NaN, epsilonB = NaN;
    if (single) {
      epsilon = 1 - 0.171 * (1 - b0 / b1) * Math.sqrt(b0 / b1);
    } else {
      epsilonC = 1 - 0.171 * (1 - b0 / (b0 + dc)) * Math.sqrt(b0 / (b0 + dc));
      const dbTerm = b0 + db / 2.0;
      epsilonB = 1 - 0.171 * (1 - b0 / dbTerm) * Math.sqrt(b0 / dbTerm);
      epsilon = epsilonC * (N - 1.0) / N + epsilonB / N;
    }
    const denom = sigma * epsilon * m * Math.sqrt(2 * g) * Math.pow(H, 1.5);
    if (!Number.isFinite(denom) || denom <= 0) return "分母<=0，请检查输入";
    const B0 = Q / denom;
    return `B0 = ${fmt(B0)} m\n` +
      `sigma = ${fmt(sigma)}, epsilon = ${fmt(epsilon)}\n` +
      `epsilon_c = ${fmt(epsilonC)}, epsilon_b = ${fmt(epsilonB)}`;
  }

  function computeA02() {
    const Q = parseFloat($("a02-q").value);
    const H0 = parseFloat($("a02-h0").value);
    const h0 = parseFloat($("a02-h0b").value);
    const hs = parseFloat($("a02-hs").value);
    const sigma = parseFloat($("a02-sigma").value);
    const g = parseFloat($("a02-g").value);
    if (![Q,H0,h0,hs,sigma,g].every(Number.isFinite)) return "输入不完整";
    if (H0 <= 0) return "H0 需大于 0";
    const headDiff = H0 - h0;
    if (headDiff <= 0) return "(H0 - h0) 需大于 0";
    const mu0 = 0.877 + Math.pow(hs / H0 - 0.65, 2);
    const denom = sigma * mu0 * Math.sqrt(2 * g * headDiff);
    if (!Number.isFinite(denom) || denom <= 0) return "分母<=0，请检查输入";
    const B0 = Q / denom;
    return `B0 = ${fmt(B0)} m\nmu0 = ${fmt(mu0)}`;
  }

  function computeA03() {
    const Q = parseFloat($("a03-q").value);
    const H0 = parseFloat($("a03-h0").value);
    const H = parseFloat($("a03-h").value);
    const he = parseFloat($("a03-he").value);
    const hc = parseFloat($("a03-hc").value);
    const ec = parseFloat($("a03-ec").value);
    const phi = parseFloat($("a03-phi").value);
    const g = parseFloat($("a03-g").value);
    if (![Q,H0,H,he,hc,ec,phi,g].every(Number.isFinite)) return "输入不完整";
    if (H0 <= 0 || H <= 0 || he <= 0) return "H0/H/he 需大于 0";
    const ratio = (he - hc) / (H - hc);
    const sigmaPrime = interpSigmaPrime(ratio);
    const lambda = 0.4 / Math.exp(Math.pow(Math.log(6 * ec), 2));
    const epsilonPrime = 1 / (1 + Math.sqrt(lambda * (1 - Math.pow(he / H, 2))));
    const mu = phi * Math.exp(epsilonPrime) / Math.sqrt(1 - epsilonPrime * he / H);
    const denom = sigmaPrime * mu * he * Math.sqrt(2 * g * H0);
    if (!Number.isFinite(denom) || denom <= 0) return "分母<=0，请检查输入";
    const B0 = Q / denom;
    return `B0 = ${fmt(B0)} m\n` +
      `sigma' = ${fmt(sigmaPrime)}, mu = ${fmt(mu)}\n` +
      `epsilon' = ${fmt(epsilonPrime)}, lambda = ${fmt(lambda)}`;
  }

  function setResult(id, text) {
    $(id).textContent = text;
  }

  const samples = {
    a01: {
      q: 120, h0: 8, h: 10, h1: 5, b0: 3, b1: 3.5, n: 1, dc: 0, db: 0, m: 0.885, g: 9.81, single: true,
    },
    a02: {
      q: 150, h0: 8, h0b: 2, hs: 5, sigma: 0.82, g: 9.81,
    },
    a03: {
      q: 180, h0: 9, h: 10, he: 4, hc: 1.5, ec: 0.2, phi: 0.96, g: 9.81,
    },
  };

  function fillSample(which) {
    if (which === "a01") {
      const s = samples.a01;
      $("a01-q").value = s.q;
      $("a01-h0").value = s.h0;
      $("a01-h").value = s.h;
      $("a01-h1").value = s.h1;
      $("a01-b0").value = s.b0;
      $("a01-b1").value = s.b1;
      $("a01-n").value = s.n;
      $("a01-dc").value = s.dc;
      $("a01-db").value = s.db;
      $("a01-m").value = s.m;
      $("a01-g").value = s.g;
      $("a01-single").checked = s.single;
    } else if (which === "a02") {
      const s = samples.a02;
      $("a02-q").value = s.q;
      $("a02-h0").value = s.h0;
      $("a02-h0b").value = s.h0b;
      $("a02-hs").value = s.hs;
      $("a02-sigma").value = s.sigma;
      $("a02-g").value = s.g;
    } else if (which === "a03") {
      const s = samples.a03;
      $("a03-q").value = s.q;
      $("a03-h0").value = s.h0;
      $("a03-h").value = s.h;
      $("a03-he").value = s.he;
      $("a03-hc").value = s.hc;
      $("a03-ec").value = s.ec;
      $("a03-phi").value = s.phi;
      $("a03-g").value = s.g;
    }
  }

  function bindTabs() {
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        tabs.forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        document.querySelectorAll(".tab-content").forEach((c) => c.classList.add("hidden"));
        $("tab-" + tab.dataset.tab).classList.remove("hidden");
      });
    });
  }

  function bindActions() {
    document.querySelectorAll("[data-fill]").forEach((btn) => {
      btn.addEventListener("click", () => fillSample(btn.dataset.fill));
    });
    document.querySelectorAll("[data-run]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const which = btn.dataset.run;
        let result = "";
        if (which === "a01") result = computeA01();
        if (which === "a02") result = computeA02();
        if (which === "a03") result = computeA03();
        setResult(which + "-result", result);
      });
    });
    $("fill-all").addEventListener("click", () => {
      fillSample("a01");
      fillSample("a02");
      fillSample("a03");
    });
  }

  function initDefaults() {
    fillSample("a01");
    fillSample("a02");
    fillSample("a03");
  }

  document.addEventListener("DOMContentLoaded", () => {
    bindTabs();
    bindActions();
    initDefaults();
  });
})();
