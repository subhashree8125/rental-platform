const decrease=document.getElementById("decrease");
const increase=document.getElementById("increase");
const reset=document.getElementById("reset");
const countlabel=document.getElementById("countlabel")
let count=0;
increase.onclick=function()
{
    count++;
    countable.textContent=count;
}
decrease.onclick=function()
{
    count--;
    countable.textContent=count;
}
reset.onclick=function()
{
    count=0;
    countable.textContent=count;
}