import { getGlobalData } from "./data/globalDataEngine.js";
import { generateTrade } from "./trade/tradeEngine.js";
import { buildOffer } from "./trade/offerBuilder.js";
import { calculateCost } from "./trade/costEngine.js";

import { createContract } from "./contracts/contractEngine.js";

import { buildPayment } from "./payment/paymentEngine.js";
import { createEscrow } from "./payment/escrowEngine.js";
import { buildMilestones } from "./payment/milestoneEngine.js";

import { createInsurance } from "./insurance/insuranceEngine.js";
import { planLogistics } from "./logistics/logisticsEngine.js";
import { matchNetwork } from "./network/networkEngine.js";
import { validate } from "./security/securityEngine.js";

export async function runZentraSystem() {
  const data = await getGlobalData();

  const trade = generateTrade(data);
  const offer = buildOffer(trade);
  const cost = calculateCost(trade);

  const contract = createContract(trade);

  const payment = buildPayment(contract);
  const escrow = createEscrow(payment);
  const milestones = buildMilestones(payment.total);

  const insurance = createInsurance(trade);
  const logistics = planLogistics(trade);
  const network = matchNetwork();
  const security = validate(trade);

  return {
    data,
    trade,
    offer,
    cost,
    contract,
    payment,
    escrow,
    milestones,
    insurance,
    logistics,
    network,
    security,
    status: "SYSTEM_READY"
  };
}
