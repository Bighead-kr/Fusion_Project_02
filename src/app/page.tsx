'use client';

import { useState, useEffect, useRef } from 'react';

export default function Home() {
  const [messages, setMessages] = useState<any[]>([
    {
      id: 1,
      type: 'ai',
      recommends: true,
      title: '캐주얼',
      content: '남성 캐주얼은 심플하고 기본적인 의류의 조합으로 완성되는 산뜻한 데일리 스타일입니다. 보편적이고 민주적인 스타일을 지향하며, 클래식한 의상의 품격과 스포츠웨어의 편안함 사이의 균형을 맞추는 것이 핵심 원칙입니다.',
      images: ['/images/recommend.png', '/images/recommend.png', '/images/recommend.png']
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [isComposing, setIsComposing] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [weather, setWeather] = useState<{ temp: number; desc: string } | null>(null);
  const [showPlusMenu, setShowPlusMenu] = useState(false);
  
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    // 초기 날씨 정보 로드
    fetch('http://localhost:8000/weather')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setWeather({ temp: data.temp, desc: data.description });
        }
      })
      .catch(err => console.error('날씨 로드 실패:', err));
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isThinking, suggestions]);

  const handleSend = async (text: string, bypassFilter = false) => {
    if (!text.trim()) return;

    // 사용자 메시지 추가
    const newMessage = { id: Date.now(), type: 'user', content: text };
    setMessages(prev => [...prev, newMessage]);
    setInputText('');
    setSuggestions([]);

    // AI 생각 중 표시
    setIsThinking(true);

    try {
      // 백엔드 추천 API 호출
      const url = `http://localhost:8000/recommend?situation=${encodeURIComponent(text)}&mood=캐주얼&bypass_filter=${bypassFilter}`;
      const response = await fetch(url);
      const data = await response.json();

      setIsThinking(false);

      if (data.status === 'success') {
        const rec = data.recommendation;
        const aiResponse = {
          id: Date.now() + 1,
          type: 'ai',
          recommends: true,
          title: rec.ref_name,
          content: `${rec.ref_name} 스타일을 추천해 드려요. ${data.weather.temp}도의 날씨에 적합한 조합입니다.`,
          images: rec.items.map((item: any) => item.image_url),
          details: rec.items.map((item: any) => `${item.category}: ${item.color} ${item.sub_category}`)
        };
        setMessages(prev => [...prev, aiResponse]);
        setSuggestions(['다른 스타일 추천해줘', '상세 정보 알려줘', '내일은 어때?']);
      } else {
        const errorResponse = {
          id: Date.now() + 1,
          type: 'ai',
          content: data.message || '추천 결과를 가져오는데 실패했습니다.'
        };
        setMessages(prev => [...prev, errorResponse]);
      }
    } catch (error) {
      console.error('API 호출 에러:', error);
      setIsThinking(false);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        type: 'ai',
        content: '서버와 통신하는 중 오류가 발생했습니다. 백엔드 서버가 실행 중인지 확인해 주세요.'
      }]);
    }
  };

  const handleSelectSuggestion = (suggestion: string) => {
    handleSend(suggestion, true); // UI 버튼 클릭은 필터 우회
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setShowPlusMenu(false);
    setIsThinking(true);
    setMessages(prev => [...prev, { id: Date.now(), type: 'user', content: '📷 사진 업로드 중...', isImage: true }]);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setIsThinking(false);

      if (data.status === 'success') {
        setMessages(prev => [...prev, {
          id: Date.now(),
          type: 'ai',
          content: `✅ 옷 분석을 완료했습니다! 마이페이지에서 확인해보세요.\n\n분석 결과: ${data.item.color} ${data.item.sub_category} (${data.item.style})`,
          image: data.item.image_url
        }]);
      } else {
        setMessages(prev => [...prev, { id: Date.now(), type: 'ai', content: '❌ 사진 분석에 실패했습니다: ' + data.message }]);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setIsThinking(false);
      setMessages(prev => [...prev, { id: Date.now(), type: 'ai', content: '❌ 서버 통신 중 오류가 발생했습니다.' }]);
    }
  };

  return (
    <div style={{ position: 'relative', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <input 
        type="file" 
        ref={fileInputRef} 
        style={{ display: 'none' }} 
        accept="image/*"
        onChange={handleFileChange}
      />
      
      <div
        ref={scrollRef}
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '20px',
          paddingBottom: '180px',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px'
        }}
      >
        {/* Header */}
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
          <h1 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Mapsee</h1>
          <div style={{ width: '40px', height: '40px', borderRadius: '20px', overflow: 'hidden' }}>
            <img src="/images/upload.png" alt="Profile" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          </div>
        </header>

        {/* Chat History */}
        {messages.map((msg) => (
          <div key={msg.id} style={{ alignSelf: msg.type === 'user' ? 'flex-end' : 'flex-start', maxWidth: msg.type === 'user' ? '70%' : '85%' }}>
            {msg.type === 'user' ? (
              <div style={{ background: '#3b82f6', color: 'white', padding: '12px 16px', borderRadius: '18px 18px 2px 18px', fontSize: '0.95rem' }}>
                {msg.content}
              </div>
            ) : (
              <div className={msg.recommends ? "glass" : "solid-bg"} style={{ padding: '16px', borderRadius: '20px', position: 'relative', border: msg.recommends ? 'none' : '1px solid var(--glass-border)' }}>
                {msg.recommends && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
                    <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)' }}>AI 추천</span>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                    </svg>
                  </div>
                )}
                {msg.title && <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: '8px' }}>{msg.title}</h2>}
                <p style={{ fontSize: '0.9rem', color: msg.recommends ? 'var(--text-secondary)' : 'var(--text-primary)', lineHeight: 1.5, whiteSpace: 'pre-wrap' }}>
                  {msg.content}
                </p>
                {msg.image && (
                  <img src={msg.image} alt="Uploaded" style={{ width: '100%', maxWidth: '200px', borderRadius: '12px', marginTop: '12px' }} />
                )}
                {msg.images && (
                  <div style={{ display: 'flex', gap: '10px', overflowX: 'auto', marginTop: '16px', paddingBottom: '4px' }}>
                    {msg.images.map((img: string, idx: number) => (
                      <img key={idx} src={img} alt={`Rec ${idx}`} style={{ width: idx === 1 ? '130px' : '110px', height: '140px', objectFit: 'cover', borderRadius: '16px', flexShrink: 0, transform: idx === 1 ? 'scale(1.05)' : 'none', boxShadow: idx === 1 ? 'var(--shadow-sm)' : 'none' }} />
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {isThinking && (
          <div style={{ alignSelf: 'flex-start', color: 'var(--text-secondary)', fontSize: '0.9rem', fontStyle: 'italic', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="dot-animation">AI가 분석 중...</span>
          </div>
        )}

        {/* Action Button */}
        <button
          onClick={() => handleSend('새로운 코디 추천해줘', true)}
          className="glass"
          style={{ margin: '10px auto', padding: '10px 24px', borderRadius: '20px', border: '1px solid var(--glass-border)', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontWeight: 600, color: '#ffffff' }}
        >
          다시하기
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="1 4 1 10 7 10"></polyline>
            <polyline points="23 20 23 14 17 14"></polyline>
            <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
          </svg>
        </button>
      </div>

      {/* Floating UI: Suggestions & Input */}
      <div style={{ position: 'fixed', bottom: '100px', left: '50%', transform: 'translateX(-50%)', width: 'calc(100% - 40px)', maxWidth: '440px', display: 'flex', flexDirection: 'column', gap: '10px', zIndex: 100 }}>

        {/* Claude-style Suggestions */}
        {suggestions.length > 0 && (
          <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
            {suggestions.map((s, i) => (
              <button
                key={i}
                onClick={() => handleSelectSuggestion(s)}
                style={{ background: 'white', border: '1px solid var(--glass-border)', borderRadius: '16px', padding: '8px 14px', fontSize: '0.85rem', whiteSpace: 'nowrap', cursor: 'pointer', boxShadow: 'var(--shadow-sm)' }}
              >
                {s}
              </button>
            ))}
          </div>
        )}

        {/* Plus Menu */}
        {showPlusMenu && (
          <div style={{ position: 'absolute', bottom: '70px', right: '0', background: 'white', borderRadius: '16px', boxShadow: 'var(--shadow-md)', padding: '8px', display: 'flex', flexDirection: 'column', minWidth: '140px', border: '1px solid var(--glass-border)' }}>
            <button 
              onClick={() => fileInputRef.current?.click()}
              style={{ padding: '10px', textAlign: 'left', background: 'none', border: 'none', cursor: 'pointer', fontSize: '0.9rem' }}
            >
              📷 사진 찍기 / 업로드
            </button>
            <button 
              onClick={() => fileInputRef.current?.click()}
              style={{ padding: '10px', textAlign: 'left', background: 'none', border: 'none', cursor: 'pointer', fontSize: '0.9rem' }}
            >
              🖼️ 갤러리에서 선택
            </button>
          </div>
        )}

        {/* Chat Input */}
        <div className="solid-bg" style={{ height: '56px', borderRadius: '28px', display: 'flex', alignItems: 'center', padding: '0 8px 0 20px' }}>
          <input
            type="text"
            placeholder="메시지 보내기"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onCompositionStart={() => setIsComposing(true)}
            onCompositionEnd={() => setIsComposing(false)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !isComposing) {
                handleSend(inputText);
              }
            }}
            style={{ flex: 1, border: 'none', background: 'transparent', outline: 'none', color: 'var(--text-primary)', fontSize: '0.95rem' }}
          />
          <div
            onClick={() => handleSend(inputText)}
            style={{ background: 'var(--primary)', color: 'var(--icon-on-primary)', width: '32px', height: '32px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginRight: '8px', cursor: 'pointer' }}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="19" x2="12" y2="5"></line>
              <polyline points="5 12 12 5 19 12"></polyline>
            </svg>
          </div>
          <div
            onClick={() => setShowPlusMenu(!showPlusMenu)}
            style={{ width: '40px', height: '40px', borderRadius: '20px', background: 'var(--plus-btn-bg)', color: 'var(--plus-btn-icon)', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}

