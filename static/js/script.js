//show and hide card overview and recipe cards
$("button.view").on("click", function () {
    $(".overview").addClass("hidden");
    $(this).parent("div.overview").next("div.recipe_card").removeClass("hidden");
});

$(".closed").on("click", function () {
    $(this).parent("div.recipe_card").addClass("hidden");
    $(".overview").removeClass("hidden");
});

//carousel on browse.html
$(document).ready(function () {
    $(".carousel").carousel({
        interval: 3000,
    });
});

//show and hide error message on search page if no results
if ($(".overview").length == 0) {
    $(".error").removeClass("hidden");
}

// close flash message
$(document).ready(function () {
    $("#successMessage").remove(), 15000;
});
