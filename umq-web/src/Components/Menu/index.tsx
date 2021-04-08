import React, { Component } from 'react';
import './Menu.css';

type Props = {
  nextPlaylistId: string,
  onSubmit: (page_url: string) => void
}

type State = {
  input: string
}

export default class Menu extends Component<Props, State> {

  state: State = {
    input: ''
  };

  supportedSitesUrl: string = "https://github.com/rg3/youtube-dl/blob/master/docs/supportedsites.md";

  handleOnChange = (e: any) => this.setState({ input: e.target.value });

  handleOnSubmit = (e: any) => {
    e.preventDefault();
    this.props.onSubmit(this.state.input);
    this.setState({input: ''});
  };

  render() {
    const nextPlaylistUrl = `/${this.props.nextPlaylistId}`;

    return (
      <form onSubmit={this.handleOnSubmit}>
        <nav className="btn-toolbar mb-3 d-flex navbar navbar-fixed-top" role="toolbar">
          <div className="input-group mr-2 flex-grow-1" role="group">
            <div className="input-group-prepend">
              <button className="btn btn-outline-secondary" id="addBtn" type="submit">
                Add
              </button>
            </div>
            <input className="form-control" id="add" required type="url" name="url"
              placeholder="a media streaming site URL (Youtube, Bandcamp, Soundcloud, etc.)"
              value={this.state.input}
              onChange={this.handleOnChange} 
            />
          </div>

          <div className="btn-group" role="group">
            <a href={this.supportedSitesUrl} className="btn btn-outline-secondary" role="button" 
              target="_blank" rel="noreferrer" title="Supported Sites"
            >
              Supported Sites
            </a>
            <a href={nextPlaylistUrl} className="btn btn-outline-secondary" role="button" 
              id="addPlaylist" title="New Playlist"
            >
              New Playlist
            </a>
          </div>
        </nav>
      </form>
    );
  }
}
