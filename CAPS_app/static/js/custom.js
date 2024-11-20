

jQuery(document).ready(function ($) {
    "use strict";
   

    // C-Slider
    if ($(".c-slider")[0]){
        $('.c-slider.owl-carousel').owlCarousel({
            loop: true,
            items:1,
            dots: false,
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: false,
            nav:true,
            navText: ["<i class='fa-solid fa-arrow-left-long'></i>","<i class='fa-solid fa-arrow-right-long'></i>"],
            responsive:{
                0:{
                    nav: false,
                },
                768:{
                    nav: true
                }
            }
        });
    }

    // Blog-Slider
    if ($(".blog-slider")[0]){
        $('.blog-slider.owl-carousel').owlCarousel({
            items:3,
            center: true,
            loop: true,
            margin:12,
            dots:true,
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: false,
            responsive:{
                0:{
                    items:1
                },
                768:{
                    center: false,
                    items:2
                },
                1000:{
                    items:3
                }
            }
        });
    }


    
    // Featured Slider Two
    if ($(".f-2-slider")[0]){
        $('.f-2-slider.owl-carousel').owlCarousel({
            items:1,
            loop: true,
            nav:true,
            navText: ["<i class='fa-solid fa-arrow-left'></i>","<i class='fa-solid fa-arrow-right'></i>"],
            dots: false,
            touchDrag  : false,
            mouseDrag  : false,
            margin: 10,
            navContainer: '.f-2-s-nav',
        });
    }


  


  
    // What we build
    $(".wwb-ul li").hover(function(){
      $(".wwb-ul li").removeClass("active");
      $(this).addClass("active");
    });

    $('.mobile-nav .menu-item-has-children').on('click', function(event) {
      $(this).toggleClass('active');
      event.stopPropagation();
    }); 

    $('#mobile-menu').click(function(){
        $(this).toggleClass('open');
        $('#mobile-nav').toggleClass('open');
    });

    $('#desktop-menu').click(function(){
        $(this).toggleClass('open');
        $('.desktop-menu').toggleClass('open');
    });

    $('#res-cross').click(function(){
        $('#mobile-nav').removeClass('open');
        $('#mobile-menu').removeClass('open')
    });


    



    // Sticky Header
    var new_scroll_position = 0;

        var last_scroll_position;

        var header = document.getElementById("stickyHeader");



        window.addEventListener('scroll', function(e) {

        last_scroll_position = window.scrollY;



        // Scrolling down

        if (new_scroll_position < last_scroll_position && last_scroll_position > 100) {

          // header.removeClass('slideDown').addClass('slideUp');

          header.classList.remove("slideDown");

          header.classList.add("slideUp");



        // Scroll top

        } 

        else if (last_scroll_position < 100) {

          header.classList.remove("slideDown");

        } 

        else if (new_scroll_position > last_scroll_position) {

          header.classList.remove("slideUp");

          header.classList.add("slideDown");

        }



          new_scroll_position = last_scroll_position;

        });

});


// theme-icon/moon
let lightmode = localStorage.getItem('light-d');
    const lightmodeToggle = document.querySelector('#theme-icon');
    const enableLightMode = () => {
        document.body.classList.add('light-d');
        localStorage.setItem('light-d', 'enabled');
        lightmodeToggle.src = 'assets/images/moon.png';
    }
    
    const disablelightmode = () => {
        document.body.classList.remove('light-d');
        localStorage.setItem('light-d', null);
        lightmodeToggle.src = 'assets/images/sun.png';
    }

    if (lightmode === 'enabled') {
        enableLightMode();
    }

    lightmodeToggle.addEventListener('click', () => {
        lightmode = localStorage.getItem('light-d'); 

        if (lightmode !== 'enabled') {
            enableLightMode();
        } else {  
            disablelightmode();
        }
    });


    // Preloader
$(window).on('load', function () {
    $("body").addClass("page-loaded");
    
});