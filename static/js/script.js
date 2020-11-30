$('button.view').on('click', function() {
    $(this).parent('div.overview').addClass('hidden');
    $(this).parent('div.overview').next('div.recipe_card').removeClass('hidden');
});

$('.close').on('click', function() {
    $(this).parent('div.recipe_card').addClass('hidden');
    $(this).parent('div.recipe_card').prev('div.overview').removeClass('hidden');
});

