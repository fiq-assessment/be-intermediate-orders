export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <style>{`
          * { box-sizing: border-box; margin: 0; padding: 0; }
          body { font-family: system-ui, sans-serif; background: #f5f5f5; padding: 2rem; }
          .container { max-width: 1200px; margin: 0 auto; }
          .card { background: white; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
          .btn { padding: 0.5rem 1rem; border: 1px solid #ddd; border-radius: 6px; background: white; cursor: pointer; }
          .btn:hover { background: #f9f9f9; }
          .btn-primary { background: #3b82f6; color: white; border-color: #3b82f6; }
          .btn-primary:hover { background: #2563eb; }
          .btn:disabled { opacity: 0.5; cursor: not-allowed; }
          .input { padding: 0.5rem; border: 1px solid #ddd; border-radius: 6px; width: 100%; }
          .table { width: 100%; border-collapse: collapse; }
          .table th, .table td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #eee; }
        `}</style>
      </head>
      <body>{children}</body>
    </html>
  );
}

