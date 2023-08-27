function validateForm() {
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var gender = document.getElementById("type").value;

    var rname=/^[A-Za-z ]+$/;
    var remail=/^[a-zA-Z][a-zA-Z0-9._]*@gmail\.com$/;
    var rpassword= /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$/;

    if (rname.test(name) && remail.test(email) && rpassword.test(password) && gender!="-1"){
        return true;
    }
    else{
        alert("please fill details carefully:name - must contain only aplhabets and spaces,email-must ends with @gmail.com,password must contains min one (uppercase,lowercase and one special character)");
        return false;
    }
}
