import { fetchGET, fetchPOST } from './baseApi';
import { Submit, Score } from '../models/codeModels';

export async function getSubmit(token: string): Promise<Submit> {
    const response: Response = await fetchGET(token, `/code/submits`);
    return new Submit(response.ok ? await response.json() : {});
}

export async function postSubmit(token: string, stages: number[], code: string): Promise<void> {
    const response: Response = await fetchPOST(token, '/code/submits', JSON.stringify({ stages: stages.map(x => x+1), code }));
    if (!response.ok) {
        throw new Error("Failed to submit code");
    }
}

export async function getFile(token: string, extension: string): Promise<void> {
    const response: Response = await fetchGET(token, '/code/dl/' + extension);

    if (!response.ok) {
        throw new Error("Failed to download file");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");

    a.href = url;
    a.download = (extension === "zip") ? "logs.zip" : `code.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

export async function getScoreboard(token: string): Promise<Score[]> {
    const response: Response = await fetchGET(token, `/code/scoreboard`);
    if (!response.ok) {
        throw new Error("Failed to retrieve scoreboard");
    }
    const arr = await response.json();
    return arr.map((obj: any) => new Score(obj));
}
