function patientvalidateForm() {
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var phone = document.getElementById("phone").value;
    var gender = document.getElementById("gender").value;
    var address = document.getElementById("address").value;
    var pin = document.getElementById("pin").value;

    var rname=/^[A-Za-z ]+$/;
    var remail=/^[a-zA-Z][a-zA-Z0-9._]*@gmail\.com$/;
    var rpassword= /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$/;
    var rphone=/^[9876]\d{9}$/;
    var rpin=/^\d{6}$/;

    if (rname.test(name) && remail.test(email) && rpassword.test(password) && rphone.test(phone) && rpin.test(pin) && gender!="-1"){
        return true;
    }
    else{
        alert("please fill details carefully:name - must contain only aplhabets and spaces,email-must ends with @gmail.com,password must contains min one (uppercase,lowercase and one special character),phone must start with (9,8,7,6) and of length 10  digits only,pincode must be of length 6 digits only");
        return false;
    }

}
