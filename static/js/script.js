//show and hide card overviews and recipes
$('button.view').on('click', function() {
    $(this).parent('div.overview').addClass('hidden');
    $(this).parent('div.overview').next('div.recipe_card').removeClass('hidden');
});

$('.closed').on('click', function() {
    $(this).parent('div.recipe_card').addClass('hidden');
    $(this).parent('div.recipe_card').prev('div.overview').removeClass('hidden');
});

//carousel on browse.html
$(document).ready(function() {
    $('#my-carousel').carousel({
      interval: 3000
    })
})

//show and hide error message on search page if no results
if ($('.overview').length == 0) {
    $('.error').removeClass("hidden")
    console.log("empty")
}
else{
    console.log("keep going")
}
