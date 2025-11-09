import React from 'react';
import { motion } from 'framer-motion';
import { ShieldIcon } from './icons/ShieldIcon';
import { MultiLLMIcon } from './icons/MultiLLMIcon';
import ProblemChart from './ProblemChart';
import { ContextAnimation } from './animations/ContextAnimation';
import { VisionAnimation } from './animations/VisionAnimation';

const problemsData = [
    {
        icon: <ContextAnimation />,
        title: 'Lost Context = Lost Productivity',
        description: 'Working across multiple contributors, LLMs, and IDEs? Your context gets fragmented. AI assistants give outdated suggestions. Your team loses track of what changed. You waste hours re-explaining the same thing to different tools and teammates.',
        solution: 'VibeAssist reviews every change you make and organizes it in a centralized location. See what\'s changed, identify conflicts, and share up-to-date context with your entire team and all your AI tools—instantly.'
    },
    {
        icon: <VisionAnimation />,
        title: 'Your Vision Gets Lost in Translation',
        description: 'Without a clear, consistent directive, AI can "drift" from the core project goals, adding un-scoped features or solving the wrong problem. This leads to wasted time and a product that misses the mark.',
        solution: 'With charter.md, VibeAssist has a single source of truth for your project\'s vision. It gently nudges development back on course, ensuring every commit serves the main goal.'
    },
    {
        icon: <ShieldIcon className="w-24 h-24 text-red-500" />,
        title: 'Best Practices are an Afterthought',
        description: 'In the rush to build, security vulnerabilities, tech debt, and poor coding patterns creep in. Traditional static analysis is too slow and noisy to be part of a creative flow state.',
        solution: 'The Guardian acts as a live linter for your project\'s health, catching security risks, secrets, and code smells in real-time before they are ever committed.'
    },
    {
        icon: <MultiLLMIcon className="w-24 h-24 text-purple-400" />,
        title: 'The LLM Ecosystem is Fragmented',
        description: 'You use Gemini for code, Claude for docs, and ChatGPT for brainstorming. Each speaks a different dialect, forcing you to constantly switch mental models and prompting styles.',
        solution: 'The Oracle is your universal translator. It understands your intent and crafts the perfect, context-rich prompt for any AI backend, giving you the best of all worlds without the friction.'
    }
];

const ProblemRow: React.FC<{ problem: typeof problemsData[0]; index: number }> = ({ problem, index }) => {
    const isReversed = index % 2 !== 0;
    const isAnimation = index === 0 || index === 1;

    const contentVariants = {
        hidden: { opacity: 0, x: isReversed ? 50 : -50 },
        visible: { opacity: 1, x: 0, transition: { duration: 0.6, delay: 0.2 } }
    };

    const imageVariants = {
        hidden: { opacity: 0, scale: 0.8 },
        visible: { opacity: 1, scale: 1, transition: { duration: 0.6 } }
    };

    return (
        <div className={`flex flex-col md:flex-row items-center gap-12 lg:gap-24 ${isReversed ? 'md:flex-row-reverse' : ''}`}>
            <motion.div 
                className={isAnimation ? "md:w-2/5 flex justify-center" : "md:w-1/3 flex justify-center"}
                variants={imageVariants}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, amount: 0.5 }}
            >
                {problem.icon}
            </motion.div>
            <motion.div 
                className={isAnimation ? "md:w-3/5" : "md:w-2/3"}
                variants={contentVariants}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, amount: 0.5 }}
            >
                <h3 className="text-2xl sm:text-3xl font-bold text-white mb-4">{problem.title}</h3>
                <p className="text-gray-400 mb-4 text-lg">{problem.description}</p>
                <p className="text-emerald-300 text-lg font-medium">{problem.solution}</p>
            </motion.div>
        </div>
    );
};


const Problems: React.FC = () => {
    return (
        <section className="py-20 sm:py-32">
            <div className="container mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center">
                    <motion.p 
                        className="text-lg font-semibold text-emerald-400 uppercase tracking-wider"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                    >
                        The Problem
                    </motion.p>
                    <motion.h2 
                        className="mt-2 text-3xl sm:text-4xl font-extrabold text-white"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.1 }}
                    >
                        The Chaos of Modern AI Development
                    </motion.h2>
                    <motion.p 
                        className="mt-4 max-w-3xl mx-auto text-lg text-gray-400"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                        "Vibe-driven development" is powerful, but it's built on a fragile foundation. Developers waste countless hours fighting tools instead of creating.
                    </motion.p>
                </div>

                <ProblemChart />

                <div className="text-center mt-24 sm:mt-32">
                     <motion.h2 
                        className="text-3xl sm:text-4xl font-extrabold text-white"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                    >
                        How VibeAssist Eliminates The Chaos
                    </motion.h2>
                    <motion.p 
                        className="mt-4 max-w-2xl mx-auto text-lg text-gray-400"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                    >
                       We tackle the biggest drains on your flow state head-on, turning friction into fluid, focused creation.
                    </motion.p>
                </div>

                <div className="mt-16 sm:mt-24 space-y-20 sm:space-y-32">
                    {problemsData.map((problem, index) => (
                        <ProblemRow key={index} problem={problem} index={index} />
                    ))}
                </div>
            </div>
        </section>
    );
};

export default Problems;