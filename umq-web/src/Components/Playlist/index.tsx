import React, { Component } from 'react';
import { Track, TrackProps } from './Track';
import { getPlaylist } from './../../Api';
import './Playlist.css';

type Props = {
  playlistId: string,
  playTrack: (track: TrackProps) => void
}

type State = {
  playlist: TrackProps[],
  loading: boolean
};

export default class Playlist extends Component<Props, State> {

  state: State = {
    playlist: [],
    loading: false
  };

  componentDidMount() {
    this.setState({
      loading: true
    }, () => {
      getPlaylist(this.props.playlistId)
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
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
          <tr>
            <th className="row-track">TRACK</th>
            <th className="row-source">SOURCE</th>
            <th className="row-delete"></th>
          </tr>
          </thead>
          <tbody id="playlist">
            {this.state.playlist.map((track) =>
              <Track 
                key={track.id} 
                handleOnClick={() => this.props.playTrack(track)}
                {...track} 
              />
            )}
          </tbody>
        </table>
        
        {this.state.loading && (
          <div className="loading-icon-container">
            <span className="fa fa-spinner fa-spin" />
          </div>
        )}
      </div>
    )
  }
}
