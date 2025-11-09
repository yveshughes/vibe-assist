import React from 'react';
import { motion } from 'framer-motion';

const MenuBarIconAnimation: React.FC = () => {
  return (
    <div className="relative flex items-center justify-center w-72 h-72">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          className="absolute w-16 h-16 rounded-full border border-emerald-400/60"
          initial={{ scale: 1, opacity: 0 }}
          animate={{
            scale: 4,
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            delay: i * 1,
            ease: "linear",
            times: [0, 0.5, 1]
          }}
        />
      ))}
      <motion.div
        className="w-16 h-16 rounded-full bg-emerald-500 shadow-lg shadow-emerald-500/50"
        animate={{
          scale: [1, 1.1, 1],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />
    </div>
  );
};


const Hero: React.FC = () => {
  return (
    <section className="relative overflow-hidden py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
        >
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 via-sky-300 to-purple-400 leading-tight">
            Context is all you need
          </h1>
        </motion.div>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          className="mt-6 max-w-2xl mx-auto text-lg text-gray-400"
        >
          Vibe Assist is a proactive AI partner that lives in your menu bar. It aligns your code with your vision, providing the live context, security, and focus that other assistants lack.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.6 }}
          className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <a
            href="#"
            className="w-full sm:w-auto bg-emerald-500 text-white font-semibold px-8 py-3 rounded-lg shadow-lg hover:bg-emerald-600 transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:ring-opacity-75"
          >
            Download for macOS
          </a>
          <a
            href="#"
            className="w-full sm:w-auto bg-slate-700 text-white font-semibold px-8 py-3 rounded-lg shadow-lg hover:bg-slate-600 transition-all duration-300 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-opacity-75"
          >
            Watch 2-min Demo
          </a>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.8 }}
          className="mt-16 sm:mt-24 flex justify-center"
        >
          <MenuBarIconAnimation />
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;