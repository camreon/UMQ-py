import logo from './logo.svg';
import React, { Component } from 'react';
import Menu from './Components/Menu';
import Playlist from './Components/Playlist';
import Player from './Components/Player';
import { TrackProps } from './Components/Playlist/Track';
import { getPlaylist } from './Api';
import './App.css';

type State = {
  playlistId: string,
  playlist: TrackProps[],
  loading: boolean
};

export default class App extends Component<{}, State> {  
  state: State = {
    playlistId: '',
    playlist: [],
    loading: false
  };

  componentDidMount() {
    this.setState({
      playlistId: window.location.pathname.substring(1),
      loading: true
    }, () => {
      getPlaylist(this.state.playlistId)
        .then((res) => {
          this.setState({ 
            playlist: res,
            loading: false
          })
        })
    });
  };

  render() {
    return (
      <div className="App">
        <div className="container body" id="playlistApp">
          <Menu />
          <Playlist playlist={this.state.playlist} />
          {this.state.loading && (
            <img src={logo} className="App-logo" alt="logo" />
          )}
        </div>
        <Player />
      </div>
    );
  }
}
