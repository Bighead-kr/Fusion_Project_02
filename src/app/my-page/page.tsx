'use client';

import { useState } from 'react';

export default function MyPage() {
  const [activeCategory, setActiveCategory] = useState<any>(null);

  const categories = [
    { id: 1, name: '상의', items: 24, privacy: '비공개', image: '/images/tops.png', bg: '#f1f5f9' },
    { id: 2, name: '하의', items: 12, privacy: '비공개', image: '/images/recommend.png', bg: '#f8fafc' },
    { id: 3, name: '아우터', items: 8, privacy: '비공개', image: '/images/upload.png', bg: '#f1f5f9' },
    { id: 4, name: '신발', items: 15, privacy: '공개', image: '/images/recommend.png', bg: '#f8fafc' },
  ];

  const mockImages = [
    '/images/tops.png', '/images/recommend.png', '/images/upload.png',
    '/images/recommend.png', '/images/tops.png', '/images/upload.png',
    '/images/tops.png', '/images/recommend.png', '/images/upload.png',
    '/images/recommend.png', '/images/tops.png', '/images/upload.png'
  ];

  if (activeCategory) {
    return (
      <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px', height: '100%', overflowY: 'auto' }}>
        <header style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <button 
            onClick={() => setActiveCategory(null)}
            style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '5px' }}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
          </button>
          <h1 style={{ fontSize: '1.2rem', fontWeight: 600 }}>{activeCategory.name}</h1>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{activeCategory.items} 아이템</span>
        </header>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px' }}>
          {mockImages.map((img, idx) => (
            <div key={idx} style={{ aspectRatio: '1/1', borderRadius: '12px', overflow: 'hidden', background: '#f1f5f9' }}>
              <img src={img} alt={`Item ${idx}`} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '30px' }}>
      {/* Header */}
      <header style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <h1 style={{ fontSize: '1.2rem', fontWeight: 600, color: 'var(--text-secondary)' }}>My Closet</h1>
      </header>

      {/* Grid Menu */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', rowGap: '40px' }}>
        {categories.slice(0, 2).map((cat) => (
          <CategoryCard key={cat.id} category={cat} onClick={() => setActiveCategory(cat)} />
        ))}
      </div>

      {/* Divider */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Seasons</span>
        <div style={{ height: '1px', background: 'var(--glass-border)', flex: 1 }}></div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', rowGap: '40px' }}>
        {categories.slice(2, 4).map((cat) => (
          <CategoryCard key={cat.id} category={cat} onClick={() => setActiveCategory(cat)} />
        ))}
      </div>
    </div>
  );
}

function CategoryCard({ category, onClick }: { category: any, onClick: () => void }) {
  return (
    <div 
      onClick={onClick}
      style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', cursor: 'pointer' }}
    >
      <div style={{ position: 'relative', width: '120px', height: '120px', marginBottom: '16px' }}>
        {/* Background card 2 */}
        <div className="glass" style={{
          position: 'absolute', top: '10px', left: '-10px', right: '10px', bottom: '-10px', borderRadius: '16px', zIndex: 1,
          background: 'rgba(56, 189, 248, 0.4)', transform: 'rotate(-5deg)'
        }}></div>
        {/* Background card 1 */}
        <div className="glass" style={{
          position: 'absolute', top: '5px', left: '10px', right: '-10px', bottom: '-5px', borderRadius: '16px', zIndex: 2,
          background: 'rgba(255, 255, 255, 0.6)', transform: 'rotate(5deg)'
        }}></div>
        {/* Main image */}
        <div style={{
          position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, borderRadius: '20px', zIndex: 3,
          overflow: 'hidden', boxShadow: 'var(--shadow-sm)', background: category.bg
        }}>
          <img src={category.image} alt={category.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
      </div>
      <h3 style={{ fontSize: '0.9rem', fontWeight: 600, textAlign: 'center', marginBottom: '4px' }}>{category.name}</h3>
      <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-secondary)', fontSize: '0.8rem' }}>
        <span>{category.privacy}</span>
        {category.privacy === '비공개' ? (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        ) : (
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="2" y1="12" x2="22" y2="12"></line>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
          </svg>
        )}
      </div>
    </div>
  );
}
