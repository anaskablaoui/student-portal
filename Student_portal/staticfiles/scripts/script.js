const container = document.querySelector('.container');
const profButn= document.querySelector('.professeur-btn');
const etuBtx = document.querySelector('.etudiant-btn');

profButn.addEventListener('click',()=>{
    container.classList.add('active');
})

etuBtx.addEventListener('click',()=>
{
    container.classList.remove('active')
})