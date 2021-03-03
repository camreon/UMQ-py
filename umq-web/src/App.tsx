import React, { Component } from 'react';
import Menu from './Components/Menu';
import Player from './Components/Player';
import Playlist from './Components/Playlist';
import { TrackProps } from './Components/Playlist/Track';
import { getTrack } from './Api';
import './App.css';

type State = {
  playlistId: string,
  currentlyPlayingTrack: TrackProps | null
};

const DEFAULT_PLAYLIST_ID = '1';

export default class App extends Component<{}, State> {  
  
  state: State = {
    playlistId: DEFAULT_PLAYLIST_ID,
    currentlyPlayingTrack: null
  };

  componentDidMount() {
    this.setState({
      playlistId: window.location.pathname.substring(1) || DEFAULT_PLAYLIST_ID,
    });
  };

  addTrack(e: any) {
    console.log(e);
  };

  playTrack = (track: TrackProps): void => {
    getTrack(this.state.playlistId, track.id)
      .then((res) => {
        this.setState({ currentlyPlayingTrack: res })
      });
  }

  render() {
    return (
      <div className="container body">
        <Menu 
          onSubmit={this.addTrack} 
        />
        <Playlist 
          playlistId={this.state.playlistId} 
          playTrack={this.playTrack}
        />
        <Player {...this.state.currentlyPlayingTrack} />
      </div>
    );
  }
}
