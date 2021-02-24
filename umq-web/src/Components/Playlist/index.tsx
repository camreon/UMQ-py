import React, { Component } from 'react';
import { Track, TrackProps } from './Track';

type Props = {
  playlist: TrackProps[]
}

export default class Playlist extends Component<Props> {

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
            {this.props.playlist.map((track) =>
              <Track key={track.id} {...track} />
            )}
          </tbody>
        </table>
      </div>
    )
  }
}
