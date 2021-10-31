
var userLoggedIn = "false";
userLoggedIn = sessionStorage.getItem("userStatus");
//console.log(userLoggedIn);

var req = new XMLHttpRequest();
var url = '/Data';

req.open('GET',url,true); // set this to POST if you would like
req.addEventListener('load',onLoad);
req.addEventListener('error',onError);

req.send();

// List to store all prices
var prices = [];
var types = [];

var totalPrice = document.getElementById('total');

// If user isnt signed in do not allow access to app
window.onload = function() {
    if(userLoggedIn === 'false'){
        location.href = "login.html";
    }
};

function onLoad() {

   var response = this.responseText;
   var parsedResponse = JSON.parse(response);
   var type = parsedResponse['Type'];
   var price = parsedResponse['Price'];
   prices.push(price);
   types.push(type);
   //console.log(type)
   //console.log(price)
   li = document.createElement('li');
   li.innerHTML = type + ', ' + '$' + price;
   li.setAttribute("class", "listitems");
   button = document.createElement("BUTTON");
   button.innerHTML = "Remove";
   button.setAttribute("onclick", "deleteItems()");
   button.setAttribute("class", "delete");
   li.appendChild(button);
   list.insertBefore(li, list.childNodes[0]);
   total()

}

// This function allows deletion of list items
function deleteItems() {

    var listitems = document.querySelectorAll(".listitems");
    
    for (var index = 0; index < listitems.length; index++){
        //listitems[index].addEventListener("click", function(){
        //    this.classList.toggle("active");
        //});
        listitems[index].querySelector(".delete").addEventListener("click",
        function(){
            // Get html text of closest listitem to the click
            var text = (this.closest(".listitems").innerHTML);
            // Split the string in 2 at the comma to get the type of item
            text = text.split(',');
            //console.log(text[0]);
            // Iterate list of item types and check if the type is in the list
            for(var i=0; i<types.length; i++){
                if(types[i] == text[0]){
                    // If the type is in the list remove it and its price at the same index
                    types.splice(types[i], 1);
                    prices.splice(types[i], 1);
                }
            }
            this.closest(".listitems").remove();
        });
    }

}

function onError() {
  // Handle error here, print message perhaps
  console.log('No data to receive');
}

var totalPrice;

// Function which adds up and displays total price
function total() {
    if(prices.length !== 0) {
        totalPrice = prices.reduce((a, b) => a + b, 0)
        console.log(totalPrice);
    } else {
        totalPrice = 0;
    }
        //for(i=0; i<prices.length; i++) {
        //    var total = 0;
        //    total = total + prices[i];
        //    console.log(total);
        //}
    totalPrice.innerHTML = "$" + totalPrice;
}

function Logout() {
    sessionStorage.setItem("userStatus", "false");
    //console.log(userLoggedIn);
    location.href = "login.html";
}

function checkout() {
    alert("Purchase Successful: " + totalPrice.value);
    // Clearing elements
    totalPrice = 0;
    prices.length = 0;
    types.length = 0;
}