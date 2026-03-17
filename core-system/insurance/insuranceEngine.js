export function createInsurance(trade) {
  return {
    policyId: "INS-" + Date.now(),
    insuredValue: trade.sellPrice * trade.volume,
    provider: "ZENTRA INSURE"
  };
}
