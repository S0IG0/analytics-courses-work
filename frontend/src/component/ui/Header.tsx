import {NamePages, Page, routes} from "@route/routes.tsx";
import {Link, NavLink} from "react-router-dom";
import {observer} from "mobx-react-lite";

export const Header = observer(() => {
    const pages: Page[] = Object.keys(NamePages)
        .filter(key => !isNaN(Number(key)))
        .map(key => routes[Number(key) as NamePages])
    return (
        <header>
            <nav className="navbar navbar-expand-md  border-bottom">
                <div className="container-fluid">
                    <Link className="navbar-brand ms-2" to={pages[NamePages.HOME].path}>
                        <i className="bi bi-clipboard2-data"></i>
                    </Link>
                    <button className="navbar-toggler collapsed" type="button" data-bs-toggle="collapse"
                            data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false"
                            aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="navbar-collapse collapse" id="navbarCollapse">
                        <ul className="nav nav-pills me-auto mb-2 mb-md-0">
                            {pages.map(page => (
                                <li className="nav-item me-2" key={page.path}>
                                    <NavLink
                                        to={page.path}
                                        className="nav-link"
                                        aria-current="page"
                                    >
                                        {page.name}
                                    </NavLink>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </nav>
        </header>
    );
});