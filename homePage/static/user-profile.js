const menuBtn = document.getElementById('menu-btn')
const popUpErrorMessage = document.getElementsByClassName('error')[0]
const popUpSuccessMessage = document.getElementsByClassName('success')[0]
let phoneNumberContainer = document.getElementById('mobile-phone')
const bar = document.getElementById('side-bar')
const bodyFilter = document.getElementsByClassName('filter')[0]
let showMenuFlag = 0 ;


function firstZeroChecker(e){
          if(e.target.value==='0'){
               e.target.value = ''
          removeEventListener('input' , firstZeroChecker)
     }
}


try {phoneNumberContainer.lastElementChild.addEventListener('input' , firstZeroChecker)} catch{}


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


function firstZeroChecker(e){
   if(e.target.value==='0'){
        e.target.value = ''
   removeEventListener('input' , firstZeroChecker)
}
}



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