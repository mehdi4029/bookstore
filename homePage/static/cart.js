const menuBtn = document.getElementById('menu-btn')
const popUpErrorMessage = document.getElementsByClassName('error')[0]
const popUpSuccessMessage = document.getElementsByClassName('success')[0]
const booksAggregate = document.getElementById('books-aggregate')
const orderAggregate = document.getElementById('order-aggregate')
const pay = document.getElementById('goToPayment')
const addressInput = document.getElementById('send-address')
const nameInput = document.getElementById('send-username')
const phoneNumberInput = document.getElementById('send-phoneNumber')
let increaseBtns = document.getElementsByClassName('increase')
let decreaseBtns = document.getElementsByClassName('decrease')
let removeBtns = document.getElementsByClassName('remove')
const bodyFilter = document.getElementsByClassName('filter')[0]
const bar = document.getElementById('side-bar')
let showMenuFlag = 0 ;
removeBtns = [...removeBtns]
decreaseBtns = [...decreaseBtns]
increaseBtns = [...increaseBtns]


async function loadCounts(){
   response = await fetch('/cart/getCounts')
}

function getCookie(name) {
   let cookieValue = null;
   if (document.cookie && document.cookie !== '') {
       const cookies = document.cookie.split(';');
       for (let i = 0; i < cookies.length; i++) {
           const cookie = cookies[i].trim();
           if (cookie.startsWith(name + '=')) {
               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
               break;
           }
       }
   }
   return cookieValue;
}

increaseBtns.forEach(increaseBtn => {
   increaseBtn.addEventListener('click' , async (e)=>{
     count = +e.target.parentElement.dataset.count
     book = e.target.parentElement.dataset.id
     count = count + 1
     response = await fetch(`/cart/count/?id=${book}&count=${count}` , {
       method : "PUT" , 
       headers : {
          'X-CSRFToken': getCookie('csrftoken'), // Required for Django
       }
     })
     if(response.status < 400){
         data = await response.json() 
         orderAggregate.innerText = data['all_cost']
         booksAggregate.innerText = data['all_books']
         e.target.parentElement.previousElementSibling.innerText = data['item']
         e.target.parentElement.dataset.count = count
         e.target.nextElementSibling.innerText = String(count)
     }
     else {
         location.href = "/cart"
     }
})
})


decreaseBtns.forEach(decreaseBtn => {
   decreaseBtn.addEventListener('click' , async (e)=>{
     count = +e.target.parentElement.dataset.count
     book = e.target.parentElement.dataset.id
     count = count - 1
     if(count < 1){
       count = 1
     }
     response = await fetch(`/cart/count/?id=${book}&count=${count}` , {
       method : "PUT" , 
       headers : {
          'X-CSRFToken': getCookie('csrftoken'), // Required for Django
       }
     })
     if(response.status < 400){
         data = await response.json()
         orderAggregate.innerText = data['all_cost']
         booksAggregate.innerText = data['all_books']
         e.target.parentElement.previousElementSibling.innerText = data['item']
         e.target.parentElement.dataset.count = count
         e.target.previousElementSibling.innerText = String(count)
     }
})
})

removeBtns.forEach(removeBtn => {
   removeBtn.addEventListener('click' , async (e)=>{
           if(e.target.tagName === 'svg'){
               dispatcher = e.target.parentElement.parentElement
           }
           if(e.target.tagName === 'path'){
                dispatcher = e.target.parentElement.parentElement.parentElement
           }
          response = await fetch(`/cart/remove/${dispatcher.dataset.id}` , {
            method : "DELETE" , 
            headers : {
               'X-CSRFToken': getCookie('csrftoken'), // Required for Django
            }
          })
          if(response.status < 400){
            data = await response.json()
            orderAggregate.innerText = data['all_cost']
            booksAggregate.innerText = data['all_books']
            dispatcher.remove()
          }
   })
});


pay.addEventListener('click' , async e=>{
    address = addressInput.value
    username = nameInput.value
    phoneNumber = phoneNumberInput.value
    if(address == '' || username == ''){
        response = await fetch('/error/address')
        if(response.status < 400){
            location.href = '/cart'
        }
    }else {
         // Proper way to set the cookie
        const jsonData = {address, username, phoneNumber};

        // Convert to JSON and encode for cookie safety
        const cookieValue = encodeURIComponent(JSON.stringify(jsonData));

        // Set expiration to 12 minutes from now
        const expirationMins = 12;
        const date = new Date();
        date.setTime(date.getTime() + (expirationMins * 60  * 1000));

        // Set the cookie
        document.cookie = `data=${cookieValue}; expires=${date.toUTCString()}; path=/`;

         response = await fetch('/checkout/begin')
         if(response.status >= 400){
             window.location.href = "/cart"
         }
         else if(response.status < 290) {
             data = await response.json()
             path = data['paymentURL']
             location.href = path
         }
    }
})


menuBtn.addEventListener('click' , (e)=>{
    if(!showMenuFlag){
       menuBtn.classList.add('opened')
       bodyFilter.style.display = 'block'
       bodyFilter.style.visibility = 'visible'
       bodyFilter.style.opacity = '1'
       bar.style.display = 'flex'
       showMenuFlag = 1 ;
    }else {
       menuBtn.classList.remove('opened')
       bodyFilter.style.visibility = 'hidden'
       bodyFilter.style.opacity = '0'
       bar.style.display = 'none'
       showMenuFlag = 0 ;
    }
})


// displaying error message that django embeded in cookies
if(popUpErrorMessage !== undefined) {
   popUpErrorMessage.classList.add('error-active')
setTimeout(()=>{
    popUpErrorMessage.classList.remove('error-active')
},6000);
}

// displaying success message that django embeded in cookies
if(popUpSuccessMessage !== undefined) {
   popUpSuccessMessage.classList.add('success-active')
setTimeout(()=>{
    popUpSuccessMessage.classList.remove('success-active')
},6000);
}



