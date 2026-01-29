<!--
 * @component AppBackground
 * @style Fluid Silk (High-End)
 * @description 无网格、流体弥散光感背景，带有微噪点纸质纹理
-->
<template>
  <div class="app-background">
    <div class="bg-color"></div>
    
    <!-- 流动的光斑 -->
    <div class="orb orb-warm"></div>
    <div class="orb orb-cool"></div>
    <div class="orb orb-light"></div>
    
    <!-- 噪点纹理 (提升质感的关键) -->
    <div class="noise-overlay"></div>
  </div>
</template>

<style scoped>
.app-background {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  z-index: 0;
  overflow: hidden;
  /* 基底：极浅的暖灰白，比冷白更有温度 */
  background-color: #fcfcfc;
}

/* 1. 暖色光斑 (呼应你的活力橙主题) */
.orb-warm {
  position: absolute;
  top: -20%;
  right: -10%;
  width: 80vw;
  height: 80vw;
  background: radial-gradient(circle, rgba(251, 146, 60, 0.08) 0%, rgba(255, 255, 255, 0) 70%);
  border-radius: 50%;
  filter: blur(80px); /* 极度柔化 */
  animation: float 20s ease-in-out infinite alternate;
}

/* 2. 冷色光斑 (增加层次感，避免全是暖色太腻) */
.orb-cool {
  position: absolute;
  bottom: -20%;
  left: -10%;
  width: 70vw;
  height: 70vw;
  /* 使用极淡的蓝紫色，制造空间景深 */
  background: radial-gradient(circle, rgba(99, 102, 241, 0.06) 0%, rgba(255, 255, 255, 0) 70%);
  border-radius: 50%;
  filter: blur(100px);
  animation: float-reverse 25s ease-in-out infinite alternate;
}

/* 3. 高光点缀 (让画面透气) */
.orb-light {
  position: absolute;
  top: 30%;
  left: 40%;
  width: 40vw;
  height: 40vw;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 60%);
  border-radius: 50%;
  mix-blend-mode: overlay; /* 叠加模式 */
  animation: breathe 15s ease-in-out infinite;
}

/* 4. 核心质感：SVG 噪点叠加 */
/* 这层纹理能消除色带(banding)，并带来“磨砂纸”般的高级触感 */
.noise-overlay {
  position: absolute;
  inset: 0;
  opacity: 0.04; /* 极低透明度，若隐若现 */
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  pointer-events: none;
}

/* 缓慢的流动动画，不干扰视线 */
@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-30px, 50px) scale(1.05); }
}

@keyframes float-reverse {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(40px, -30px) scale(1.1); }
}

@keyframes breathe {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}
</style>