import React, { Component } from 'react';

export default class Menu extends Component {
  
  render() {
    return (
      <nav className="add-url-input navbar-fixed-top input-group ">
        <span className="input-group-btn">
          <button className="btn btn-default" id="addBtn" type="submit">Add</button>
        </span>
        
        <input className="form-control" id="add" required type="url" name="url"
               placeholder="audio/video streaming site URL (i.e. youtube, bandcamp, soundcloud)" />
        
        <span className="input-group-btn">  
          <button className="btn btn-default" type="button" aria-label="Supported Sites">
            <a href="https://github.com/rg3/youtube-dl/blob/master/docs/supportedsites.md" 
               target="_blank" rel="noreferrer" title="Supported Sites" 
               className="glyphicon glyphicon-th-list" aria-hidden="true">
            </a>
          </button>
          <button className="btn btn-default" type="button" 
                  aria-label="New Playlist" id="addPlaylist">
            <a href="/newplaylist" title="New Playlist">
              <span className="glyphicon glyphicon-plus" aria-hidden='true'></span>
            </a>
          </button>
        </span>
      </nav>
    )
  }
}
