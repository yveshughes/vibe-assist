
import React from 'react';
import { motion } from 'framer-motion';

const NUM_STARS = 100;
const NUM_FRAMES = 5;
const NUM_SPARKLES = 10;

export const ContextAnimation: React.FC = () => {
    const stars = React.useMemo(() => {
        return Array.from({ length: NUM_STARS }).map(() => ({
            cx: Math.random() * 400,
            cy: Math.random() * 300,
            r: Math.random() * 0.7 + 0.2,
            duration: Math.random() * 2 + 1,
            delay: Math.random() * 2,
        }));
    }, []);

    const frameWidth = 60;
    const frameHeight = 80;
    const frameSpacing = 45;
    const totalWidth = (NUM_FRAMES - 1) * frameSpacing + frameWidth;

    return (
        <div className="w-full h-full flex items-center justify-center">
            <svg viewBox="0 0 400 300" className="w-full h-auto overflow-visible">
                <defs>
                    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                    <radialGradient id="end-glow" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                        <stop offset="0%" style={{ stopColor: '#38bdf8', stopOpacity: 1 }} />
                        <stop offset="100%" style={{ stopColor: '#0ea5e9', stopOpacity: 0.8 }} />
                    </radialGradient>
                </defs>

                {/* Starry Background */}
                <g>
                    {stars.map((star, i) => (
                        <motion.circle
                            key={i}
                            cx={star.cx}
                            cy={star.cy}
                            r={star.r}
                            fill="white"
                            opacity={0.7}
                            animate={{
                                opacity: [0.2, 0.7, 0.2],
                            }}
                            transition={{
                                duration: star.duration,
                                repeat: Infinity,
                                delay: star.delay,
                                ease: "easeInOut"
                            }}
                        />
                    ))}
                </g>

                <g transform="translate(10, 80) matrix(1, -0.4, 0.2, 1, 0, 0)">
                    {/* Glow Filter Group */}
                    <g filter="url(#glow)">

                        {/* Connection Line */}
                        <line
                            x1={frameWidth / 2}
                            y1={frameHeight / 2}
                            x2={totalWidth - frameWidth/2}
                            y2={frameHeight / 2}
                            stroke="#38bdf8"
                            strokeWidth="1"
                            strokeOpacity="0.8"
                        />

                        {/* Frames */}
                        {Array.from({ length: NUM_FRAMES -1 }).map((_, i) => (
                            <g key={i} transform={`translate(${i * frameSpacing}, 0)`}>
                                {[0, 1, 2].map(j => (
                                     <rect
                                        key={j}
                                        x={j*2}
                                        y={j*2}
                                        width={frameWidth - j*4}
                                        height={frameHeight - j*4}
                                        rx="8"
                                        ry="8"
                                        fill="none"
                                        stroke="#38bdf8"
                                        strokeWidth="0.7"
                                        strokeOpacity={1 - j*0.3}
                                    />
                                ))}
                            </g>
                        ))}

                        {/* Final Solid Rectangle */}
                        <g transform={`translate(${(NUM_FRAMES - 1) * frameSpacing}, 0)`}>
                             <rect
                                x="0"
                                y="0"
                                width={frameWidth}
                                height={frameHeight}
                                rx="8"
                                ry="8"
                                fill="url(#end-glow)"
                                stroke="#60a5fa"
                                strokeWidth="1.5"
                            />
                        </g>

                        {/* Sparkles */}
                         {Array.from({ length: NUM_SPARKLES }).map((_, i) => {
                            const duration = 2 + Math.random() * 2;
                            const delay = (duration / NUM_SPARKLES) * i;
                             return (
                                <motion.circle
                                    key={i}
                                    r="1.5"
                                    fill="#f0f9ff"
                                    initial={{
                                        x: frameWidth / 2,
                                        y: frameHeight / 2,
                                        opacity: 0
                                    }}
                                    animate={{
                                        x: [
                                            frameWidth / 2,
                                            totalWidth - frameWidth / 2,
                                        ],
                                        y: frameHeight / 2,
                                        opacity: [0, 1, 1, 0]
                                    }}
                                    transition={{
                                        duration,
                                        delay,
                                        repeat: Infinity,
                                        ease: 'linear',
                                        times: [0, 0.1, 0.9, 1]
                                    }}
                                />
                            );
                        })}
                    </g>
                </g>
            </svg>
        </div>
    );
};
