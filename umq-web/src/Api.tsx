import { TrackProps } from './Components/Playlist/Track';

const url = '/playlist';

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

export async function getTrack(id: string, track_id: number): Promise<TrackProps> {
  const response = await fetch(`${url}/${id}/${track_id}`);

  await assertOk(response);

  return response.json();
}
