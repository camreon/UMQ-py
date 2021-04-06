import React, { Component } from 'react';
import { TrackProps } from '../Playlist/Track';
import './Player.css';

type Props = {
  streamUrl: string,
  handleOnNext: () => void,
  handleOnPrev: () => void
}

export default class Player extends Component<TrackProps & Props> {
  
  public static defaultProps = {
    id: null,
    title: '',
    artist: '',
    page_url: ''
  };

  render() {
    return (
      <nav className="navbar navbar-default fixed-bottom">
        <div className="container" id="player">
              
          <audio 
            autoPlay 
            controls 
            controlsList="nodownload"
            src={this.props.streamUrl}
            onEnded={this.props.handleOnNext}
          ></audio>
          
          <div className="controls">
            <button 
              className="btn fa fa-step-backward" id="playPrev" aria-hidden="true" title="Play Previous"
              onClick={this.props.handleOnPrev}
            ></button>
            <button 
              className="btn fa fa-step-forward" id="playNext" aria-hidden="true" title="Play Next"
              onClick={this.props.handleOnNext}
            ></button>
          </div>
          
        </div>
      </nav>
    )
  }
}
