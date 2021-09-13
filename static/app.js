function myFunction(vars)
{
    document.getElementById("demo").innerHTML = 5 + 6 + vars;
}

function drawLine(vars)
{
    document.getElementById("demo").innerHTML = 5 + 6 + vars;
}

function drawCircle()
{
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    ctx.beginPath();
    ctx.arc(95, 50, 40, 0, 2 * Math.PI);
    ctx.stroke();
}

