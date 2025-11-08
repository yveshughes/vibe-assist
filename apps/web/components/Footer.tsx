import React from 'react';
import { motion } from 'framer-motion';

const Footer: React.FC = () => {
  return (
    <footer className="py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <motion.p 
          className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-sky-400"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
        >
          VibeAssist. Your project's alignment system.
        </motion.p>
        <p className="mt-4 text-sm text-gray-500">
          &copy; {new Date().getFullYear()} VibeAssist. All rights reserved.
        </p>
      </div>
    </footer>
  );
};

export default Footer;