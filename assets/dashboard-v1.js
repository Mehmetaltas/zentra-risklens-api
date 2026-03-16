import { computeSignals } from "../../core/signal_engine/signal-engine.js";

async function loadDashboard() {
  try {
    const response = await fetch("../global-signals.json");
    const data = await response.json();

    const result = computeSignals(data);

    setText("globalRiskScore", result.globalRiskScore);
    setText("riskLevel", result.riskLevel?.toUpperCase() || "LOW");
    setText("dominantDriver", result.dominantDriver || "Unknown");
    setText("riskSummary", result.summary || "No summary available.");

    setText("oilValue", result.markets?.oil ?? "--");
    setText("goldValue", result.markets?.gold ?? "--");
    setText("sp500Value", result.markets?.sp500 ?? "--");
    setText("interestValue", result.markets?.interestRate ?? "--");
    setText("shippingValue", result.markets?.shipping ?? "--");

    renderSignals(result.signals || []);
  } catch (error) {
    console.error("Dashboard load failed:", error);
    setText("riskSummary", "Dashboard data could not be loaded.");
  }
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function renderSignals(signals) {
  const list = document.getElementById("signalsList");
  if (!list) return;

  list.innerHTML = "";

  signals.forEach(signal => {
    const item = document.createElement("div");
    item.className = "signal-item";

    item.innerHTML = `
      <div class="signal-head">
        <strong>${signal.title}</strong>
        <span class="signal-severity ${signal.severity}">${signal.severity}</span>
      </div>
      <div class="signal-summary">${signal.summary}</div>
    `;

    list.appendChild(item);
  });
}

document.addEventListener("DOMContentLoaded", loadDashboard);
