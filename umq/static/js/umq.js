$(function() {

    createMessageBox = function(message) {
        return $('#message')
            .append($("<div class='alert alert-info alert-dismissible'></div>")
                .append($("<button class='close' type='button' data-dismiss='alert' aria-label='Close'></button>")
                    .append($("<span aria-hidden='true'>x</span>")))
                .append(message))

    }

    createErrorMessageBox = function(message) {
        return $('#message')
            .append($("<div class='alert alert-danger alert-dismissible'></div>")
                .append($("<button class='close' type='button' data-dismiss='alert' aria-label='Close'></button>")
                    .append($("<span aria-hidden='true'>x</span>")))
                .append(message))
    }

    var Track = Backbone.Model.extend({
        parse: function(attrs, options) {
            // TODO: adding a url returns a list of tracks in case it's a playlist
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
                playing: false,
                loading: false
            };
        }
    });

    Track.prototype.toString = function() {
        attributes = this.attributes;
        if (!attributes) return;

        return attributes.title + ' (' + attributes.page_url + ')';
    };

    var TrackList = Backbone.Collection.extend({
        initialize: function(models, options) {
            options = options || {id: 1};
            this.id = options.id;
        },
        model: Track,
        url: function() {
            return '/playlist/' + this.id;
        },
        sync: function(method, model, options) {
            options = options || {id: 1};
            if (options.id) this.id = options.id;

            return Backbone.Collection.prototype.sync.call(this, method, model, options);
        },
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
            'click .deleteConfirmation': 'deleteConfirmationMessage',
            'click .delete': 'delete',
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

            this.$el.toggleClass('loading', this.model.attributes.loading);
            this.$el.toggleClass('playing', this.model.attributes.playing);

            return this;
        },
        delete: function() {
            this.model.destroy({
                success: function(model, response) {
                    console.log('Deleted', model);
                    createMessageBox('Deleted: ' + model.toString());
                },
                error: function(model, xhr, options) {
                    console.log('Error deleting: ' + model.attributes.page_url);

                    createErrorMessageBox(xhr.responseJSON.message)
                }
            });
        },
        deleteConfirmationMessage: function() {
            var modal = new ConfirmationModalView({
                text: 'Are you sure you want to delete ' + this.model.toString() + '?'
            }).render();

            this.listenToOnce(modal, 'confirm', this.delete);
        },
        playTrack: function () {
            $('#playlist tr').removeClass('playing');

            this.model.set('loading', true);

            // get a fresh stream url every time the track is played
            this.model.fetch({
                success: function(track) {
                    Player.play(track);
                },
                error: function(model, xhr, options) {
                    console.log('Error playing: ' + model.attributes.page_url);

                    createErrorMessageBox(xhr.responseJSON.message)
                }
            });
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
            nextTrack.set('loading', true);

            nextTrack.fetch({
                success: function(track) {
                    Player.play(track);
                },
                error: this.error
            });
        },
        play: function(track) {
            this.nowPlaying = track;
            this.nowPlaying.set('loading', false);
            this.nowPlaying.set('playing', true);

            this.$el.attr('paused', false);
            this.$el.attr('src', track.attributes.stream_url);

            this.$el[0].play();
        },
        error: function (error) {
            errorMessage = 'Error playing: ' + this.nowPlaying.attributes.page_url

            console.log(errorMessage);

            createErrorMessageBox(errorMessage);
        },
        pauseOrResume: function() {
            var audio = this.$el[0];
            if (audio.src !== '' && audio.paused)
                audio.play();
            else audio.pause();
        }
    });

    var Player = new PlayerView;

    var Router = Backbone.Router.extend({
        routes: {
            '(:id)' : 'loadPlaylist'
        },
        loadPlaylist: function(id) {
            Tracks.fetch({id: id});
        }
    });

    var AppView = Backbone.View.extend({
        el: $('#playlistApp'),
        events: {
            'keypress #add': 'createOnEnter',
            'click #addBtn': 'createOnEnter',
            'click #addPlaylist': 'newPlaylist',
            'click #deleteAll': 'deleteAll',
            'error': 'error'
        },
        initialize: function() {
            this.input = this.$('#add');
            this.listenTo(Tracks, 'add', this.addTrack);

            this.router = new Router();

            Backbone.history.start({pushState: true});
        },
        addTrack: function(track) {
            var view = new TrackView({model: track});
            this.$('#playlist').append(view.render().el);
        },
        createOnEnter: function(e) {
            if (e.keyCode !== undefined && e.keyCode != 13) return;
            if (!this.input.val()) return;

            Tracks.create({ page_url: this.input.val() }, {
                wait: true,
                error: this.error,
                success: function() {
                    $("html, body").animate({ scrollTop: $(document).height() }, 2000);
                }
            });

            this.input.val('');
        },
        newPlaylist: function() {
            var playlist_id = new TrackList();
            
            console.log('new playlist ' + playlist_id);
        },
        deleteAll: function() {
            _.invoke(Tracks.models, 'destroy');
            return false;
        },
        error: function(model, xhr, options) {
            console.log('Error adding url:', xhr);

            createErrorMessageBox(xhr.responseJSON.message)
        },
    });

    var App = new AppView;

    var ConfirmationModalView = Backbone.View.extend({
        el: $('#message'),
        template: _.template($('#confirmation-modal-template').html()),
        events: {
            'click .confirm': 'confirm',
        },
        initialize: function (options) {
            this.options = options;
        },
        render: function() {
            this.$el.html(this.template(this.options));
            return this;
        },
        confirm: function() {
            this.trigger('confirm');
            this.remove();
        },
        remove: function() {
            // override default `remove` method to avoid deleting the `#message` container
            this.$el.empty();
            this.stopListening();
            return this;
        }
    });

    $(document).keydown(function (e) {
        if (e.which === 27) // esc
            $('#message').empty();
        if (e.which === 0 || e.which === 32) { // space
            e.preventDefault();
            Player.pauseOrResume();
        }
    });

});
