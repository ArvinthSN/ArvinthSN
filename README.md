<!--
GitHub README — Premium AI Engineer Portfolio
Designed for: Arvinth S.N.
Theme: Neon violet, electric blue, emerald green, glassmorphism, cyberpunk
-->

<div align="center">
  <img src="Assets/profile-hero.svg" width="100%" alt="Arvinth S.N. Hero Banner" />
</div>

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Orbitron&size=32&duration=1800&pause=900&color=A855F7&center=true&vCenter=true&width=900&lines=AI+Engineer;Software+Engineer;Full+Stack+Developer;Data+Analytics+Enthusiast;Building+Intelligent+Systems;Future+Product+Engineer" alt="Arvinth S.N. typing banner" />
</div>

## ⚡ React Motion Banner

Use this animated text effect for the hero banner in a React/Next.js app:

```tsx
'use client';

import { motion, useReducedMotion } from 'framer-motion';
import { useEffect, useMemo, useRef, useState } from 'react';

const clamp = (value: number, min: number, max: number) =>
  Math.min(Math.max(value, min), max);

const MAX_LAYERS = 64;

const getLayerColor = (faceColor: string, depthColor: string, index: number, total: number) => {
  const progress = total <= 1 ? 1 : index / total;
  const eased = progress * progress;
  const faceMix = Math.round((1 - eased) * 72 + 4);
  return `color-mix(in srgb, ${faceColor} ${faceMix}%, ${depthColor})`;
};

type DepthTextProps = {
  text?: string;
  layers?: number;
  depth?: number;
  faceColor?: string;
  depthColor?: string;
  tilt?: number;
  pointerTracking?: boolean;
  smoothing?: number;
  perspective?: number;
  autoOrbit?: boolean;
  orbitSpeed?: number;
  fontSize?: string;
  fontWeight?: number;
  shadow?: boolean;
  className?: string;
};

export default function DepthText({
  text = 'Elevate',
  layers = 34,
  depth = 2.4,
  faceColor = '#f8fafc',
  depthColor = '#7c3aed',
  tilt = 7.5,
  pointerTracking = true,
  smoothing = 0.14,
  perspective = 900,
  autoOrbit = true,
  orbitSpeed = 0.35,
  fontSize = 'clamp(3rem, 12vw, 7rem)',
  fontWeight = 900,
  shadow = true,
  className = '',
}: DepthTextProps) {
  const rootRef = useRef<HTMLSpanElement | null>(null);
  const safeLayers = clamp(Math.round(Number(layers) || 1), 2, MAX_LAYERS);
  const safeDepth = clamp(Number(depth) || 0, 0, 12);
  const safeTilt = clamp(Number(tilt) || 0, 0, 12);
  const safeSmoothing = clamp(Number(smoothing) || 0.14, 0.02, 0.35);
  const safePerspective = clamp(Number(perspective) || 900, 300, 2000);
  const safeOrbitSpeed = clamp(Number(orbitSpeed) || 0, 0, 2);
  const reducedMotion = useReducedMotion();
  const [pointer, setPointer] = useState({ x: 0, y: 0 });
  const [isPointerActive, setIsPointerActive] = useState(false);

  const depthLayers = useMemo(
    () =>
      Array.from({ length: safeLayers }, (_, layerIndex) => {
        const index = safeLayers - layerIndex;
        return {
          index,
          color: getLayerColor(faceColor, depthColor, index, safeLayers),
          z: -index * safeDepth,
        };
      }),
    [safeLayers, safeDepth, faceColor, depthColor]
  );

  useEffect(() => {
    if (!rootRef.current || reducedMotion || typeof window === 'undefined') return;

    const root = rootRef.current;

    const handlePointerMove = (event: PointerEvent) => {
      const rect = root.getBoundingClientRect();
      if (!rect.width || !rect.height) return;

      const x = clamp((event.clientX - (rect.left + rect.width / 2)) / (rect.width * 0.8), -1, 1);
      const y = clamp((event.clientY - (rect.top + rect.height / 2)) / (rect.height * 0.8), -1, 1);

      setPointer({ x, y });
      setIsPointerActive(true);
    };

    const handlePointerLeave = () => {
      setIsPointerActive(false);
      setPointer({ x: 0, y: 0 });
    };

    if (pointerTracking) {
      window.addEventListener('pointermove', handlePointerMove);
      window.addEventListener('pointerleave', handlePointerLeave);
      window.addEventListener('blur', handlePointerLeave);
    }

    return () => {
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('pointerleave', handlePointerLeave);
      window.removeEventListener('blur', handlePointerLeave);
    };
  }, [pointerTracking, reducedMotion]);

  useEffect(() => {
    if (reducedMotion) return;
    if (!autoOrbit || isPointerActive) return;

    const id = window.setInterval(() => {
      const angle = performance.now() * 0.0006 * safeOrbitSpeed;
      const nextX = -safeTilt * 0.32 + Math.sin(angle) * safeTilt * 0.55;
      const nextY = safeTilt * 0.42 + Math.cos(angle * 0.85) * safeTilt * 0.55;

      if (rootRef.current) {
        rootRef.current.style.transform = `rotateX(${nextX.toFixed(3)}deg) rotateY(${nextY.toFixed(3)}deg)`;
      }
    }, 16);

    return () => window.clearInterval(id);
  }, [autoOrbit, isPointerActive, reducedMotion, safeOrbitSpeed, safeTilt]);

  useEffect(() => {
    if (reducedMotion || !rootRef.current) return;

    const targetX = -safeTilt * 0.32 - pointer.y * safeTilt;
    const targetY = safeTilt * 0.42 + pointer.x * safeTilt;
    rootRef.current.style.transform = `rotateX(${targetX.toFixed(3)}deg) rotateY(${targetY.toFixed(3)}deg)`;
  }, [pointer, pointerTracking, reducedMotion, safeTilt]);

  const rootStyle = {
    perspective: `${safePerspective}px`,
    fontSize,
    fontWeight,
    ['--depth-text-face-color' as any]: faceColor,
    ['--depth-text-depth-color' as any]: depthColor,
    ['--depth-text-shadow' as any]: shadow
      ? `0 22px 34px color-mix(in srgb, ${depthColor} 36%, transparent), 0 4px 8px rgba(0, 0, 0, 0.28)`
      : 'none',
  } as React.CSSProperties;

  return (
    <span ref={rootRef} className={`depth-text ${className}`.trim()} style={rootStyle}>
      <span className="depth-text__stage">
        {depthLayers.map((layer) => (
          <motion.span
            aria-hidden="true"
            className="depth-text__layer"
            key={layer.index}
            style={{
              color: layer.color,
              transform: `translateZ(${layer.z}px)`,
            }}
            animate={{ opacity: [0.5, 1, 0.85] }}
            transition={{ duration: 2.2, repeat: Infinity, ease: 'easeInOut', delay: layer.index * 0.02 }}
          >
            {text}
          </motion.span>
        ))}
        <motion.span
          className="depth-text__face"
          animate={{
            filter: [
              'drop-shadow(0 0 0 rgba(168,85,247,0))',
              'drop-shadow(0 0 18px rgba(168,85,247,0.7))',
              'drop-shadow(0 0 0 rgba(168,85,247,0))',
            ],
          }}
          transition={{ duration: 2.5, repeat: Infinity, ease: 'easeInOut' }}
        >
          {text}
        </motion.span>
      </span>
    </span>
  );
}
```

