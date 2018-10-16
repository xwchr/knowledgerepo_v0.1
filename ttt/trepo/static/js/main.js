function toggleTopnavMenu() {
    var x = document.getElementById("topnav");
    if (x.className === "") {
        x.className = "responsive";
    } else {
        x.className = "";
    }
}