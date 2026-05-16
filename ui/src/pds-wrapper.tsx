// @ts-nocheck
import React from 'react';
import { Plus, Trash2, Save, Edit2, X, ChevronRight, Download, Upload, Activity, Zap, Search, Filter, RotateCcw, Menu } from 'lucide-react';

// Mock Provider
export const PorscheDesignSystemProvider = ({ children }: any) => <div className="pds-provider">{children}</div>;

// Polyfills for Layout & Style
export const PFlex = ({ children, direction, gap, alignItems, justifyContent, style, wrap }: any) => {
  return (
    <div style={{
      display: 'flex',
      flexDirection: direction || 'row',
      gap: gap || '0px',
      alignItems: alignItems || 'stretch',
      justifyContent: justifyContent || 'flex-start',
      flexWrap: wrap || 'nowrap',
      ...style
    }}>
      {children}
    </div>
  );
};

export const PHeadline = ({ children, variant, theme, style }: any) => (
  <h1 style={{ 
    fontSize: variant === 'headline-1' ? '2.5rem' : '1.5rem', 
    fontWeight: 700, 
    color: theme === 'dark' ? 'white' : 'var(--porsche-black)',
    margin: 0,
    ...style 
  }}>{children}</h1>
);

export const PHeading = ({ children, size, theme, style, tag: Tag = 'h2' }: any) => (
  <Tag style={{ 
    fontSize: size === 'small' ? '1.1rem' : size === 'large' ? '1.8rem' : '1.5rem', 
    fontWeight: 600, 
    color: theme === 'dark' ? 'white' : 'var(--porsche-black)',
    margin: 0,
    ...style 
  }}>{children}</Tag>
);

export const PText = ({ children, size, theme, style, weight }: any) => (
  <span style={{ 
    fontSize: size === 'small' ? '0.875rem' : size === 'x-small' ? '0.75rem' : '1rem', 
    color: theme === 'dark' ? 'white' : 'var(--porsche-black)',
    fontWeight: weight === 'semi-bold' ? 600 : weight === 'bold' ? 700 : 400,
    display: 'inline-block',
    ...style 
  }}>{children}</span>
);

export const PButton = ({ children, variant, onClick, icon, theme, size, type, hideLabel, style, loading }: any) => {
  const [isHovered, setIsHovered] = React.useState(false);

  const IconComponent = () => {
    const iconSize = size === 'small' ? 14 : 18;
    switch (icon) {
      case 'plus': return <Plus size={iconSize} />;
      case 'delete': return <Trash2 size={iconSize} />;
      case 'save': return <Save size={iconSize} />;
      case 'edit': return <Edit2 size={iconSize} />;
      case 'close': return <X size={iconSize} />;
      case 'arrow-right': return <ChevronRight size={iconSize} />;
      case 'download': return <Download size={iconSize} />;
      case 'upload': return <Upload size={iconSize} />;
      case 'activity': return <Activity size={iconSize} />;
      case 'rotate-ccw': return <RotateCcw size={iconSize} />;
      default: return null;
    }
  };

  const isSecondary = variant === 'secondary';
  
  const getBgColor = () => {
    if (variant === 'primary') return isHovered ? '#E6001E' : 'var(--tf-accent)';
    return isHovered ? 'rgba(255, 255, 255, 0.1)' : 'transparent';
  };

  return (
    <button 
      type={type || 'button'}
      onClick={onClick}
      disabled={loading}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        padding: size === 'small' ? '6px 12px' : '10px 20px',
        backgroundColor: getBgColor(),
        color: isSecondary ? (isHovered ? 'white' : 'var(--tf-text-secondary)') : 'white',
        border: isSecondary ? `1px solid ${isHovered ? 'rgba(255,255,255,0.4)' : 'var(--tf-border)'}` : 'none',
        borderRadius: '4px',
        cursor: loading ? 'not-allowed' : 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '8px',
        fontSize: '14px',
        fontWeight: 600,
        transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
        whiteSpace: 'nowrap',
        opacity: loading ? 0.7 : 1,
        transform: isHovered && !loading ? 'translateY(-1px)' : 'none',
        boxShadow: (variant === 'primary' && isHovered && !loading) ? '0 6px 20px rgba(213, 0, 28, 0.4)' : 'none',
        ...style
      }}
    >
      {loading ? <span className="animate-spin">◌</span> : <IconComponent />}
      {children && !hideLabel && <span>{children}</span>}
    </button>
  );
};

