import React, { useContext, useEffect, useState } from 'react';
import { globalContext, GlobalContextProvider } from '../../script/Values';
import { loginUser, registerUser, getUser } from '../../api/userApi';
import { User } from '../../models/userModels';
import '../../styles/Connect.css';

const Connect: React.FC = () => {
    const context        : GlobalContextProvider           = useContext(globalContext);
    const [mode, setMode]: [boolean, (b: boolean) => void] = useState<boolean>(false);
    const [user, setUser]: [User, (u: User) => void]       = useState<User>(new User({}));

    useEffect(() => {
        if (context.token === '') setUser(new User({}));
        else (async () => setUser(await getUser(context.token)))();
    }, [context.token]);

    function handleRegister() {
        const nickname = document.getElementById('nickname') as HTMLInputElement;
        const email = document.getElementById('email') as HTMLInputElement;
        const password = document.getElementById('password') as HTMLInputElement;

        alert('Try to register...');
        if (nickname && email && password) {
            (async () => context.setToken(await registerUser(email.value, nickname.value, password.value)))();
        }
    };

    function handleLogin() {
        const nickname = document.getElementById('nickname') as HTMLInputElement;
        const password = document.getElementById('password') as HTMLInputElement;

        if (nickname && password) (async () => context.setToken(await loginUser(nickname.value, nickname.value, password.value)))();
    };

    useEffect(() => {
        if (context.dev) console.log('Rendering Connect');
    });

    return (
        <>
            <h1>User</h1>
            <hr />
            {!context.token ? (
                <div className='connect'>
                    <div className='connect-switch'>
                        <button onClick={() => setMode(true)} style={{ backgroundColor: mode ? '' : 'transparent'}}>Login</button>
                        <button onClick={() => setMode(false)} style={{ backgroundColor: mode ? 'transparent' : ''}}>Register</button>
                    </div>
                    <div className='connect-input'>
                        <input type='text' id='nickname' placeholder='' autoComplete='username' required />
                        <label>Team name{mode ? ' or Email' : ''}</label>
                    </div>
                    <div className='connect-input' style={{ display: mode ? 'none' : ''}}>
                        <input type='email' id='email' placeholder='' autoComplete='email' required />
                        <label>Email</label>
                    </div>
                    <div className='connect-input'>
                        <input type='password' id='password' placeholder='' autoComplete='new-password' required />
                        <label>Password</label>
                    </div>
                    <button onClick={mode ? handleLogin : handleRegister}>{mode ? 'Login' : 'Register'}</button>
                </div>
            ) : (
                <div className='connect'>
                    <p>Team : {user.nickname}</p>
                    <p>Email : {user.email}</p>
                    <button onClick={() => context.setToken('')}>Logout</button>
                </div>
            )}
        </>  
    );
};

export default Connect;
