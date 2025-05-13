const menuBtn = document.getElementById('menu-btn')
const firstBtnLine = document.getElementsByClassName('first')[0]
const secondBtnLine = document.getElementsByClassName('third')[0]
const bodyFilter = document.getElementsByClassName('filter')[0]
const bar = document.getElementById('side-bar')
const filtersContainer = document.getElementById('Filters')
let addToCartBook = document.getElementsByClassName('book-add-to-cart')
let temp 
addToCartBook = [...addToCartBook]

showMenuFlag = 0 ;
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
filtersContainer.addEventListener('click' , (e)=>{
     if(e.target.tagName === 'DIV'){
          temp = [...filtersContainer.children]
          temp.forEach(filter => {
              if(e.target === filter){
                  e.target.style.borderBottom = '1px solid black'
              }
              else {
                  filter.style.borderBottom = 'none'
              }
          })
     }
})
addToCartBook.forEach(bookButton => {
   bookButton.addEventListener('click' , (e)=>{
      console.log(e.target)
   })
})