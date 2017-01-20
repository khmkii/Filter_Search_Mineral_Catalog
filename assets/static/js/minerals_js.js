/**
 * Created by james on 16/01/2017.
 */

$(document).ready( function () {

    const streakAnchorElems =  document.getElementsByClassName('streak__anchor');

    for (var i = 0; i < streakAnchorElems.length; i += 1) {
        streakAnchorElems[i].style.background = streakAnchorElems[i].text;
    }

});

$(document).ready( function () {
    const url = (window.location.href).split('/').pop();
    const anchorTags = document.getElementsByClassName('letter__links');
    const counter = anchorTags.length;
    for (var i = 0; i < counter; i += 1) {
        var currentAnchorTag = anchorTags[i];
        if (currentAnchorTag.text.trim() == url) {
            currentAnchorTag.style.fontWeight = 'bold';
            currentAnchorTag.style.fontSize = '14pt';
        }
    }

});