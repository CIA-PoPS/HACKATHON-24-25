export class User {
    id: number;
    email: string;
    nickname: string;
    password: string;
    registrationTime: Date;
    isAdmin: boolean;
    isVerified: boolean;
    isATeam: boolean;

    constructor(data: any) {
        this.id               =   Number(data.userId               ?? data.id               ?? -1);
        this.email            =          data.userEmail            ?? data.email            ?? "";
        this.nickname         =          data.userNickname         ?? data.nickname         ?? "";
        this.password         =          data.userPassword         ?? data.password         ?? "";
        this.registrationTime = new Date(data.userRegistrationTime ?? data.registrationTime ?? 0);
        this.isAdmin          =  Boolean(data.userIsAdmin          ?? data.isAdmin          ?? false);
        this.isVerified       =  Boolean(data.userIsVerified       ?? data.isVerified       ?? false);
        this.isATeam          =  Boolean(data.userIsATeam          ?? data.isATeam          ?? false);
    }
}
