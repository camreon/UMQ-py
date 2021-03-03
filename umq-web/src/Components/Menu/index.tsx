import React, { Component } from 'react';
import './Menu.css';

type Props = {
  onSubmit: (e: any) => void
}

type State = {
  input: string
}

export default class Menu extends Component<Props, State> {

  state: State = {
    input: ''
  };

  handleOnChange = (e: any) => this.setState({ input: e.target.value });

  handleOnSubmit = (e: any) => this.props.onSubmit(e.target.value);

  render() {
    return (
      <form onSubmit={this.handleOnSubmit}>
        <nav className="add-url-input navbar-fixed-top input-group ">
          <span className="input-group-btn">
            <button className="btn btn-default" id="addBtn" type="submit">Add</button>
          </span>
          
          <input className="form-control" id="add" required type="url" name="url"
                placeholder="audio/video streaming site URL (i.e. youtube, bandcamp, soundcloud)"
                value={this.state.input}
                onChange={this.handleOnChange} />
        
        <span className="input-group-btn">  
          <button className="btn btn-default" type="button" aria-label="Supported Sites">
            <a href="https://github.com/rg3/youtube-dl/blob/master/docs/supportedsites.md" 
               target="_blank" rel="noreferrer" title="Supported Sites" 
               className="fa fa-th-list" aria-hidden="true">
            </a>
          </button>
          <button className="btn btn-default" type="button" 
                  aria-label="New Playlist" id="addPlaylist">
            <a href="/newplaylist" title="New Playlist">
              <span className="fa fa-plus" aria-hidden='true'></span>
            </a>
          </button>
        </span>
      </nav>
    </form>
    )
  }
}
