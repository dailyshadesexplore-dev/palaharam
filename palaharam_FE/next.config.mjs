/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
    images: {
      domains: ['images.unsplash.com','plus.unsplash.com'],
      remotePatterns: [
        {
          protocol: 'https',
          hostname: 'images.unsplash.com',
          pathname: '/**',
        },
        {
          protocol: 'https',
          hostname: 'plus.unsplash.com',
          pathname: '/**',
        },
      ],
    },
};
export default nextConfig;
