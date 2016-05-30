
function HTML5() {
    Source.apply(this, arguments);
    var audio;

    this.LoadTrack = function(audioURL) {
        audio = $('audio')[0] || document.createElement('audio');
        audio.src = audioURL;
        audio.setAttribute("controls", ""); // play/pause buttons

        if ($('audio').length === 0) {
            $('#player').prepend(audio);
            $('audio').bind("ended", Play(NextTrack())); // first load fires this event
        }
        
        audio.play();
    };

    this.Stop = function() {
        audio.pause();
        audio.currentTime = 0;
    }
};

HTML5.prototype = new Source();
