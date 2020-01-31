$(function() {

    var Track = Backbone.Model.extend({
        parse: function(attrs, options) {
            // adding a url returns a list of tracks in case it's a playlist
            // for now just grab the first and usually only track
            return attrs[0] ? attrs[0] : attrs;
        },
        defaults: function() {
            return {
                id: null,
                title: null,
                artist: null,
                stream_url: null,
                page_url: null,
                order: Tracks.nextOrder(),
                playing: false
            };
        }
    });

    var TrackList = Backbone.Collection.extend({
        model: Track,
        url: '/playlist',
        modelId: function(attrs) {
            return attrs.id;
        },
        nextOrder: function() {
          if (!this.length) return 1;
          return this.last().get('order') + 1;
        },
        comparator: 'order'
    });

    var Tracks = new TrackList;

    var TrackView = Backbone.View.extend({
        tagName: 'tr',
        template: _.template($('#track-template').html()),
        events: {
            'click .delete': 'clear',
            'click .url': 'playTrack',
            'click .track': 'playTrack'
        },
        initialize: function() {
            this.listenTo(this.model, 'sync change', this.render);
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));

            this.$el.toggleClass('loading', this.isLoading());
            this.$el.toggleClass('playing', this.model.attributes.playing);

            return this;
        },
        clear: function() {
            this.model.destroy();
        },
        playTrack: function () {
            $('#playlist tr').removeClass('playing');
            Player.play(this.model);
        },
        isLoading: function() {
            return !this.model.attributes.title;
        }
    });

    var PlayerView =  Backbone.View.extend({
        el: 'audio',
        nowPlaying: null,
        events: {
            'ended': 'playNext',
            'error': 'error'
        },
        playNext: function() {
            this.nowPlaying.set('playing', false);

            nextTrack = Tracks.next(this.nowPlaying);
            this.play(nextTrack);
        },
        play: function(track) {
            this.nowPlaying = track;
            this.nowPlaying.set('playing', true);

            this.$el.attr('paused', false);
            this.$el.attr('src', 'playlist/' + track.id);

            this.$el[0].play();
        },
        error: function(e) {
            console.log('MediaError code:', e.target.error.code, 'from URL:', this.nowPlaying.attributes.page_url);

            $('#message').empty()
                .append($("<div class='alert alert-danger alert-dismissible'></div>")
                    .append($("<button class='close' type='button' data-dismiss='alert' aria-label='Close'></button>")
                        .append($("<span aria-hidden='true'>x</span>")))
                    .append($('<p>Error playing: '+this.nowPlaying.attributes.page_url+'</p>')))
        },
        pauseOrResume: function() {
            var audio = this.$el[0];
            if (audio.src !== '' && audio.paused)
                audio.play();
            else audio.pause();
        }
    });

    var Player = new PlayerView;

    var AppView = Backbone.View.extend({
        el: $('#playlistApp'),
        events: {
            'keypress #add': 'createOnEnter',
            'click #addBtn': 'createOnEnter',
            'click #deleteAll': 'clearAll'
        },
        initialize: function() {
            this.input = this.$('#add');
            this.listenTo(Tracks, 'add', this.addTrack);
            Tracks.fetch();
        },
        addTrack: function(track) {
            var view = new TrackView({model: track});
            this.$('#playlist').append(view.render().el);
        },
        createOnEnter: function(e) {
            if (e.keyCode !== undefined && e.keyCode != 13) return;
            if (!this.input.val()) return;

            Tracks.create({ page_url: this.input.val() });

            this.input.val('');
            $("html, body").animate({ scrollTop: $(document).height() }, 2000);
        },
        clearAll: function() {
            _.invoke(Tracks.models, 'destroy');
            return false;
        }
    });

    var App = new AppView;


    $(document).keyup(function (e) {
        if (e.which === 27) // esc
            $('#message').empty();
        if (e.which === 0 || e.which === 32) { // space
            Player.pauseOrResume();
        }
    });

});
