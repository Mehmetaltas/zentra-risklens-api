const counters = {
  trade: 0,
  offer: 0,
  contract: 0,
  action: 0,
  payment: 0,
  escrow: 0
};

function pad(num, size = 4) {
  return String(num).padStart(size, "0");
}

function stamp() {
  const d = new Date();

  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");

  return `${y}${m}${day}`;
}

function next(type) {
  counters[type] = (counters[type] || 0) + 1;
  return counters[type];
}

export function createTradeId() {
  return `TRD-${stamp()}-${pad(next("trade"))}`;
}

export function createOfferId() {
  return `OFF-${stamp()}-${pad(next("offer"))}`;
}

export function createContractId() {
  return `CNT-${stamp()}-${pad(next("contract"))}`;
}

export function createActionId() {
  return `ACT-${stamp()}-${pad(next("action"))}`;
}

export function createPaymentId() {
  return `PAY-${stamp()}-${pad(next("payment"))}`;
}

export function createEscrowId() {
  return `ESC-${stamp()}-${pad(next("escrow"))}`;
}

export function createIdBundle() {
  return {
    actionId: createActionId(),
    tradeId: createTradeId(),
    offerId: createOfferId(),
    contractId: createContractId(),
    paymentId: createPaymentId(),
    escrowId: createEscrowId()
  };
}
