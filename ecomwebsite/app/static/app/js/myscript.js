$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// Plus Ajax code 
$('.plus-cart').click(function () {
    var id = $(this).attr("id").toString();
    var eml = this.parentNode.children[2];

    
    // console.log(id)
    $.ajax({
        type :"GET",
        url : "/pluscart",
        data: {
            prod_id:id
        },
        success: function (data) {
            // console.log(data);
            // console.log("success");
            eml.innerText = data.quantity;
            // document.getElementById("quantity").innerText = data.quantity //// this donot work on for loop
            document.getElementById("amount").innerText = data.amount
            document.getElementById("totalamount").innerText = data.totalamount

            

        }
    })
})



// Minus Ajax code 
$('.minus-cart').click(function () {
    var id = $(this).attr("id").toString();
    var eml = this.parentNode.children[2];

    
    // console.log(id)
    $.ajax({
        type :"GET",
        url : "/minuscart",
        data: {
            prod_id:id
        },
        success: function (minus_data) {
            // console.log(data);
            // console.log("success");
            eml.innerText = minus_data.quantity;
            // document.getElementById("quantity").innerText = data.quantity //// this donot work on for loop
            document.getElementById("amount").innerText = minus_data.amount
            document.getElementById("totalamount").innerText = minus_data.totalamount

            

        }
    })
})


// Remove Ajax code 
$('.remove-cart').click(function () {
    var id = $(this).attr("id").toString();
    var eml = this
    
    
    console.log(id)
    $.ajax({
        type :"GET",
        url : "/removecart",
        data: {
            prod_id:id
        },
        success: function (remove_data) {
            // console.log(data);
            console.log("success");
            // eml.innerText = minus_data.quantity;
            // document.getElementById("quantity").innerText = data.quantity //// this donot work on for loop
            document.getElementById("amount").innerText = remove_data.amount;
            document.getElementById("totalamount").innerText = remove_data.totalamount;
            eml.parentNode.parentNode.parentNode.parentNode.remove()

            

        }
    })
})