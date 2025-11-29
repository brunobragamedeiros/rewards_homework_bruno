const { merge } = require('webpack-merge');
const commonConfig = require('./common.config');

module.exports = merge(commonConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  devServer: {
    port: 3000,
    proxy: {
      '/': {
        target: 'http://django:8000',
        timeout: 30000,
        proxyTimeout: 30000,
        changeOrigin: true,
        logLevel: 'warn',
        onError: (err, req, res) => {
          console.log('Proxy error:', err.message);
        },
        onProxyReq: (proxyReq, req, res) => {
          // Add keep-alive header to prevent connection drops
          proxyReq.setHeader('Connection', 'keep-alive');
          // Preserve original host for CSRF validation
          if (req.headers.host) {
            proxyReq.setHeader('X-Forwarded-Host', req.headers.host);
          }
        },
      },
    },
    // We need hot=false (Disable HMR) to set liveReload=true
    hot: false,
    liveReload: true,
  },
});
