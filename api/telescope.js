import { computeSignals } from "../core/signal_engine/signal-engine.js";

export async function getTelescopeData() {
  const response = await fetch("../data/global-signals.json");
  const data = await response.json();

  return computeSignals(data);
}
