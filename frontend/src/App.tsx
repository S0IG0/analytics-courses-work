import {Header} from "@ui/Header.tsx";
import {Footer} from "@ui/Footer.tsx";
import {Route, Routes} from "react-router-dom";
import {NamePages, Page, routes} from "@route/routes.tsx";
import {NotFoundPage} from "@page/public/NotFoundPage.tsx";

function App() {
    const pages: Page[] = Object.keys(NamePages)
        .filter(key => !isNaN(Number(key)))
        .map(key => routes[Number(key) as NamePages])

    return (
        <>
            <Header/>
            <main className="flex-shrink-1">
                <div className="p-4">
                    <Routes>
                        {pages.map(page => (
                            <Route
                                key={page.path}
                                path={page.path}
                                element={page.component}
                            />
                        ))}
                        <Route path={"*"} element={<NotFoundPage/>}/>
                    </Routes>
                </div>
            </main>
            <Footer/>
        </>
    )
}

export default App;
