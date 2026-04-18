'use client';

import { useState, useEffect } from 'react';

export default function MyPage() {
  const [items, setItems] = useState<any[]>([]);
  const [activeCategory, setActiveCategory] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/closet')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setItems(data.items);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch closet:', err);
        setLoading(false);
      });
  }, []);

  const getCategoryData = (name: string) => {
    const categoryItems = items.filter(item => item.category === name);
    return {
      name,
      items: categoryItems.length,
      privacy: '비공개',
      image: categoryItems.length > 0 ? categoryItems[0].image_url : '/images/recommend.png',
      bg: name === '상의' || name === '아우터' ? '#f1f5f9' : '#f8fafc',
      allItems: categoryItems
    };
  };

  const categories = [
    getCategoryData('상의'),
    getCategoryData('하의'),
    getCategoryData('아우터'),
    getCategoryData('원피스/치마'), // 통합 카테고리
  ];

  if (activeCategory) {
    const categoryDetail = categories.find(c => c.name === activeCategory.name);
    const displayItems = categoryDetail?.allItems || [];

    return (
      <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '20px', height: '100%', overflowY: 'auto' }}>
        <header style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <button 
            onClick={() => setActiveCategory(null)}
            style={{ background: 'none', border: 'none', cursor: 'pointer', padding: '5px' }}
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--back-btn-color)" strokeWidth="2">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
          </button>
          <h1 style={{ fontSize: '1.2rem', fontWeight: 600 }}>{activeCategory.name}</h1>
          <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{displayItems.length} 아이템</span>
        </header>

        {displayItems.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '100px 0', color: 'var(--text-secondary)' }}>
            아이템이 없습니다.
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px' }}>
            {displayItems.map((item, idx) => (
              <div key={idx} style={{ aspectRatio: '1/1', borderRadius: '12px', overflow: 'hidden', background: '#f1f5f9' }}>
                <img src={item.image_url} alt={item.sub_category} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              </div>
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '30px', height: '100%', overflowY: 'auto' }}>
      {/* Header */}
      <header style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <h1 style={{ fontSize: '1.2rem', fontWeight: 600, color: 'var(--text-secondary)' }}>My Closet</h1>
      </header>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '50px', color: 'var(--text-secondary)' }}>로딩 중...</div>
      ) : (
        <>
          {/* Grid Menu */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', rowGap: '40px' }}>
            {categories.slice(0, 2).map((cat, idx) => (
              <CategoryCard key={idx} category={cat} onClick={() => setActiveCategory(cat)} />
            ))}
          </div>

          {/* Divider */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 500 }}>Others</span>
            <div style={{ height: '1px', background: 'var(--glass-border)', flex: 1 }}></div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', rowGap: '40px' }}>
            {categories.slice(2, 4).map((cat, idx) => (
              <CategoryCard key={idx} category={cat} onClick={() => setActiveCategory(cat)} />
            ))}
          </div>
        </>
      )}
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
