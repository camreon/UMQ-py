$(function() {
    $('#playlist #title, #playlist #artist').click(function(e) {
        nowPlaying = $(e.currentTarget).parent().index() + 1;
        Load(CurrentTrack());
    });

    // close alerts w/ ESC key
    $(document).keyup(function (event) {
        if (event.which === 27) {
            $('#message').empty();
        }
    });

    $('#deleteModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) ;
        var trackID = button.data('trackid');
        var title = button.data('title');
        var modal = $(this);
        modal.find('.modal-title').text('Delete ' + title + '?');
        modal.find('.modal-body #confirmDelete').attr('href', '/delete/' + trackID);
    })
});

var nowPlaying; // number of the track that's currently playing
var playlistLength = $("#playlist tr").length;
var player = new Player();

function Load(track) {
    var id = track.find('#id').attr('data-trackID');

    if (id == undefined) {
        console.log('track id:', id, 'is invalid');
    } else {
        player.Play(id);
        Highlight(track);
    }
}

function Highlight(track) {
    $('#playlist tr').removeClass('info');
    track.addClass('info');
}

function CurrentTrack() {
    return $("#playlist tr:eq("+nowPlaying+")");
}

function NextTrack() {
    nowPlaying++;
    if (nowPlaying >= playlistLength) nowPlaying = 1;
    return CurrentTrack();
}

