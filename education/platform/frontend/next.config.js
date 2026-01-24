/**
 * Next.js configuration for claw-son-four-point-five education platform.
 * 
 * This config includes:
 * - Experimental features for enhanced performance
 * - Environment variable configuration
 * - Custom headers and security settings
 * - Image optimization settings
 * - Webpack customizations
 */

const { createSecureHeaders } = require('next-secure-headers');
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

const securityHeaders = createSecureHeaders({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: "'self'",
      styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      imgSrc: ["'self'", "data:", "https:"],
      scriptSrc: ["'self'"],
      connectSrc: ["'self'", "https://api.github.com"],
      frameSrc: ["'none'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      manifestSrc: ["'self'"],
      workerSrc: ["'self'"],
    },
  },
  referrerPolicy: 'strict-origin-when-cross-origin',
  permissionsPolicy: {
    camera: [],
    microphone: [],
    geolocation: [],
    payment: [],
    usb: [],
  },
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Experimental features
  experimental: {
    appDir: true,
    serverComponentsExternalPackages: ['@prisma/client'],
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-icons',
      'date-fns',
      'framer-motion',
    ],
  },

  // Image optimization
  images: {
    domains: [
      'localhost',
      'avatars.githubusercontent.com',
      'images.unsplash.com',
      'res.cloudinary.com',
    ],
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 60 * 60 * 24 * 7, // 7 days
  },

  // Environment variables
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },

  // Rewrites for API proxy
  async rewrites() {
    return [
      {
        source: '/api/v1/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/:path*`,
      },
    ];
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/home',
        destination: '/',
        permanent: true,
      },
      {
        source: '/learn/:path*',
        destination: '/tutorials/:path*',
        permanent: true,
      },
    ];
  },

  // Headers for security and performance
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          ...securityHeaders,
          {
            key: 'X-DNS-Prefetch-Control',
            value: 'on',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains',
          },
        ],
      },
      {
        source: '/api/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'no-store, must-revalidate',
          },
        ],
      },
      {
        source: '/_next/static/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/images/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=86400',
          },
        ],
      },
    ];
  },

  // Webpack configuration
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Add custom webpack configurations
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      path: false,
      os: false,
    };

    // Add custom aliases
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': require('path').resolve(__dirname, 'src'),
      '@/components': require('path').resolve(__dirname, 'src/components'),
      '@/pages': require('path').resolve(__dirname, 'src/pages'),
      '@/hooks': require('path').resolve(__dirname, 'src/hooks'),
      '@/utils': require('path').resolve(__dirname, 'src/utils'),
      '@/styles': require('path').resolve(__dirname, 'src/styles'),
      '@/assets': require('path').resolve(__dirname, 'src/assets'),
      '@/types': require('path').resolve(__dirname, 'src/types'),
    };

    // Monaco Editor configuration
    config.module.rules.push({
      test: /\.ttf$/,
      type: 'asset/resource',
    });

    // Optimization for Monaco Editor
    if (!isServer) {
      config.resolve.alias['monaco-editor'] = 'monaco-editor/esm/vs/editor/editor.api';
    }

    // Bundle analyzer
    if (process.env.ANALYZE === 'true') {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          openAnalyzer: false,
        })
      );
    }

    return config;
  },

  // Output configuration
  output: 'standalone',

  // Power headers
  poweredByHeader: false,

  // Compression
  compress: true,

  // Development configurations
  ...(process.env.NODE_ENV === 'development' && {
    logging: {
      fetches: {
        fullUrl: true,
      },
    },
  }),

  // Internationalization
  i18n: {
    locales: ['en', 'es', 'fr', 'de', 'zh', 'ja'],
    defaultLocale: 'en',
    domains: [
      {
        domain: 'localhost',
        defaultLocale: 'en',
      },
    ],
  },

  // Server configuration
  serverRuntime: 'edge',
  
  // Static generation
  generateEtags: true,
  generateBuildId: async () => {
    return `build-${Date.now()}`;
  },

  // Error handling
  onDemandEntries: {
    maxInactiveAge: 25 * 1000,
    pagesBufferLength: 2,
  },

  // Custom server options
  ...(!process.env.SKIP_BUILD && {
    output: 'standalone',
  }),
};

// Bundle analyzer wrapper
module.exports = withBundleAnalyzer(nextConfig);