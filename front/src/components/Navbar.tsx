import React, { useContext, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { globalContext, GlobalContextProvider, dataURL } from '../script/Values';
import '../styles/Navbar.css';

const Navbar: React.FC = () => {
    const context: GlobalContextProvider = useContext(globalContext);

    const year: number = new Date().getFullYear();

    useEffect(() => {
        if (context.dev) console.log('Rendering Navbar');
    });

    return (
        <header id='navbar'>
            <Link to='/' className='navbar-logo-link'>
                <img src={dataURL + '/images/logo/cia_marge.svg'} />
                <div className='navbar-zero'>
                    <h1>CIA - POPS</h1>
                    <small>{year}</small>
                </div>
            </Link>
            <nav className='navbar-links'>
                <ul>
                    <li>
                        <Link to='/doc'>
                            <i className='fas fa-newspaper' />
                            <p className='navbar-second'> Doc</p>
                        </Link>
                    </li>
                    <li>
                        <Link to='/code'>
                            <i className='fas fa-code' />
                            <p className='navbar-second'> Code</p>
                        </Link>
                    </li>
                    <li>
                        <Link to='/scoreboard'>
                            <i className="fas fa-trophy" />
                            <p className='navbar-second'> Scoreboard</p>
                        </Link>
                    </li>
                    <Link to='/connect' className='navbar-links-connect'>
                        <i className="fas fa-user" />
                        <p className='navbar-first'> {context.token ? "Team" : "Connexion"}</p>
                    </Link>
                </ul>
            </nav>
        </header>
    );
};

export default Navbar;
