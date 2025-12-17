import React from 'react';
import Root from '../components/Root';

// This component wraps the entire Docusaurus app
export default function AppRoot({ children }) {
  return <Root>{children}</Root>;
}