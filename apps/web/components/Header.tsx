import React from 'react';
import { motion } from 'framer-motion';
import { VibeAssistLogo } from './icons/VibeAssistLogo';

const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 bg-slate-950/70 backdrop-blur-lg border-b border-slate-300/10">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center space-x-3"
          >
            <VibeAssistLogo className="h-8 w-8 text-emerald-500" />
            <span className="text-xl font-bold text-white">VibeAssist</span>
          </motion.div>
          <motion.a
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            href="#"
            className="hidden sm:inline-block bg-emerald-500 text-white font-semibold px-4 py-2 rounded-lg shadow-lg hover:bg-emerald-600 transition-colors focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:ring-opacity-75"
          >
            Download for macOS
          </motion.a>
        </div>
      </div>
    </header>
  );
};

export default Header;