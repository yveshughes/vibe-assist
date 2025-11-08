import React from 'react';
import { motion } from 'framer-motion';

const NUM_STARS = 100;

export const VisionAnimation: React.FC = () => {
    const stars = React.useMemo(() => {
        return Array.from({ length: NUM_STARS }).map(() => ({
            cx: Math.random() * 400,
            cy: Math.random() * 300,
            r: Math.random() * 0.7 + 0.2,
            duration: Math.random() * 2 + 1,
            delay: Math.random() * 2,
        }));
    }, []);

    return (
        <div className="w-full h-full flex items-center justify-center">
            <svg viewBox="0 0 400 300" className="w-full h-auto overflow-visible">
                <defs>
                    <filter id="glow-vision" x="-50%" y="-50%" width="200%" height="200%">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                    <radialGradient id="star-glow" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                        <stop offset="0%" style={{ stopColor: '#fde047', stopOpacity: 1 }} />
                        <stop offset="100%" style={{ stopColor: '#facc15', stopOpacity: 0 }} />
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

                <g transform="translate(200, 150)" filter="url(#glow-vision)">
                    {/* Compass Outer Ring */}
                    <circle cx="0" cy="0" r="100" stroke="#facc15" strokeWidth="1.5" fill="none" opacity="0.6" />
                    <circle cx="0" cy="0" r="95" stroke="#facc15" strokeWidth="0.5" fill="none" opacity="0.4" />
                    
                    {/* Compass Tick Marks */}
                    {Array.from({ length: 12 }).map((_, i) => {
                        const angle = (i / 12) * 360;
                        return (
                            <line
                                key={i}
                                x1={85 * Math.cos(angle * Math.PI / 180)}
                                y1={85 * Math.sin(angle * Math.PI / 180)}
                                x2={95 * Math.cos(angle * Math.PI / 180)}
                                y2={95 * Math.sin(angle * Math.PI / 180)}
                                stroke="#fde047"
                                strokeWidth="1.5"
                            />
                        );
                    })}
                    
                    {/* Drifting Path visualization */}
                    <motion.path
                        d="M 0 0 C 30 -50, -20 -70, 0 -90"
                        fill="none"
                        stroke="#fbbf24"
                        strokeWidth="1"
                        strokeDasharray="3 3"
                        initial={{ pathLength: 0, opacity: 0 }}
                        animate={{ pathLength: 1, opacity: [0, 0.7, 0] }}
                        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut", delay: 0.5, times: [0, 0.5, 1] }}
                    />

                    {/* Guiding Star (Vision) */}
                    <g transform="translate(0, -90)">
                        <motion.circle cx="0" cy="0" r="12" fill="url(#star-glow)" 
                            animate={{ scale: [1, 1.15, 1]}}
                            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut"}}
                        />
                        <motion.circle cx="0" cy="0" r="4" fill="#fff" />
                    </g>
                    
                    {/* Compass Needle */}
                    <motion.g
                        initial={{ rotate: -30 }}
                        animate={{ rotate: [ -30, 20, -15, 10, 0, 0, 0, 0 ] }}
                        transition={{
                            duration: 4,
                            repeat: Infinity,
                            ease: "easeInOut",
                        }}
                    >
                         <polygon points="0,0 -7,-80 0,-100 7,-80" fill="#fde047" />
                         <polygon points="0,0 -5,55 0,65 5,55" fill="#fde047" opacity="0.5" />
                    </motion.g>

                    {/* Center point */}
                    <circle cx="0" cy="0" r="4" fill="#fde047" />
                </g>
            </svg>
        </div>
    );
};