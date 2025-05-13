const menuBtn = document.getElementById('menu-btn')
const popUpErrorMessage = document.getElementsByClassName('error')[0]
const popUpSuccessMessage = document.getElementsByClassName('success')[0]
const booksAggregate = document.getElementById('books-aggregate')
const orderAggregate = document.getElementById('order-aggregate')
const pay = document.getElementById('goToPayment')
const addressInput = document.getElementById('send-address')
const nameInput = document.getElementById('send-username')
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
     console.log(count)
     console.log(e.target.nextElementSibling)
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
     console.log(count)
     console.log(e.target.previousElementSibling)
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
    if(address == ' ' || username == ''){
        response = await fetch('/error/address')
        if(response.status < 400){
            location.href = '/cart'
        }
    }else {
         response = await fetch('/order/create' , {
            method : 'POST' , 
            headers : {
                "Content-Type" : "application/json" ,
                'X-CSRFToken': getCookie('csrftoken'), // Required for Django
            } ,
            body : JSON.stringify({
                'address' : address , 
                'username' : username
            })
         })
         if(response.status < 400){
             data = await response.json()
             console.log(data)
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
},2000);
}

// displaying success message that django embeded in cookies
if(popUpSuccessMessage !== undefined) {
   popUpSuccessMessage.classList.add('success-active')
setTimeout(()=>{
    popUpSuccessMessage.classList.remove('success-active')
},2000);
}



