export function createMilestones() {
  return [
    { step: "PAYMENT_LOCK", status: "DONE" },
    { step: "SHIPMENT_START", status: "PENDING" },
    { step: "DELIVERY", status: "PENDING" }
  ];
}
