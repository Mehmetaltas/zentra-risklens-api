document.querySelector("button").onclick = function () {

const question = document.querySelector("input").value;

let result = "No analysis";

if(question.includes("inflation")) {
result = "Inflation risk increasing globally.";
}

if(question.includes("bank")) {
result = "Banking sector volatility detected.";
}

if(question.includes("oil")) {
result = "Oil market risk elevated.";
}

alert(result);

}
