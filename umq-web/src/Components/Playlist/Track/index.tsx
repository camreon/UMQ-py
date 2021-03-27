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
  isLoading: boolean,
  isPlaying: boolean,
  number: number,
  handleOnClick: () => void,
  handleOnDelete: () => void
}

export class Track extends Component<TrackProps & Props> {

  handleOnDelete = (e: any) => {
    e.stopPropagation()
    this.props.handleOnDelete();
  }

  render() {
    const isPlaying: boolean = this.props.isPlaying;
    const isLoading: boolean = isPlaying && this.props.isLoading;

    const trackClass = [
      isPlaying ? "playing" : "",
      isLoading ? "loading" : ""
    ].join(' ');

    return (
      <tr 
        className={trackClass} 
        onClick={this.props.handleOnClick}
      >
        <td>{this.props.number}</td>
        <td className="track">
          <div className="track-title" title={this.props.title}>{this.props.title}</div>
          <div className="track-artist" title={this.props.artist}> {this.props.artist}</div>
        </td>
        <td className="url" title={this.props.stream_url}>{this.props.page_url}</td>
        <td>
          <button 
            className="deleteConfirmation btn" 
            title={"Delete " + this.props.id}
            onClick={this.handleOnDelete}
          >
            <span className="fa fa-remove" aria-hidden="true"></span>
          </button>
        </td>
      </tr>
    );
  }
}
