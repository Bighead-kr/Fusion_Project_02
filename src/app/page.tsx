export default function Home() {
  return (
    <div style={{ padding: '20px', paddingBottom: '100px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <h1 style={{ fontSize: '1.2rem', fontWeight: 600 }}>AI Outfits</h1>
        <div style={{ width: '40px', height: '40px', borderRadius: '20px', overflow: 'hidden' }}>
          <img src="/images/upload.png" alt="Profile" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
      </header>

      {/* User Bubble */}
      <div style={{ alignSelf: 'flex-end', maxWidth: '70%' }}>
        <div style={{ borderRadius: '16px', overflow: 'hidden', boxShadow: 'var(--shadow-sm)' }}>
          <img src="/images/upload.png" alt="Uploaded Outfit" style={{ width: '100%', display: 'block' }} />
        </div>
      </div>

      {/* AI Bubble */}
      <div className="glass" style={{ alignSelf: 'flex-start', maxWidth: '85%', padding: '16px', borderRadius: '20px', position: 'relative' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
          <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>AI recommends</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
        </div>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '8px' }}>Casual</h2>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
          Men's casual is a discreet everyday style built on a combination of simple basic clothing. It is universal, and its main principle is democracy, that is, a balance between the severity of classic outfits and the convenience of sportswear.
        </p>
      </div>

      <div style={{ alignSelf: 'flex-start', color: 'var(--text-secondary)' }}>
        ...
      </div>

      {/* Horizontal Recommendation Images */}
      <div style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '10px' }}>
        <img src="/images/recommend.png" alt="Recommend 1" style={{ width: '120px', height: '140px', objectFit: 'cover', borderRadius: '16px', flexShrink: 0 }} />
        <img src="/images/recommend.png" alt="Recommend 2" style={{ width: '140px', height: '140px', objectFit: 'cover', borderRadius: '16px', flexShrink: 0, transform: 'scale(1.05)', boxShadow: 'var(--shadow-sm)' }} />
        <img src="/images/recommend.png" alt="Recommend 3" style={{ width: '120px', height: '140px', objectFit: 'cover', borderRadius: '16px', flexShrink: 0 }} />
      </div>

      {/* Button */}
      <button className="glass" style={{ margin: '0 auto', padding: '10px 24px', borderRadius: '20px', border: '1px solid var(--glass-border)', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 600 }}>
        Again
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="1 4 1 10 7 10"></polyline>
          <polyline points="23 20 23 14 17 14"></polyline>
          <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
        </svg>
      </button>

      {/* Chat Input */}
      <div className="glass" style={{ position: 'fixed', bottom: '100px', left: '50%', transform: 'translateX(-50%)', width: 'calc(100% - 40px)', maxWidth: '440px', height: '56px', borderRadius: '28px', display: 'flex', alignItems: 'center', padding: '0 8px 0 20px', justifySelf: 'center', zIndex: 10 }}>
        <input type="text" placeholder="Send massage" style={{ flex: 1, border: 'none', background: 'transparent', outline: 'none', color: 'var(--text-primary)', fontSize: '0.95rem' }} />
        <div style={{ background: 'var(--primary)', color: 'var(--bg-color)', width: '32px', height: '32px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginRight: '10px' }}>
           <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="12" y1="19" x2="12" y2="5"></line>
            <polyline points="5 12 12 5 19 12"></polyline>
          </svg>
        </div>
        <img src="/images/upload.png" alt="Attach" style={{ width: '40px', height: '40px', borderRadius: '12px', objectFit: 'cover' }} />
      </div>
    </div>
  );
}
