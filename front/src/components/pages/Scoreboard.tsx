import React, { useContext, useEffect, useState } from 'react';
import { GlobalContextProvider, globalContext } from '../../script/Values';
import { getScoreboard } from '../../api/codeApi';
import { Score } from '../../models/codeModels';
import '../../styles/Scoreboard.css';
import Loading from '../Loading';


const Event: React.FC = () => {
    const context: GlobalContextProvider = useContext(globalContext);
    const [scoreboard, setScoreboard] = useState<Score[]>([]);

    useEffect(() => {
        if (context.dev) console.log('Rendering Event');
    });

    useEffect(() => {
        if (context.dev) console.log('Rendering Event');
        getScoreboard(context.token)
            .then(setScoreboard)
            .catch((error) => alert('Can\'t retrieve scoreboard :' + error));
    }, []);

    return <Loading />;
    return (
        <div className="scoreboard-container">
            <h2 className="scoreboard-title">🏆 Scoreboard</h2>
            {scoreboard.length === 0 ? (
                <p className="no-scores">No scores available.</p>
            ) : (
                <table className="scoreboard-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Name</th>
                            <th>Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        {[...scoreboard].sort((a, b) => b.score - a.score).map((player, index) => (
                            <tr key={index}>
                                <td>{index + 1}</td>
                                <td>{player.team}</td>
                                <td>{player.score}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default Event;
