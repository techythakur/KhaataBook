console.log("Register Working!");

// Selects the class or id to be manipulated
const usernameField = document.querySelector("#usernameField");
const invalid_user = document.querySelector(".invalid-user");
const emailField = document.querySelector("#emailField")
const invalid_email = document.querySelector(".invalid-email");
const usernameSuccess = document.querySelector(".username-success");
const emailSuccess = document.querySelector(".email-success");
const passwordField = document.querySelector("#passwordField")
const showPassword = document.querySelector(".showPassword");
const showBtn = document.querySelector(".showBtn");


const handleShowToggle = (e) => {
    console.log("Working Login");
    if (showPassword.textContent === "SHOW"){
        showPassword.textContent="HIDE";
        passwordField.setAttribute("type", "text");
    }else{
        showPassword.textContent="SHOW";
        passwordField.setAttribute("type", "password");
    }
}

usernameField.addEventListener("keyup", (e)=>{

    const userNameval = e.target.value;
    console.log("userNameval: ",userNameval);

    invalid_user.style.display = "none";
    usernameField.classList.remove("is-invalid");

    const formData = new FormData();

    if (userNameval.length>0) {

        usernameSuccess.innerHTML = `<p style="color: green;">Checking ${userNameval}</p>`
        usernameSuccess.style.display = "block";

        formData.append("username", userNameval)

        fetch("/authentication/validate-username/", {
            body: formData,
            method: "POST",
        }).then(res => res.json()).then( data => {

            usernameSuccess.style.display = "none";

            if (!Boolean(data.flag) ) {
                showBtn.disabled = true;
                usernameField.classList.add("is-invalid");
                invalid_user.style.display = "block";
                invalid_user.innerHTML = `<p style="color: red;">${data.msg}</p>`;
            }else{
                showBtn.removeAttribute("disabled");
            }

        });
    }
    
});

emailField.addEventListener("keyup", (e)=>{

    const emailVal = e.target.value
    console.log(emailVal)

    const formData = new FormData()

    emailField.classList.remove("is-invalid");
    invalid_email.style.display = "none";

    if (emailVal.length>0){

        // Shows content on web
        emailSuccess.innerHTML = `<p style="color: green;">Checking ${emailVal}</p>`;
        emailSuccess.style.display = "block";

        // Created FormData to be sent
        formData.append("email", emailVal);

        // To fetch the data from API
        fetch("/authentication/validate-email/", {
            body: formData,
            method: "POST"
        }).then(res=>res.json()).then(data => {
            console.log(data)
            emailSuccess.style.display = "none";
            if ( !Boolean(data.flag) ){
                showBtn.disabled = true;
                emailField.classList.add("is-invalid");
                invalid_email.style.display = "block";
                invalid_email.innerHTML = `<p style="color: red;">${data.msg}</p>`
            }else{
                showBtn.removeAttribute("disabled");
            }
        }); 
    }

    

    
});

showPassword.addEventListener("click", handleShowToggle);