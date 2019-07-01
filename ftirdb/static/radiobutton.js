function changeSrc() {
    if (document.getElementById("onegraph").checked) {
    document.getElementById("picture").src = "http://localhost:6543/static/fig2.png";
    } else if (document.getElementById("twographs").checked) { 
    document.getElementById("picture").src = "http://localhost:6543/static/fig.png";
    }
}

function showMenu() {
     document.getElementsByClassName("menu")[0].style.display = "block";
}