const menuBtn = document.getElementById('menu-btn')
const firstBtnLine = document.getElementsByClassName('first')[0]
const secondBtnLine = document.getElementsByClassName('third')[0]
const bodyFilter = document.getElementsByClassName('filter')[0]
const bar = document.getElementById('side-bar')
let booksContainer = document.getElementById('BooksContainer')
const filtersContainer = document.getElementById('Filters')
let addToCartBook = document.getElementsByClassName('book-add-to-cart')
const searchInput = document.getElementById('searchInput')
let searchResult = document.getElementById('result')
let popUpErrorMessage = document.getElementsByClassName('error')[0]
let popUpSuccessMessage = document.getElementsByClassName('success')[0]
let viewCategoriesBtn = document.getElementById('view-categories')
let categoriesBox = document.getElementById('categoriesContainer')
let temp ; let key ; let value ; let fragment
addToCartBook = [...addToCartBook]
temp = [...filtersContainer.children]


// smooth scroll
viewCategoriesBtn.addEventListener('click' , e =>{
    console.log('hello')
    categoriesBox.scrollIntoView({
        behavior : "smooth" ,
        block : 'center'
    })
})



function createFiltersFragment(data) {
    let str = '' ; let key
    for(book of data){
           str += `
                   <article href="" class="book">
                       <a href="/fav/add/${book['id']}" class="favourite">
                                   <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path fill-rule="evenodd" clip-rule="evenodd" d="M3.80638 6.20635C4.70651 5.30649 5.92719 4.80097 7.19998 4.80097C8.47276 4.80097 9.69344 5.30649 10.5936 6.20635L12 7.61155L13.4064 6.20635C13.8492 5.7479 14.3788 5.38223 14.9644 5.13066C15.5501 4.8791 16.1799 4.74669 16.8172 4.74115C17.4546 4.73561 18.0866 4.85706 18.6766 5.09841C19.2665 5.33975 19.8024 5.69617 20.2531 6.14685C20.7038 6.59754 21.0602 7.13347 21.3015 7.72337C21.5429 8.31327 21.6643 8.94533 21.6588 9.58268C21.6532 10.22 21.5208 10.8499 21.2693 11.4355C21.0177 12.0211 20.652 12.5508 20.1936 12.9935L12 21.1883L3.80638 12.9935C2.90651 12.0934 2.401 10.8727 2.401 9.59995C2.401 8.32716 2.90651 7.10648 3.80638 6.20635V6.20635Z" stroke="#EC1818" stroke-width="2" stroke-linejoin="round"/>
                                   </svg>
                       </a>
                       <section class="book-image"><a href="/book/${book['id']}"><img src="${book['image-url']}" alt=""></a></section>
                       <section class="book-details">
                              <p>${book['name']}</p>
                              <p>${book['author']}</p>
                              <p>${book['price']}</p>
                       </section>
                       <section class="book-add-to-cart">
                         <a href="/cart/add/${book['id']}">افزودن به سبد خرید</a>
                       </section>
                   </article>
           `
    }
    return str
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



searchInput.addEventListener('keyup' , async e=>{
       if(searchInput.value !== '') {
           fragment = ''
           response = await fetch('/search/', {
               method: 'POST',
               headers: {
                   'X-CSRFToken': getCookie('csrftoken'), // Required for Django
               },
               body: JSON.stringify({'inputValue': searchInput.value})
           })
           data = await response.json()
           for (key in data) {
               fragment +=
                   `
                           <div class="result-container">
                                 <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                                     <path stroke-linecap="round" stroke-linejoin="round" d="m18.75 4.5-7.5 7.5 7.5 7.5m-6-15L5.25 12l7.5 7.5" />
                                 </svg>
                                <a href=\"book\\${key}\" class="search-result">${data[key]['name']}-${data[key]['author']}</a>
                             </div>
                         `
           }
           searchResult.innerHTML = fragment
           searchResult.style.display = 'flex'
       } else {
           searchResult.style.display = 'none'
       }
})

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

filtersContainer.addEventListener('click' , async (e)=>{
     if(e.target.tagName === 'DIV'){
          temp.forEach(filter => {
              if(e.target === filter){
                  e.target.style.borderBottom = '1px solid black'
              }
              else {
                  filter.style.borderBottom = 'none'
              }
          })
          let response = await fetch(`/getbook/${e.target.id}`)
          let data = await response.json()
          booksContainer.innerHTML = createFiltersFragment(data)
     }
})

addToCartBook.forEach(bookButton => {
   bookButton.addEventListener('click' , (e)=>{
      console.log(e.target)
   })
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