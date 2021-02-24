import React, { Component } from 'react';
import './Track.css';

export type TrackProps = {
  id: number,
  title: string,
  artist?: string,
  page_url: string,
  stream_url: string,
}

export class Track extends Component<TrackProps> {

  render() {
    return (
      <tr>
        <td className="track">
          <div className="track-title" title={this.props.title}>{this.props.title}</div>
          <div className="track-artist" title={this.props.artist}> {this.props.artist}</div>
        </td>
        <td className="url" title={this.props.stream_url}>{this.props.page_url}</td>
        <td>
          <button className="deleteConfirmation" title={"Delete " + this.props.id}>
            <span className="glyphicon glyphicon-remove" aria-hidden="true"></span>
          </button>
        </td>
      </tr>
    );
  }
}
