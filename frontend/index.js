const decrease = document.getElementById("decrease");
const increase = document.getElementById("increase");
const reset = document.getElementById("reset");
const countLabel = document.getElementById("countlabel");

let count = 0;

increase.onclick = function () {
    count++;
    countLabel.textContent = count;
};

decrease.onclick = function () {
    count--;
    countLabel.textContent = count;
};

reset.onclick = function () {
    count = 0;
    countLabel.textContent = count;
};
