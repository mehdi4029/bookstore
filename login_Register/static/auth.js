let form = document.getElementsByTagName('form')
let submitBtn = document.getElementsByClassName('submit-btn')[0]
let inputs = document.getElementsByTagName('input')
let phoneNumberContainer = document.getElementById('mobile-phone')
let popUpErrorMessage = document.getElementsByClassName('error')[0]
let popUpSuccessMessage = document.getElementsByClassName('success')[0]
let validationCheckSubmit = document.getElementById('submit-arrow')
form = form[0]
let obj ;
let blurFilter = document.getElementById('filter')
let loader = document.getElementsByClassName('loader')[0]

url_params = new URLSearchParams(window.location.search)
searchParam = url_params.get('next')


// input[0] is a hidden input for csrf_token , the form data is stored in 1 and above indexes
inputs = [...inputs]


// ------------------------------------------------------------ functions ---------------------------------------
function loadingAnimation(){
      loader.style.display = 'block'
      filter.style.display = 'block'
      setTimeout((e)=>{
           loader.style.display = 'none'
           filter.style.display = 'none'
      },5000)
}





// ------------------------------------------------ callback functions ----------------------------------

// make sure that phoneNumber don't have any zero at beginning --- callback function
function firstZeroChecker(e){
          if(e.target.value==='0'){
               e.target.value = ''
          removeEventListener('input' , firstZeroChecker)
     }
}

let login = async obj => {
     try {
          let response = await fetch('/auth/api/login', {
               method: 'POST',
               headers: {
                    "Content-Type": "application/json",
               },
               body: JSON.stringify(obj)
          })
          let data = await response.json()
          if(response.status === 200){
               location.href = '/auth/retrieveCodeValidation?next=/'
          } else if(response.status === 400){
               location.href = '/auth/login'
          }
     }
     catch{}
}

let register = async obj => {
     try {
          loadingAnimation()
          let response = await fetch('/auth/api/register', {
               method: 'POST',
               headers: {
                    "Content-Type": "application/json",
               },
               body: JSON.stringify(obj)
          })

          // if an error raise in backend , no validate data will be sent , so the catch block will execute
          // for showing messages from cookies

          let data = await response.json()
          location.href = '/auth/retrieveCodeValidation?next=/'
     }
     catch{
          location.href = "/auth/register"
     }
}

let validationCheckTimer = ()=>{
     try {
          if (document.getElementById('retrieveCodeValidationBtn')) {
               let zeroForSec;
               let x
               let seconds = 120;
               let btn = document.getElementById('retrieveCodeValidationBtn')
               let interval = setInterval(() => {
                    seconds -= 1
                    if (seconds === 0) {
                         btn.innerText = 'ارسال دوباره کد تایید'
                         btn.addEventListener('click', (e) => {
                              location.href = `/auth/retrieveCodeValidation?next=${searchParam}`
                         })
                         clearInterval(interval)
                    } else {
                         x = seconds % 60
                         if (x < 10) {
                              zeroForSec = '0'
                         } else {
                              zeroForSec = ''
                         }
                         btn.innerText = `${zeroForSec + x} : ${Math.floor(seconds / 60)} `
                    }
               }, 1000)
          }
     } catch{
     }
}

let retrieve = async obj => {
     try {
          loadingAnimation()
          let response = await fetch('/auth/api/retrieve', {
               method : 'POST' ,
               headers: {
                    "Content-Type": "application/json",
               },
               body: JSON.stringify(obj)
          })
          if(response.status === 500 || response.status === 404){
               throw new Error('invalid request')
          }
          location.href = '/auth/retrieveCodeValidation?next=/auth/makeNewPassword'
     }
     catch{
          location.href = '/auth/retrievePass'
     }
}

let checkTheCode = async searchParam => {
     try{
          loadingAnimation()
          let response = await fetch(`/auth/api/checkValidationCode?next=${searchParam}`, {
               method : 'POST' ,
               headers: {
                    "Content-Type": "application/json",
               },
               body: JSON.stringify({'validation' : inputs[1].value})
          })
          if(response.status === 500 || response.status === 404){
               throw new Error('invalid request')
          }
          console.log(response)
          let data = await response.json()
          console.log(data)
          location.href = data['path']
     }
     catch{
          location.href = `/auth/login`
     }
}

let submitPasswd = async obj => {
     try {
          loadingAnimation()
          let response = await fetch('/auth/api/submitPassword', {
               method: 'POST',
               headers: {
                    "Content-Type": "application/json",
               },
               body: JSON.stringify(obj)
          })
          if (response.status === 500 || response.status === 404) {
               throw new Error('invalid request')
          }
          let data = await response.json()
          location.href = '/auth/login'
     }
     catch{
          location.href = '/auth/retrievePass'
     }
}

// --------------------------------------------- logic ---------------------------------------------

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





// ----------------------------------------------- event listeners ------------------------------------

// 1
window.addEventListener('load', validationCheckTimer)

// 2
window.addEventListener('beforeunload' , (e)=>{
     loadingAnimation()
})

// 3
try {phoneNumberContainer.lastElementChild.addEventListener('input' , firstZeroChecker)} catch{}


// 4
submitBtn.addEventListener('click' , (e)=>{
      if(form.id === 'login'){
           obj = {
                'uniqueMail' : inputs[1].value ,
                'phoneNumber' : inputs[2].value ,
                'password' : inputs[3].value,
           }
           login(obj)
      }
      if(form.id === 'register'){
           obj = {
                'username' : inputs[1].value ,
                'uniqueMail' : inputs[2].value ,
                'phoneNumber' : inputs[3].value ,
                'password' : inputs[4].value
           }
           register(obj)
      }
      if(form.id === 'retrieve'){
           obj = {
                'phoneNumber' : inputs[1].value ,
                'uniqueMail' : inputs[2].value ,
           }
           retrieve(obj)
      }
      if(form.id === 'makeNewPassword'){
           obj = {
                'password' : inputs[1].value
           }
           submitPasswd(obj)
      }
})

5
try{
validationCheckSubmit.addEventListener('click' , (e)=>{
     checkTheCode(searchParam)
})} catch{}






