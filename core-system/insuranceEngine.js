export function createInsurance(trade) {
  return {
    policyId: "INS_" + Date.now(),
    insuredValue: trade.sellPrice * trade.volume,
    provider: "GLOBAL_INSURE",
    status: "ACTIVE"
  };
}
