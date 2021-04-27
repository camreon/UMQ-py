import { TrackProps } from './Playlist/Track';

const url = '/api';

type Response = {
  ok: any,
  json: any
}

async function assertOk(response: Response) {
  if (!response.ok) {
    const errors = await response.json();
    throw new Error(errors.errors);
  }
};

export async function getPlaylist(id: string): Promise<TrackProps[]> {
  const response = await fetch(`${url}/${id}`);
  
  await assertOk(response);
  return response.json();
}

export async function getTrack(playlist_id: string, track_id: number): Promise<TrackProps> {
  const response = await fetch(`${url}/${playlist_id}/${track_id}`);
  
  await assertOk(response);
  return response.json();
}

export async function addTrack(playlist_id: string, page_url: string): Promise<TrackProps[]> {
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ page_url: page_url })
};
  const response = await fetch(`${url}/${playlist_id}`, options);
  
  await assertOk(response);
  return response.json();
}

export async function deleteTrack(playlist_id: string, track_id: number): Promise<TrackProps[]> {
  const options = {
    method: 'DELETE',
};
  const response = await fetch(`${url}/${playlist_id}/${track_id}`, options);
  
  await assertOk(response);
  return response.json();
}

export async function getNextPlaylistId(): Promise<string> {
  const response = await fetch(`${url}/newplaylist/`);
  
  await assertOk(response);
  return response.json();
}
