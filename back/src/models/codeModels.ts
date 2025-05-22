export class Submit {
    teamId: number;
    time: Date;
    status: string;
    score: number;
    canHaveError: boolean;

    constructor(data: any) {
        this.teamId       =   Number(data.teamId             ?? -1);
        this.time         = new Date(data.submitTime         ?? data.time         ?? 0);
        this.status       =          data.submitStatus       ?? data.status       ?? "";
        this.score        =   Number(data.submitScore        ?? data.score        ?? -1);
        this.canHaveError =  Boolean(data.submitCanHaveError ?? data.canHaveError ?? false);
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
