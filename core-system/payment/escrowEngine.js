export function createEscrow(payment) {
  return {
    escrowId: "ESCROW_" + Date.now(),
    amount: payment.amount,
    status: "LOCKED"
  };
}
