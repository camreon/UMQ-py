import React, { Component } from 'react';
import Menu from './Components/Menu';
import Player from './Components/Player';
import Playlist from './Components/Playlist';
import { TrackProps } from './Components/Playlist/Track';
import { getPlaylist, getTrack, addTrack, deleteTrack } from './Components/Api';
import './App.css';

const DEFAULT_PLAYLIST_ID = '1';

type State = {
  playlistId: string,
  streamUrl: string,
  currentIndex: number,
  tracks: TrackProps[],
  loading: boolean
};

export default class App extends Component<{}, State> {  
  
  state: State = {
    playlistId: DEFAULT_PLAYLIST_ID,
    streamUrl: '',
    currentIndex: -1,
    tracks: [],
    loading: false
  };

  componentDidMount() {
    this.setState({
      loading: true,
      playlistId: window.location.pathname.substring(1) || DEFAULT_PLAYLIST_ID
    }, () => {
      getPlaylist(this.state.playlistId)
        .then((res) => {
          this.setState({ 
            tracks: res,
            loading: false
          })
        })
    });
  };

  addTrack = (page_url: string): void => {
    this.setState({
      loading: true,
    }, () => {
      addTrack(this.state.playlistId, page_url)
        .then((res) => {
          this.setState({
            tracks: this.state.tracks.concat(res),
            loading: false
          });
        })
    });
  };

  playTrack = (track_index: number): void => {
    this.setState({
      loading: true,
      currentIndex: track_index
    }, () => {
      let track = this.state.tracks[track_index];

      getTrack(this.state.playlistId, track.id)
        .then((res) => {
          this.setState({streamUrl: res.stream_url})
        })
        .catch((e) => {
          // TODO: this doesn;t work
          console.log(e);
        })
        .finally(() => {
          this.setState({loading: false})
        })
    });
  }

  deleteTrack = (track_id: number): void => {
    deleteTrack(this.state.playlistId, track_id)
      .then((res) => {
        this.setState({
          tracks: this.state.tracks.filter((t) => t.id !== track_id)
        });
      });
  };

  nextTrack = () => {
    const nextIndex = (this.state.currentIndex + 1) % this.state.tracks.length;
    this.playTrack(nextIndex);
  };

  prevTrack = () => {
    const prevIndex = (this.state.currentIndex - 1) > -1 
      ? this.state.currentIndex - 1
      : this.state.tracks.length - 1;

    this.playTrack(prevIndex);
  };

  render() {
    const currentTrack = this.state.tracks[this.state.currentIndex];

    return (
      <div className="container body">
        <Menu 
          onSubmit={this.addTrack}
        />
        <Playlist 
          loading={this.state.loading}
          currentIndex={this.state.currentIndex}
          tracks={this.state.tracks} 
          playTrack={this.playTrack}
          deleteTrack={this.deleteTrack}
        />
        <Player 
          handleOnNext={() => this.nextTrack()}
          handleOnPrev={() => this.prevTrack()}
          streamUrl={this.state.streamUrl}
          {...currentTrack} 
        />
      </div>
    );
  }
}
