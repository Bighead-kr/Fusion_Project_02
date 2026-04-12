import type { Metadata } from 'next';
import './globals.css';
import { ReactNode } from 'react';
import BottomNav from './BottomNav'; // 👈 새로 만든 하단바 컴포넌트를 불러옵니다.

export const metadata: Metadata = {
  title: 'AI Outfits',
  description: 'AI-powered fashion recommendations and virtual closet',
};

// 플로팅 버튼 아이콘은 여기에 남겨둡니다.
const PlusIcon = () => (
  <svg viewBox="0 0 24 24">
    <line x1="12" y1="5" x2="12" y2="19"></line>
    <line x1="5" y1="12" x2="19" y2="12"></line>
  </svg>
);

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main>
          {children}

          {/* Floating Action Button */}
          <div style={{ position: 'fixed', bottom: '90px', right: '20px', zIndex: 1001 }}>
            <div className="tab-item floating-btn">
              <PlusIcon />
            </div>
          </div>

          {/* 👈 기존의 길었던 <nav> 코드를 지우고 이렇게 한 줄로 교체합니다! */}
          <BottomNav /> 
          
        </main>
      </body>
    </html>
  );
}