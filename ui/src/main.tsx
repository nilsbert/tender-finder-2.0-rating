import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';
import { load as loadPorscheDesignSystem } from '@porsche-design-system/components-js';
import {PorscheDesignSystemProvider} from '@porsche-design-system/components-react';

// Initialize Porsche Design System
loadPorscheDesignSystem();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <PorscheDesignSystemProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </PorscheDesignSystemProvider>
  </React.StrictMode>
);