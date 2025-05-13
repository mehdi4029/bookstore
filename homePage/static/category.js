const menuBtn = document.getElementById('menu-btn')
const bodyFilter = document.getElementsByClassName('filter')[0]
const bar = document.getElementById('side-bar')
const showAvailableBtn = document.getElementsByClassName('button')[0]
const circleInBtn = document.getElementsByClassName('circle')[0]
const popUpErrorMessage = document.getElementsByClassName('error')[0]
const popUpSuccessMessage = document.getElementsByClassName('success')[0]
let queryString = window.location.search
let urlParams = new URLSearchParams(queryString)
let filterValue = urlParams.get('filter')
let availability = urlParams.get('availability')
let catID = location.pathname[10]
let showMenuFlag = 0 ;
let openBtnFlag = 0 ;
let availableFlag = 0;


if(availability === 'True'){
       circleInBtn.style.right = '34px'
       showAvailableBtn.style.backgroundColor = '#7D482A'
}
if(availability === 'False') {
    circleInBtn.style.right = '3px'
    showAvailableBtn.style.backgroundColor = '#c6c3c3'
}



try {
    filterElem = document.getElementById(`${filterValue}`)
    filterElem.style.borderBottom = '1px solid #4B2E1E'
}finally {
    // used try - finally for avoiding error when user sent illegal filter manually from URL
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



// the btn will get brown background after clicking
showAvailableBtn.addEventListener('click' , e=>{
    console.log(availability)
    if(availability === 'True'){
       circleInBtn.style.right = '3px'
       showAvailableBtn.style.backgroundColor = '#c6c3c3'
       location.href = `/category/${catID}?filter=${filterValue}&page=1&availability=False`
    }
    if(availability === 'False'){
       circleInBtn.style.right = '34px'
       showAvailableBtn.style.backgroundColor = '#7D482A'
       location.href = `/category/${catID}?filter=${filterValue}&page=1&availability=True`
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