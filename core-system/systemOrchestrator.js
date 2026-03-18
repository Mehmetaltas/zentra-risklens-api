import { getGlobalMarketData } from "./data/globalDataEngine.js";
import { createTrade } from "./trade/tradeEngine.js";
import { calculateCost } from "./trade/costEngine.js";
import { buildOffer } from "./trade/offerBuilder.js";
import { initiatePayment } from "./payment/paymentEngine.js";
import { createEscrow } from "./payment/escrowEngine.js";
import { createMilestones } from "./payment/milestoneEngine.js";
import { planLogistics } from "./logistics/logisticsEngine.js";
import { generateContract } from "./contracts/contractEngine.js";
import { createInsurance } from "./insurance/insuranceEngine.js";
import { matchPartners } from "./network/networkEngine.js";
import { runSecurityCheck } from "./security/securityEngine.js";
import { createIdBundle } from "./idEngine.js";

import { runAIDecisionEngine } from "./ai/aiDecisionEngine.js";
import { runPredictiveTradeEngine } from "./ai/predictiveTradeEngine.js";
import { runRiskForecastEngine } from "./ai/riskForecastEngine.js";

export function runZentraFlow() {
  const ids = createIdBundle();

  const data = getGlobalMarketData();

  const trade = {
    ...createTrade({
      product: data.product,
      buyPrice: data.basePrice,
      sellPrice: data.basePrice * 1.2,
      volume: 100
    }),
    tradeId: ids.tradeId
  };

  const cost = calculateCost(trade);

  const offer = {
    ...buildOffer(trade, cost),
    offerId: ids.offerId
  };

  const payment = {
    ...initiatePayment(trade),
    paymentId: ids.paymentId
  };

  const escrow = {
    ...createEscrow(payment),
    escrowId: ids.escrowId
  };

  const milestones = createMilestones();
  const logistics = planLogistics(trade);

  const contract = {
    ...generateContract(trade),
    contractId: ids.contractId
  };

  const insurance = createInsurance(trade);
  const network = matchPartners();
  const security = runSecurityCheck();

  const aiDecision = runAIDecisionEngine({
    data,
    trade,
    cost,
    offer,
    logistics,
    security
  });

  const predictiveTrade = runPredictiveTradeEngine({
    data,
    trade,
    offer
  });

  const riskForecast = runRiskForecastEngine({
    data,
    logistics,
    security
  });
version: "AI_BUILD_1",
aiMarker: "AI_ON",
  return {
    ids,
    data,
    trade,
    cost,
    offer,
    payment,
    escrow,
    milestones,
    logistics,
    contract,
    insurance,
    network,
    security,
    aiDecision,
    predictiveTrade,
    riskForecast,
    status: "ZENTRA_FLOW_COMPLETED"
  };
}
