
import React from 'react';
import { motion } from 'framer-motion';

const chartData = [
    { label: 'Debugging/Time Sink', value: 14 },
    { label: 'Outdated/Hallucinated Code', value: 12 },
    { label: 'Tech Debt/Spaghetti', value: 11 },
    { label: 'Scaling/Architecture', value: 8 },
    { label: 'Security Risks', value: 7 },
    { label: 'Weak Fundamentals', value: 6 },
    { label: 'Cost/Token Usage', value: 6 },
    { label: 'Reproducibility', value: 5 },
    { label: 'Slow Tools', value: 4 },
    { label: 'Version Conflicts', value: 3 },
    { label: 'Context Window/State', value: 3 },
    { label: 'Collaboration Friction', value: 2 },
    { label: 'Data Privacy', value: 2 },
    { label: 'Testing Difficulty', value: 2 },
];

const containerVariants = {
    hidden: {},
    visible: {
        transition: {
            staggerChildren: 0.05,
            delayChildren: 0.3,
        },
    },
};

const barVariants = {
    hidden: { height: 0, opacity: 0 },
    visible: (custom: number) => ({
        height: custom,
        opacity: 1,
        transition: {
            duration: 0.8,
            ease: [0.25, 1, 0.5, 1],
        },
    }),
};

const ProblemChart: React.FC = () => {
    const chartHeight = 250;
    const chartWidth = 800;
    const yAxisWidth = 40;
    const xAxisHeight = 100;

    const maxValue = 14;
    
    const bandWidth = (chartWidth - yAxisWidth) / chartData.length;
    const barWidth = bandWidth * 0.7;

    const xScale = (index: number) => yAxisWidth + index * bandWidth + (bandWidth - barWidth) / 2;
    const yScale = (value: number) => chartHeight - (value / maxValue) * chartHeight;
    
    const yAxisLabels = [0, 2, 4, 6, 8, 10, 12, 14];

    return (
        <motion.div 
            className="w-full max-w-5xl mx-auto bg-slate-900/50 border border-slate-800 rounded-xl p-4 sm:p-6 lg:p-8 mt-16"
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.6 }}
        >
            <h3 className="text-xl sm:text-2xl font-bold text-white mb-2 text-center">Top Frustrations in AI-Powered Development</h3>
            <p className="text-sm text-gray-400 mb-8 text-center">Data from a survey of 100+ professional developers shows a clear pattern of friction.</p>
            
            <div className="w-full overflow-x-auto pb-4">
                <svg className="min-w-[800px]" viewBox={`0 0 ${chartWidth} ${chartHeight + xAxisHeight}`}>
                    {/* Y-axis */}
                    {yAxisLabels.map((label) => (
                        <g key={label} className="text-gray-500">
                            <line
                                x1={yAxisWidth - 5}
                                y1={yScale(label)}
                                x2={chartWidth}
                                y2={yScale(label)}
                                stroke="currentColor"
                                strokeWidth="0.5"
                                strokeDasharray="2 2"
                            />
                            <text
                                x={yAxisWidth - 10}
                                y={yScale(label) + 4}
                                textAnchor="end"
                                fontSize="12"
                                fill="currentColor"
                            >
                                {label}
                            </text>
                        </g>
                    ))}

                    <motion.g
                        variants={containerVariants}
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true, amount: 0.1 }}
                    >
                        {chartData.map((d, i) => {
                            const barHeight = (d.value / maxValue) * chartHeight;
                            const x = xScale(i);
                            return (
                                <g key={d.label}>
                                    <title>{`${d.label}: ${d.value}`}</title>
                                    <motion.rect
                                        x={x}
                                        y={yScale(d.value)}
                                        width={barWidth}
                                        rx="3"
                                        ry="3"
                                        fill="#f59e0b" // amber-500
                                        custom={barHeight}
                                        variants={barVariants}
                                    />
                                    <text
                                        x={x + barWidth / 2}
                                        y={chartHeight + 15}
                                        transform={`rotate(-55, ${x + barWidth / 2}, ${chartHeight + 15})`}
                                        textAnchor="end"
                                        fontSize="12"
                                        fill="#9ca3af" // gray-400
                                        className="font-medium"
                                    >
                                        {d.label}
                                    </text>
                                </g>
                            );
                        })}
                    </motion.g>
                </svg>
            </div>
        </motion.div>
    );
};

export default ProblemChart;
