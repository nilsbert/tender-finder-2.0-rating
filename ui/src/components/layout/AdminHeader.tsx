import React, { useState } from 'react';
import { PIcon } from '../../pds-wrapper';

interface AdminHeaderProps {
  activeService: 'crawling' | 'enriching' | 'ai' | 'rating' | 'distributing';
}

const AdminHeader: React.FC<AdminHeaderProps> = ({ activeService }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const services = [
    { id: 'crawling', name: 'Crawling', path: '/ms/crawling/', title: 'Data Collection' },
    { id: 'enriching', name: 'Enriching', path: '/ms/enriching/', title: 'Enriching' },
    { id: 'ai', name: 'AI Service', path: '/ms/ai/', title: 'AI Service' },
    { id: 'iam', name: 'IAM', path: '/ms/iam/admin', title: 'IAM' },
    { id: 'distributing', name: 'Distributing', path: '/ms/distributing/', title: 'Distributing' },
  ];

  const currentService = services.find(s => s.id === activeService);

  return (
    <>
      <header style={{
        backgroundColor: 'rgba(17, 17, 17, 0.8)',
        borderBottom: '1px solid var(--tf-border)',
        padding: '0 20px',
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
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button 
            className="show-mobile"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              padding: '8px',
              display: 'none' // Hidden by default, shown by CSS media query
            }}
          >
            <PIcon name={isMobileMenuOpen ? 'close' : 'menu-lines'} theme="dark" />
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <svg viewBox="0 0 32 32" style={{ width: '28px', height: '28px' }}>
              <rect width="32" height="32" rx="8" fill="var(--tf-accent)" />
              <path d="M8 16L14 10L20 16L14 22Z" fill="#fff" />
              <path d="M16 13L22 7L28 13L22 19Z" fill="rgba(255,255,255,0.5)" />
            </svg>
            <span style={{ margin: 0, letterSpacing: '-0.02em', whiteSpace: 'nowrap', fontWeight: 700, fontSize: '14px', color: '#fff' }}>
              TENDER FINDER <span className="hide-mobile" style={{ fontWeight: 300, opacity: 0.5 }}>| {currentService?.title || 'Admin Suite'}</span>
            </span>
          </div>

          <nav className="hide-mobile" style={{ display: 'flex', gap: '4px', marginLeft: '12px' }}>
            {services.map((s) => {
              const isActive = s.id === activeService;
              return (
                <a
                  key={s.id}
                  href={s.path}
                  style={{
                    textDecoration: 'none',
                    padding: '0 12px',
                    height: '64px',
                    display: 'flex',
                    alignItems: 'center',
                    color: isActive ? 'var(--tf-accent)' : 'var(--tf-text-muted)',
                    fontSize: '12px',
                    fontWeight: isActive ? '600' : '500',
                    transition: 'all 0.2s ease',
                    borderBottom: isActive ? '2px solid var(--tf-accent)' : '2px solid transparent',
                    backgroundColor: isActive ? 'var(--tf-accent-soft)' : 'transparent',
                  }}
                >
                  {s.name}
                </a>
              );
            })}
          </nav>
        </div>

        <div className="hide-mobile" style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
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
            <span style={{ color: '#01ba6d', fontWeight: 'bold', fontSize: '10px', letterSpacing: '0.5px' }}>ONLINE</span>
          </div>
        </div>
      </header>

      {/* Mobile Menu Overlay */}
      <div className={`mobile-menu-overlay ${isMobileMenuOpen ? 'open' : ''}`}>
        <div style={{ marginBottom: '20px', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '12px' }}>
          <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--tf-accent)', letterSpacing: '1px' }}>ADMIN NAVIGATION</span>
        </div>
        {services.map((s) => {
          const isActive = s.id === activeService;
          return (
            <a
              key={s.id}
              href={s.path}
              className={`mobile-nav-link ${isActive ? 'active' : ''}`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              {s.name}
            </a>
          );
        })}
        
        <div style={{ marginTop: 'auto', padding: '20px', textAlign: 'center', opacity: 0.5 }}>
          <span style={{ fontSize: '10px', fontWeight: 600 }}>SYSTEM STATUS: ONLINE</span>
        </div>
      </div>
    </>
  );
};

export default AdminHeader;
