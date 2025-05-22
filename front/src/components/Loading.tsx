import React, { useContext, useEffect } from 'react';
import { GlobalContextProvider, globalContext } from '../script/Values';
import '../styles/Loading.css';

const Loading: React.FC = () => {
    const context: GlobalContextProvider = useContext(globalContext);

    useEffect(() => {
        if (context.dev) console.log('Rendering Loading');
    });

    return (
        <h1>Loading...</h1>
    );
};

export default Loading;
