import { SOURCES } from "../data/source-registry.js";

export function calculateGlobalRisk(signals) {

  let risk = 0;
  let drivers = [];

  if (signals.oil_price > 80) {
    risk += 25;
    drivers.push("oil shock");
  }

  if (signals.container_rate > 3000) {
    risk += 20;
    drivers.push("logistics stress");
  }

  if (signals.cyber_threat > 40) {
    risk += 15;
    drivers.push("cyber instability");
  }

  if (signals.inflation > 5) {
    risk += 20;
    drivers.push("inflation pressure");
  }

  return {
    score: risk,
    drivers: drivers
  };

}
