'use strict';

import './scss/bulma_custom.scss';

// The Bulma package does not come with any JavaScript.

// Here is however an implementation example, which sets the click handler
// for Bulma message delete all on the page, in vanilla JavaScript.

document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.message .message-header .delete') || []).forEach(($delete) => {
        var $message = $delete.parentNode.parentNode;

        $delete.addEventListener('click', () => {
            $message.parentNode.removeChild($message);
        });
    });
});

// Here is however an implementation example, which toggles the class is-active
// on both the navbar-burger and the targeted navbar-menu, in Vanilla Javascript.

document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {

        // Add a click event on each of them
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');

            });
        });
    }
});



document.addEventListener('DOMContentLoaded', () => {

    // Get all "expand-button" elements
    const $expandButton = Array.prototype.slice.call(document.querySelectorAll('.expand-button'), 0);

    // Check if there are any expand button
    if ($expandButton.length > 0) {

        // Add a click event on each of them
        $expandButton.forEach(el => {
            el.addEventListener('click', () => {

                // Get targets from the "data-target" attribute
                const target = el.dataset.target;
                const $targets = document.getElementsByClassName(target);

                // Toggle
                Array.prototype.forEach.call($targets, function(element) {
                    element.classList.toggle("is-hidden");
                });

                // Toggle
                el.children[0].children[0].classList.toggle('fa-angle-right');
                el.children[0].children[0].classList.toggle('fa-angle-down');

            });
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {

    // Get all "modal-button" elements
    const $modalButton = Array.prototype.slice.call(document.querySelectorAll('.modal-button'), 0);

    // Check if there are any modal button
    if ($modalButton.length > 0) {

        // Add a click event on each of them
        $modalButton.forEach(el => {
            el.addEventListener('click', () => {

                // Get targets from the "data-target" attribute
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                // Toggle the "is-active" class
                $target.classList.toggle('is-active');

            });
        });
    }
});
