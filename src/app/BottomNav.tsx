'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const HomeIcon = () => (
  <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
);
const NetworkIcon = () => (
  <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
);
const ManualsIcon = () => (
  <svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
);
const ProfileIcon = () => (
  <svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
);

export default function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="tab-bar glass">
      {/* 주소가 '/' 일 때만 active 추가 */}
      <Link href="/" className={`tab-item ${pathname === '/' ? 'active' : ''}`}>
        <HomeIcon />
        Accueil
      </Link>
      
      {/* 주소가 '/network' 일 때만 active 추가 (필요시 href 수정) */}
      <Link href="/network" className={`tab-item ${pathname === '/network' ? 'active' : ''}`}>
        <NetworkIcon />
        Réseau
      </Link>
      
      {/* 주소가 '/manuals' 일 때만 active 추가 (필요시 href 수정) */}
      <Link href="/manuals" className={`tab-item ${pathname === '/manuals' ? 'active' : ''}`}>
        <ManualsIcon />
        Manuels
      </Link>
      
      {/* 주소가 '/my-page' 일 때만 active 추가 */}
      <Link href="/my-page" className={`tab-item ${pathname === '/my-page' ? 'active' : ''}`}>
        <ProfileIcon />
        Profil
      </Link>
    </nav>
  );
}