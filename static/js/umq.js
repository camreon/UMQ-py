$(function() {

    var Track = Backbone.Model.extend({
        parse: function(attrs) {
            attrs.id = (attrs._id === undefined) ? null : attrs._id.$oid;
            return attrs;
        },
        defaults: function() {
            return {
                title: null,
                artist: null,
                url: 'n/a',
                page_url: null,
                order: Tracks.nextOrder()
            };
        }
    });

    var TrackList = Backbone.Collection.extend({
        model: Track,
        url: '/playlist',
        modelId: function(attrs) {
            // null id for new models b/c mongodb will create it
            return (attrs._id === undefined) ? null : attrs._id.$oid;
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
            'click': 'playTrack'
        },
        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        clear: function() {
            this.model.destroy();
        },
        playTrack: function () {
            $('#playlist tr').removeClass('playing');
            this.$el.toggleClass('playing');
            Player.play(this.model);
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
            nextTrack = Tracks.next(this.nowPlaying);
            this.play(nextTrack);
        },
        play: function(track) {
            this.nowPlaying = track;
            this.$el.attr('paused', false);
            this.$el.attr('src', 'playlist/' + track.id);
        },
        error: function(e) {
            console.log('MediaError code:', e.target.error.code, 'from URL:', e.target.src);
            $('#message').empty()
                .append($("<div class='alert alert-danger alert-dismissible'></div>")
                    .append($("<button class='close' type='button' data-dismiss='alert' aria-label='Close'></button>")
                        .append($("<span aria-hidden='true'>x</span>")))
                    .append($('<p>Error playing: '+e.target.src+'</p>')))
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
            Tracks.create({url: this.input.val()});
            this.input.val('');
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
