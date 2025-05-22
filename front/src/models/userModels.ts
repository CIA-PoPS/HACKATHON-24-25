export class User {
    id: number;
    email: string;
    nickname: string;
    password: string;
    registrationTime: Date;
    isAdmin: boolean;
    isVerified: boolean;

    constructor(data: any) {
        this.id               =   Number(data.id               ?? -1);
        this.email            =          data.email            ?? "";
        this.nickname         =          data.nickname         ?? "";
        this.password         =          data.password         ?? "";
        this.registrationTime = new Date(data.registrationTime ?? 0);
        this.isAdmin          =  Boolean(data.isAdmin          ?? false);
        this.isVerified       =  Boolean(data.isVerified       ?? false);
    }
}
