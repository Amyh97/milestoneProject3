$('button.view').on('click', function() {
    $(this).parent('div.overview').addClass('hidden');
    $(this).parent('div.overview').next('div.recipe_card').removeClass('hidden');
});

$('.closed').on('click', function() {
    $(this).parent('div.recipe_card').addClass('hidden');
    $(this).parent('div.recipe_card').prev('div.overview').removeClass('hidden');
});

$(document).ready(function() {
    $('#my-carousel').carousel({
      interval: 2000
    })
})