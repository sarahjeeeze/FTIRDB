function changeSrc() {
    if (document.getElementById("onegraph").checked) {
    document.getElementById("picture").src = "https://pbs.twimg.com/profile_images/447374371917922304/P4BzupWu.jpeg";
    } else if (document.getElementById("twographs").checked) { 
    document.getElementById("picture").src = "http://localhost:6543/static/fig.png";
    }
}