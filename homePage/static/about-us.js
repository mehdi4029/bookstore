const menuBtn = document.getElementById('menu-btn')
const popUpErrorMessage = document.getElementsByClassName('error')[0]
const popUpSuccessMessage = document.getElementsByClassName('success')[0]
const bodyFilter = document.getElementsByClassName('filter')[0]
const bar = document.getElementById('side-bar')
let showMenuFlag = 0 ;



// Create a Leaflet map
const neshanMap = new L.Map("map", {
   key: "web.2bbebaa8a7fc461da845135dcd34db96", // Get your own API Key on https://platform.neshan.org/panel
   maptype: "neshan",
   poi: true,
   traffic: true,
   center: [35.699756, 51.338076],
   zoom: 14,
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
