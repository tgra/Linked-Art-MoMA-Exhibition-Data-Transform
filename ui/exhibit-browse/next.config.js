module.exports = {
    pageExtensions: ['mdx', 'md', 'jsx', 'js', 'json','tsx', 'ts'],
    typescript: {
      // !! WARN !!
      // Dangerously allow production builds to successfully complete even if
      // your project has type errors.
      // !! WARN !!
      ignoreBuildErrors: true,
    },
  }