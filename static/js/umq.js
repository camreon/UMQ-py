
var nowPlaying; // number of the track that's currently playing
var source;

$('#playlist tr').click(function (e) {
	nowPlaying = $(e.currentTarget).index() + 1;
	Play(CurrentTrack());
});


function Play(track) {
	var id = track.find('#id').html();
	if (id == undefined)
		console.log('track id:', id, 'is invalid');
	else {
		$.get('playlist/' + id)
			.done(function(url) {
				if (source) source.Stop();
				DetermineSource(url);
				source.LoadTrack(url);
				Highlight(track);
			})
			.fail(function() {
				console.log('url for track #'+id+' not found');
			});
	}
}

function Highlight(track) {
	$('#playlist tr').removeClass('success');
	track.addClass('success');
}

function CurrentTrack() {
	return $("#playlist tr:eq("+nowPlaying+")");
}

function NextTrack() {
	nowPlaying++;
	return CurrentTrack();
}

function DetermineSource(url)
{
	if (~url.indexOf('youtube')) source = new Youtube();
	else {
		source = new HTML5();
		// console.log('invalid audio source');
		// source = null;
	}
}
