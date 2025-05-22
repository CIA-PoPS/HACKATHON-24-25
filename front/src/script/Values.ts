import { createContext } from 'react';

export const backURL         = 'https://api.mes4game.com' as const;
export const frontURL        = 'https://www.mes4game.com' as const;
export const dataURL         = 'https://bde-pops.github.io/VPS-DATA/cia' as const;
export const defaultLanguage = 'en' as const;
export const languages       = [defaultLanguage, 'fr'] as const;
export type  Language        = typeof languages[number];

export class GlobalContextProvider {
    modeTheme      : boolean;
    token          : string;
    dev            : boolean;
    setModeTheme   : (theme: boolean) => void;
    setToken       : (token: string) => void;

    constructor (data: any) {
        this.modeTheme      = data.modeTheme      ?? false;
        this.token          = data.token          ?? "";
        this.dev            = data.dev            ?? false;
        this.setModeTheme   = data.setModeTheme   ?? (() => {});
        this.setToken       = data.setToken       ?? (() => {});
    }
}

export const globalContext = createContext<GlobalContextProvider>(new GlobalContextProvider({}));
