var req = new XMLHttpRequest();
var url = '/Data';

req.open('GET',url,true); // set this to POST if you would like
req.addEventListener('load',onLoad);
req.addEventListener('error',onError);

req.send();

function onLoad() {
   var response = this.responseText;
   var parsedResponse = JSON.parse(response);

   var message = parsedResponse['message'];
   console.log(message)
   li = document.createElement('li');
   li.innerHTML = message;
   li.setAttribute("class", "listitems");
   button = document.createElement("BUTTON");
   button.innerHTML = "Remove";
   button.setAttribute("class", "delete");
   li.appendChild(button);
   list.insertBefore(li, list.childNodes[0]);

}

// This function allows deletion of list items
function deleteItems() {

    var listitems = document.querySelectorAll(".listitems");
    for (var index = 0; index < listitems.length; index++){
        listitems[index].addEventListener("click", function(){
            this.classList.toggle("active");
        });
        listitems[index].querySelector(".delete").addEventListener("click",
        function(){
            this.closest(".listitems").remove();
        });
    }

}

function onError() {
  // Handle error here, print message perhaps
  console.log('error receiving async AJAX call');
}

// Calls the delete function every second
setInterval(deleteItems, 1000);