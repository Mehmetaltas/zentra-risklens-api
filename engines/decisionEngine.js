export function strategicAdvisory(risk){

if(risk.riskLevel==="high"){

return {
shortTerm:"Tighten monitoring",
midTerm:"Prepare hedge scenarios"
}

}

if(risk.riskLevel==="medium"){

return {
shortTerm:"Increase observation",
midTerm:"Monitor markets"
}

}

return {
shortTerm:"System stable",
midTerm:"Maintain monitoring"
}

}
