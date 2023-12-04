import {makeAutoObservable} from "mobx";
import {File} from "@model/response";

class Store {
    constructor() {
        makeAutoObservable(this);
    }

    file: File | null = null;
}


export const store = new Store();