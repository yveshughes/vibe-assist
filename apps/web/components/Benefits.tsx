import React from 'react';
import { motion } from 'framer-motion';
import { CheckIcon } from './icons/CheckIcon';

const benefits = [
    "Stay in Flow. Minimize context switching and documentation deep-dives. Stay focused on solving creative problems.",
    "Ship with Confidence. Proactive security and test-gated suggestions mean fewer bugs and safer code.",
    "Eliminate Project Drift. Ensure your final product is the one you envisioned from the start.",
    "Supercharge Your AI. Turn your generic AI assistant into a specialized expert on your codebase.",
    "Lightweight & Ambient. Lives quietly in your menu bar. It's there when you need it, invisible when you don't."
];

const Benefits: React.FC = () => {
    return (
        <section className="py-20 sm:py-32 bg-slate-900">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="max-w-3xl mx-auto text-center">
                    <motion.h2 
                        className="text-3xl sm:text-4xl font-extrabold text-white"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                    >
                        The VibeAssist Promise
                    </motion.h2>
                </div>

                <div className="mt-16 max-w-4xl mx-auto">
                    <ul className="space-y-8">
                        {benefits.map((benefit, index) => (
                            <motion.li
                                key={index}
                                className="flex items-start p-6 bg-slate-800/50 rounded-lg border border-slate-700"
                                initial={{ opacity: 0, x: -30 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true, amount: 0.5 }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                            >
                                <CheckIcon className="h-8 w-8 text-emerald-400 flex-shrink-0 mr-5 mt-1" />
                                <div>
                                    <p className="text-lg text-gray-300">{benefit}</p>
                                </div>
                            </motion.li>
                        ))}
                    </ul>
                </div>
            </div>
        </section>
    );
};

export default Benefits;