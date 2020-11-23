$('.view').on('click', function(){
    $('.recipe_card').removeClass('hidden') 
    $('.overview').addClass('hidden')
})

$('.close').on('click', function(){
    $('.recipe_card').addClass('hidden')
    $('.overview').removeClass('hidden')
})
