export function generateTrade(data) {
  return {
    buyer: "auto-buyer",
    seller: "auto-supplier",
    amount: 100000,
    basedOn: data.driver
  };
}
