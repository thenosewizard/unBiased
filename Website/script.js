// JavaScript source code
function change(id) {
    if (id == "pc") {
        console.log("PC tab");
        document.getElementById("l_pc").style.display = "flex";
        document.getElementById("l_console").style.display = "none";
        document.getElementById("l_mobile").style.display = "none";
    } if (id == "console") {
        console.log('console tab')
        document.getElementById("l_pc").style.display = "none";
        document.getElementById("l_console").style.display = "flex";
        document.getElementById("l_mobile").style.display = "none";
    } if (id == "mobile") {
        console.log('mobile tab')
        document.getElementById("l_pc").style.display = "none";
        document.getElementById("l_console").style.display = "none";
        document.getElementById("l_mobile").style.display = "flex";
    }
}