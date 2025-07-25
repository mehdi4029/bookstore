const menuBtn = document.getElementById('menu-btn')
const bodyFilter = document.getElementsByClassName('filter')[0]
const bar = document.getElementById('side-bar')
let popUpErrorMessage = document.getElementsByClassName('error')[0]
let popUpSuccessMessage = document.getElementsByClassName('success')[0]
let showMenuFlag = 0 ;

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