"use strict";

function showTabContent(e) {
    // Hide All Tab Conents
    document.querySelectorAll('.tabcontent')
        .forEach(tabcontent => tabcontent.style.display = "none");
    var source = e.target || e.srcElement;
    const targetID = 'ImpactTab_' + source.attributes.value.value;
    console.log("Event ('click'): Source=", source, "; Target ID=", targetID);
    // Show the target tab
    document.getElementById(targetID).style.display = "block";
}

// Add Tab Link Event Listener
(() => document.querySelectorAll('.tablink')
    .forEach(tablink => tablink.addEventListener('click', showTabContent)))();


// ------- Hospital Breach: 'None' unchecks all others at once if they selected -------

// Add Hospital Breach 'None' Event Listener
(() => document.getElementById('XHB_N')
    .addEventListener('click', () =>
        document.querySelectorAll("input[class='checkbox_XHB']")
            .forEach(input => input.checked = false)
    ))();

// Add Hospital Breach other 'XHB' input Event Listener
(() => document.querySelectorAll("input[class='checkbox_XHB']")
    .forEach(el => el.addEventListener('click', () =>
        (document.getElementById('XHB_N').checked = false),
        // register an event handler in the capturing phase, not in the bubbling phase
        // useCapture=true  (defaul is false)
        // so, this listeners is triggered before any one in the bubbling phase (hvsscalculator10.js)
        true
    )))();

// -----------------------------------------------------------

// FIXME: until we completely remove Scope, as a workaround, automatically click the input "Scope Unchanged" (id="S_U")
document.getElementById('S_U').click();
