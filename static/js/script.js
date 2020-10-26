var cuisine=[];

$("#italian").innerHTML=cuisine;
function add_cuisine() {
        cuisine.push("italian");
       console.log(cuisine);
    }


var carbs=[];

$("#rice").innerHTML=carbs;
function add_carbs() {
        carbs.concat("rice");
       console.log(carbs);
    } 
$("#pasta").innerHTML=carbs;
function add_carbs() {
        carbs.concat("pasta");
       console.log(carbs);
    }