const riskURL="https://zentra-risklens-api-2.onrender.com/health";
const stressURL="https://zentra-credit-stress-api.onrender.com/health";

async function checkHealth(url,el){
try{
const r=await fetch(url);
if(r.ok){ el.textContent="LIVE"; el.style.color="#19e68c"; }
else{ el.textContent="ERROR"; el.style.color="#ff4d6d"; }
}catch{
el.textContent="OFFLINE";
el.style.color="#ff4d6d";
}
}

checkHealth(riskURL,document.getElementById("riskStatus"));
checkHealth(stressURL,document.getElementById("stressStatus"));

document.getElementById("runScore").onclick=()=>{
const score=Math.floor(Math.random()*40)+60;
document.getElementById("scoreOutput").textContent=
JSON.stringify({
risk_score:score,
risk_band: score>80?"LOW":"MID",
model:"v1"
},null,2);
};

const dict={
tr:{
heroTitle:"Davranışsal Finansal Altyapı",
heroSub:"Bankalar ve regülasyon yoğun fintech’ler için lisanslanabilir risk altyapısı.",
heroBtn:"Canlı Sistem"
},
en:{
heroTitle:"Behavioral Financial Infrastructure",
heroSub:"Licensable risk infrastructure for banks and regulated fintechs.",
heroBtn:"Live System"
}
};

function applyLang(l){
document.getElementById("heroTitle").innerText=dict[l].heroTitle;
document.getElementById("heroSub").innerText=dict[l].heroSub;
document.getElementById("heroBtn").innerText=dict[l].heroBtn;
document.getElementById("trBtn").classList.toggle("active",l==="tr");
document.getElementById("enBtn").classList.toggle("active",l==="en");
}

document.getElementById("trBtn").onclick=()=>applyLang("tr");
document.getElementById("enBtn").onclick=()=>applyLang("en");

applyLang("tr");
