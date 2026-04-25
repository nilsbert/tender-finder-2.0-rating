import React from 'react';
import { PHeading, PFlex, PText } from '@porsche-design-system/components-react';

interface AdminHeaderProps {
  activeService: 'crawling' | 'enriching' | 'ai' | 'iam' | 'rating' | 'distributing';
}

const AdminHeader: React.FC<AdminHeaderProps> = ({ activeService }) => {
  const services = [
    { id: 'crawling', name: 'Crawling', port: 8001, path: '/ms/crawling/', title: 'Data Collection' },
    { id: 'enriching', name: 'Enriching', port: 8002, path: '/ms/enriching/', title: 'Data Intelligence' },
    { id: 'ai', name: 'AI Service', port: 8004, path: '/ms/ai/', title: 'Inference Engine' },
    { id: 'iam', name: 'IAM', port: 8003, path: '/ms/iam/admin', title: 'Identity Authority' },
    { id: 'rating', name: 'Rating', port: 8012, path: '/ms/rating/', title: 'Relevancy & Scoring' },
    { id: 'distributing', name: 'Distributing', port: 8005, path: '/ms/dispatching/', title: 'Delivery Authority' },
  ];

  const currentService = services.find(s => s.id === activeService);

  return (
    <header style={{
      backgroundColor: '#0e0e12',
      borderBottom: '1px solid rgba(255, 255, 255, 0.06)',
      padding: '0 40px',
      height: '64px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
      backdropFilter: 'blur(10px)',
      width: '100%',
      boxSizing: 'border-box'
    }}>
      <PFlex alignItems="center" style={{ gap: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <svg viewBox="0 0 32 32" style={{ width: '32px', height: '32px' }}>
            <rect width="32" height="32" rx="8" fill="#d5001c" />
            <path d="M8 16L14 10L20 16L14 22Z" fill="#fff" />
            <path d="M16 13L22 7L28 13L22 19Z" fill="rgba(255,255,255,0.5)" />
          </svg>
          <PHeading size="small" theme="dark" style={{ margin: 0, letterSpacing: '-0.02em', whiteSpace: 'nowrap' }}>
            TENDER FINDER <span style={{ fontWeight: 'normal', opacity: 0.5 }}>| {currentService?.title || 'Admin Suite'}</span>
          </PHeading>
        </div>

        <nav style={{ display: 'flex', gap: '8px', marginLeft: '24px' }}>
          {services.map((s) => {
            const isActive = s.id === activeService;
            const url = s.path;
            
            return (
              <a
                key={s.id}
                href={url}
                style={{
                  textDecoration: 'none',
                  padding: '0 16px',
                  height: '64px',
                  display: 'flex',
                  alignItems: 'center',
                  color: isActive ? '#d5001c' : '#8b8b9e',
                  fontSize: '13px',
                  fontWeight: isActive ? '600' : '500',
                  transition: 'all 0.2s ease',
                  borderBottom: isActive ? '2px solid #d5001c' : '2px solid transparent',
                  backgroundColor: isActive ? 'rgba(213, 0, 28, 0.05)' : 'transparent',
                }}
              >
                {s.name}
              </a>
            );
          })}
        </nav>
      </PFlex>

      <PFlex alignItems="center" style={{ gap: '16px' }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '8px', 
          padding: '4px 12px', 
          backgroundColor: 'rgba(1, 186, 109, 0.1)', 
          borderRadius: '100px', 
          border: '1px solid rgba(1, 186, 109, 0.2)' 
        }}>
          <div style={{ 
            width: '8px', 
            height: '8px', 
            borderRadius: '50%', 
            backgroundColor: '#01ba6d',
            boxShadow: '0 0 8px rgba(1, 186, 109, 0.4)'
          }} />
          <PText size="x-small" theme="dark" style={{ color: '#01ba6d', fontWeight: 'bold', fontSize: '11px' }}>SYSTEM ONLINE</PText>
        </div>
      </PFlex>
    </header>
  );
};

export default AdminHeader;
