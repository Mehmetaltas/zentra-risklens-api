export function createEscrow(payment) {
  return {
    amount: payment.amount,
    status: "LOCKED"
  };
}
