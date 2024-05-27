console.log("Login Working!");


const showPassword = document.querySelector(".showPassword")
const passwordField = document.querySelector("#passwordField")


const showPasswordToggle = (e) =>{
    console.log("Working Login");
    if (showPassword.textContent === "SHOW"){
        showPassword.textContent="HIDE";
        passwordField.setAttribute("type", "text");
    }else{
        showPassword.textContent="SHOW";
        passwordField.setAttribute("type", "password");
    }
}

showPassword.addEventListener("click", showPasswordToggle);

