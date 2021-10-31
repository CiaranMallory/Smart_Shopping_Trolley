
window.onload = function() {

    const loginform = document.getElementById('login');

    loginform.addEventListener('submit', (event) => {

        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;

        // Search database for user
        // Check that user is not already signed up
        var db = `http://192.168.1.8:3000/getuser/${username}`;

        fetch(db)
            .then(response => {
                return response.json();
            })
            .then(result => {
                //console.log(result);
                // If user exists
                if(result.userStatus === 1){
                    // Check Password matches entered password
                    var db = `http://192.168.1.8:3000/getpassword/${username}/${password}`;

                    fetch(db)
                    .then(response => {
                        return response.json();
                    })
                    .then(result => {
                        //console.log(result.passwordStatus);
                        // If passwords match sign in user
                        if(result.passwordStatus === 1){
                            var userLoggedIn = 'true';
                            sessionStorage.setItem("userStatus", userLoggedIn);
                            sessionStorage.setItem("username", username);
                            location.href = 'start.html';
                        } else {
                            alert('Incorrect Password');
                        }
                    });

                } else {
                    alert('User doesnt exist')
                }
            });
    });
};