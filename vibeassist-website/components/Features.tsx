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
    title: 'Code Monitor Agent',
    subtitle: 'Your Autopilot for Code Quality',
    description: "Continuously monitors your codebase, identifying potential issues, tech debt, and vulnerabilities before they become problems. It's like having a senior developer reviewing your code in real-time.",
    features: [
      'Live Tech Debt Analysis: Get a real-time score of your code’s health and maintainability.',
      'Vulnerability Detection: Catches common security risks and leaked secrets as you type.',
      'Best Practice Suggestions: Offers contextual advice to improve your code quality.'
    ],
  },
  {
    icon: <ChecklistIcon className="w-8 h-8 text-yellow-500" />,
    title: 'Security Agent',
    subtitle: 'Your Proactive Security Analyst',
    description: "Acts as a dedicated security analyst for your project, ensuring your application is secure from the ground up. It actively scans for threats and helps you maintain a strong security posture.",
    features: [
      'Automated Security Audits: Regularly scans your dependencies and code for known vulnerabilities.',
      'Threat Modeling: Helps you identify and mitigate potential security threats in your architecture.',
      'Compliance Checks: Ensures your code adheres to industry-standard security and compliance guidelines.'
    ],
  },
  {
    icon: <OracleIcon className="w-8 h-8 text-sky-500" />,
    title: 'Project Manager Agent',
    subtitle: 'Your AI Project Coordinator',
    description: "Keeps your project on track by managing tasks, monitoring progress, and ensuring your team is aligned with the project's goals. It's the ultimate tool for efficient and organized development.",
    features: [
      'Automated Task Management: Creates, assigns, and tracks tasks based on your project’s needs.',
      'Progress Reporting: Generates real-time reports on your project’s status and team’s performance.',
      'Goal Alignment: Ensures every line of code contributes to the project’s overall objectives.'
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