```css
.depth-text {
  display: inline-block;
  perspective: var(--depth-text-perspective, 900px);
  perspective-origin: 50% 48%;
  isolation: isolate;
}

.depth-text__stage {
  position: relative;
  display: inline-grid;
  place-items: center;
  transform-style: preserve-3d;
  transform-origin: 50% 50%;
  will-change: transform;
}

.depth-text__layer,
.depth-text__face {
  grid-area: 1 / 1;
  display: inline-block;
  font-size: var(--depth-text-font-size, clamp(3rem, 12vw, 7rem));
  font-weight: var(--depth-text-font-weight, 900);
  line-height: 0.86;
  letter-spacing: -0.065em;
  white-space: nowrap;
  user-select: none;
  transform-style: preserve-3d;
  backface-visibility: hidden;
  font-kerning: normal;
  text-rendering: geometricPrecision;
}

.depth-text__layer {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  filter: saturate(0.95) brightness(0.9);
}

.depth-text__face {
  position: relative;
  z-index: 1;
  color: var(--depth-text-face-color, #f8fafc);
  text-shadow: var(--depth-text-shadow, none);
  transform: translateZ(0.6px);
}
```

### ✨ StarBorder Glow Button Variant

```tsx
import StarBorder from './StarBorder';

<StarBorder as="button" className="custom-class" color="#A855F7" speed="5s">
  Elevate
</StarBorder>
```

