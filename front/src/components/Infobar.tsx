import React, { useContext, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { globalContext, GlobalContextProvider } from '../script/Values';
import '../styles/Infobar.css';

const Infobar: React.FC = () => {
    const context: GlobalContextProvider = useContext(globalContext);

    useEffect(() => {
        if (context.dev) console.log('Rendering Infobar');
    });

    return (
        <footer id='infobar'>
            <div className='footer-section'>
                <h3>Contactez nous</h3>
                <ul>
                    <li>
                        <div className='footer-line'>
                            <i className='fas fa-map-marker-alt' />
                            <p> Adresse : </p>
                            <a href='https://maps.app.goo.gl/Y4Ds6c3uUZM1t8gLA' target='_blank' rel='noreferrer'>Salle B007, Bâtiment 620, Maison de l'Ingénieur, Rue Louis de Broglie, 91190 Orsay, France</a>
                        </div>
                    </li>
                    <li>
                        <div className='footer-line'>
                            <i className='fas fa-envelope' />
                            <p> Email : </p>
                            <a href='mailto:cia.polytech@gmail.com' target='_blank' rel='noreferrer'>cia.polytech@gmail.com</a>
                        </div>
                    </li>
                </ul>
            </div>
            <div className='footer-section'>
                <h3>Liens utiles</h3>
                <ul>
                    <li>
                        <Link to='/' className='footer-line'>
                            <i className='fas fa-home' />
                            <p> Home</p>
                        </Link>
                    </li>
                    <li>
                        <Link to='/doc' className='footer-line'>
                            <i className='fas fa-newspaper' />
                            <p> Doc</p>
                        </Link>
                    </li>
                    <li>
                        <Link to='/code' className='footer-line'>
                            <i className='fas fa-code' />
                            <p> Code</p>
                        </Link>
                    </li>
                    <li>
                        <Link to='/scoreboard' className='footer-line'>
                            <i className="fa-solid fa-trophy" />
                            <p> Scoreboard</p>
                        </Link>
                    </li>
                    <li>
                        <Link to='/connect' className='footer-line'>
                            <i className="fa-solid fa-user" />
                            <p> Connexion</p>
                        </Link>
                    </li>
                </ul>
            </div>
            <div className='footer-section'>
                <h3>Suivez nous</h3>
                <ul>
                    <li>
                        <a href='https://discord.gg/S8gRM95wqw' target='_blank' rel='noreferrer' className='footer-line'><i className='fab fa-discord' /> Discord</a>
                    </li>
                    <li>
                        <a href='https://github.com/CIA-PoPS' target='_blank' rel='noreferrer' className='footer-line'><i className='fab fa-github' /> GitHub</a>
                    </li>
                    <li>
                        <a href='https://www.facebook.com/profile.php?id=61555761136479' target='_blank' rel='noreferrer' className='footer-line'><i className='fab fa-facebook' /> Facebook</a>
                    </li>
                    <li>
                        <a href='https://www.instagram.com/cia_polytech_paris_saclay/' target='_blank' rel='noreferrer' className='footer-line'><i className='fab fa-instagram' /> Instagram</a>
                    </li>
                </ul>
            </div>
        </footer>
    );
};

export default Infobar;
