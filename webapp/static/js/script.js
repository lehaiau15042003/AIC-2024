document.getElementById('login-form').addEventListener('submit', function(event)
{
    event.preventDefault();

    const username = document.getElementById('border_user').value;

    const password = document.getElementById('border_pass').value;

    const errorMessage = document.getElementById('error-message');

    if (username == "admin" && password == "admin"){
        alert("Login Success");
        window.location.href = "base.html";
    }
    else{
        errorMessage.textContent = "Invalid username or password";
        errorMessage.style.display = "block";
    }
});
