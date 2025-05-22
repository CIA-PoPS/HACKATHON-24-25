export class Submit {
    time: Date;
    status: string;
    score: number;
    canHaveError: boolean;

    constructor(data: any) {
        this.time         = new Date(data.time         ?? 0);
        this.status       =          data.status       ?? "";
        this.score        =   Number(data.score        ?? -1);
        this.canHaveError =  Boolean(data.canHaveError ?? false);
    }
}

export class Score {
    team: string;
    score: number;

    constructor(data: any) {
        this.team  =        data.team  ?? "";
        this.score = Number(data.score ?? -1);
    }
}
