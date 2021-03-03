import React, { Component } from 'react';
import './Track.css';

export type TrackProps = {
  id: number,
  title: string,
  artist?: string,
  page_url: string,
  stream_url: string,
}

type Props = {
  handleOnClick: () => void
}

export class Track extends Component<TrackProps & Props> {

  render() {
    return (
      <tr onClick={() => this.props.handleOnClick()}>
        <td className="track">
          <div className="track-title" title={this.props.title}>{this.props.title}</div>
          <div className="track-artist" title={this.props.artist}> {this.props.artist}</div>
        </td>
        <td className="url" title={this.props.stream_url}>{this.props.page_url}</td>
        <td>
          <button className="deleteConfirmation" title={"Delete " + this.props.id}>
            <span className="fa fa-remove" aria-hidden="true"></span>
          </button>
        </td>
      </tr>
    );
  }
}