```tsx
'use client';

import './StarBorder.css';

const StarBorder = ({
  as: Component = 'button',
  className = '',
  color = 'white',
  speed = '6s',
  thickness = 1,
  backgroundColor = '#000000',
  textColor = '#ffffff',
  borderColor = '#222222',
  children,
  ...rest
}) => {
  return (
    <Component
      className={`star-border-container ${className}`}
      style={{
        padding: `${thickness}px 0`,
        ...rest.style,
      }}
      {...rest}
    >
      <div
        className="border-gradient-bottom"
        style={{
          background: `radial-gradient(circle, ${color}, transparent 10%)`,
          animationDuration: speed,
        }}
      />
      <div
        className="border-gradient-top"
        style={{
          background: `radial-gradient(circle, ${color}, transparent 10%)`,
          animationDuration: speed,
        }}
      />
      <div
        className="inner-content"
        style={{ background: backgroundColor, color: textColor, borderColor }}
      >
        {children}
      </div>
    </Component>
  );
};

export default StarBorder;
```

```css
.star-border-container {
  display: inline-block;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
}

.border-gradient-bottom {
  position: absolute;
  width: 300%;
  height: 50%;
  opacity: 0.7;
  bottom: -12px;
  right: -250%;
  border-radius: 50%;
  animation: star-movement-bottom linear infinite alternate;
  z-index: 0;
}

.border-gradient-top {
  position: absolute;
  opacity: 0.7;
  width: 300%;
  height: 50%;
  top: -12px;
  left: -250%;
  border-radius: 50%;
  animation: star-movement-top linear infinite alternate;
  z-index: 0;
}

.inner-content {
  position: relative;
  border: 1px solid #222;
  background: #000;
  color: white;
  font-size: 16px;
  text-align: center;
  padding: 16px 26px;
  border-radius: 20px;
  z-index: 1;
}

@keyframes star-movement-bottom {
  0% {
    transform: translate(0%, 0%);
    opacity: 1;
  }
  100% {
    transform: translate(-100%, 0%);
    opacity: 0;
  }
}

@keyframes star-movement-top {
  0% {
    transform: translate(0%, 0%);
    opacity: 1;
  }
  100% {
    transform: translate(100%, 0%);
    opacity: 0;
  }
}
```

Usage example:

```tsx
import DepthText from './DepthText';

export default function Hero() {
  return (
    <DepthText
      text="Elevate"
      layers={34}
      depth={2.4}
      faceColor="#f8fafc"
      depthColor="#7c3aed"
      tilt={7.5}
      pointerTracking
      smoothing={0.14}
      perspective={900}
      autoOrbit
      orbitSpeed={0.35}
      fontSize="clamp(3rem, 12vw, 7rem)"
      fontWeight={900}
      shadow
    />
  );
}
```

---

<h1 align="center">
  <span style="color:#A855F7;">Arvinth</span>
  <span style="color:#00D4FF;">S.N.</span>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/AI%20Engineer-A855F7?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Software%20Engineer-00D4FF?style=for-the-badge&logo=codeforces&logoColor=white" />
  <img src="https://img.shields.io/badge/Data%20Analyst-00FFB3?style=for-the-badge&logo=googleanalytics&logoColor=black" />
  <img src="https://img.shields.io/badge/Full%20Stack%20Developer-00D4FF?style=for-the-badge&logo=github&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Tiruppur%2C%20India-050816?style=flat-square&logo=googlemaps&logoColor=00D4FF" />
  <img src="https://img.shields.io/badge/ValueMomentum%20%28Owlsure%29-050816?style=flat-square&logo=rocket&logoColor=00FFB3" />
</p>

> "I don't just write code. I engineer systems that solve real-world problems."

<div align="center">
  <img src="https://img.shields.io/badge/Open%20to%20Collaboration-Yes-00FFB3?style=for-the-badge&logo=handshake&logoColor=black" />
  <img src="https://img.shields.io/badge/Current%20Focus-AI%20%7C%20Full%20Stack%20%7C%20Data-00D4FF?style=for-the-badge&logo=githubactions&logoColor=white" />
</div>

---

## 🧠 3D Developer Card

<table>
  <tr>
    <td width="220" align="center">
      <img src="https://avatars.githubusercontent.com/u/0?v=4" width="170" style="border-radius: 24px; border: 2px solid #A855F7; box-shadow: 0 0 24px rgba(168,85,247,0.7);" alt="Arvinth profile" />
    </td>
    <td valign="middle">
      <h3 style="color:#A855F7; margin: 0 0 8px 0;">AI Engineer • Software Engineer • Data Analyst • Full Stack Developer</h3>
      <p><strong>📍</strong> Tiruppur, India</p>
      <p><strong>💼</strong> ValueMomentum (Owlsure)</p>
      <p><strong>🎓</strong> B.Sc Computer Science with Data Analytics</p>
      <p><strong>⚡</strong> Current Focus: AI systems, product engineering, backend architecture, analytics</p>
    </td>
  </tr>
</table>

---

## 🏆 Achievement Timeline

