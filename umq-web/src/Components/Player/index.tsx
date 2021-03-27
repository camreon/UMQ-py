import React, { Component } from 'react';
import { TrackProps } from '../Playlist/Track';
import './Player.css';

export default class Player extends Component<TrackProps> {
  
  public static defaultProps = {
    id: null,
    title: '',
    artist: '',
    page_url: '',
    stream_url: '',
  };

  render() {
    return (
      <nav className="navbar navbar-default fixed-bottom">
        <div className="container" id="player">
              
          <audio 
            autoPlay 
            controls 
            controlsList="nodownload"
            src={this.props.stream_url} 
          ></audio>
          
          <div className="controls">
            <button className="btn fa fa-step-backward" id="playPrev" aria-hidden="true" title="Play Previous"></button>
            <button className="btn fa fa-step-forward" id="playNext" aria-hidden="true" title="Play Next"></button>
          </div>
          
        </div>
      </nav>
    )
  }
}
