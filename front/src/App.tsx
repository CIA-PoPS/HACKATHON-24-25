import React, { lazy, Suspense, useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { GlobalContextProvider, globalContext } from './script/Values';
import Loading from './components/Loading';
import Navbar from './components/Navbar';
import Infobar from './components/Infobar';
import HUD from './components/HUD';
import './styles/General.css';
import '@fortawesome/fontawesome-free/css/all.min.css';


const Home       = lazy(() => import('./components/pages/Home'));
const Doc        = lazy(() => import('./components/pages/Doc'));
const Code       = lazy(() => import('./components/pages/Code'));
const Scoreboard = lazy(() => import('./components/pages/Scoreboard'));
const Connect    = lazy(() => import('./components/pages/Connect'));


const App: React.FC = () => {
    const [__modeTheme, __setModeTheme]    : [boolean,  (b: boolean) => void]  = useState<boolean>(Boolean(Number(localStorage.getItem('modeTheme'))));
    const [__token, __setToken]            : [string,   (s: string) => void]   = useState<string>(sessionStorage.getItem('token') || '');

    const context: GlobalContextProvider = new GlobalContextProvider({
        modeTheme: __modeTheme,
        token: __token,
        dev: true,
        setModeTheme: __setModeTheme,
        setToken: __setToken
    });

    useEffect(() => {
        localStorage.setItem('modeTheme', context.modeTheme ? '1' : '0');
    }, [context.modeTheme]);

    useEffect(() => {
        sessionStorage.setItem('token', context.token);
    }, [context.token]);

    function updateSizes(): void {
        const infobarHeight: number = document.getElementById('infobar')?.offsetHeight || 0;
        document.documentElement.style.setProperty('--infobar-height', `${infobarHeight}px`);
    };

    useEffect(() => {
        updateSizes();
        window.addEventListener('resize', updateSizes);
        return () => {
            window.removeEventListener('resize', updateSizes);
        }
    });

    useEffect(() => {
        if (context.dev) console.log('Rendering App');
    });

    useEffect(() => {
        if (context.dev) console.log('Calling App');
    }, []);

    return (
        <globalContext.Provider value={context}>
            <Router>
                <input type='checkbox' id='mode-theme' checked={context.modeTheme} readOnly />
                <div id='subroot'>
                    <div id='fixed-background'></div>
                    <Navbar />
                    <main id='main'>
                        <Suspense fallback={<Loading />}>
                            <Routes>
                                <Route path='/' element={<Home />} />
                                <Route path='/doc' element={<Doc />} />
                                <Route path='/code' element={<Code />} />
                                <Route path='/scoreboard' element={<Scoreboard />} />
                                <Route path='/connect' element={<Connect />} />
                            </Routes>
                        </Suspense>
                    </main>
                    <Infobar />
                    <HUD />
                </div>
            </Router>
        </globalContext.Provider>
    );
};

export default App;
