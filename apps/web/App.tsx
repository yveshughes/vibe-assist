
import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Problems from './components/Problems';
import Features from './components/Features';
import Benefits from './components/Benefits';
import Footer from './components/Footer';

const App: React.FC = () => {
  return (
    <div className="bg-slate-950 text-gray-300 font-sans antialiased">
      <div className="absolute inset-0 -z-10 h-full w-full bg-slate-950 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px]"></div>
      <Header />
      <main>
        <Hero />
        <Problems />
        <Features />
        <Benefits />
      </main>
      <Footer />
    </div>
  );
};

export default App;