<div align="center">
  <img src="https://img.shields.io/badge/Best%20Trainee%20Award-🏆-A855F7?style=for-the-badge&logo=trophy&logoColor=white" />
  <img src="https://img.shields.io/badge/NPTEL%20Java-Silver%20Medal-00FFB3?style=for-the-badge&logo=java&logoColor=black" />
  <img src="https://img.shields.io/badge/Python%20for%20Data%20Science-🎓-00D4FF?style=for-the-badge&logo=python&logoColor=white" />
</div>

- 🏆 Best Trainee Award
- 🥈 NPTEL Java Silver Medal
- 🎓 IIT Madras Python for Data Science
- 🏅 NPTEL Programming in C
- 📊 Datathon Third Place
- 🤝 NSS Participation
- 💼 NitroWare Internship

---

## ⚙️ 3D Tech Stack

<div align="center">
  <img src="https://skillicons.dev/icons?i=java,python,sql,c,react,tailwind,javascript,fastapi,spring,nodejs,postgresql,mongodb,supabase,openai,langchain,php,docker,git,github,linux&theme=dark" alt="Tech stack" />
</div>

### Languages
- Java
- Python
- SQL
- C

### Frontend
- React
- Tailwind
- JavaScript

### Backend
- FastAPI
- Spring Boot
- Node.js

### Databases
- PostgreSQL
- MongoDB
- Supabase

### AI
- OpenAI
- LangChain
- RAG
- Qdrant

### Data
- Power BI
- Tableau
- Pandas
- NumPy

### DevOps
- Docker
- Git
- GitHub
- Linux

---

## 🧠 Animated Skill Matrix

<div align="center">
  <img src="Assets/skill-network.svg" width="100%" alt="Skill network diagram" />
</div>

- AI
- Backend
- Frontend
- Cloud
- Data
- System Design

---

## 🚀 Featured Projects

### SYNOVA
AI Insurance Aggregator • Voice Agent • RAG • OCR • FastAPI • React • PostgreSQL

<div align="center">
  <img width="900" src="https://user-images.githubusercontent.com/42633287/184486595-1e3fdc31-7006-4a59-be38-6c8d4d1a56ff.png" alt="SYNOVA dashboard" />
</div>

### Global LLM Market Analytics
ETL • Power BI • PostgreSQL • Hugging Face • Analytics

<div align="center">
  <img width="900" src="https://user-images.githubusercontent.com/42633287/170160272-0d2ea9b9-7d32-4fe7-b1ec-4d9e096f1d76.png" alt="Global LLM analytics dashboard" />
</div>

### AI Call Center Analytics
Speech to Text • NLP • Classification • Real-Time Monitoring

<div align="center">
  <img width="900" src="https://user-images.githubusercontent.com/42633287/163477229-8d86d0d0-4a5d-45f3-9620-d2872bbdb744.png" alt="AI call center dashboard" />
</div>

---

## 📊 Advanced GitHub Stats

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=arvinthsn&show_icons=true&hide_border=true&theme=radical&title_color=A855F7&icon_color=00D4FF&text_color=E5E7EB&bg_color=050816" alt="GitHub Stats" />
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=arvinthsn&theme=dark&hide_border=true&background=050816&stroke=00D4FF&ring=A855F7&fire=00FFB3&currStreakLabel=00D4FF" alt="GitHub streak stats" />
</div>

<div align="center">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=arvinthsn&layout=compact&theme=radical&hide_border=true&bg_color=050816&title_color=A855F7&text_color=E5E7EB&icon_color=00D4FF" alt="Most used languages" />
</div>

---

## 🐍 Feeding My Consistency Every Day

<div align="center">
  <img src="https://raw.githubusercontent.com/platane/platane/output/github-contribution-grid-snake.svg" width="850" alt="Contribution snake" />
</div>

> Success is consistency compounded.

---

## 🌌 Contribution Galaxy

Every commit tells a story.

<div align="center">
  <img src="https://raw.githubusercontent.com/pavithran26/pavithran26/main/profile-3d-contrib/profile-night-rainbow.svg" width="1000" alt="3D contribution graph" />
</div>

---

## 🌟 Developer Philosophy

> Build before you're ready.

> Consistency beats motivation.

> The future belongs to engineers who combine AI with software.

> Every bug is a lesson in disguise.

> Learn. Build. Share. Repeat.

---

## 🔗 Connect

<div align="center">
  <a href="https://github.com/ArvinthSN" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="https://www.linkedin.com/in/arvinth-s-n/" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="mailto:arvinthsn.dev@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
</div>

> Build. Learn. Ship. Repeat.

---

<div align="center">
  <img src="Assets/image.png" width="100%" alt="Arvinth S.N. final artwork" />
</div>
