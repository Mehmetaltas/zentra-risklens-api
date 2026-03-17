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

export function runZentraFlow() {
  const data = getGlobalMarketData();

  const trade = createTrade({
    product: data.product,
    buyPrice: data.basePrice,
    sellPrice: data.basePrice * 1.2,
    volume: 100
  });

  const cost = calculateCost(trade);
  const offer = buildOffer(trade, cost);
  const payment = initiatePayment(trade);
  const escrow = createEscrow(payment);
  const milestones = createMilestones();
  const logistics = planLogistics(trade);
  const contract = generateContract(trade);
  const insurance = createInsurance(trade);
  const network = matchPartners();
  const security = runSecurityCheck();

  return {
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
    status: "ZENTRA_FLOW_COMPLETED"
  };
    }
