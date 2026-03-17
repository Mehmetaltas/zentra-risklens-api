export function createEscrow(payment) {
  return {
    escrowId: "ESCROW-" + Date.now(),
    amount: payment.amount,
    status: "LOCKED"
  };
}
