$(function() {
    $('#playlist #title, #playlist #artist').click(function(e) {
        nowPlaying = $(e.currentTarget).parent().index() + 1;
        Load(CurrentTrack());
    });

    $(document).keyup(function (e) {
        if (e.which === 27) // esc
            $('#message').empty();
        if (e.which === 0 || e.which === 32) // space
            player.PauseOrResume();
    }).on('keyup', '#deleteModal', function(e) {
        if (e.which === 13) // enter
            $('#confirmDelete').submit();
    });

    $('#deleteModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) ;
        var trackID = button.data('trackid');
        var title = button.data('title');
        if (title === undefined) title = 'all tracks';
        if (trackID === undefined) trackID = '';

        $(this).find('.modal-title').text('Are you sure you want to delete ' + title + '?');
        $(this).find('.modal-body #confirmDelete').attr('action', '/delete/'+trackID);
    })
});

var nowPlaying; // index of the current track
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

