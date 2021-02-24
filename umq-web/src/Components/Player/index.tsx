import React, { Component } from 'react';

export default class Player extends Component {
  
  render() {
    return (
      <header className="App-header">
        <nav className="navbar navbar-default navbar-fixed-bottom">
          <div className="container" id="player">
                
            <audio controls autoPlay controlsList="nodownload"></audio>
            
            <div className="controls">
              <button className="glyphicon glyphicon-step-backward" id="playPrev" aria-hidden="true" title="Play Previous"></button>
              <button className="glyphicon glyphicon-step-forward" id="playNext" aria-hidden="true" title="Play Next"></button>
            </div>
            
          </div>
        </nav>
      </header>
    )
  }
}
