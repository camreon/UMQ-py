
function Player() {

    var audio;

    this.Play = function(id) {
        self = this;
        audio = $('audio')[0];

        if (audio.src === '') {
            $('audio').bind('error', function(e) {
                self.Error(e);
            });
            $('audio').bind('ended', function() {
                Load(NextTrack());
            });
        }
        audio.setAttribute('controls', '');
        audio.setAttribute('autoplay', '');
        audio.src = 'playlist/'+id;
    }

    this.PauseOrResume = function() {
        if (audio === undefined) return;
        if (audio.paused)
            audio.play();
        else
            audio.pause();
    }

    this.Stop = function() {
        audio.pause();
        audio.currentTime = 0;
    }

    this.Error = function(e) {
        console.log('MediaError code:', e.target.error.code, 'from URL:', e.target.src);

        $('#message').empty()
            .append($("<div class='alert alert-danger alert-dismissible'></div>")
                .append($("<button class='close' type='button' data-dismiss='alert' aria-label='Close'></button>")
                    .append($("<span aria-hidden='true'>x</span>"))
                )
                .append($('<p>Error playing: '+e.target.src+'</p>'))
            )
    }
}
