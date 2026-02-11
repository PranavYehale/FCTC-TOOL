// Vercel deployment webhook trigger
const https = require('https');

const deploymentData = {
  name: 'fctc-tool',
  gitSource: {
    type: 'github',
    repo: 'PranavYehale/FCTC-TOOL',
    ref: 'master'
  },
  target: 'production'
};

// This would need your Vercel API token to work
console.log('Deployment configuration ready for:', deploymentData);
console.log('Please deploy via Vercel Dashboard at: https://vercel.com/dashboard');