export const PTag = ({ children, color, theme, style }: any) => {
  const getColors = () => {
    switch (color) {
      case 'success': return { bg: '#01ba6d22', text: '#01ba6d', border: '#01ba6d44' };
      case 'error': return { bg: '#ff444422', text: '#ff4444', border: '#ff444444' };
      case 'warning': return { bg: '#ffcc0022', text: '#ffcc00', border: '#ffcc0044' };
      case 'background-base': return { bg: 'rgba(255,255,255,0.1)', text: 'white', border: 'rgba(255,255,255,0.2)' };
      default: return { bg: 'rgba(255,255,255,0.05)', text: 'var(--tf-text-secondary)', border: 'rgba(255,255,255,0.1)' };
    }
  };
  const colors = getColors();
  return (
    <span style={{
      padding: '2px 10px',
      borderRadius: '4px',
      fontSize: '11px',
      fontWeight: 700,
      backgroundColor: colors.bg,
      color: colors.text,
      border: `1px solid ${colors.border}`,
      display: 'inline-flex',
      alignItems: 'center',
      ...style
    }}>
      {children}
    </span>
  );
};

export const PModal = ({ open, heading, children, onDismiss, theme = 'dark', width }: any) => {
  if (!open) return null;
  
  return (
    <div style={{
      position: 'fixed',
      inset: '0px',
      backgroundColor: 'rgba(0,0,0,0.85)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 2000,
      backdropFilter: 'blur(10px)'
    }} onClick={onDismiss}>
      <div className="glass-panel" style={{
        backgroundColor: '#111111',
        color: 'white',
        padding: '0',
        width: '95%',
        maxWidth: width || '800px',
        maxHeight: '90vh',
        overflow: 'hidden',
        display: 'flex',
        flexDirection: 'column',
        position: 'relative',
        borderRadius: '16px',
        boxShadow: '0 40px 80px rgba(0,0,0,0.6)',
      }} onClick={e => e.stopPropagation()}>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '24px 32px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
          <PHeading theme="dark" size="small" style={{ margin: 0 }}>{heading}</PHeading>
          <button 
            type="button" 
            onClick={onDismiss}
            style={{
              background: 'rgba(255,255,255,0.05)',
              border: 'none',
              borderRadius: '50%',
              width: '32px',
              height: '32px',
              cursor: 'pointer',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            <X size={18} />
          </button>
        </div>
        
        <div style={{ overflowY: 'auto', padding: '32px', flex: 1 }}>
          {children}
        </div>
      </div>
    </div>
  );
};

export const PTextFieldWrapper = ({ label, children, theme }: any) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '16px' }}>
    <label style={{ fontSize: '14px', fontWeight: 600, color: 'var(--tf-text-secondary)' }}>{label}</label>
    {children}
  </div>
);

export const PSelectWrapper = ({ label, children, theme }: any) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '16px' }}>
    <label style={{ fontSize: '14px', fontWeight: 600, color: 'var(--tf-text-secondary)' }}>{label}</label>
    {children}
  </div>
);

export const PIcon = ({ name, color, size, theme, style }: any) => {
  const iconSize = size === 'small' ? 14 : size === 'large' ? 24 : 18;
  switch (name) {
    case 'arrow-head-down': return <ChevronRight size={iconSize} style={{ transform: 'rotate(90deg)', ...style }} />;
    case 'arrow-head-right': return <ChevronRight size={iconSize} style={style} />;
    case 'plus': return <Plus size={iconSize} style={style} />;
    case 'delete': return <Trash2 size={iconSize} style={style} />;
    case 'save': return <Save size={iconSize} style={style} />;
    case 'edit': return <Edit2 size={iconSize} style={style} />;
    case 'warning': return <Zap size={iconSize} style={{ color: '#ffcc00', ...style }} />;
    case 'menu': return <Menu size={iconSize} style={style} />;
    case 'search': return <Search size={iconSize} style={style} />;
    case 'filter': return <Filter size={iconSize} style={style} />;
    case 'activity': return <Activity size={iconSize} style={style} />;
    default: return <Activity size={iconSize} style={style} />;
  }
};
