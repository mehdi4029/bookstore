let form = document.getElementsByTagName('form')
let submitBtn = document.getElementsByClassName('submit-btn')[0]
let inputs = document.getElementsByTagName('input')
let popUpErrorMessage = document.getElementsByClassName('error')[0]
form = form[0]
// input[0] is a hidden input for csrf_token , the form data is stored in 1 and above indexes
inputs = [...inputs]

console.log(popUpErrorMessage)
if(popUpErrorMessage !== undefined) {
     popUpErrorMessage.classList.add('error-active')
setTimeout(()=>{
      popUpErrorMessage.classList.remove('error-active')
},2000);
}


let login = async obj => {
     let response = await fetch('/auth/api/login', {
          method : 'POST' ,
          headers: {
               "Content-Type" : "application/json" ,
          } ,
          body : JSON.stringify(obj)
     })
     let data = await response.json()
}


let register = async obj => {
     let response = await fetch('/auth/api/register' , {
          method : 'POST' ,
          headers : {
               "Content-Type" : "application/json" ,
          } ,
          body : JSON.stringify(obj)
     })
     let data = await response.json()
     location.href = "/"
}


let obj ;
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
})


