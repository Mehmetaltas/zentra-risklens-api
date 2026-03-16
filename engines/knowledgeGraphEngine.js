export function buildKnowledgeGraph(data) {
  return {
    nodes: [
      "Markets",
      "Signals",
      "Finance",
      "Trade",
      "Risk",
      "Decision"
    ],
    links: [
      ["Markets", "Signals"],
      ["Signals", "Risk"],
      ["Finance", "Risk"],
      ["Trade", "Risk"],
      ["Risk", "Decision"]
    ],
    summary: "Basic knowledge graph built"
  };
}
