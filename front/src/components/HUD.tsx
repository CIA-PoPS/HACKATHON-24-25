import React, { useContext, useEffect } from 'react';
import { defaultLanguage, GlobalContextProvider, globalContext } from '../script/Values';
import '../styles/HUD.css';

const HUD: React.FC = () => {
    const context: GlobalContextProvider = useContext(globalContext);

    function goToTop(): void {
        window.scrollTo({top: 0, behavior: 'smooth'});
        document.documentElement.scrollTo({ top: 0, behavior: 'smooth' });
        document.body.scrollTo({ top: 0, behavior: 'smooth' });
    }

    useEffect(() => {
        if (context.dev) console.log('Rendering HUD');
    });

    return (
        <div id='hud' className='hud'>
            <button className='hud-button' onClick={() => context.setModeTheme(!context.modeTheme)}>
                <i className={'fas ' + (context.modeTheme ? 'fa-moon' : 'fa-sun')} />
            </button>
            <button className='hud-button' onClick={goToTop}>
                <i className='fas fa-arrow-up' />
            </button>
        </div>
    );
};

export default HUD;
