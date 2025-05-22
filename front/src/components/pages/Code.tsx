import React, { useContext, useState, useEffect } from 'react';
import { GlobalContextProvider, globalContext } from '../../script/Values';
import { postSubmit, getSubmit, getFile } from '../../api/codeApi';
import { Submit } from '../../models/codeModels';
import '../../styles/Code.css';

const Code: React.FC = () => {
    const context: GlobalContextProvider = useContext(globalContext);
    const [stages, setStages]: [number[], (s: number[]) => void] = useState<number[]>([]);
    const [submit, setSubmit]: [Submit, (s: Submit) => void] = useState<Submit>(new Submit({}));
    const items: string[] = ['MORE', 'LESS', 'ODD', 'EVEN', 'BORDER', 'FIX', 'CLING'];

    useEffect(() => {
        if (context.dev) console.log('Rendering Code');
    });

    function handleSubmit() {
        alert('Submit sent');
        const code = (document.getElementById('code') as HTMLTextAreaElement).value;
        postSubmit(context.token, stages, code)
            .catch(error => alert('Submit failed :' + error));
    }

    function handleDownload(file: string) {
        alert('Downloading ' + file + '...');
        getFile(context.token, file)
            .then(response => alert('Downloaded ' + file))
            .catch(error => alert('Download failed :' + error));
    }

    useEffect(() => {
        if (context.dev) console.log('Rendering Submit');
    });

    useEffect(() => {
        getSubmit(context.token)
            .then(setSubmit)
            .catch(error => alert('Can\'t retrieve last submit :' + error));
    }, []);

    function handleCheckboxChange(index: number) {
        setStages(stages.includes(index) ? stages.filter((i) => i !== index) : [...stages, index]);
    }

    return (
        <section className='submit'>
            <div className='submit-container'>
                <label htmlFor='code'>Code</label>
                <textarea id='code' name='code' rows={10} cols={50}></textarea>
                <div className='submit-select'>
                    <h2>Select stages</h2>
                    <div className="checkbox-list">
                        {items.map((item, index) => (
                            <label key={index} className={"checkbox-item" + (stages.includes(index) ? " selected" : "")}>
                                <input
                                    type="checkbox"
                                    checked={stages.includes(index)}
                                    onChange={() => handleCheckboxChange(index)}
                                    className="checkbox-input"
                                />
                                {item}
                            </label>
                        ))}
                    </div>
                    <div className="selected-indices">
                        Selected indices: {stages.map((index) => items[index]).join(', ')}
                    </div>
                </div>
                <button onClick={handleSubmit}>Submit</button>
            </div>
            <div className='submit-history'>
                <h2>Last Submit</h2>
                <p>Time : {submit.time.toUTCString()}</p>
                <p>Status : {submit.status}</p>
                <p>Score : {submit.score}</p>
                <p>Maybe errors ? : {submit.canHaveError ? 'Yes' : 'No'}</p>
                <button onClick={() => handleDownload('zip')}>Download Logs archive</button>
                <button onClick={() => handleDownload('py')}>Download Code</button>
            </div>
        </section>
    );
};

export default Code;
