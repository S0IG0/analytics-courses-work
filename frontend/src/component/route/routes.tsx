import {ReactNode} from "react";
import {HomePage} from "@page/public/HomePage.tsx";
import ViewingData from "@page/public/ViewingData.tsx";

export enum Visibly {
    PUBLIC,
}


export enum NamePages {
    HOME,
    ANALYTICS,
}


export interface Page {
    name: string
    path: string
    component: ReactNode
    visibly: Visibly[]
}


export const routes: { [key in NamePages]: Page } = {
    [NamePages.HOME]: {
        name: "Главная",
        path: "/",
        component: <HomePage/>,
        visibly: [Visibly.PUBLIC],
    } as Page,
    [NamePages.ANALYTICS]: {
        name: "Просмотр данных",
        path: "/analytics",
        component: <ViewingData/>,
        visibly: [Visibly.PUBLIC],
    } as Page,
}

