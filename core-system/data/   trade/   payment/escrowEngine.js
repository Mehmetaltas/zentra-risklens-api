export function createEscrow(payment) {
  return {
    escrowId: "ESC-" + Date.now(),
    amount: payment.total,
    status: "locked"
  };
}
