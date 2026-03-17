import { getGlobalMarketData } from "./data/globalDataEngine.js";
import { createTrade } from "./trade/tradeEngine.js";
import { calculateCost } from "./trade/costEngine.js";
import { buildOffer } from "./trade/offerBuilder.js";
import { initiatePayment } from "./payment/paymentEngine.js";
import { createEscrow } from "./payment/escrowEngine.js";
import { createMilestones } from "./payment/milestoneEngine.js";
import { planLogistics } from "./logistics/logisticsEngine.js";
import { generateContract } from "./contracts/contractEngine.js";
import {
