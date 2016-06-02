
function Player() {

    var audio;
    var nextTrackID;

    this.Load = function(url) {
        self = this;
        if ($('audio').length === 0) {
            audio = $(document.createElement('audio'));
            audio.bind('error', function(e) {
                self.Error(e);
            });
            audio.bind('ended', function() {
                Load(NextTrack());
            });
            $('#player').prepend(audio);
        }

        audio = $('audio')[0];
        audio.setAttribute("controls", "");
        audio.src = url;
        audio.play();
    };

    this.Play = function(id) {
        var self = this;
        $.get('playlist/' + id)
            .done(function(url) {
                self.Load(url);
            })
            .fail(function() {
                console.error('url for track #'+id+' not found');
            });
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
                .append($("<p>Error playing: " + e.target.src + "</p>"))
            )
    }
}
