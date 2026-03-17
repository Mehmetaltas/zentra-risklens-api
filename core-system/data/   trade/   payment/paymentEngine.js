export function buildPayment(contract) {
  return {
    total: contract.amount,
    currency: "USD"
  };
}
