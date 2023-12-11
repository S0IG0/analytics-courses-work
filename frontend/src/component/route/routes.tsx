import {ReactNode} from "react";
import {HomePage} from "@page/public/HomePage.tsx";
import ViewingData from "@page/public/ViewingData.tsx";
import TestPage from "@page/public/TestPage.tsx";
import AnalyticPage from "@page/public/AnalyticPage.tsx";
import BrokerPage from "@page/public/BrokerPage.tsx";

export enum Visibly {
    PUBLIC,
    PUBLIC_HIDDEN,
}


export enum NamePages {
    HOME,
    VIEW_DATA,
    TEST,
    ANALYTIC,
    BROKER
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
    [NamePages.VIEW_DATA]: {
        name: "Просмотр данных",
        path: "/view-data",
        component: <ViewingData/>,
        visibly: [Visibly.PUBLIC],
    } as Page,
    [NamePages.TEST]: {
        name: "Тестирование всяких красивых штучек :З",
        path: "/test",
        component: <TestPage/>,
        visibly: [Visibly.PUBLIC],
    } as Page,
    [NamePages.ANALYTIC]: {
        name: "Аналитика",
        path: "/analytic/:id",
        component: <AnalyticPage/>,
        visibly: [Visibly.PUBLIC_HIDDEN],
    } as Page,
    [NamePages.BROKER]: {
        name: "Брокер",
        path: "/broker",
        component: <BrokerPage/>,
        visibly: [Visibly.PUBLIC],
    } as Page,
}
