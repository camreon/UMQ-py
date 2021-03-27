import React, { Component } from 'react';
import { Track, TrackProps } from './Track';
import './Playlist.css';

type Props = {
  loading: boolean,
  nowPlayingId: number | undefined, 
  tracks: TrackProps[],
  playTrack: (track: TrackProps) => void,
  deleteTrack: (track_id: number) => void
}

export default class Playlist extends Component<Props> {

  render() {
    const loadingIcon = this.props.loading && (
      <div className="loading-icon-container">
        <span className="fa fa-spinner fa-spin" />
      </div>
    );

    return (
      <div className="table-responsive">
        <table className="table table-hover">
          <thead>
          <tr>
            <th className="row-index">{loadingIcon}</th>
            <th className="row-track">TRACK</th>
            <th className="row-source">SOURCE</th>
            <th className="row-delete"></th>
          </tr>
          </thead>
          <tbody id="playlist">
            {this.props.tracks.map((track, index) =>
              <Track 
                key={track.id}
                isLoading={this.props.loading}
                isPlaying={this.props.nowPlayingId === track.id}
                number={index + 1}
                handleOnClick={() => this.props.playTrack(track)}
                handleOnDelete={() => this.props.deleteTrack(track.id)}
                {...track} 
              />
            )}
          </tbody>
        </table>

        {!this.props.tracks.length && (
          <p>No tracks found</p>
        )}
      </div>
    )
  }
}
