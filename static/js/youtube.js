
function Youtube() {
    Source.apply(this, arguments);
    var player;

    this.LoadTrack = function(audioURL) {
        if (typeof(YT) == 'undefined' || typeof(YT.Player) == 'undefined') {
            window.onYouTubeIframeAPIReady = function() { this.SetupPlayer(audioURL); };
            $.getScript('//www.youtube.com/iframe_api');
        } else {
            this.SetupPlayer(audioURL);
        }
    };

    this.SetupPlayer = function(audioURL) {
        player = new YT.Player('player', {
            playerVars: { showinfo: 0, autohide: 0, height: '50' },
            events: {
                'onReady': function(e) {
                    player.loadVideoByUrl(audioURL);
                },
                'onStateChange': function(e) {
                    if (e.data == YT.PlayerState.ENDED) { Play(NextTrack()); }
                }
            }
        });
    };

    this.Stop = function() {
        player.stopVideo();
        player.destroy();
    }
};

Youtube.prototype = new Source();
