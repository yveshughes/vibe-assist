import React from 'react';
import { motion } from 'framer-motion';
import { ShieldIcon } from './icons/ShieldIcon';
import { ChecklistIcon } from './icons/ChecklistIcon';
import { OracleIcon } from './icons/OracleIcon';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  subtitle: string;
  description: string;
  features: string[];
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, subtitle, description, features }) => {
  return (
    <motion.div 
      className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 h-full flex flex-col"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.6 }}
    >
      <div className="flex items-center gap-4">
        <div className="bg-slate-800 p-3 rounded-lg">
          {icon}
        </div>
        <div>
          <h3 className="text-xl font-bold text-white">{title}</h3>
          <p className="text-emerald-400 font-semibold">{subtitle}</p>
        </div>
      </div>
      <p className="mt-6 text-gray-400 flex-grow">{description}</p>
      <ul className="mt-6 space-y-4">
        {features.map((feature, index) => (
          <li key={index} className="flex items-start gap-3">
            <svg className="w-6 h-6 text-emerald-500 flex-shrink-0 mt-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span className="text-gray-300">{feature}</span>
          </li>
        ))}
      </ul>
    </motion.div>
  );
};

const featuresData = [
  {
    icon: <ShieldIcon className="w-8 h-8 text-red-500" />,
    title: 'The Guardian',
    subtitle: 'Align with Confidence',
    description: "No more 'commit and pray.' The Guardian is your live safety net, catching issues before they become crises.",
    features: [
      'Proactive Security: Catches vulnerabilities and leaked secrets as you type with live `git diff` analysis.',
      'Live Tech Debt Analysis: Continuously scores your codebase for complexity and maintainability.'
    ],
  },
  {
    icon: <ChecklistIcon className="w-8 h-8 text-yellow-500" />,
    title: 'The Charter',
    subtitle: 'Align with Vision',
    description: "Stop the drift. Build the product you intended. The Charter is your project's living mission statement.",
    features: [
      'Interactive Roadmap: Define core features in `charter.md` and see progress in your menu bar.',
      'Drift Detection: Alerts you if a commit introduces an un-scoped feature, keeping you focused.'
    ],
  },
  {
    icon: <OracleIcon className="w-8 h-8 text-sky-500" />,
    title: 'The Oracle',
    subtitle: 'Align with Reality',
    description: "Turn vague vibes into perfect, context-aware code. The Oracle is your on-demand prompt engineer.",
    features: [
      'On-Screen Awareness: A simple hotkey summons the Oracle to understand your immediate context.',
      'Engineered Prompts: Synthesizes your goal, screen, and codebase into a perfect prompt for any AI tool.'
    ],
  },
];

const Features: React.FC = () => {
  return (
    <section className="py-20 sm:py-32">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <motion.h2 
            className="text-3xl sm:text-4xl font-extrabold text-white"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            How VibeAssist Works
          </motion.h2>
          <motion.p 
            className="mt-4 max-w-2xl mx-auto text-lg text-gray-400"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            VibeAssist aligns your development workflow through three intelligent, automated layers.
          </motion.p>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuresData.map((feature, index) => (
            <FeatureCard key={index} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;