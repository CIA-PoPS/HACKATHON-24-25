import React, { useContext, useEffect } from 'react';
import { globalContext, GlobalContextProvider, dataURL } from '../../script/Values';
import '../../styles/Home.css';

const Home: React.FC = () => {
    const context: GlobalContextProvider = useContext(globalContext);

    useEffect(() => {
        if (context.dev) console.log('Rendering Home');
    });

    return (
        <>
            <section className='home-welcome'>
                <h1>Bienvenue au CIA</h1>
            </section>
            <section className='home-info'>
                <ul>
                    <li className='home-info-block'>
                        <img src={dataURL + '/images/logo/cia.svg'} />
                        <div>
                            <h2>Qui sommes nous ?</h2>
                            <p>Le Club d'Informatique et d'Algorithmique (CIA) est un groupe d'étudiants passionnés par l'informatique et les algorithmes à l'école d'ingénieur. Nous nous réunissons régulièrement pour travailler sur des projets, organiser des compétitions et partager nos connaissances avec les autres membres. Notre mission est de promouvoir l'intérêt pour l'informatique et de fournir un environnement où les étudiants peuvent apprendre, collaborer et innover.</p>
                        </div>
                    </li>
                    <li className='home-info-block reverse'>
                        <img src={dataURL + '/images/home/event.png'} />
                        <div>
                            <h2>Évènement</h2>
                            <p>Nous organisons régulièrement des événements liés à l'informatique, tels que des hackathons, des ateliers de programmation et des compétitions d'algorithmique. Ces événements offrent aux étudiants l'occasion de mettre en pratique leurs compétences, de se mesurer à d'autres passionnés et de se préparer pour des compétitions de plus grande envergure.</p>
                        </div>
                    </li>
                    <li className='home-info-block'>
                        <img src={dataURL + '/images/home/courses.png'} />
                        <div>
                            <h2>Cours</h2>
                            <p>Nous proposons des cours et des ateliers pour aider les membres à améliorer leurs compétences en programmation et en algorithmique. Que vous soyez débutant ou expérimenté, vous trouverez des ressources et des formations adaptées à votre niveau. Nos cours couvrent un large éventail de sujets, allant des bases de la programmation aux techniques avancées d'algorithmes.</p>
                        </div>
                    </li>
                    <li className='home-info-block reverse'>
                        <img src={dataURL + '/images/home/office.png'} />
                        <div>
                            <h2>Bureau</h2>
                            <p>Voici notre bureau actuel: Maxime DAUPHIN (Prez), Julien TAP (VP), Maël HOUPLINE (Trez), David Luca (Repso. Projet), Simon RENARD (Respo. Algo) et Rémi RUELLE (Respo. Comm). Nous sommes là pour vous aider et répondre à vos questions.</p>
                        </div>
                    </li>
                </ul>
            </section>
        </>  
    );
};

export default Home;
